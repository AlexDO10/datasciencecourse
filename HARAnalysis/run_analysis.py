"""
run_analysis.py
===============
Human Activity Recognition (UCI HAR Dataset) — Data Cleaning Pipeline

Steps:
  1. Merge the training and test sets into one dataset
  2. Extract only mean and std measurements
  3. Apply descriptive activity names
  4. Label columns with descriptive variable names
  5. Create a second tidy dataset: average of each variable per activity per subject

Usage:
  python run_analysis.py

Output:
  tidy_data.csv — wide tidy dataset with one row per subject/activity combination
"""

import pandas as pd
import os

# ──────────────────────────────────────────────────────────────────────────────
# Configuration — update this path if the dataset is in a different location
# ──────────────────────────────────────────────────────────────────────────────
DATA_DIR = os.path.expanduser("~/Downloads/UCI HAR Dataset")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 0: Load shared reference files
# ──────────────────────────────────────────────────────────────────────────────
print("Loading reference files...")

# 561 feature names
features = pd.read_csv(
    os.path.join(DATA_DIR, "features.txt"),
    sep=r"\s+",
    header=None,
    names=["index", "feature_name"]
)

# Activity labels: maps numeric ID → descriptive name
activity_labels = pd.read_csv(
    os.path.join(DATA_DIR, "activity_labels.txt"),
    sep=r"\s+",
    header=None,
    names=["activity_id", "activity_name"]
)

print(f"  Features loaded   : {len(features)} features")
print(f"  Activities loaded : {len(activity_labels)} activities")
print(f"  Activities        : {activity_labels['activity_name'].tolist()}")

# The features.txt file has 84 duplicate names — make them unique by appending index
# e.g. "fBodyAcc-bandsEnergy()-1,8" appears multiple times
seen = {}
unique_names = []
for idx, name in zip(features["index"], features["feature_name"]):
    if name in seen:
        seen[name] += 1
        unique_names.append(f"{name}_{seen[name]}")
    else:
        seen[name] = 0
        unique_names.append(name)
features["feature_name"] = unique_names
print(f"  Deduplicated feature names (were {features['feature_name'].duplicated().sum()} dupes)\n")


# ──────────────────────────────────────────────────────────────────────────────
# Helper: load one split (train or test)
# ──────────────────────────────────────────────────────────────────────────────
def load_split(split: str, feature_names: list) -> pd.DataFrame:
    """
    Loads X, y, and subject files for a given split ('train' or 'test')
    and returns a combined DataFrame with labeled columns.
    """
    base = os.path.join(DATA_DIR, split)

    X = pd.read_csv(
        os.path.join(base, f"X_{split}.txt"),
        sep=r"\s+",
        header=None,
        names=feature_names
    )
    y = pd.read_csv(
        os.path.join(base, f"y_{split}.txt"),
        sep=r"\s+",
        header=None,
        names=["activity_id"]
    )
    subjects = pd.read_csv(
        os.path.join(base, f"subject_{split}.txt"),
        sep=r"\s+",
        header=None,
        names=["subject_id"]
    )

    df = pd.concat([subjects, y, X], axis=1)
    df["split"] = split  # optional: track origin
    return df


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1: Merge training and test sets
# ──────────────────────────────────────────────────────────────────────────────
print("Step 1: Merging training and test sets...")

train_df = load_split("train", features["feature_name"].tolist())
test_df  = load_split("test",  features["feature_name"].tolist())

merged = pd.concat([train_df, test_df], axis=0, ignore_index=True)

print(f"  Train rows : {len(train_df)}")
print(f"  Test rows  : {len(test_df)}")
print(f"  Merged rows: {len(merged)}\n")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2: Extract only mean() and std() measurements
# ──────────────────────────────────────────────────────────────────────────────
print("Step 2: Extracting mean() and std() measurements...")

# Keep identifier columns plus any feature column containing mean() or std()
id_cols  = ["subject_id", "activity_id", "split"]
mean_std = [col for col in merged.columns
            if "mean()" in col or "std()" in col]

merged_filtered = merged[id_cols + mean_std].copy()

print(f"  Features selected: {len(mean_std)}")
print(f"  Total columns now: {merged_filtered.shape[1]}\n")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3: Apply descriptive activity names
# ──────────────────────────────────────────────────────────────────────────────
print("Step 3: Replacing activity IDs with descriptive names...")

merged_filtered = merged_filtered.merge(
    activity_labels,
    on="activity_id",
    how="left"
)
# Drop the numeric ID, keep only the name
merged_filtered.drop(columns=["activity_id"], inplace=True)

print(f"  Activity name column added.")
print(f"  Sample:\n{merged_filtered[['subject_id','activity_name']].head(3)}\n")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4: Label columns with descriptive variable names
# ──────────────────────────────────────────────────────────────────────────────
print("Step 4: Applying descriptive variable names...")

def make_descriptive(name: str) -> str:
    """Expand cryptic abbreviations into readable names."""
    name = name.replace("tBody",       "time_body_")
    name = name.replace("tGravity",    "time_gravity_")
    name = name.replace("fBody",       "frequency_body_")
    name = name.replace("fGravity",    "frequency_gravity_")
    name = name.replace("Acc",         "accelerometer_")
    name = name.replace("Gyro",        "gyroscope_")
    name = name.replace("Jerk",        "jerk_")
    name = name.replace("Mag",         "magnitude_")
    name = name.replace("-mean()",     "_mean")
    name = name.replace("-std()",      "_std")
    name = name.replace("-X",          "_X")
    name = name.replace("-Y",          "_Y")
    name = name.replace("-Z",          "_Z")
    name = name.replace("__",          "_")   # clean up double underscores
    name = name.strip("_").lower()
    return name

rename_map = {col: make_descriptive(col)
              for col in mean_std}
merged_filtered.rename(columns=rename_map, inplace=True)

print("  Sample renamed columns:")
for old, new in list(rename_map.items())[:5]:
    print(f"    {old:<30} → {new}")
print()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5: Create tidy dataset — average per variable per activity per subject
# ──────────────────────────────────────────────────────────────────────────────
print("Step 5: Creating tidy dataset with averages per subject/activity...")

group_cols     = ["subject_id", "activity_name"]
measure_cols   = [c for c in merged_filtered.columns
                  if c not in group_cols + ["split"]]

tidy = (
    merged_filtered
    .groupby(group_cols)[measure_cols]
    .mean()
    .reset_index()
)

# Sort for readability
tidy.sort_values(["subject_id", "activity_name"], inplace=True)
tidy.reset_index(drop=True, inplace=True)

print(f"  Tidy dataset shape: {tidy.shape}")
print(f"  Rows (subject × activity combinations): {len(tidy)}")
print(f"  Sample:\n{tidy[['subject_id','activity_name']].head(8).to_string(index=False)}\n")


# ──────────────────────────────────────────────────────────────────────────────
# Save outputs
# ──────────────────────────────────────────────────────────────────────────────
output_dir = os.path.dirname(os.path.abspath(__file__))

tidy_path   = os.path.join(output_dir, "tidy_data.csv")
merged_path = os.path.join(output_dir, "merged_data.csv")

tidy.to_csv(tidy_path,   index=False)
merged_filtered.drop(columns=["split"]).to_csv(merged_path, index=False)

print(f"✅ Saved: {tidy_path}")
print(f"✅ Saved: {merged_path}")
print("\nDone!")

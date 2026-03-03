# HAR Analysis — Getting and Cleaning Data (Week 3 Assignment)

**Course:** Johns Hopkins University — Getting and Cleaning Data  
**Dataset:** UCI Human Activity Recognition Using Smartphones

---

## Repository Contents

| File              | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| `run_analysis.py` | Main script — full data cleaning pipeline                         |
| `tidy_data.txt`   | Final output — tidy dataset (space-separated, 180 rows × 68 cols) |
| `tidy_data.csv`   | Same output as CSV (for local exploration)                        |
| `merged_data.csv` | Intermediate — all 10,299 observations after steps 1–4            |
| `README.md`       | This file                                                         |

---

## How to Run

```bash
python run_analysis.py
```

> **Requirement:** The UCI HAR Dataset must be unzipped at `~/Downloads/UCI HAR Dataset`.  
> Update the `DATA_DIR` variable at the top of `run_analysis.py` if it lives elsewhere.

---

## What the Script Does

The script performs a 5-step cleaning pipeline on raw smartphone sensor data:

### Step 1 — Merge Training and Test Sets

Loads six files and combines them into one dataset:

```
train/X_train.txt       + test/X_test.txt        → 561 measurement columns
train/y_train.txt       + test/y_test.txt         → activity labels (numeric)
train/subject_train.txt + test/subject_test.txt   → subject IDs
```

The three column groups are joined horizontally (`pd.concat(..., axis=1)`) and the two splits stacked vertically — producing **10,299 rows × 563 columns**.

---

### Step 2 — Extract Mean and Standard Deviation Measurements

From the 561 original features, only columns whose name contains **`mean()`** or **`std()`** are kept. This yields **66 measurement columns**.

> `meanFreq()` columns are excluded — they represent a weighted average of frequency components, not a direct mean of a measurement signal.

---

### Step 3 — Apply Descriptive Activity Names

The numeric activity ID column is replaced with human-readable labels by merging with `activity_labels.txt`:

```
1 → WALKING
2 → WALKING_UPSTAIRS
3 → WALKING_DOWNSTAIRS
4 → SITTING
5 → STANDING
6 → LAYING
```

---

### Step 4 — Label Columns with Descriptive Variable Names

Cryptic original names are expanded into readable lowercase names using string replacement rules:

```
tBodyAcc-mean()-X   →   time_body_accelerometer_mean_x
fBodyGyro-std()-Z   →   frequency_body_gyroscope_std_z
tBodyAccMag-mean()  →   time_body_accelerometer_magnitude_mean
```

Full expansion rules:

| Original   | Expanded          |
| ---------- | ----------------- |
| `tBody`    | `time_body_`      |
| `tGravity` | `time_gravity_`   |
| `fBody`    | `frequency_body_` |
| `Acc`      | `accelerometer_`  |
| `Gyro`     | `gyroscope_`      |
| `Jerk`     | `jerk_`           |
| `Mag`      | `magnitude_`      |
| `-mean()`  | `_mean`           |
| `-std()`   | `_std`            |

---

### Step 5 — Create Independent Tidy Dataset

The cleaned dataset is grouped by **subject** and **activity**, and the **mean** of every measurement column is computed for each group.

```
30 subjects × 6 activities = 180 rows
```

The result is saved as `tidy_data.txt` (space-separated, no row index) — matching the format of R's `write.table(df, row.names=FALSE)`.

---

## Code Book

### Identifier Columns

| Column          | Type    | Values    | Description                                    |
| --------------- | ------- | --------- | ---------------------------------------------- |
| `subject_id`    | integer | 1–30      | ID of the volunteer who performed the activity |
| `activity_name` | string  | see below | Activity being performed                       |

**Activity names:**

- `WALKING`
- `WALKING_UPSTAIRS`
- `WALKING_DOWNSTAIRS`
- `SITTING`
- `STANDING`
- `LAYING`

---

### Measurement Columns (66 total)

All 66 measurement columns follow this naming pattern:

```
{domain}_{component}_{sensor}[_jerk][_magnitude]_{statistic}[_{axis}]
```

| Part        | Values                       | Meaning                                                  |
| ----------- | ---------------------------- | -------------------------------------------------------- |
| `domain`    | `time`, `frequency`          | Time domain or FFT frequency domain signal               |
| `component` | `body`, `gravity`            | Body motion or gravitational component                   |
| `sensor`    | `accelerometer`, `gyroscope` | Device sensor                                            |
| `jerk`      | _(optional)_ `jerk`          | Jerk signal (time derivative of linear/angular velocity) |
| `magnitude` | _(optional)_ `magnitude`     | Euclidean magnitude of 3-axial signal                    |
| `statistic` | `mean`, `std`                | Mean or standard deviation of the signal                 |
| `axis`      | _(optional)_ `x`, `y`, `z`   | Axis of measurement (omitted for magnitude signals)      |

> All values are **normalized and bounded within [-1, 1]** (dimensionless).  
> Each value in `tidy_data.txt` is the **average** of all observations for that subject/activity combination.

---

### Full List of Measurement Columns

**Time domain — Body Accelerometer**

- `time_body_accelerometer_mean_x/y/z`
- `time_body_accelerometer_std_x/y/z`

**Time domain — Gravity Accelerometer**

- `time_gravity_accelerometer_mean_x/y/z`
- `time_gravity_accelerometer_std_x/y/z`

**Time domain — Body Accelerometer Jerk**

- `time_body_accelerometer_jerk_mean_x/y/z`
- `time_body_accelerometer_jerk_std_x/y/z`

**Time domain — Body Gyroscope**

- `time_body_gyroscope_mean_x/y/z`
- `time_body_gyroscope_std_x/y/z`

**Time domain — Body Gyroscope Jerk**

- `time_body_gyroscope_jerk_mean_x/y/z`
- `time_body_gyroscope_jerk_std_x/y/z`

**Time domain — Magnitudes**

- `time_body_accelerometer_magnitude_mean/std`
- `time_gravity_accelerometer_magnitude_mean/std`
- `time_body_accelerometer_jerk_magnitude_mean/std`
- `time_body_gyroscope_magnitude_mean/std`
- `time_body_gyroscope_jerk_magnitude_mean/std`

**Frequency domain — Body Accelerometer**

- `frequency_body_accelerometer_mean_x/y/z`
- `frequency_body_accelerometer_std_x/y/z`

**Frequency domain — Body Accelerometer Jerk**

- `frequency_body_accelerometer_jerk_mean_x/y/z`
- `frequency_body_accelerometer_jerk_std_x/y/z`

**Frequency domain — Body Gyroscope**

- `frequency_body_gyroscope_mean_x/y/z`
- `frequency_body_gyroscope_std_x/y/z`

**Frequency domain — Magnitudes**

- `frequency_body_accelerometer_magnitude_mean/std`
- `frequency_body_accelerometer_jerk_magnitude_mean/std`
- `frequency_body_gyroscope_magnitude_mean/std`
- `frequency_body_gyroscope_jerk_magnitude_mean/std`

---

## Tidy Data Principles

This dataset is **tidy** in the sense of Hadley Wickham (2014):

1. **Each variable forms a column** — one column per measurement signal statistic
2. **Each observation forms a row** — one row per unique subject/activity combination
3. **Each observational unit forms a table** — one table for the summary averages

---

## Original Data Source

Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra and Jorge L. Reyes-Ortiz.  
_Human Activity Recognition on Smartphones using a Multiclass Hardware-Friendly Support Vector Machine._  
International Workshop of Ambient Assisted Living (IWAAL 2012). Vitoria-Gasteiz, Spain. Dec 2012.

# Data Science Coursera Course

A collection of projects and assignments from the **Data Science Specialization** on Coursera, covering data collection, exploratory data analysis, and data cleaning.

---

## Repository Structure

```
├── DataCollection/         # Data collection assignments and projects
├── HARAnalysis/            # Human Activity Recognition analysis
├── ExploratoryDataAnalysis/# EDA project (household power consumption)
├── data/                   # Raw datasets
├── plot1.py / plot1.png    # EDA Plot 1 — Global Active Power histogram
├── plot2.py / plot2.png    # EDA Plot 2 — Global Active Power time series
├── plot3.py / plot3.png    # EDA Plot 3 — Energy sub metering time series
├── plot4.py / plot4.png    # EDA Plot 4 — 2×2 power metrics subplots
└── dataScience.ipynb       # General data science notebook
```

---

## Exploratory Data Analysis — Household Power Consumption

### Goal
Examine how household energy usage varies over a **2-day period (February 1–2, 2007)** using the [UCI Household Power Consumption dataset](https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption).

### Dataset
- **File:** `ExploratoryDataAnalysis/household_power_consumption.txt`
- **Separator:** `;`
- **Columns:** `Date`, `Time`, `Global_active_power`, `Global_reactive_power`, `Voltage`, `Global_intensity`, `Sub_metering_1`, `Sub_metering_2`, `Sub_metering_3`

### Plots

| File | Description |
|------|-------------|
| `plot1.png` | Histogram of Global Active Power (kilowatts) |
| `plot2.png` | Time series of Global Active Power over Thu–Sat |
| `plot3.png` | Time series of energy sub metering (3 sub-meters) |
| `plot4.png` | 2×2 subplots: Active Power, Voltage, Sub metering, Reactive Power |

All plots are **480×480 pixels**. Each `.py` file fully reproduces its corresponding `.png`.

### How to Run

```bash
# Run any individual plot script from the repo root
python3 plot1.py
python3 plot2.py
python3 plot3.py
python3 plot4.py
```

### Requirements

```bash
pip install pandas matplotlib
```

---

## HAR Analysis

Cleaning and tidying the **Human Activity Recognition (HAR)** dataset. See [HARAnalysis/README.md](HARAnalysis/README.md) for details.

---

## Author
**Alejandro Dominguez** — Coursera Data Science Specialization

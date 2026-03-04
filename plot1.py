#!/usr/bin/env python
"""
Plot 1: Have total US PM2.5 emissions decreased from 1999 to 2008?
Bar chart of total emissions across all sources for each year.
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Total emissions per year (in millions of tons)
total_by_year = NEI.groupby("year")["Emissions"].sum() / 1e6

fig, ax = plt.subplots(figsize=(480/100, 480/100), dpi=100)
ax.bar(total_by_year.index.astype(str), total_by_year.values, color="steelblue", width=0.5)
ax.set_xlabel("Year")
ax.set_ylabel("Total PM2.5 Emissions (millions of tons)")
ax.set_title("Total PM2.5 Emissions in the US (1999–2008)")
for i, (yr, val) in enumerate(total_by_year.items()):
    ax.text(i, val + 0.05, f"{val:.2f}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("plot1.png", dpi=100, bbox_inches="tight")
plt.close()
print("Plot 1 saved as plot1.png")

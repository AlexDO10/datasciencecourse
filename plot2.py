#!/usr/bin/env python
"""
Plot 2: Have total Baltimore City PM2.5 emissions decreased from 1999 to 2008?
Bar chart of total emissions for Baltimore City (fips == "24510").
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Filter Baltimore City
baltimore = NEI[NEI["fips"] == "24510"]
baltimore_by_year = baltimore.groupby("year")["Emissions"].sum()

fig, ax = plt.subplots(figsize=(480/100, 480/100), dpi=100)
ax.bar(baltimore_by_year.index.astype(str), baltimore_by_year.values, color="tomato", width=0.5)
ax.set_xlabel("Year")
ax.set_ylabel("Total PM2.5 Emissions (tons)")
ax.set_title("Total PM2.5 Emissions — Baltimore City, MD (1999–2008)")
for i, (yr, val) in enumerate(baltimore_by_year.items()):
    ax.text(i, val + 20, f"{val:.0f}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("plot2.png", dpi=100, bbox_inches="tight")
plt.close()
print("Plot 2 saved as plot2.png")

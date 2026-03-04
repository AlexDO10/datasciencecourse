#!/usr/bin/env python
"""
Plot 6: Baltimore City vs Los Angeles County — which city saw greater change
in motor vehicle (ON-ROAD) PM2.5 emissions from 1999–2008?
Side-by-side line charts for direct comparison.
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Filter both cities, ON-ROAD only
motor_both = NEI[
    (NEI["fips"].isin(["24510", "06037"])) & (NEI["type"] == "ON-ROAD")
].copy()
motor_both["City"] = motor_both["fips"].map({
    "24510": "Baltimore City, MD",
    "06037": "Los Angeles County, CA"
})

grouped = motor_both.groupby(["City", "year"])["Emissions"].sum().reset_index()
colors = {"Baltimore City, MD": "tomato", "Los Angeles County, CA": "steelblue"}

fig, axes = plt.subplots(1, 2, figsize=(480/100, 480/100), dpi=100)
for ax, (city, group) in zip(axes, grouped.groupby("City")):
    ax.plot(group["year"], group["Emissions"], marker="o", color=colors[city], linewidth=2)
    ax.fill_between(group["year"], group["Emissions"], alpha=0.15, color=colors[city])
    ax.set_title(city, fontsize=9)
    ax.set_xlabel("Year")
    ax.set_ylabel("PM2.5 Emissions (tons)")
    ax.set_xticks([1999, 2002, 2005, 2008])

fig.suptitle("Motor Vehicle PM2.5 Emissions (1999–2008)\nBaltimore City vs Los Angeles County", fontsize=10)
plt.tight_layout()
plt.savefig("plot6.png", dpi=100, bbox_inches="tight")
plt.close()

# Print % change summary
print("% change in motor vehicle emissions (1999 → 2008):")
for city, group in grouped.groupby("City"):
    start = group[group["year"] == 1999]["Emissions"].values[0]
    end = group[group["year"] == 2008]["Emissions"].values[0]
    print(f"  {city}: {((end/start)-1)*100:.1f}%")
print("\nPlot 6 saved as plot6.png")

#!/usr/bin/env python
"""
Plot 5: How have motor vehicle emissions changed in Baltimore City from 1999–2008?
Line chart of ON-ROAD type emissions for Baltimore City (fips == "24510").
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Motor vehicles = ON-ROAD type, Baltimore City only
motor_baltimore = NEI[(NEI["fips"] == "24510") & (NEI["type"] == "ON-ROAD")]
motor_balt_by_year = motor_baltimore.groupby("year")["Emissions"].sum()

fig, ax = plt.subplots(figsize=(480/100, 480/100), dpi=100)
ax.plot(motor_balt_by_year.index, motor_balt_by_year.values, marker="o", color="darkorange", linewidth=2)
ax.fill_between(motor_balt_by_year.index, motor_balt_by_year.values, alpha=0.2, color="darkorange")
ax.set_xlabel("Year")
ax.set_ylabel("PM2.5 Emissions (tons)")
ax.set_title("Motor Vehicle PM2.5 Emissions\nBaltimore City, MD (1999–2008)")
ax.set_xticks([1999, 2002, 2005, 2008])
for yr, val in motor_balt_by_year.items():
    ax.annotate(f"{val:.1f}", (yr, val), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("plot5.png", dpi=100, bbox_inches="tight")
plt.close()
print("Plot 5 saved as plot5.png")

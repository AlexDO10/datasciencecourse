#!/usr/bin/env python
"""
Plot 3: Which source types in Baltimore City increased/decreased from 1999–2008?
Line chart per source type (POINT, NONPOINT, ON-ROAD, NON-ROAD) for Baltimore City.
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Filter Baltimore City, group by year and type
baltimore = NEI[NEI["fips"] == "24510"]
baltimore_type = baltimore.groupby(["year", "type"])["Emissions"].sum().reset_index()

colors = {"POINT": "steelblue", "NONPOINT": "tomato", "ON-ROAD": "seagreen", "NON-ROAD": "goldenrod"}

fig, ax = plt.subplots(figsize=(480/100, 480/100), dpi=100)
for source_type, group in baltimore_type.groupby("type"):
    ax.plot(group["year"], group["Emissions"], marker="o",
            label=source_type, color=colors.get(source_type))
ax.set_xlabel("Year")
ax.set_ylabel("PM2.5 Emissions (tons)")
ax.set_title("PM2.5 Emissions by Source Type\nBaltimore City, MD (1999–2008)")
ax.legend(title="Source Type")
ax.set_xticks([1999, 2002, 2005, 2008])
plt.tight_layout()
plt.savefig("plot3.png", dpi=100, bbox_inches="tight")
plt.close()
print("Plot 3 saved as plot3.png")

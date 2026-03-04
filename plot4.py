#!/usr/bin/env python
"""
Plot 4: How have US coal combustion emissions changed from 1999–2008?
Bar chart of total coal combustion PM2.5 emissions across the US per year.
"""

import pyreadr
import pandas as pd
import matplotlib.pyplot as plt

# Read data
NEI = pyreadr.read_r("ExploratoryDataAnalysis/summarySCC_PM25.rds")[None]
SCC = pyreadr.read_r("ExploratoryDataAnalysis/Source_Classification_Code.rds")[None]
NEI["Emissions"] = pd.to_numeric(NEI["Emissions"], errors="coerce")
NEI["year"] = NEI["year"].astype(int)

# Filter SCC for coal combustion sources
coal_scc = SCC[
    SCC["EI.Sector"].str.contains("Coal", case=False, na=False) &
    SCC["EI.Sector"].str.contains("Comb", case=False, na=False)
]["SCC"].astype(str)

coal_nei = NEI[NEI["SCC"].astype(str).isin(coal_scc)]
coal_by_year = coal_nei.groupby("year")["Emissions"].sum() / 1e3  # thousands of tons

fig, ax = plt.subplots(figsize=(480/100, 480/100), dpi=100)
ax.bar(coal_by_year.index.astype(str), coal_by_year.values, color="slategray", width=0.5)
ax.set_xlabel("Year")
ax.set_ylabel("PM2.5 Emissions (thousands of tons)")
ax.set_title("US PM2.5 Emissions from Coal Combustion (1999–2008)")
for i, (yr, val) in enumerate(coal_by_year.items()):
    ax.text(i, val + 1, f"{val:.1f}k", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("plot4.png", dpi=100, bbox_inches="tight")
plt.close()
print("Plot 4 saved as plot4.png")

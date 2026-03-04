#!/usr/bin/env python
"""
Plot 2: Time series of Global Active Power
This script reads household power consumption data and creates a time series plot
of the Global Active Power for February 1-2, 2007.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv("ExploratoryDataAnalysis/household_power_consumption.txt", sep=";")

# Filter for the two days
filteredDf = df[df["Date"].isin(["1/2/2007", "2/2/2007"])]

# Create DateTime column
filteredDf["DateTime"] = pd.to_datetime(filteredDf["Date"] + " " + filteredDf["Time"], format="%d/%m/%Y %H:%M:%S")

# Create the plot
plt.figure(figsize=(480/100, 480/100), dpi=100)
plt.plot(filteredDf['DateTime'], filteredDf['Global_active_power'], linewidth=0.5)
plt.xlabel('datetime')
plt.ylabel('Global Active Power (kilowatts)')
plt.title('Global Active Power')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot2.png', dpi=100, bbox_inches='tight')
plt.close()

print("Plot 2 saved as plot2.png")

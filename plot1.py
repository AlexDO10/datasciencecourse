#!/usr/bin/env python
"""
Plot 1: Histogram of Global Active Power
This script reads household power consumption data and creates a histogram
of the Global Active Power for February 1-2, 2007.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv("ExploratoryDataAnalysis/household_power_consumption.txt", sep=";")

# Filter for the two days
filteredDf = df[df["Date"].isin(["1/2/2007", "2/2/2007"])]

# Create the plot
plt.figure(figsize=(480/100, 480/100), dpi=100)  # 480x480 pixels
plt.hist(filteredDf['Global_active_power'], bins=30, color='red')
plt.xlabel('Global Active Power (kilowatts)')
plt.ylabel('Frequency')
plt.title('Global Active Power')
plt.savefig('plot1.png', dpi=100, bbox_inches='tight')
plt.close()

print("Plot 1 saved as plot1.png")

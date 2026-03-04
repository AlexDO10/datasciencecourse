#!/usr/bin/env python
"""
Plot 3: Time series of Energy sub metering
This script reads household power consumption data and creates a multi-line time series plot
of the three sub-metering values for February 1-2, 2007.
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
plt.plot(filteredDf['DateTime'], filteredDf['Sub_metering_1'], label='Sub_metering_1', linewidth=0.5)
plt.plot(filteredDf['DateTime'], filteredDf['Sub_metering_2'], label='Sub_metering_2', color='red', linewidth=0.5)
plt.plot(filteredDf['DateTime'], filteredDf['Sub_metering_3'], label='Sub_metering_3', color='blue', linewidth=0.5)
plt.xlabel('datetime')
plt.ylabel('Energy sub metering (kilowatts)')
plt.title('Energy sub metering')
plt.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot3.png', dpi=100, bbox_inches='tight')
plt.close()

print("Plot 3 saved as plot3.png")

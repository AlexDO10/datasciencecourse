#!/usr/bin/env python
"""
Plot 4: 2x2 subplots of power metrics
This script reads household power consumption data and creates a 2x2 subplot figure
showing Global Active Power, Voltage, Energy sub metering, and Global reactive power
for February 1-2, 2007.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv("ExploratoryDataAnalysis/household_power_consumption.txt", sep=";")

# Filter for the two days
filteredDf = df[df["Date"].isin(["1/2/2007", "2/2/2007"])]

# Create DateTime column
filteredDf["DateTime"] = pd.to_datetime(filteredDf["Date"] + " " + filteredDf["Time"], format="%d/%m/%Y %H:%M:%S")

# Create the 2x2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(480/100, 480/100), dpi=100)

# Top left: Global Active Power
axes[0, 0].plot(filteredDf['DateTime'], filteredDf['Global_active_power'], linewidth=0.5)
axes[0, 0].set_ylabel('Global Active Power (kilowatts)')
axes[0, 0].set_xlabel('datetime')
axes[0, 0].tick_params(axis='x', rotation=45)

# Top right: Voltage
axes[0, 1].plot(filteredDf['DateTime'], filteredDf['Voltage'], linewidth=0.5)
axes[0, 1].set_ylabel('Voltage')
axes[0, 1].set_xlabel('datetime')
axes[0, 1].tick_params(axis='x', rotation=45)

# Bottom left: Sub metering
axes[1, 0].plot(filteredDf['DateTime'], filteredDf['Sub_metering_1'], label='Sub_metering_1', linewidth=0.5)
axes[1, 0].plot(filteredDf['DateTime'], filteredDf['Sub_metering_2'], label='Sub_metering_2', color='red', linewidth=0.5)
axes[1, 0].plot(filteredDf['DateTime'], filteredDf['Sub_metering_3'], label='Sub_metering_3', color='blue', linewidth=0.5)
axes[1, 0].set_ylabel('Energy sub metering (kilowatts)')
axes[1, 0].set_xlabel('datetime')
axes[1, 0].legend(loc='upper right', fontsize='small')
axes[1, 0].tick_params(axis='x', rotation=45)

# Bottom right: Global Reactive Power
axes[1, 1].plot(filteredDf['DateTime'], filteredDf['Global_reactive_power'], linewidth=0.5)
axes[1, 1].set_ylabel('Global reactive power (kilowatts)')
axes[1, 1].set_xlabel('datetime')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('plot4.png', dpi=100, bbox_inches='tight')
plt.close()

print("Plot 4 saved as plot4.png")

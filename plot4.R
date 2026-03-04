# plot4.R
# Q4: How have US coal combustion emissions changed from 1999–2008?
# Bar chart of total coal combustion PM2.5 emissions across the US per year.

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")
SCC <- readRDS("ExploratoryDataAnalysis/Source_Classification_Code.rds")

# Filter SCC for coal combustion sources
coal_scc <- SCC[
  grepl("Coal", SCC$EI.Sector, ignore.case = TRUE) &
  grepl("Comb", SCC$EI.Sector, ignore.case = TRUE),
  "SCC"
]

# Subset NEI for coal combustion sources
coal_nei <- subset(NEI, SCC %in% coal_scc)
coal_by_year <- aggregate(Emissions ~ year, data = coal_nei, FUN = sum)
coal_by_year$Emissions <- coal_by_year$Emissions / 1e3  # thousands of tons

# Save to PNG
png("plot4.png", width = 480, height = 480)

barplot(
  coal_by_year$Emissions,
  names.arg = coal_by_year$year,
  col = "slategray",
  xlab = "Year",
  ylab = "PM2.5 Emissions (thousands of tons)",
  main = "US PM2.5 Emissions from Coal Combustion (1999–2008)",
  ylim = c(0, max(coal_by_year$Emissions) * 1.15)
)

dev.off()

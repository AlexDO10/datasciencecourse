# plot1.R
# Q1: Have total US PM2.5 emissions decreased from 1999 to 2008?
# Bar chart of total PM2.5 emissions for all US sources per year.

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Aggregate total emissions by year (in millions of tons)
total_by_year <- aggregate(Emissions ~ year, data = NEI, FUN = sum)
total_by_year$Emissions <- total_by_year$Emissions / 1e6

# Save to PNG
png("plot1.png", width = 480, height = 480)

barplot(
  total_by_year$Emissions,
  names.arg = total_by_year$year,
  col = "steelblue",
  xlab = "Year",
  ylab = "Total PM2.5 Emissions (millions of tons)",
  main = "Total PM2.5 Emissions in the US (1999–2008)",
  ylim = c(0, max(total_by_year$Emissions) * 1.15)
)

dev.off()

# plot2.R
# Q2: Have total Baltimore City PM2.5 emissions decreased from 1999 to 2008?
# Bar chart of total emissions for Baltimore City (fips == "24510").

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Filter Baltimore City
baltimore <- subset(NEI, fips == "24510")
baltimore_by_year <- aggregate(Emissions ~ year, data = baltimore, FUN = sum)

# Save to PNG
png("plot2.png", width = 480, height = 480)

barplot(
  baltimore_by_year$Emissions,
  names.arg = baltimore_by_year$year,
  col = "tomato",
  xlab = "Year",
  ylab = "Total PM2.5 Emissions (tons)",
  main = "Total PM2.5 Emissions — Baltimore City, MD (1999–2008)",
  ylim = c(0, max(baltimore_by_year$Emissions) * 1.15)
)

dev.off()

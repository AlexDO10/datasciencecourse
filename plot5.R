# plot5.R
# Q5: How have motor vehicle emissions changed in Baltimore City from 1999–2008?
# Line chart of ON-ROAD type emissions for Baltimore City (fips == "24510").

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Motor vehicles = ON-ROAD type, Baltimore City only
motor_baltimore <- subset(NEI, fips == "24510" & type == "ON-ROAD")
motor_by_year <- aggregate(Emissions ~ year, data = motor_baltimore, FUN = sum)

# Save to PNG
png("plot5.png", width = 480, height = 480)

plot(
  motor_by_year$year,
  motor_by_year$Emissions,
  type = "b",
  pch = 19,
  col = "darkorange",
  lwd = 2,
  xlab = "Year",
  ylab = "PM2.5 Emissions (tons)",
  main = "Motor Vehicle PM2.5 Emissions\nBaltimore City, MD (1999–2008)",
  xaxt = "n"
)
axis(1, at = c(1999, 2002, 2005, 2008))

dev.off()

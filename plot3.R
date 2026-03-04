# plot3.R
# Q3: Which source types in Baltimore City increased/decreased from 1999–2008?
# Line chart per source type using ggplot2.

library(ggplot2)

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Filter Baltimore City, aggregate by year and type
baltimore <- subset(NEI, fips == "24510")
baltimore_type <- aggregate(Emissions ~ year + type, data = baltimore, FUN = sum)

# Save to PNG
png("plot3.png", width = 480, height = 480)

p <- ggplot(baltimore_type, aes(x = year, y = Emissions, color = type, group = type)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_x_continuous(breaks = c(1999, 2002, 2005, 2008)) +
  labs(
    title = "PM2.5 Emissions by Source Type\nBaltimore City, MD (1999–2008)",
    x = "Year",
    y = "PM2.5 Emissions (tons)",
    color = "Source Type"
  ) +
  theme_bw()

print(p)
dev.off()

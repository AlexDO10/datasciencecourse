# plot3.R
# Q3: Which source types in Baltimore City increased/decreased from 1999–2008?
# Faceted line chart per source type using ggplot2.
# Decreased: NON-ROAD, NONPOINT, ON-ROAD | Increased: POINT (spike in 2005, then down)

library(ggplot2)

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Filter Baltimore City, aggregate by year and type
baltimore <- subset(NEI, fips == "24510")
baltimore_type <- aggregate(Emissions ~ year + type, data = baltimore, FUN = sum)

# Label each type with its trend for the subtitle
trend_label <- c(
  "NON-ROAD"  = "NON-ROAD (Decreased)",
  "NONPOINT"  = "NONPOINT (Decreased)",
  "ON-ROAD"   = "ON-ROAD (Decreased)",
  "POINT"     = "POINT (Increased)"
)
baltimore_type$type_label <- trend_label[baltimore_type$type]

# Save to PNG
png("plot3.png", width = 480, height = 480)

p <- ggplot(baltimore_type, aes(x = year, y = Emissions, color = type_label, group = type_label)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  facet_wrap(~ type_label, scales = "free_y", ncol = 2) +
  scale_x_continuous(breaks = c(1999, 2002, 2005, 2008)) +
  scale_color_manual(values = c(
    "NON-ROAD (Decreased)"  = "seagreen",
    "NONPOINT (Decreased)"  = "steelblue",
    "ON-ROAD (Decreased)"   = "goldenrod",
    "POINT (Increased)"     = "tomato"
  )) +
  labs(
    title = "PM2.5 Emissions by Source Type — Baltimore City, MD (1999–2008)",
    x = "Year",
    y = "PM2.5 Emissions (tons)"
  ) +
  theme_bw() +
  theme(legend.position = "none",
        strip.text = element_text(size = 8))

print(p)
dev.off()

# plot6.R
# Q6: Baltimore City vs Los Angeles County — which city saw greater change
# in motor vehicle (ON-ROAD) PM2.5 emissions from 1999–2008?
# Side-by-side line charts using ggplot2.

library(ggplot2)

NEI <- readRDS("ExploratoryDataAnalysis/summarySCC_PM25.rds")

# Filter both cities, ON-ROAD only
motor_both <- subset(NEI, fips %in% c("24510", "06037") & type == "ON-ROAD")
motor_both$City <- ifelse(motor_both$fips == "24510",
                          "Baltimore City, MD",
                          "Los Angeles County, CA")

grouped <- aggregate(Emissions ~ City + year, data = motor_both, FUN = sum)

# Save to PNG
png("plot6.png", width = 480, height = 480)

p <- ggplot(grouped, aes(x = year, y = Emissions, color = City, group = City)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  facet_wrap(~ City, scales = "free_y") +
  scale_x_continuous(breaks = c(1999, 2002, 2005, 2008)) +
  scale_color_manual(values = c("Baltimore City, MD" = "tomato",
                                "Los Angeles County, CA" = "steelblue")) +
  labs(
    title = "Motor Vehicle PM2.5 Emissions (1999–2008)\nBaltimore City vs Los Angeles County",
    x = "Year",
    y = "PM2.5 Emissions (tons)"
  ) +
  theme_bw() +
  theme(legend.position = "none")

print(p)
dev.off()

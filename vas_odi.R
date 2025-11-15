# Load libraries
library(readxl)
library(dplyr)
library(ggplot2)

# Read your file (update path if needed)
data <- read_excel("C:/Users/shaik/OneDrive/Documents/VAS_ODI/grouped_data.xlsx")

# Filter only needed columns
odi <- data %>% select(`Post Test VAS`, Group)

# Convert Group to factor
odi$Group <- as.factor(odi$Group)

# Summary statistics
summary_stats <- odi %>%
  group_by(Group) %>%
  summarise(
    mean = mean(`Post Test VAS`, na.rm = TRUE),
    median = median(`Post Test VAS`, na.rm = TRUE),
    sd = sd(`Post Test VAS`, na.rm = TRUE),
    se = sd / sqrt(n())
  )
print(summary_stats)

# Independent t-test
t_test_result <- t.test(`Post Test VAS` ~ Group, data = odi)
print(t_test_result)

# Boxplot
ggplot(odi, aes(x = Group, y = `Post Test VAS`, fill = Group)) +
  geom_boxplot() +
  labs(title = "Post-test ODI Comparison (Group 0 vs Group 1)",
       y = "Post-test ODI", x = "Group") +
  theme_minimal()

# Barplot of means with error bars (SE)
ggplot(summary_stats, aes(x = Group, y = mean, fill = Group)) +
  geom_col(width = 0.6) +
  geom_errorbar(aes(ymin = mean - se, ymax = mean + se), width = 0.2) +
  labs(title = "Mean Post-test ODI with Standard Errors",
       y = "Mean ODI") +
  theme_minimal()

rm(list = ls())
library("dplyr")
library("ggpubr")
library(car)
library(ggplot2)



df <- read.csv("/home/beedata/Documents/uni/SMDE/Assignment-1/laptop_data_cleaned.csv")
print(unique(df$Company))

# Read the laptop price data set and create a sub dataset including only laptop
# brands “Dell”,“Acer” and “Hp”

# List of values to filter by
values_to_filter <- c("Dell", "Acer", "HP")

# Filter dataframe by the column 'column_name' with values in 'values_to_filter'
filtered_df <- subset(df, Company %in% values_to_filter)

#  Summarize the variable “company”
filtered_df$Company <- factor(filtered_df$Company)

summary(filtered_df$Company)

# Check the overall distribution of Price and Weight for this subset.
# Check the overall distribution of Price and Weight for this subset.

pdf("q2_plt_1a.pdf")
#par(mfrow = c(1, 2), mar = c(2, 2, 1, 1), mai = c(0.1, 0.1, 0.1, 0.1), pin = c(3, 2))  # 1 row, 2 columns
par(mfrow = c(1, 2))
# Plot histogram of Price
hist(filtered_df$Price,
     main = "Distribution of Price",
     xlab = "Price Values",
     ylab = "Frequency")

dev.off()

pdf("q2_plt_1b.pdf")
#par(mfrow = c(1, 2), mar = c(2, 2, 1, 1), mai = c(0.1, 0.1, 0.1, 0.1), pin = c(3, 2))  # 1 row, 2 columns
par(mfrow = c(1, 2))
# Plot histogram of Price
hist(filtered_df$Weight,
     main = "Distribution of Weight",
     xlab = "Weight Values",
     ylab = "Frequency")

dev.off()
# Create model for testing
model_price <- lm(Price ~ Company + Weight + Company:Weight, data = filtered_df)
model_weight <- lm(Weight ~ Company + Price + Company:Price, data = filtered_df)
company_levels <- unique(filtered_df$Company)


## Check independence assumtion
# Calculate correlations between predictor variables
correlation_matrix <- cor(filtered_df[, c("Price", "Weight")])
print(correlation_matrix)
pdf("q2_plot_2.pdf")
library(corrplot)
corrplot(correlation_matrix, method = "circle")
dev.off()

# Durbin-Watson Test
durbin_watson_price <-car::durbinWatsonTest(model_price)
durbin_watson_weight <-car::durbinWatsonTest(model_weight)
print(durbin_watson_price)
print(durbin_watson_weight)


residuals_price_by_company <- split(resid(model_price), filtered_df$Company)
residuals_weight_by_company <- split(resid(model_weight), filtered_df$Company)


#Test if 'Price' follows normal distribution
# Set up multi-panel plot layout
pdf("q2_plot_3.pdf")

par(mfrow = c(1, 3))  # 2 rows, 2 columns

# Loop through each level of the company
for (company_level in names(residuals_price_by_company)) {
  cat("Company:", company_level, "\n")
  print(shapiro.test(residuals_price_by_company[[company_level]]))
  # Plot QQ plot
  qqnorm(residuals_price_by_company[[company_level]], main = paste("QQ Plot for", company_level))
  qqline(residuals_price_by_company[[company_level]])
  
  # Add text to the plot
  text(-2, 2, labels = paste("Company:", company_level), pos = 4)
}
dev.off()


par(mfrow = c(1, 1))  # 2 rows, 2 columns


#Test if 'Weight' follows normal distribution
# Set up multi-panel plot layout
pdf("q2_plot_4.pdf")
par(mfrow = c(1, 3))  # 2 rows, 2 columns

# Loop through each level of the company
for (company_level in names(residuals_weight_by_company)) {
  cat("Company:", company_level, "\n")
  print(shapiro.test(residuals_weight_by_company[[company_level]]))
  # Plot QQ plot
  qqnorm(residuals_weight_by_company[[company_level]], main = paste("QQ Plot for", company_level))
  qqline(residuals_weight_by_company[[company_level]])
  
  # Add text to the plot
  text(-2, 2, labels = paste("Company:", company_level), pos = 4)
}
dev.off()
par(mfrow = c(1, 1))  # 2 rows, 2 columns





# Bartlett's test for Price
bartlett_test <- bartlett.test(Price ~ Company, data = filtered_df)
print(bartlett_test)


# Bartlett's test for Weight
bartlett_test <- bartlett.test(Weight ~ Company, data = filtered_df)
print(bartlett_test)


## Do ANOVA
anova_result <- anova(model_price)

# View ANOVA table
print(anova_result)

## Brand and ts on price
# Model formula: price ~ brand * TS
filtered_df$TouchScreen <- factor(filtered_df$TouchScreen)

# plot
pdf("q2_plot_5.pdf")
boxplot(Price ~ TouchScreen + Company, data = filtered_df, col = c("salmon", "beige"), xlab="TouchScreen and Company distributions")
dev.off()
# Fit the two-way ANOVA model
model <- aov(Price ~ TouchScreen * Company, data = filtered_df)

# Print summary of the model
summary(model)

# Check assumptions
# 1. Normality of residuals
shapiro_test <- shapiro.test(residuals(model))
print(shapiro_test)

# 2. Homogeneity of variances
# Levene's test
levene_test <- leveneTest(residuals(model) ~ TouchScreen * Company, data = filtered_df)
print(levene_test)

# 3. Independence of observations
# You can check this assumption by examining the residuals plot or conducting Durbin-Watson test


# Durbin-Watson test
durbin_watson_test <- durbinWatsonTest(model)
print(durbin_watson_test)

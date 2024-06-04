library(ggplot2)
library(dplyr)
rm(list = ls())

library(MASS)
library(lmtest) 
library(car) # For assumption testing
# Load the dataset
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data1 <- read.csv("laptop_data_cleaned.csv")
data <- subset(data1, !Ram %in% 64) #delete the outlier from the dataset

# Convert categorical variables to factors
data$Company <- as.factor(data$Company)
data$TypeName <- as.factor(data$TypeName)
data$TouchScreen <- as.factor(data$TouchScreen)
data$Cpu_brand <- as.factor(data$Cpu_brand)
data$Gpu_brand <- as.factor(data$Gpu_brand)
data$Os <- as.factor(data$Os)

# Fit the initial model with Ram and SSD
base_model <- lm(Price ~ Ram + SSD, data = data)

# List of categorical variables
categorical_factors <- c("Company", "TypeName", "TouchScreen", "Cpu_brand", "Gpu_brand", "Os")
#iterate through every factor and add it to the base model
for (factor in categorical_factors) {
  formula <- paste("Price ~ Ram + SSD +", factor)
  model <- lm(formula, data = data) #our new model
  
  # Print summary of each model so we can evaluate them
  cat("\nSummary for model with factor:", factor, "\n")
  print(summary(model)) 
}
# Fit the final model
final_model <- lm(Price ~ Ram + SSD + Cpu_brand, data = data)
par(mfrow = c(1, 1)) 


# Residuals vs Fitted plot for linearity
plot(final_model, which = 1)

# Normal Q-Q plot for normality and histogram 
plot(final_model, which = 2)
hist(final_model$residuals)

#bp test to check homoscedasticity
bptest(final_model)

#to check independance
dwtest(final_model)
## now we try to transform the variables so we achieve homoscedasticity ##
##First we tries boxcox transformation
library(MASS)
boxcox_model <- boxcox(lm(Price ~ Ram + SSD, data = data))
lambda <- boxcox_model$x[which.max(boxcox_model$y)]
data$boxcox_Price <- (data$Price^lambda - 1) / lambda
data$boxcox_Ram <- (data$Ram^lambda - 1) / lambda
data$boxcox_SSD <- (data$SSD^lambda - 1) / lambda

model <- lm(boxcox_Price ~ boxcox_Ram + boxcox_SSD + Cpu_brand, data = data)
summary(model)
bptest(model)
hist(model$residuals)
plot(model, which = 2)

#Then Log transformation on Price
data$Log_Price <- log(data$Price)
modellog <- lm(Log_Price ~ Ram + SSD + Cpu_brand, data = data)
summary(modellog)
bptest(modellog)
hist(modellog$residuals)

#Then cubic root transformation
data$Ram_cubic_root <- data$Ram^(1/3)
data$SSD_cubic_root <- data$SSD^(1/3)
cubic_root_model <- lm(Price ~ Ram_cubic_root + SSD_cubic_root + Cpu_brand, data = data)
bptest(cubic_root_model)


#Then 4th root transformation
data$Ram_4_root <- data$Ram^(1/4)
data$SSD_4_root <- data$SSD^(1/4)
four_model <- lm(Price ~ Ram_4_root + SSD_4_root + Cpu_brand, data = data)
bptest(four_model)

#Finally, least squares
weights <- 1 / fitted(final_model)^2
wls_model <- lm(Price ~ Ram + SSD + Cpu_brand, data = data, weights = weights)
summary(wls_model)
bptest(wls_model)
hist(wls_model$residuals)
dwtest(wls_model)
vif(wls_model)
vif(final_model)


#Comparing the base_model to the wls_model aka best_model
# Compare the R-squared values
r_squared_base <- summary(base_model)$r.squared
r_squared_wls <- summary(wls_model)$r.squared

# Compare the adjusted R-squared values
adj_r_squared_base <- summary(base_model)$adj.r.squared
adj_r_squared_wls <- summary(wls_model)$adj.r.squared

# Compare AIC
aic_base <- AIC(base_model)
aic_wls <- AIC(wls_model)

# Compare BIC
bic_base <- BIC(base_model)
bic_wls <- BIC(wls_model)

# Compare p-values of coefficients (optional)
p_values_base <- summary(base_model)$coefficients[, 4]
p_values_wls <- summary(wls_model)$coefficients[, 4]

# Print the comparison
cat("Base model:\n")
cat("R-squared:", r_squared_base, "\n")
cat("Adjusted R-squared:", adj_r_squared_base, "\n")
cat("AIC:", aic_base, "\n")
cat("BIC:", bic_base, "\n")
cat("\n")

cat("WLS model:\n")
cat("R-squared:", r_squared_wls, "\n")
cat("Adjusted R-squared:", adj_r_squared_wls, "\n")
cat("AIC:", aic_wls, "\n")
cat("BIC:", bic_wls, "\n")

#Now we will check the validity using VIF values
library(car)
vif_values <- vif(wls_model)
print(vif_values)

#set working directory to current file location
#install lmtest package
install.packages("lmtest", force = TRUE) 
library(lmtest) 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(tidyverse) 
library(car) # For assumption testing
laptop_data <- read.csv("laptop_data_cleaned.csv", header = TRUE, sep = ",")

# You had already assigned the type of the variables. Now fit a linear regression model to predict price of laptops.  
# a)Consider  the  numerical  variables  in  the  data  set  and find  the  best  simple  linear  regression model to predict 
# the prices (Test  the assumptions and use  transformations if it is required.)
corMat <- laptop_data %>% 
  select(Price, where(is.numeric)) %>% 
  cor(use = "pairwise.complete.obs")
# Get the correlation of the Price variable with the other numerical variables
print(corMat["Price", ]) # Theres is a cprrelation between Price and Ram,
# Using Ram as it has the highest correlation with Price, had to remove outlier of 64GB
model_ram <- lm(Price ~ Ram, data = laptop_data)
(summary(model_ram))
bptest(model_ram) # test for Homoscedasticity
print(shapiro.test(model_ram$residuals) )# Shapiro-Wilk Test, test for normality of residuALS
hist(model_ram$residuals)
# test for linearity of the relationship between the dependent and independent variables using a scatter plot
plot(laptop_data$Ram, laptop_data$Price, main = "Price vs Log(Ram)", xlab = "Log(Ram)", ylab = "Price", pch = 19, col = "blue")
# add regression line to the scatter plot
abline(model_ram, col = "red")
#scatter plot tells us that the relationship between price and ram is linear
# residual vs fitted plot tells us that the residuals are homoscedastic
# histogram tells us that the residuals are normally distributed
# qq plot tells us that the residuals are normally distributed
# Assumptions:
par(mfrow = c(2, 2))  # Arrange plots in a 2x2 grid
plot(model_ram) 


# b) Fit a multivariate linear regression model with two (numerical) independent variables. Choose the most significant regression 
# model with two predictors. (Transform the variables if it is needed and test all the assumptions.)
# Then compare this model to the simple linear regression model that you fit in (a). Which one is a better model? Why? (25p)
# Assuming 'laptop_data' has your data and 'Price' is the dependent variable
# A list of potential predictors 
potential_predictors <- c("Ram", "SSD", "Ppi") 

# Remove the dependent variable ('Price') from the list
potential_predictors <- potential_predictors[!potential_predictors == "Price"]

# Function to build a model, check assumptions, and store results (modify as needed)
build_and_assess_model <- function(formula, data) {
  model <- lm(formula, data = data)
  # Add assumption checks here using 'plot(model)'... 
  results <- summary(model)$adj.r.squared
  return(results)  
}

# Empty container to store model results
model_results <- matrix(nrow = choose(length(potential_predictors), 2), 
                        ncol = 4,
                        dimnames = list(NULL, c("Combination", "Adj. R-squared", "AIC", "BIC")))

# Loop through combinations of two predictors
counter <- 1
for (i in 1:(length(potential_predictors) - 1)) {
  for (j in (i + 1):length(potential_predictors)) {
    formula <- as.formula(paste("Price ~", potential_predictors[i], "+", potential_predictors[j]))
    model_results[counter,] <- c(paste(potential_predictors[i], "+", potential_predictors[j]), build_and_assess_model(formula, data = laptop_data))
    counter <- counter + 1
  }
}

# Print the results
print(model_results)


# Select the two most significant predictors
best_model <- lm(Price ~ Ram + SSD, data = laptop_data)
plot(best_model)
summary(best_model)
bptest(best_model)
print(shapiro.test(best_model$residuals) )# Shapiro-Wilk Tes
hist(best_model$residuals)
dwtest(best_model)#use dw test to check for autocorrelation




# Check the assumptions of the multivariate linear regression model

# Compare the models using metrics like R-squared, adjusted R-squared, and AIC/BIC values

# c) Now add a factor to the regression model you have chosen in section (b). (You can write a loop to add factors one by one to 
# the previous model and decide based on the results.) Interpret the coefficients and overall summary of the model.
# Test the model in section (b) with the model that has an additional factor. Which one would you choose? Why? (35p)

# Add a factor variable to the model

# Interpret the coefficients and overall summary of the model

# Compare the models using metrics like R-squared, adjusted R-squared, and AIC/BIC values

# d) Test the validity of the final model. (15p)

# Perform hypothesis tests on the coefficients to assess their significance

# Check the overall significance of the model using an F-test

# Evaluate the goodness of fit of the model using metrics like R-squared, adjusted R-squared, and AIC/BIC values

# Perform diagnostic checks on the model assumptions
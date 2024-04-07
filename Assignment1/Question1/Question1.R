echo = TRUE 
# a) Import data set to R assigning the type of each variable correctly. (5p)
laptop_prices <- read.csv("laptop_data_cleaned.csv", header = TRUE, sep = ",")

# b) Create a dataset including only types of laptops: Ultrabook, Notebook and 2 in 1 Convertible. (5p)
laptop_prices_filtered <- laptop_prices[laptop_prices$TypeName %in% c("Ultrabook", "Notebook", "2 in 1 Convertible"), ]
print(head(laptop_prices_filtered)) 

#print(head(laptop_prices_filtered))
# c) Summarize the variables Weight, Price and the categorical variables in the new created data set. (10p)

print("Summary of the variables in the new created data set:")
# 1. Identify Columns to Convert
columns_to_convert <- c("Company", "TypeName", "TouchScreen", "Ips", "Cpu_brand", "Gpu_brand", "Os", "HDD", "SSD", "Ram", "Ppi")

for (column_name in columns_to_convert) {
  laptop_prices_filtered[, column_name] <- factor(laptop_prices_filtered[, column_name])
}
print(summary(laptop_prices_filtered))

# d) Cross classify the variables type of computer and the touch screen indicator in a table. Compute and interpret the conditional probability tables. (15p)
# Replace 1 with "Touch Screen" and 0 with "No Touch Screen" 
laptop_prices_filtered$TouchScreen <- factor(laptop_prices_filtered$TouchScreen,
                                             levels = c(0, 1),
                                             labels = c("Not Touch Screen", "Touch Screen"))

# Cross-classification table
print("Probability table for TypeName and TouchScreen:")
print(table(laptop_prices_filtered$TypeName, laptop_prices_filtered$TouchScreen))

# Conditional probability tables
print(prop.table(table(laptop_prices_filtered$TypeName, laptop_prices_filtered$TouchScreen), 1)) 
print(prop.table(table(laptop_prices_filtered$TypeName, laptop_prices_filtered$TouchScreen), 2)) 


# e) Is there an association between the type of computer and the touch screen characteristic of a computer. Analyze it by using proper statistical method. (10p)
print("Chi-square test for TypeName and TouchScreen:")
print(chisq.test(table(laptop_prices_filtered$TypeName, laptop_prices_filtered$TouchScreen)))

# f) Check the distribution of Price first for all observations then for subgroups of type of laptop in the data set created in section (b).
#     Does it follow a normal distribution? (15p)
#Histogram for all observations
print("Shapiro-Wilk test for Price for all observations:")
hist(laptop_prices_filtered$Price, main = "Histogram of Price for all observations", xlab = "Price", ylab = "Frequency", col = "lightblue")
print(shapiro.test(laptop_prices_filtered$Price))

print("Shapiro-Wilk test for Price for subgroups of type of laptop:")
#Histogram for subgroups of type of laptop
hist(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "Ultrabook"], main = "Histogram of Price for Ultrabooks", xlab = "Price", ylab = "Frequency", col = "lightblue")
print(shapiro.test(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "Ultrabook"]))

hist(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "Notebook"], main = "Histogram of Price for Notebooks", xlab = "Price", ylab = "Frequency", col = "lightblue")
print(shapiro.test(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "Notebook"]))

hist(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "2 in 1 Convertible"], main = "Histogram of Price for 2 in 1 Convertibles", xlab = "Price", ylab = "Frequency", col = "lightblue")
print(shapiro.test(laptop_prices_filtered$Price[laptop_prices_filtered$TypeName == "2 in 1 Convertible"]))

# g) Create a data frame just by including Ultrabooks and Notebooks. (5p)
laptop_prices_filtered_2 <- laptop_prices_filtered[laptop_prices_filtered$TypeName %in% c("Ultrabook", "Notebook"), ]
laptop_prices_filtered_2$TypeName <- factor(laptop_prices_filtered_2$TypeName,
                                            levels = c("Ultrabook", "Notebook")) # Specify only desired levels

# Now create the boxplot
boxplot(Price ~ TypeName, data = laptop_prices_filtered_2)


# h) Make a boxplot to show the distribution of Price across two categories of Type: Ultrabook vs. Notebook. Interpret it. (10p)
boxplot(Price ~ TypeName, data = laptop_prices_filtered_2)

# i) Compare the average price of Ultrabooks and Notebooks by using the appropriate method. Do not forget to test the assumptions. (25p)

print("T-test for Price between Ultrabooks and Notebooks:")
print(t.test(Price ~ TypeName, data = laptop_prices_filtered_2))

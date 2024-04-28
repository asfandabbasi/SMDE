rm(list = ls())
library(FactoMineR)
library(car)
library(ggplot2)
library(corrplot)
library(ggcorrplot)
library(psych)
library(lmtest)

data(decathlon)
head(decathlon)


#res.pca = PCA(decathlon[,1:12], scale.unit=TRUE, ncp=5, quanti.sup=c(11: 12), graph=T)
# Filter dataset for quantitative columns only.
cols_pca = c("100m", "Long.jump", "Shot.put", "High.jump", "400m", "110m.hurdle", "Discus", "Pole.vault", "Javeline", "1500m","Points")

decastar <- subset(decathlon, Competition == "Decastar")[,cols_pca]
olympic <- subset(decathlon, Competition == "OlympicG")[,cols_pca]
decastar <- scale(decastar)  # Standardize the Decastar data
olympic <- scale(olympic)    # Standardize the Olympic data


# Check independence or weak dependence
correlation_matrix_decastar <- cor(decastar)  # Correlation matrix for Decastar data
correlation_matrix_olympic <- cor(olympic)    # Correlation matrix for Olympic data
# Create correlation plots
pdf("q4_plot_1a.pdf")
par(mfrow = c(1, 1))  # 1 row, 2 columns
ggcorrplot(cor(decastar))
dev.off()

pdf("q4_plot_1b.pdf")
par(mfrow = c(1, 1))  # 1 row, 2 columns
ggcorrplot(cor(olympic))
dev.off()



# Perform Bartlett's test for sphericity
# Bartlett's test
n_decastar <- nrow(decastar)
n_olympic <- nrow(olympic)
bartlett_decastar <- cortest.bartlett(correlation_matrix_decastar, n_decastar)
bartlett_olympic <- cortest.bartlett(correlation_matrix_olympic, n_decastar)

# Print the results
print(bartlett_decastar)
print(bartlett_olympic)

#Apply PCA
pca_decastar <- PCA(decastar, scale.unit = TRUE, ncp = 5)
pca_olympic <- PCA(olympic, scale.unit = TRUE, ncp = 5)

# Plot PCA results for variables and individuals
pdf("q4_plot_2a_decastar.pdf")
plot(pca_decastar, choix = "var", main = "PCA graph of variables in Décastar competition")
dev.off()
pdf("q4_plot_2b_olympic.pdf")
plot(pca_olympic, choix = "var", main = "PCA graph of variables in Olympic competition")
dev.off()
pdf("q4_plot_3a_decastar.pdf")
plot(pca_decastar, choix = "ind")
dev.off()
pdf("q4_plot_3b_olympic.pdf")
plot(pca_olympic, choix = "ind")
dev.off()
summary(pca_decastar)
summary(pca_olympic)

#Linear Regression
# Add the response variable to the data frame containing the principal components
pc_decastar <- pca_decastar$ind$coord[, 1:5]  # First 5 principal components for Decastar
pc_olympic <- pca_olympic$ind$coord[, 1:5]    # First 5 principal components for Olympic

pc_decastar_with_response <- cbind(pc_decastar, Points = decastar[,"Points"])
pc_olympic_with_response <- cbind(pc_olympic, Points = olympic[,"Points"])

# Perform linear regression using the first 5 principal components along with the response variable
# For Decastar
lm_decastar <- lm(Points ~ ., data = as.data.frame(pc_decastar_with_response))
summary(lm_decastar)  # Summary of the regression model

# For Olympic
lm_olympic <- lm(Points ~ ., data = as.data.frame(pc_olympic_with_response))
summary(lm_olympic)  # Summary of the regression model

# New Lms
lm_olympic <- lm(Points ~ Dim.1 + Dim.3 + Dim.4, data = data.frame(pc_olympic_with_response))
lm_decastar <- lm(Points ~Dim.1 + Dim.3 + Dim.5 , data = as.data.frame(pc_decastar_with_response))
summary(lm_decastar)  # Summary of the regression model
summary(lm_olympic)
# Predictions for Olympic data
predictions_olympic <- predict(lm_olympic, newdata = data.frame(pc_olympic_with_response)[c(1, 3, 4)], interval = "prediction")
predictions_decastar <- predict(lm_decastar, newdata = data.frame(pc_decastar_with_response)[c(1, 3, 5)], interval = "prediction")
plot(data.frame(pc_olympic_with_response)$Points, predictions_olympic[, 1], xlab = "Recorded points", ylab = "Predicted points", main = "Olympic Games points predictions")
abline(0, 1)
plot(data.frame(pc_decastar_with_response)$Points, predictions_decastar[, 1], xlab = "Recorded points", ylab = "Predicted points", main = "Decastar Games points predictions")
abline(0, 1)

# Test assumptions 
shapiro.test(residuals(lm_olympic))
bptest(lm_olympic)

shapiro.test(residuals(lm_decastar))
bptest(lm_decastar)

# Plot residuals 
plot(residuals(lm_olympic))
plot(residuals(lm_decastar))

# Durbin-Watson test 
dwtest(lm_olympic, alternative = "two.sided")
dwtest(lm_decastar, alternative = "two.sided")

# Bartlett's test for Olympic data
n_olympic <- nrow(olympic[, 1:10])
cortest.bartlett(cor(scale(olympic)), n_olympic)
n_decastar <- nrow(decastar[, 1:10])
cortest.bartlett(cor(scale(decastar)), n_decastar)


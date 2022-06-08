rm(list=ls())
library(data.table)

data <- fread("../../Results/predictions_NC_test_FLGA_train_with_indis_s.csv")

pdf(file = "../../Visualizations/Bracketed_Predictions.pdf", width = 10, height = 8)
par(mfrow=c(2,2))
c1 <- sum(data$race[data$Black < 0.25] == "Black")/length(data$race[data$Black < 0.25])
c2 <- sum(data$race[data$Black >= 0.25 & data$Black < 0.50] == "Black")/length(data$race[data$Black >= 0.25 & data$Black < 0.50])
c3 <- sum(data$race[data$Black >= 0.50 & data$Black < 0.75] == "Black")/length(data$race[data$Black >= 0.50 & data$Black < 0.75])
c4 <- sum(data$race[data$Black >= 0.75] == "Black")/length(data$race[data$Black >= 0.75])

plot(c(0.3, 0.9, 1.5, 2.1), c(c1, c2, c3, c4),
     ylim = c(0, 1), xlim = c(0, 2.4), las = 1,
     pch = 16, 
     ylab = "True Proportion",
     main = "Black",
     xlab = "Predicted Probability",
     xaxt = "n")
lines(c(0.3, 0.3), c(0, c1))
lines(c(0.9, 0.9), c(0, c2))
lines(c(1.5, 1.5), c(0, c3))
lines(c(2.1, 2.1), c(0, c4))
axis(1, at = c(0.3, 0.9, 1.5, 2.1), label = c("[0, 0.25)",
                                               "[0.25, 0.50)",
                                               "[0.50, 0.75)",
                                               "[0.75, 1]"))
     
c1 <- sum(data$race[data$White < 0.25] == "White")/length(data$race[data$White < 0.25])
c2 <- sum(data$race[data$White >= 0.25 & data$White < 0.50] == "White")/length(data$race[data$White >= 0.25 & data$White < 0.50])
c3 <- sum(data$race[data$White >= 0.50 & data$White < 0.75] == "White")/length(data$race[data$White >= 0.50 & data$White < 0.75])
c4 <- sum(data$race[data$White >= 0.75] == "White")/length(data$race[data$White >= 0.75])

plot(c(0.3, 0.9, 1.5, 2.1), c(c1, c2, c3, c4),
     ylim = c(0, 1), xlim = c(0, 2.4), las = 1,
     pch = 16, 
     ylab = "True Proportion",
     main = "White",
     xlab = "Predicted Probability",
     xaxt = "n")
lines(c(0.3, 0.3), c(0, c1))
lines(c(0.9, 0.9), c(0, c2))
lines(c(1.5, 1.5), c(0, c3))
lines(c(2.1, 2.1), c(0, c4))
axis(1, at = c(0.3, 0.9, 1.5, 2.1), label = c("[0, 0.25)",
                                              "[0.25, 0.50)",
                                              "[0.50, 0.75)",
                                              "[0.75, 1]"))

c1 <- sum(data$race[data$Asian < 0.25] == "Asian")/length(data$race[data$Asian < 0.25])
c2 <- sum(data$race[data$Asian >= 0.25 & data$Asian < 0.50] == "Asian")/length(data$race[data$Asian >= 0.25 & data$Asian < 0.50])
c3 <- sum(data$race[data$Asian >= 0.50 & data$Asian < 0.75] == "Asian")/length(data$race[data$Asian >= 0.50 & data$Asian < 0.75])
c4 <- sum(data$race[data$Asian >= 0.75] == "Asian")/length(data$race[data$Asian >= 0.75])

plot(c(0.3, 0.9, 1.5, 2.1), c(c1, c2, c3, c4),
     ylim = c(0, 1), xlim = c(0, 2.4), las = 1,
     pch = 16, 
     ylab = "True Proportion",
     main = "Asian",
     xlab = "Predicted Probability",
     xaxt = "n")
lines(c(0.3, 0.3), c(0, c1))
lines(c(0.9, 0.9), c(0, c2))
lines(c(1.5, 1.5), c(0, c3))
lines(c(2.1, 2.1), c(0, c4))
axis(1, at = c(0.3, 0.9, 1.5, 2.1), label = c("[0, 0.25)",
                                              "[0.25, 0.50)",
                                              "[0.50, 0.75)",
                                              "[0.75, 1]"))

c1 <- sum(data$race[data$Hispanic < 0.25] == "Hispanic")/length(data$race[data$Hispanic < 0.25])
c2 <- sum(data$race[data$Hispanic >= 0.25 & data$Hispanic < 0.50] == "Hispanic")/length(data$race[data$Hispanic >= 0.25 & data$Hispanic < 0.50])
c3 <- sum(data$race[data$Hispanic >= 0.50 & data$Hispanic < 0.75] == "Hispanic")/length(data$race[data$Hispanic >= 0.50 & data$Hispanic < 0.75])
c4 <- sum(data$race[data$Hispanic >= 0.75] == "Hispanic")/length(data$race[data$Hispanic >= 0.75])

plot(c(0.3, 0.9, 1.5, 2.1), c(c1, c2, c3, c4),
     ylim = c(0, 1), xlim = c(0, 2.4), las = 1,
     pch = 16, 
     ylab = "True Proportion",
     main = "Hispanic",
     xlab = "Predicted Probability",
     xaxt = "n")
lines(c(0.3, 0.3), c(0, c1))
lines(c(0.9, 0.9), c(0, c2))
lines(c(1.5, 1.5), c(0, c3))
lines(c(2.1, 2.1), c(0, c4))
axis(1, at = c(0.3, 0.9, 1.5, 2.1), label = c("[0, 0.25)",
                                              "[0.25, 0.50)",
                                              "[0.50, 0.75)",
                                              "[0.75, 1]"))


dev.off()



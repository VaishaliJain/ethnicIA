## Moving Avg: SMALL DONORS
rm(list=ls())
library(data.table)
library(stringr)

## Merge the Names Data
data <- fread("../../Data/CaseStudy/FECdata.csv")

## Contributions by Weeks/Days to Election
data$TRANSACTION_DT <- str_pad(data$TRANSACTION_DT, 8, pad = "0")
data$TRANSACTION_DT <- as.Date(data$TRANSACTION_DT, format = "%m%d%Y")
data$days_to_election <- as.Date("2020-11-03") - data$TRANSACTION_DT
data <- data[TRANSACTION_DT < "2021-01-31", ]

data <- data[presidential_race == 1, ]

## Merge the Names Data
data$small_donors <- as.numeric(data$TRANSACTION_AMT < 1000)
data <- data[small_donors == 1, ]

data[, de_ID := .GRP, by = c("CAND_NAME", "CAND_PID", "predicted_race", "presidential_race")]
data[, count_donors := .N, by = c("de_ID", "days_to_election")]

temp.01 <- temp.02 <- list()
for(i in 1:max(data$de_ID)) {
  data.temp <- data[de_ID == i, ]
  
  for(j in 1:100) {
    week.data <- subset(data.temp,                        
                        subset = (as.numeric(data.temp$days_to_election) > (100 - j) 
                                  & as.numeric(data.temp$days_to_election) <= (100 - j + 7)))
    temp.01[[j]] <- c(j, mean(week.data$count_donors, na.rm = TRUE))
  }
  
  temp.02[[i]] <- cbind(i, do.call('rbind', temp.01))
}

moving <- data.table(do.call('rbind', temp.02))
colnames(moving) <- c("de_ID", "days_to_election","mov_amount")
moving$mov_amount[is.nan(moving$mov_amount)] <- 0
moving$days_to_election <- abs(moving$days_to_election - 100)

data.mov <- data[, .(.N), by = c("de_ID", "CAND_NAME", "CAND_PID", "predicted_race", "presidential_race")]

data.mov.f <- merge(moving, data.mov, by = "de_ID")
data.mov.f$N <- NULL



write.csv(data.mov.f, file = "../../Data/CaseStudy/FECdata_WeeksToElection_SmallDonorCount.csv", row.names = F)

data.mov.f$mov_amount <- data.mov.f$mov_amount/1000

mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "White" & data.mov.f$CAND_NAME == "BIDEN"])/mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "White" & data.mov.f$CAND_NAME == "TRUMP"])
mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Black" & data.mov.f$CAND_NAME == "BIDEN"])/mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Black" & data.mov.f$CAND_NAME == "TRUMP"])
mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Hispanic" & data.mov.f$CAND_NAME == "BIDEN"])/mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Hispanic" & data.mov.f$CAND_NAME == "TRUMP"])
mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Asian" & data.mov.f$CAND_NAME == "BIDEN"])/mean(data.mov.f$mov_amount[data.mov.f$days_to_election < 7 & data.mov.f$predicted_race == "Asian" & data.mov.f$CAND_NAME == "TRUMP"])


pdf(file = "../../Visualizations/Donors/small_donors.pdf", width = 8, height = 8)
par(mfrow=c(2,2))
plot(data.mov.f$days_to_election[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "White"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "White"],
     type = "l", col = "blue", las = 1, xlab = "Days to Election", ylab = "Number of Small Donors (in thousands)", main = "White Donors", ylim = c(0, 80))
points(data.mov.f$days_to_election[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "White"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "White"], col = "red", type = "l",
       lty = "dashed")
legend(60, 70, legend=c("Trump", "Biden"),
       col=c("red", "blue"), lty=2:1, cex=1)

plot(data.mov.f$days_to_election[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Black"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Black"],
     type = "l", col = "blue", las = 1, xlab = "Days to Election", ylab = "Number of Small Donors (in thousands)", main = "Black Donors", ylim = c(0, 80))
points(data.mov.f$days_to_election[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Black"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Black"], col = "red", type = "l",
       lty = "dashed")

plot(data.mov.f$days_to_election[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Hispanic"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Hispanic"],
     type = "l", col = "blue", las = 1, xlab = "Days to Election", ylab = "Number of Small Donors (in thousands)", main = "Hispanic Donors", ylim = c(0, 80))
points(data.mov.f$days_to_election[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Hispanic"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Hispanic"], col = "red", type = "l",
       lty = "dashed")

plot(data.mov.f$days_to_election[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Asian"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "DEM" & data.mov.f$predicted_race == "Asian"],
     type = "l", col = "blue", las = 1, xlab = "Days to Election", ylab = "Number of Small Donors (in thousands)", main = "Asian Donors", ylim = c(0, 80))
points(data.mov.f$days_to_election[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Asian"], data.mov.f$mov_amount[data.mov.f$CAND_PID == "REP" & data.mov.f$predicted_race == "Asian"], col = "red", type = "l",
       lty = "dashed")
dev.off()


## Moving Avg: SMALL DONORS
rm(list=ls())
library(data.table)
library(stringr)

## Merge the Names Data
data <- fread("../../Data/CaseStudy/FECdata.csv")

data <- data[presidential_race == 1, ]

## Amounts
data[STATE == "FL", .(amount = sum(TRANSACTION_AMT)), by = c("CAND_NAME", "predicted_race")]

## Transactions
data[STATE == "FL", .(amount = .N), by = c("CAND_NAME", "predicted_race")]


## Amounts
data[STATE == "FL" & TRANSACTION_AMT < 1000, .(amount = sum(TRANSACTION_AMT)), by = c("CAND_NAME", "predicted_race")]

## Transactions
data[STATE == "FL"  & TRANSACTION_AMT < 1000, .(amount = .N), by = c("CAND_NAME", "predicted_race")]

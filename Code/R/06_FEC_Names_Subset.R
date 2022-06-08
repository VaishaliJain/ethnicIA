rm(list = ls())
library(data.table)
library('stringr')

data <- fread("../../Data/CaseStudy/FECdataRaw_UP.csv")

## Keep only the official committees
data <- data[!(CMTE_ID %in% c("C00314575", "C00544684")), ]

## Merge the Names Data
data.class <- fread("../../Results/predictions_CaseStudy_test_FLGANC_train_s.csv")
data.class$first_name <- data.class$last_name <- NULL
data <- merge(data, data.class, by = "id", all.x = TRUE)
data$ZIP_CODE <- substr(data$ZIP_CODE, 1, 5)
data$predicted_race[is.na(data$predicted_race)] <- "Indistinguishable"
data$presidential_race <- ifelse(data$CAND_NAME %in% c("TRUMP", "BIDEN"), 1, 0)

data$TRANSACTION_DT <- str_pad(data$TRANSACTION_DT, 8, pad = "0")
data$TRANSACTION_DT <- as.Date(data$TRANSACTION_DT, format = "%m%d%Y")
data$days_to_election <- as.Date("2020-11-03") - data$TRANSACTION_DT
data <- data[TRANSACTION_DT < "2021-01-31", ]

write.csv(data, file = "../../Data/CaseStudy/FECdata.csv", row.names = F)

## Contributions by Candidate, State, City
data.city <- data[, .(amount = sum(TRANSACTION_AMT)), by = c("CITY", "STATE", "CAND_NAME", "CAND_PID","predicted_race", "presidential_race")]
write.csv(data.city, file = "../../Data/CaseStudy/FECdata_City.csv", row.names = F)

## Contributions by Weeks/Days to Election
data$TRANSACTION_DT <- str_pad(data$TRANSACTION_DT, 8, pad = "0")
data$TRANSACTION_DT <- as.Date(data$TRANSACTION_DT, format = "%m%d%Y")

data$days_to_election <- as.Date("2020-11-03") - data$TRANSACTION_DT

data$weeks_to_election <- (as.numeric(data$days_to_election - 1) %/% 7) + 1
data.weeks <- data[, .(amount = sum(TRANSACTION_AMT)), by = c("STATE", "CAND_NAME", "CAND_PID", "predicted_race", "weeks_to_election", "presidential_race")]
write.csv(data.weeks, file = "../../Data/CaseStudy/FECdata_WeeksToElection.csv", row.names = F)

data[, de_ID := .GRP, by = c("STATE", "CAND_NAME", "CAND_PID", "predicted_race", "presidential_race")]

temp.01 <- temp.02 <- list()
for(i in 1:max(data$de_ID)) {
  data.temp <- data[de_ID == i, ]

  for(j in 1:100) {
    week.data <- subset(data.temp,                        
                        subset = (as.numeric(data.temp$days_to_election) > (100 - j) 
                        & as.numeric(data.temp$days_to_election) <= (100 - j + 7)))
    temp.01[[j]] <- c(j, mean(week.data$TRANSACTION_AMT, na.rm = TRUE))
  }
  
  temp.02[[i]] <- cbind(i, do.call('rbind', temp.01))
}

moving <- data.table(do.call('rbind', temp.02))
colnames(moving) <- c("de_ID", "days_to_election","mov_amount")

data.mov <- data[, .(.N), by = c("de_ID", "STATE", "CAND_NAME", "CAND_PID", "predicted_race", "presidential_race")]

data.mov.f <- merge(moving, data.mov, by = "de_ID")
data.mov.f$N <- NULL

write.csv(data.mov.f, file = "../../Data/CaseStudy/FECdata_WeeksToElection_MovingAverage.csv", row.names = F)


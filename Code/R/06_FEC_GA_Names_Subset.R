rm(list = ls())
library(data.table)
library('stringr')

data <- fread("../../Data/CaseStudy/FECdataRaw_GA_UP.csv")

## Keep only the official committees
data <- data[!(CMTE_ID %in% c("C00314575", "C00544684")), ]

## Merge the Names Data
data.class <- fread("../../Results/predictions_CaseStudy_GA_test_FLGANC_train_s.csv")
data.class$first_name <- data.class$last_name <- NULL
data <- merge(data, data.class, by = "id", all.x = TRUE)
data$ZIP_CODE <- substr(data$ZIP_CODE, 1, 5)
data$predicted_race[is.na(data$predicted_race)] <- "Indistinguishable"
data$presidential_race <- ifelse(data$CAND_NAME %in% c("TRUMP", "BIDEN"), 1, 0)
data$STATE <- data$contributor_state
data$CITY <- data$contributor_city
data$contributor_state <- NULL
write.csv(data, file = "../../Data/CaseStudy/FECdata_GA.csv", row.names = F)


## Contributions by Candidate, State, City
data.city <- data[, .(amount = sum(TRANSACTION_AMT)), by = c("CITY", "STATE", "CAND_NAME", "CAND_PID","predicted_race", "presidential_race")]
write.csv(data.city, file = "../../Data/CaseStudy/FECdata_GA_City.csv", row.names = F)

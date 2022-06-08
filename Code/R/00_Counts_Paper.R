rm(list=ls())
library(data.table)
library(glmnet)

data <- fread("../../Data/NameRaceData/FL.csv")

data$first_name[data$first_name == ""] <- NA
data$last_name[data$last_name == ""] <- NA
data <- data[!is.na(first_name), ]
data <- data[!is.na(last_name), ]
data <- data[!is.na(race), ]

data[ , count_fn := .N, by = c("first_name") ]
data[ , count_ln := .N, by = c("last_name") ]

sum(data$count_fn <= 5 & data$count_ln <= 5)
sum(data$count_fn <= 10 & data$count_ln <= 10)
sum(data$count_fn <= 15 & data$count_ln <= 15)
nrow(data)
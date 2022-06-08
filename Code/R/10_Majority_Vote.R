rm(list=ls())
library(data.table)

## --------------------
## Load Data
## --------------------

train.data <- fread("../../Data/NameRaceData/FL.csv")
train.data$id <- 1:nrow(train.data)

train.data$first_name[train.data$first_name == ""] <- NA
train.data$last_name[train.data$last_name == ""] <- NA
train.data <- train.data[!is.na(first_name), ]
train.data <- train.data[!is.na(last_name), ]
train.data <- train.data[!is.na(race), ]

test.data <- fread("../../Data/NameRaceData/NC.csv")
test.data$id <- 1:nrow(test.data)

test.data$first_name[test.data$first_name == ""] <- NA
test.data$last_name[test.data$last_name == ""] <- NA
test.data <- test.data[!is.na(first_name), ]
test.data <- test.data[!is.na(last_name), ]
test.data <- test.data[!is.na(race), ]

## Take 1: Exact matches in terms of Names (First + Last Name)

## Calculate the majority voting for each name of the train data:
train.data[race == "White", count_white := .N, by = c("first_name", "last_name")]
train.data[race == "Black", count_black := .N, by = c("first_name", "last_name")]
train.data[race == "Hispanic", count_hispa := .N, by = c("first_name", "last_name")]
train.data[race == "Asian", count_asian := .N, by = c("first_name", "last_name")]

train.data[ , count_white_f := mean(count_white, na.rm = T), by = c("first_name", "last_name")]
train.data[ , count_black_f := mean(count_black, na.rm = T), by = c("first_name", "last_name")]
train.data[ , count_hispa_f := mean(count_hispa, na.rm = T), by = c("first_name", "last_name")]
train.data[ , count_asian_f := mean(count_asian, na.rm = T), by = c("first_name", "last_name")]

train.data$count_white_f[is.nan(train.data$count_white_f)] <- 0
train.data$count_black_f[is.nan(train.data$count_black_f)] <- 0
train.data$count_hispa_f[is.nan(train.data$count_hispa_f)] <- 0
train.data$count_asian_f[is.nan(train.data$count_asian_f)] <- 0

train.data$count_white <- train.data$count_black <- train.data$count_hispa <- train.data$count_asian <- NULL
train.data$u <- runif(nrow(train.data))
train.data[, keep := max(u) == u, by = c("first_name", "last_name") ]
train.data <- train.data[keep == 1, ]

train.data$race <- NULL
train.data$keep <- NULL
train.data$u <- NULL

## Merge with test data:
test.train <- merge(test.data, train.data, by = c("first_name", "last_name"))

test.train$count_white_f[is.na(test.train$count_white_f)] <- 0
test.train$count_black_f[is.na(test.train$count_black_f)] <- 0
test.train$count_hispa_f[is.na(test.train$count_hispa_f)] <- 0
test.train$count_asian_f[is.na(test.train$count_asian_f)] <- 0

test.train[ , count_white_f := max(count_white_f, na.rm = T), by = c("first_name", "last_name")]
test.train[ , count_black_f := max(count_black_f, na.rm = T), by = c("first_name", "last_name")]
test.train[ , count_hispa_f := max(count_hispa_f, na.rm = T), by = c("first_name", "last_name")]
test.train[ , count_asian_f := max(count_asian_f, na.rm = T), by = c("first_name", "last_name")]

test.train[, max_r := max(c(count_white_f, count_black_f, count_hispa_f, count_asian_f), na.rm = T), by = c("first_name", "last_name")]
test.train[, pred := which(max_r == c(count_white_f, count_black_f, count_hispa_f, count_asian_f))[1], ]

test.train$pred_white <- 0
test.train$pred_white[test.train$count_white_f == test.train$max_r] <- 1

test.train$pred_black <- 0
test.train$pred_black[test.train$count_black_f == test.train$max_r] <- 1

test.train$pred_asian <- 0
test.train$pred_asian[test.train$count_asian_f == test.train$max_r] <- 1

test.train$pred_hispa <- 0
test.train$pred_hispa[test.train$count_hispa_f == test.train$max_r] <- 1

test.train$sum_pred <- test.train$pred_hispa + test.train$pred_asian + test.train$pred_black + test.train$pred_white

test.train$acc_white <- 0
test.train$acc_white[test.train$pred_white == 1 & test.train$race == "White"] <- 1
test.train$acc_white[test.train$acc_white == 1 & test.train$sum_pred > 1] <- 0 ## resolving ties

test.train$acc_black <- 0
test.train$acc_black[test.train$pred_black == 1 & test.train$race == "Black"] <- 1
test.train$acc_black[test.train$acc_black == 1 & test.train$sum_pred > 1] <- 0 ## resolving ties

test.train$acc_hispa <- 0
test.train$acc_hispa[test.train$pred_hispa == 1 & test.train$race == "Hispanic"] <- 1
test.train$acc_hispa[test.train$acc_hispa == 1 & test.train$sum_pred > 1] <- 0 ## resolving ties

test.train$acc_asian <- 0
test.train$acc_asian[test.train$pred_asian == 1 & test.train$race == "Asian"] <- 1
test.train$acc_asian[test.train$acc_asian == 1 & test.train$sum_pred > 1] <- 0 ## resolving ties

mean(test.train$acc_white[test.train$race == "White"])
mean(test.train$acc_black[test.train$race == "Black"])
mean(test.train$acc_hispa[test.train$race == "Hispanic"])
mean(test.train$acc_asian[test.train$race == "Asian"])

mean(test.train$acc_white + test.train$acc_black + test.train$acc_hispa + test.train$acc_asian > 0)

nrow(test.train)/nrow(test.data)

(mean(test.train$acc_white[test.train$race == "White"]) + mean(test.train$acc_black[test.train$race == "Black"]) +
    mean(test.train$acc_hispa[test.train$race == "Hispanic"]) + mean(test.train$acc_asian[test.train$race == "Asian"]))/4

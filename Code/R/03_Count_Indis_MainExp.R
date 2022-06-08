rm(list=ls())
library(data.table)
set.seed(12345)

data.train <- fread("../../Data/FinalDataSet_Combos/FLtrain_NCtest_GAtest/FL_Train_s.csv")
data.test <- fread("../../Data/FinalDataSet_Combos/FLtrain_NCtest_GAtest/NCtest_FLtrain_s.csv")

table(data.train$indis)
table(data.test$indis)

table(data.train$race); nrow(data.test)
table(data.test$race); nrow(data.test)

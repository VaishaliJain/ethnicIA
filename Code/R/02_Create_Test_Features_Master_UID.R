rm(list=ls())
library(data.table)
set.seed(12345)

source("02_Create_Test_Features_sparse_UID.R")
create_test_features_UID("NC_UID", "FLtrain_NCtest_GAtest/FL_Train_UID.csv", "FLtrain_NCtest_GAtest/NCtest_FLtrain_UID.csv")

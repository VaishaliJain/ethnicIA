rm(list=ls())
library(data.table)

source("01_Create_Train_Features_sparse_UID.R")
create_train_features_UID(list("FL_UID"), "FLtrain_NCtest_GAtest/FL_Train_UID.csv")


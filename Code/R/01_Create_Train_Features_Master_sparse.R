rm(list=ls())
library(data.table)

source("01_Create_Train_Features_sparse.R")
create_train_features(list("FL"), "FLtrain_NCtest_GAtest/FL_Train_s.csv")
create_train_features(list("GA"), "GAtrain_NCtest_FLtest/GA_Train_s.csv")
create_train_features(list("NC"), "NCtrain_FLtest_GAtest/NC_Train_s.csv")
create_train_features(list("FL", "GA"), "FLGAtrain_NCtest/FLGA_Train_s.csv")
create_train_features(list("FL", "GA", "NC"), "FLGANCtrain_ContrPred/FLGANC_Train_s.csv")
create_train_features(list("NC_rest"), "NCtrain_NCtest_white/NC_rest_Train_s.csv")


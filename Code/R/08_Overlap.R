library(data.table)

dataTest <- fread("../../Data/CaseStudy/FECdataRaw_UP.csv")
dataTrain <- fread("../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/FLGANC_Train_s.csv")

dataT1 <- dataTest[, .(count_test = .N), by = c("first_name", "last_name")]
dataT2 <- dataTrain[, .(count_train = .N), by = c("first_name", "last_name")]

dataM <- merge(dataT1, dataT2, by = c("first_name", "last_name"))

sum(dataM$count_test)/nrow(dataTest)

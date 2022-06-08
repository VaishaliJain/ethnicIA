rm(list=ls())
gc()
library(data.table)

dataFL <- fread("../../Data/FinalDataSet_Combos/FLtrain_NCtest_GAtest/FL_Train_s.csv")
dataNC <- fread("../../Results/predictions_NC_test_FL_train_with_indis_s.csv")

## Prob(Indis | Ethnic Group)
probs <- dataFL[, .(probs = mean(indis)), by = "race"]
probs <- probs[order(race), ]
## Prob(Race | dis test)
probs.race <- prop.table(table(dataNC$predicted_race[dataNC$indis == 0]))

## Number of White among the Indis
denominator <- sum(probs[, "probs"] * probs.race)

## Whites
round((nrow(dataNC[indis == 1, ]) * probs[race == "White", "probs"] * probs.race["White"])/denominator, 0)
## Blacks
round((nrow(dataNC[indis == 1, ]) * probs[race == "Black", "probs"] * probs.race["Black"])/denominator, 0)

rm(list=ls())
gc()
library(data.table)

dataGA <- fread("../../Data/FinalDataSet_Combos/GAtrain_NCtest_FLtest/GA_Train_s.csv")
dataNC <- fread("../../Results/predictions_NC_test_GA_train_with_indis_s.csv")

## Prob(Indis | Ethnic Group)
probs <- dataGA[, .(probs = mean(indis)), by = "race"]
probs <- probs[order(race), ]

## Prob(Race | dis test)
probs.race <- prop.table(table(dataNC$predicted_race[dataNC$indis == 0]))
probs.race2 <- colSums(dataNC[indis == 0, c("Asian", "Black", "Hispanic", "White")])/nrow(dataNC[indis == 0, ])

## Number of White among the Indis
denominator <- sum(probs[, "probs"] * probs.race2)

## Whites
round((nrow(dataNC[indis == 1, ]) * probs[race == "White", "probs"] * probs.race2["White"])/denominator, 0)
## Blacks
round((nrow(dataNC[indis == 1, ]) * probs[race == "Black", "probs"] * probs.race["Black"])/denominator, 0)






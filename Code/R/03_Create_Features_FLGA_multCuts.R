rm(list=ls())
library(data.table)

## --------------------
## Cutpoints
## --------------------

c <- 1
# cut2_gs <- seq(0.05, 0.30, by = 0.05)
# cut4_gs <- seq(0.01, 0.15, by = 0.01)
# cut5 <- 0.50
cut5_g <- seq(0.01, 0.25, by = 0.01)
cutl_g <- seq(0, 30, by = 3)

## --------------------
## Load Data
## --------------------

train.data <- fread("../../Data/NameRaceData/FL.csv")
data <- fread("../../Data/NameRaceData/GA.csv")
train.data <- data.table(rbind(data, train.data))
rm(data); gc()
train.data$id <- 1:nrow(train.data)

## --------------------
## Feature Creation
## --------------------

## First Names
train.data[race == "Asian", pop_asian := .N, by = c("first_name") ]
train.data[race == "Hispanic", pop_hispa := .N, by = c("first_name") ]
train.data[race == "Black", pop_black := .N, by = c("first_name") ]
train.data[race == "White", pop_white := .N, by = c("first_name") ]

train.data[ , pop_fn_asian := mean(pop_asian, na.rm = T)/(.N + c), by = c("first_name") ]
train.data[ , pop_fn_hispa := mean(pop_hispa, na.rm = T)/(.N + c), by = c("first_name") ]
train.data[ , pop_fn_black := mean(pop_black, na.rm = T)/(.N + c), by = c("first_name") ]
train.data[ , pop_fn_white := mean(pop_white, na.rm = T)/(.N + c), by = c("first_name") ]
train.data$pop_asian <- train.data$pop_black <- train.data$pop_white <- train.data$pop_hispa <- NULL
train.data[is.na(train.data)] <- 0

## Last Names
train.data[race == "Asian", pop_asian := .N, by = c("last_name") ]
train.data[race == "Hispanic", pop_hispa := .N, by = c("last_name") ]
train.data[race == "Black", pop_black := .N, by = c("last_name") ]
train.data[race == "White", pop_white := .N, by = c("last_name") ]

train.data[ , pop_ln_asian := mean(pop_asian, na.rm = T)/(.N + c), by = c("last_name") ]
train.data[ , pop_ln_hispa := mean(pop_hispa, na.rm = T)/(.N + c), by = c("last_name") ]
train.data[ , pop_ln_black := mean(pop_black, na.rm = T)/(.N + c), by = c("last_name") ]
train.data[ , pop_ln_white := mean(pop_white, na.rm = T)/(.N + c), by = c("last_name") ]
train.data$pop_asian <- train.data$pop_black <- train.data$pop_white <- train.data$pop_hispa <- NULL
train.data$pop_ln_asian[is.na(train.data$pop_ln_asian)] <- 0
train.data$pop_ln_hispa[is.na(train.data$pop_ln_hispa)] <- 0
train.data$pop_ln_white[is.na(train.data$pop_ln_white)] <- 0
train.data$pop_ln_black[is.na(train.data$pop_ln_black)] <- 0

for(i in 1:length(cut5_g)) {
  for(j in 1:length(cutl_g)) {
    print(i)
    print(j)
    cut5 <- cut5_g[i]
    cutl <- cutl_g[j]
    
    train.data[, first_name_low := as.numeric(.N < cutl), by = c("first_name")]
    # Indistinguishable First Name
    train.data[, over_pop_fn := .N, by = c("first_name")]
    train.data[ , white_black_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_white) <= cut5)),  by = c("first_name")]
    train.data[ , white_asian_indis_fn := as.numeric((abs(pop_fn_asian - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_asian, pop_fn_white) <= cut5)),  by = c("first_name")]
    train.data[ , white_hispa_indis_fn := as.numeric((abs(pop_fn_hispa - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_hispa, pop_fn_white) <= cut5)),  by = c("first_name")]
    train.data[ , black_asian_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_asian) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_asian) <= cut5)),  by = c("first_name")]
    train.data[ , black_hispa_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_hispa) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_hispa) <= cut5)),  by = c("first_name")]
    train.data[ , asian_hispa_indis_fn := as.numeric((abs(pop_fn_asian - pop_fn_hispa) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_asian, pop_fn_hispa) <= cut5)),  by = c("first_name")]
    
    train.data[, last_name_low := as.numeric(.N < cutl), by = c("last_name")]
    # Indistinguishable Last Name
    train.data[, over_pop_ln := .N, by = c("last_name")]
    train.data[ , white_black_indis_ln := as.numeric((abs(pop_ln_black - pop_ln_white) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_black, pop_ln_white) <= cut5)),  by = c("last_name")]
    train.data[ , white_asian_indis_ln := as.numeric((abs(pop_ln_asian - pop_ln_white) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_asian, pop_ln_white) <= cut5)),  by = c("last_name")]
    train.data[ , white_hispa_indis_ln := as.numeric((abs(pop_ln_hispa - pop_ln_white) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_hispa, pop_ln_white) <= cut5)),  by = c("last_name")]
    train.data[ , black_asian_indis_ln := as.numeric((abs(pop_ln_black - pop_ln_asian) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_black, pop_ln_asian) <= cut5)),  by = c("last_name")]
    train.data[ , black_hispa_indis_ln := as.numeric((abs(pop_ln_black - pop_ln_hispa) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_black, pop_ln_hispa) <= cut5)),  by = c("last_name")]
    train.data[ , asian_hispa_indis_ln := as.numeric((abs(pop_ln_asian - pop_ln_hispa) <= cut5) * (max(pop_ln_black, pop_ln_white, pop_ln_asian, pop_ln_hispa) - min(pop_ln_asian, pop_ln_hispa) <= cut5)),  by = c("last_name")]
    
    # Indistinguishable
    train.data[ , indis_fn := as.numeric(white_black_indis_fn +  white_hispa_indis_fn +  white_asian_indis_fn +  black_asian_indis_fn +  black_hispa_indis_fn + asian_hispa_indis_fn > 0), by = c("first_name") ]
    train.data[ , indis_ln := as.numeric(white_black_indis_ln +  white_hispa_indis_ln +  white_asian_indis_ln +  black_asian_indis_ln +  black_hispa_indis_ln + asian_hispa_indis_ln> 0), by = c("last_name") ]
    train.data[ , indis := as.numeric(indis_fn + indis_ln == 2), ]
    
    train.data.sub <- train.data[indis == 1, ]
    
    out <- c(cut5, cutl, nrow(train.data.sub), nrow(train.data.sub) - nrow(train.data.sub[last_name_low == 1 & first_name_low == 1, ]))
    save(out, file = paste0("../../Data/FinalDataSet_Combos/FLGAtrain_NCtest_cuts/FLGA_Train_", i, "_", j, ".RData"))
  }
}

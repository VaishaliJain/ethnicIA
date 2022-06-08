rm(list=ls())
library(data.table)
library(stringr)

create_train_features <- function(train_data_labels, output_file_path) {
  
  ## --------------------
  ## Load Data
  ## --------------------
  
  n_train_data_labels <- length(train_data_labels)
  
  print(train_data_labels[1])
  path <- sprintf("../../Data/NameRaceData/%s.csv", train_data_labels[1])
  train.data <- fread(path)
  
  if (n_train_data_labels >= 2) {
    print(train_data_labels[2])
    path <- sprintf("../../Data/NameRaceData/%s.csv", train_data_labels[2])
    data <- fread(path)
    train.data <- data.table(rbind(data, train.data))
    rm(data); gc()
  } 
  if (n_train_data_labels == 3) {
    print(train_data_labels[3])
    path <- sprintf("../../Data/NameRaceData/%s.csv", train_data_labels[3])
    data <- fread(path)
    train.data <- data.table(rbind(data, train.data))
    rm(data); gc()
  }
  train.data$id <- 1:nrow(train.data)
  
  train.data$first_name[train.data$first_name == ""] <- NA
  train.data$last_name[train.data$last_name == ""] <- NA
  train.data <- train.data[!is.na(first_name), ]
  train.data <- train.data[!is.na(last_name), ]
  train.data <- train.data[!is.na(race), ]
  
  ## --------------------
  ## Cutpoints
  ## --------------------
  
  c <- 1
  cut5 <- 0.15
  cutl <- 10
  
  ## --------------------
  ## Feature Creation
  ## --------------------
  
  ## ---------------------------------------------
  ## 1. First four letters of the first/last name:
  ## ---------------------------------------------
  
  train.data[ , first_name_f4 := substr(first_name, 1, 4), by = c("first_name") ]
  train.data[ , last_name_f4 := substr(last_name, 1, 4), by = c("last_name") ]
  
  ## First Names
  train.data[race == "Asian", pop_asian_f4 := .N, by = c("first_name_f4") ]
  train.data[race == "Hispanic", pop_hispa_f4 := .N, by = c("first_name_f4") ]
  train.data[race == "Black", pop_black_f4 := .N, by = c("first_name_f4") ]
  train.data[race == "White", pop_white_f4 := .N, by = c("first_name_f4") ]
  
  train.data[ , pop_fn_asian_f4 := mean(pop_asian_f4, na.rm = T)/(.N + c), by = c("first_name_f4") ]
  train.data[ , pop_fn_hispa_f4 := mean(pop_hispa_f4, na.rm = T)/(.N + c), by = c("first_name_f4") ]
  train.data[ , pop_fn_black_f4 := mean(pop_black_f4, na.rm = T)/(.N + c), by = c("first_name_f4") ]
  train.data[ , pop_fn_white_f4 := mean(pop_white_f4, na.rm = T)/(.N + c), by = c("first_name_f4") ]
  train.data$pop_asian_f4 <- train.data$pop_black_f4 <- train.data$pop_white_f4 <- train.data$pop_hispa_f4 <- NULL
  train.data[is.na(train.data)] <- 0
  
  ## Last Names
  train.data[race == "Asian", pop_asian_f4 := .N, by = c("last_name_f4") ]
  train.data[race == "Hispanic", pop_hispa_f4 := .N, by = c("last_name_f4") ]
  train.data[race == "Black", pop_black_f4 := .N, by = c("last_name_f4") ]
  train.data[race == "White", pop_white_f4 := .N, by = c("last_name_f4") ]
  
  train.data[ , pop_ln_asian_f4 := mean(pop_asian_f4, na.rm = T)/.N, by = c("last_name_f4") ]
  train.data[ , pop_ln_hispa_f4 := mean(pop_hispa_f4, na.rm = T)/.N, by = c("last_name_f4") ]
  train.data[ , pop_ln_black_f4 := mean(pop_black_f4, na.rm = T)/.N, by = c("last_name_f4") ]
  train.data[ , pop_ln_white_f4 := mean(pop_white_f4, na.rm = T)/.N, by = c("last_name_f4") ]
  train.data$pop_asian_f4 <- train.data$pop_black_f4 <- train.data$pop_white_f4 <- train.data$pop_hispa_f4 <- NULL
  train.data$pop_ln_asian_f4[is.na(train.data$pop_ln_asian_f4)] <- 0
  train.data$pop_ln_hispa_f4[is.na(train.data$pop_ln_hispa_f4)] <- 0
  train.data$pop_ln_white_f4[is.na(train.data$pop_ln_white_f4)] <- 0
  train.data$pop_ln_black_f4[is.na(train.data$pop_ln_black_f4)] <- 0
  
  ## ---------------------------------------------
  ## 2. Last four letters of the first/last name:
  ## ---------------------------------------------
  
  substrR <- function(x, n){ substr(x, nchar(x)-n+1, nchar(x)) }
  train.data[ , first_name_l4 := substrR(first_name, 4), by = c("first_name") ]
  train.data[ , last_name_l4 := substrR(last_name, 4), by = c("last_name") ]
  
  ## First Names
  train.data[race == "Asian", pop_asian_l4 := .N, by = c("first_name_l4") ]
  train.data[race == "Hispanic", pop_hispa_l4 := .N, by = c("first_name_l4") ]
  train.data[race == "Black", pop_black_l4 := .N, by = c("first_name_l4") ]
  train.data[race == "White", pop_white_l4 := .N, by = c("first_name_l4") ]
  
  train.data[ , pop_fn_asian_l4 := mean(pop_asian_l4, na.rm = T)/(.N + c), by = c("first_name_l4") ]
  train.data[ , pop_fn_hispa_l4 := mean(pop_hispa_l4, na.rm = T)/(.N + c), by = c("first_name_l4") ]
  train.data[ , pop_fn_black_l4 := mean(pop_black_l4, na.rm = T)/(.N + c), by = c("first_name_l4") ]
  train.data[ , pop_fn_white_l4 := mean(pop_white_l4, na.rm = T)/(.N + c), by = c("first_name_l4") ]
  train.data$pop_asian_l4 <- train.data$pop_black_l4 <- train.data$pop_white_l4 <- train.data$pop_hispa_l4 <- NULL
  train.data[is.na(train.data)] <- 0
  
  ## Last Names
  train.data[race == "Asian", pop_asian_l4 := .N, by = c("last_name_l4") ]
  train.data[race == "Hispanic", pop_hispa_l4 := .N, by = c("last_name_l4") ]
  train.data[race == "Black", pop_black_l4 := .N, by = c("last_name_l4") ]
  train.data[race == "White", pop_white_l4 := .N, by = c("last_name_l4") ]
  
  train.data[ , pop_ln_asian_l4 := mean(pop_asian_l4, na.rm = T)/(.N + c), by = c("last_name_l4") ]
  train.data[ , pop_ln_hispa_l4 := mean(pop_hispa_l4, na.rm = T)/(.N + c), by = c("last_name_l4") ]
  train.data[ , pop_ln_black_l4 := mean(pop_black_l4, na.rm = T)/(.N + c), by = c("last_name_l4") ]
  train.data[ , pop_ln_white_l4 := mean(pop_white_l4, na.rm = T)/(.N + c), by = c("last_name_l4") ]
  train.data$pop_asian_l4 <- train.data$pop_black_l4 <- train.data$pop_white_l4 <- train.data$pop_hispa_l4 <- NULL
  train.data$pop_ln_asian_l4[is.na(train.data$pop_ln_asian_l4)] <- 0
  train.data$pop_ln_hispa_l4[is.na(train.data$pop_ln_hispa_l4)] <- 0
  train.data$pop_ln_white_l4[is.na(train.data$pop_ln_white_l4)] <- 0
  train.data$pop_ln_black_l4[is.na(train.data$pop_ln_black_l4)] <- 0
  
  ## ---------------------------------------------
  ## 3. First/last name:
  ## ---------------------------------------------

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

  ## First Names
  train.data[race == "Asian", pop_asian := .N, by = c("last_name") ]
  train.data[race == "Hispanic", pop_hispa := .N, by = c("last_name") ]
  train.data[race == "Black", pop_black := .N, by = c("last_name") ]
  train.data[race == "White", pop_white := .N, by = c("last_name") ]
  
  train.data[ , pop_ln_asian := mean(pop_asian, na.rm = T)/(.N + c), by = c("last_name") ]
  train.data[ , pop_ln_hispa := mean(pop_hispa, na.rm = T)/(.N + c), by = c("last_name") ]
  train.data[ , pop_ln_black := mean(pop_black, na.rm = T)/(.N + c), by = c("last_name") ]
  train.data[ , pop_ln_white := mean(pop_white, na.rm = T)/(.N + c), by = c("last_name") ]
  train.data$pop_asian <- train.data$pop_black <- train.data$pop_white <- train.data$pop_hispa <- NULL
  
  ## Indicator Low Frequency of Name:
  train.data[is.na(train.data)] <- 0
  train.data[, first_name_low := as.numeric(.N < cutl), by = c("first_name")]
  train.data[, last_name_low := as.numeric(.N < cutl), by = c("last_name")]
  
  # Best Evidence
  train.data[ , best_evidence_asian := max(pop_ln_asian, pop_fn_asian), by = c("id") ]
  train.data[ , best_evidence_hispanic := max(pop_ln_hispa, pop_fn_hispa), by = c("id") ]
  train.data[ , best_evidence_white := max(pop_ln_white, pop_fn_white), by = c("id") ]
  train.data[ , best_evidence_black := max(pop_ln_black, pop_fn_black), by = c("id") ]

  # Auxiliary Features
  train.data$dash_indicator <- as.numeric(str_count(paste(train.data$first_name, train.data$last_name, sep = " "), "-") >= 1)
  train.data$n_sub_names <- str_count(paste(train.data$first_name, train.data$last_name, sep = " "), " ") +
    str_count(paste(train.data$first_name, train.data$last_name, sep = " "), "-")
  
  # Indistinguishable
  
  # Indistinguishable First Name
  train.data[, over_pop_fn := .N, by = c("first_name")]
  train.data[ , white_black_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_white) <= cut5)),  by = c("first_name")]
  train.data[ , white_asian_indis_fn := as.numeric((abs(pop_fn_asian - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_asian, pop_fn_white) <= cut5)),  by = c("first_name")]
  train.data[ , white_hispa_indis_fn := as.numeric((abs(pop_fn_hispa - pop_fn_white) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_hispa, pop_fn_white) <= cut5)),  by = c("first_name")]
  train.data[ , black_asian_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_asian) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_asian) <= cut5)),  by = c("first_name")]
  train.data[ , black_hispa_indis_fn := as.numeric((abs(pop_fn_black - pop_fn_hispa) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_black, pop_fn_hispa) <= cut5)),  by = c("first_name")]
  train.data[ , asian_hispa_indis_fn := as.numeric((abs(pop_fn_asian - pop_fn_hispa) <= cut5) * (max(pop_fn_black, pop_fn_white, pop_fn_asian, pop_fn_hispa) - min(pop_fn_asian, pop_fn_hispa) <= cut5)),  by = c("first_name")]
  
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

  train.data <- train.data[, c('id', 'first_name', 'last_name', 'race', 
                               "first_name_f4", "first_name_l4",
                               "last_name_f4", "last_name_l4",
                               "pop_ln_asian", "pop_ln_hispa",
                               "pop_ln_black", "pop_ln_white",
                               "pop_fn_asian", "pop_fn_hispa",
                               "pop_fn_black", "pop_fn_white",
                               "best_evidence_asian", "best_evidence_black",
                               "best_evidence_hispanic", "best_evidence_white",
                               'dash_indicator', 'n_sub_names',
                               "pop_ln_asian_f4", "pop_ln_hispa_f4",
                               "pop_ln_black_f4", "pop_ln_white_f4",
                               "pop_fn_asian_f4", "pop_fn_hispa_f4",
                               "pop_fn_black_f4", "pop_fn_white_f4",
                               "pop_ln_asian_l4", "pop_ln_hispa_l4",
                               "pop_ln_black_l4", "pop_ln_white_l4",
                               "pop_fn_asian_l4", "pop_fn_hispa_l4",
                               "pop_fn_black_l4", "pop_fn_white_l4",
                               'indis_fn', 'indis_ln', 'indis',
                               'white_black_indis_fn', 'white_hispa_indis_fn', 'white_asian_indis_fn',
                               'black_asian_indis_fn', 'black_hispa_indis_fn', 'asian_hispa_indis_fn',
                               'white_black_indis_ln', 'white_hispa_indis_ln', 'white_asian_indis_ln',
                               'black_asian_indis_ln', 'black_hispa_indis_ln', 'asian_hispa_indis_ln',
                               'last_name_low', 'first_name_low'), 
                           with = F]
  
  output_file_path <- sprintf("../../Data/FinalDataSet_Combos/%s", output_file_path)
  write.csv(train.data, file = output_file_path, row.names = F)
}

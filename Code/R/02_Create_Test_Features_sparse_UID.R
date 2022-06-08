rm(list=ls())
library(data.table)
library(stringr)
set.seed(12345)

create_test_features_UID <- function(test_data_label, train_data_path, output_file_path) {
  
  ## --------------------
  ## Load Data
  ## --------------------
  
  path <- sprintf("../../Data/NameRaceData/%s.csv", test_data_label)
  
  if(test_data_label=="CaseStudy"){
    path <- "../../Data/CaseStudy/FECdataRaw_UP.csv"
  }
  else if(test_data_label=="CaseStudyGA"){
    path <- "../../Data/CaseStudy/FECdataRaw_GA_UP.csv"
  }
  
  data <- fread(path)
  
  data$first_name[data$first_name == ""] <- NA
  data$last_name[data$last_name == ""] <- NA
  data <- data[!is.na(first_name), ]
  data <- data[!is.na(last_name), ]
  if(sum(colnames(data) == "race") != 0) {  data <- data[!is.na(race), ]}

  if(test_data_label=="CaseStudy" | test_data_label=="CaseStudyGA"){
    data <- data[, c("first_name", "last_name", "id")]
  }
  else{
    data$id <- 1:nrow(data)
  }
  
  ## --------------------
  ## Add features from Train DataSet
  ## --------------------
  
  train_data_path <- sprintf("../../Data/FinalDataSet_Combos/%s", train_data_path)
  train_data <- fread(train_data_path)
  
  ## First Name
  train_data.fn <- train_data[, c("first_name_id", 
                          "pop_fn_asian",
                          "pop_fn_hispa",
                          "pop_fn_black",
                          "pop_fn_white",
                          "indis_fn")]
  train_data.fn[, unif := runif(.N), by = "first_name_id"] 
  train_data.fn[, keep := max(unif) == unif, by = "first_name_id"] 
  train_data.fn <- train_data.fn[keep == 1]
  train_data.fn$keep <- train_data.fn$unif <- NULL
  
  data.final <- merge(data, train_data.fn, by = c("first_name_id"), all.x = T)
  
  train_data.ln <- train_data[, c("last_name_id", 
                          "pop_ln_asian",
                          "pop_ln_hispa",
                          "pop_ln_black",
                          "pop_ln_white",
                          "indis_ln")]
  train_data.ln[, unif := runif(.N), by = "last_name_id"] 
  train_data.ln[, keep := max(unif) == unif, by = "last_name_id"] 
  train_data.ln <- train_data.ln[keep == 1]
  train_data.ln$keep <- train_data.ln$unif <- NULL
  
  data.final <- merge(data.final, train_data.ln, by = c("last_name_id"), all.x = T)
  
  # Best Evidence
  data.final$pop_ln_asian_2 <- data.final$pop_ln_asian
  data.final$pop_ln_white_2 <- data.final$pop_ln_white
  data.final$pop_ln_hispa_2 <- data.final$pop_ln_hispa
  data.final$pop_ln_black_2 <- data.final$pop_ln_black
  
  data.final$pop_ln_asian_2[is.na(data.final$pop_ln_asian)] <- 0
  data.final$pop_ln_white_2[is.na(data.final$pop_ln_white)] <- 0
  data.final$pop_ln_hispa_2[is.na(data.final$pop_ln_hispa)] <- 0
  data.final$pop_ln_black_2[is.na(data.final$pop_ln_black)] <- 0
  
  data.final$pop_fn_asian_2 <- data.final$pop_fn_asian
  data.final$pop_fn_white_2 <- data.final$pop_fn_white
  data.final$pop_fn_hispa_2 <- data.final$pop_fn_hispa
  data.final$pop_fn_black_2 <- data.final$pop_fn_black
  
  data.final$pop_fn_asian_2[is.na(data.final$pop_fn_asian)] <- 0
  data.final$pop_fn_white_2[is.na(data.final$pop_fn_white)] <- 0
  data.final$pop_fn_hispa_2[is.na(data.final$pop_fn_hispa)] <- 0
  data.final$pop_fn_black_2[is.na(data.final$pop_fn_black)] <- 0
  
  data.final[ , best_evidence_asian := max(pop_ln_asian_2, pop_fn_asian_2), by = c("id") ]
  data.final[ , best_evidence_hispanic := max(pop_ln_hispa_2, pop_fn_hispa_2), by = c("id") ]
  data.final[ , best_evidence_white := max(pop_ln_white_2, pop_fn_white_2), by = c("id") ]
  data.final[ , best_evidence_black := max(pop_ln_black_2, pop_fn_black_2), by = c("id") ]
  
  # Indistinguishable
  data.final[ , indis := as.numeric(indis_fn + indis_ln == 2), ]
  
  # Auxiliary Features
  data.final$dash_indicator <- as.numeric(str_count(paste(data.final$first_name, data.final$last_name, sep = " "), "-") >= 1)
  data.final$n_sub_names <- str_count(paste(data.final$first_name, data.final$last_name, sep = " "), " ") +
    str_count(paste(data.final$first_name, data.final$last_name, sep = " "), "-")
  
  # Clean Up
  data.final$pop_fn_asian_2 <- data.final$pop_fn_hispa_2 <- data.final$pop_fn_white_2 <- data.final$pop_fn_black_2 <- NULL
  data.final$pop_ln_asian_2 <- data.final$pop_ln_hispa_2 <- data.final$pop_ln_white_2 <- data.final$pop_ln_black_2 <- NULL
  
  output_file_path <- sprintf("../../Data/FinalDataSet_Combos/%s", output_file_path)
  write.csv(data.final, file = output_file_path, row.names = F)
}


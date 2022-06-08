library(data.table)
library(stringr)

donations_stats <- function(small_donations, unique_names){

    data <- fread("../../Data/CaseStudy/FECdata_GA.csv")
    if(small_donations){
        data <- data[TRANSACTION_AMT < 1000, ]
    }
    data <- data[CAND_NAME != "TRUMP" & CAND_NAME != "BIDEN" & CAND_NAME != "COLLINS", ]
    
    data$fec_election_year[nchar(data$fec_election_year) == 7] <- str_pad(data$fec_election_year[nchar(data$fec_election_year) == 7], 8, pad = "0") 
    data$fec_election_year <- as.Date(data$fec_election_year, format = "%m%d%Y")
    data <- data[fec_election_year < "2021-01-31", ]
    
    if(unique_names) {
        data$id_2 <- paste(data$first_name, data$last_name, data$STATE, sep = " ")
        data$dup <- duplicated(data$id_2)
        data <- data[dup == 0, ]
    }

    data$in_state <- ifelse(data$STATE == "GA", 1, 0)
    data <- data[, .(amount = .N), by = c("CAND_PID", "predicted_race", "in_state")]
    data <- data[order(CAND_PID, predicted_race, in_state), ]

    ## In-State
    ## Asian
    cat("In-State\n")
    cat(paste("Asians donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Asian" & data$in_state == 1]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Asian" & data$in_state == 1], 2), "\n"))
    ## Black
    cat(paste("Black donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Black" & data$in_state == 1]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Black" & data$in_state == 1], 2), "\n"))
    ## Hispanic
    cat(paste("Hispanic donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Hispanic" & data$in_state == 1]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Hispanic" & data$in_state == 1], 2), "\n"))
    ## White
    cat(paste("White donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "White" & data$in_state == 1]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "White" & data$in_state == 1], 2), "\n"))
    
    ## Out-of-State
    ## Asian
    cat("Out-of-State\n")
    cat(paste("Asians donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Asian" & data$in_state == 0]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Asian" & data$in_state == 0], 2), "\n"))
    ## Black
    cat(paste("Black donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Black" & data$in_state == 0]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Black" & data$in_state == 0], 2), "\n"))
    ## Hispanic
    cat(paste("Hispanic donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "Hispanic" & data$in_state == 0]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "Hispanic" & data$in_state == 0], 2), "\n"))
    ## White
    cat(paste("White donors: ", round(data$amount[data$CAND_PID == "DEM" & data$predicted_race == "White" & data$in_state == 0]/data$amount[data$CAND_PID == "REP" & data$predicted_race == "White" & data$in_state == 0], 2), "\n"))
}

donations_stats(small_donations = F, unique_names = F)
##donations_stats(small_donations = T, unique_names = F)

donations_stats(small_donations = F, unique_names = T)
##donations_stats(small_donations = T, unique_names = T)

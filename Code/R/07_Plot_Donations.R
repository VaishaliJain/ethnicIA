library(data.table)
library(stringr)

plot_donations <- function(in_state_flag, include_collins, small_donations){
    
    data <- fread("../../Data/CaseStudy/FECdata_GA.csv")
    if(include_collins) {
        data <- data[CAND_NAME != "TRUMP" & CAND_NAME != "BIDEN", ]
    } else {
        data <- data[CAND_NAME != "TRUMP" & CAND_NAME != "BIDEN" & CAND_NAME != "COLLINS", ]
    }
    
    data$fec_election_year[nchar(data$fec_election_year) == 7] <- str_pad(data$fec_election_year[nchar(data$fec_election_year) == 7], 8, pad = "0") 
    data$fec_election_year <- as.Date(data$fec_election_year, format = "%m%d%Y")
    data <- data[fec_election_year < "2021-01-31", ]
    
    data$in_state <- ifelse(data$STATE == "GA", 1, 0)
    if(small_donations) {
        data <- data[TRANSACTION_AMT < 1000, ]
        data <- data[, .(amount = sum(TRANSACTION_AMT)), by = c("CAND_PID", "predicted_race", "in_state")]
    } else {
        data <- data[, .(amount = sum(TRANSACTION_AMT)), by = c("CAND_PID", "predicted_race", "in_state")]    
    }
    
    if(include_collins) {
        output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateInState_wCollins.pdf'
        plot_title = "Donation Intensity: In-State"
    } else {
        output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateInState.pdf'
        plot_title = "Donation Intensity: In-State"
    }

    if(in_state_flag==1 & small_donations==1){
        if(include_collins) {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateSmallInState_wCollins.pdf'
        } else {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateSmallInState.pdf'
        }
        plot_title = "Donation Intensity: In-State"
    }
    
    if(in_state_flag==0){
        if(include_collins) {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateOutsideState_wCollins.pdf'
        } else {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateOutsideState.pdf'
        }
        plot_title = "Donation Intensity: Outside-State"
    }
    
    if(in_state_flag==0 & small_donations==1){
        if(include_collins) {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateSmallOutsideState_wCollins.pdf'
        } else {
            output_file_path = '../../Visualizations/GASenateContributionPlots/GASenateSmallOutsideState.pdf'
        }
        plot_title = "Donation Intensity: Outside-State"
    }
    
    pdf(output_file_path, h=10, w=10)
    library(igraph)
    plot(0,0, type="n", xaxt="n", yaxt = "n", xlab = "", ylab="",
         xlim=c(0,5), ylim=c(1,14), main = plot_title, cex.main = 2.5)
    
    x <- 1:4
    y <- rep(2, 4)
    
    text(0.75, (y - 0.7 + 0*3)[1], "White", cex = 2)
    text(0.75, (y + 0.2 +  3*3)[1], "Black", cex = 2)
    text(4.25, (y - 0.7 + 0*3)[1], "Hispanic", cex = 2)
    text(4.25, (y + 0.2 + 3*3)[1], "Asian", cex = 2)

    if(include_collins) {
        text(2.5, 6, "Ossoff + \nWarnock", col = "blue", cex = 2)
        text(2.5, 8.75, "Loeffler + \nPerdue + Collins", col = "red", cex = 2)
    } else {
        text(2.5, 6, "Ossoff + \nWarnock", col = "blue", cex = 2)
        text(2.5, 8.75, "Loeffler + \nPerdue", col = "red", cex = 2)
    }
    
    iArrows <- igraph:::igraph.Arrows
    mycolors <- rep(c("green", "orange", "red", "blue"), 1)
    data$amount <- data$amount/2000000
    
    ## Whites
    dataW <- data[predicted_race == "White" & in_state == in_state_flag, ]
    iArrows(0.75, 2.25, 1.95, 8,
            h.lwd = dataW$amount[dataW$CAND_PID == "REP"]/1.5, 
            sh.lwd = dataW$amount[dataW$CAND_PID == "REP"],
            sh.col = "#3B9AB2",
            curve = 0.15, width = 2.5, size =1.1)
    iArrows(0.75, 2.25, 2.05, 4.6,
            h.lwd = dataW$amount[dataW$CAND_PID == "DEM"]/1.5, 
            sh.lwd = dataW$amount[dataW$CAND_PID == "DEM"], 
            sh.col = "#3B9AB2",
            curve = -0.15, width = 2, size=2)
    
    ## Black
    dataB <- data[predicted_race == "Black" & in_state == in_state_flag, ]
    iArrows(0.75, 10.45, 1.95, 9.3,
            h.lwd = dataB$amount[dataB$CAND_PID == "REP"]/1.5, 
            sh.lwd = dataB$amount[dataB$CAND_PID == "REP"], 
            sh.col = "#EBCC2A",
            curve = 0.15, width = 2, size = 0.7)
    iArrows(0.75, 10.45, 1.95, (y + 1*3)[1] + 0.7,
            h.lwd = dataB$amount[dataB$CAND_PID == "DEM"]/1.5, 
            sh.lwd = dataB$amount[dataB$CAND_PID == "DEM"], 
            sh.col = "#EBCC2A",
            curve = -0.3, width = 2, size=0.7)
    
    ## Asian
    dataA <- data[predicted_race == "Asian" & in_state == in_state_flag, ]
    iArrows(4.25, 10.45, 2.9, 9.3,
            h.lwd = dataA$amount[dataA$CAND_PID == "REP"]/1.5, 
            sh.lwd = dataA$amount[dataA$CAND_PID == "REP"], 
            sh.col = "#007600",      
            curve = 0.3, width = 2, size = 0.7)
    iArrows(4.25, 10.45, 3, (y + 1*3)[1] + 0.7,
            h.lwd = dataA$amount[dataA$CAND_PID == "DEM"]/1.5, 
            sh.lwd = dataA$amount[dataA$CAND_PID == "DEM"], 
            sh.col = "#007600",       
            curve = 0.3, width = 2, size = 0.7)
    
    ## Hispanics
    dataH <- data[predicted_race == "Hispanic" & in_state == in_state_flag, ]
    iArrows(4.25, 2.25, 3.0, (y + 2*3)[1] - 0.2,
            h.lwd = dataH$amount[dataH$CAND_PID == "REP"]/1.5, 
            sh.lwd = dataH$amount[dataH$CAND_PID == "REP"], 
            sh.col = "#DC863B",
            curve = -0.15, width = 2, size=0.8)
    iArrows(4.25, 2.25, 3.0, (y + 1*3)[1] - 0.2,
            h.lwd = dataH$amount[dataH$CAND_PID == "DEM"]/1.5, 
            sh.lwd = dataH$amount[dataH$CAND_PID == "DEM"], 
            sh.col = "#DC863B",
            curve = -0.15, width = 2, size=0.8)
    dev.off()
}

plot_donations(1, include_collins = F, small_donations = F) #In State, GA Senate 2020
plot_donations(0, include_collins = F, small_donations = F) #Outside State, GA Senate 2020

plot_donations(1, include_collins = T, small_donations = F) #In State, GA Senate 2020
plot_donations(0, include_collins = T, small_donations = F) #Outside State, GA Senate 2020

plot_donations(1, include_collins = F, small_donations = T) #In State, GA Senate 2020
plot_donations(0, include_collins = F, small_donations = T) #Outside State, GA Senate 2020
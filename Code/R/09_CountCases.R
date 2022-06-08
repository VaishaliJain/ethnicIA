## :::Count observations in our voter files:::
library(data.table)

d1 <- nrow(fread("../../Data/NameRaceData/GA.csv"))
d2 <- nrow(fread("../../Data/NameRaceData/NC.csv"))
d3 <- nrow(fread("../../Data/NameRaceData/FL.csv"))

c1 <- d1 + d2 + d3 

## Number of eligible voters from http://www.electproject.org/
c2 <- 15551739 + 7383562 + 7759051

c1/c2

ga <- fread("../../Data/NameRaceData/GA.csv")
nc <- fread("../../Data/NameRaceData/NC.csv")
fl <- fread("../../Data/NameRaceData/FL.csv")

nc[nc$first_name == ""] <- NA
nc$last_name[nc$last_name == ""] <- NA
nc <- nc[!is.na(first_name), ]
nc <- nc[!is.na(last_name), ]
nc <- nc[!is.na(race), ]

fl$name <- paste(fl$first_name, fl$last_name)
nc$name <- paste(nc$first_name, nc$last_name)

length(nc$name[nc$name %in% unique(fl$name)])/nrow(nc)

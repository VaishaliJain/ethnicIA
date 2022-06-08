rm(list=ls())
library(data.table)
library(stringr)

source("05_Create_FLGA_Train_Duplicates.R")

create_FLGA_duplicates(5)
create_FLGA_duplicates(10)
create_FLGA_duplicates(20)
create_FLGA_duplicates(30)
create_FLGA_duplicates(50)
create_FLGA_duplicates(100)
create_FLGA_duplicates(250)
create_FLGA_duplicates(500)

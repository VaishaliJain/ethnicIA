rm(list=ls())
library(data.table)
library(fastLink)

data1 <- fread("../../Data/NameRaceData/FL.csv")
data2 <- fread("../../Data/NameRaceData/NC.csv")

unique.fn <- data.table(cbind(unique(c(data1$first_name, data2$first_name))))
colnames(unique.fn) <- "first_name"

unique.ln <- data.table(cbind(unique(c(data1$last_name, data2$last_name))))
colnames(unique.ln) <- "last_name"

nclu.names <- max(1, round(nrow(unique.fn)/5000))
unique.fn$cluster.fn <- kmeans(x = as.numeric(as.factor(unique.fn$first_name)), centers = nclu.names)$cluster

nclu.lnames <- max(1, round(nrow(unique.ln)/5000))
unique.ln$cluster.ln <- kmeans(x = as.numeric(as.factor(unique.ln$last_name)), centers = nclu.lnames)$cluster

results.names <- list()
for(i in 1:nclu.names) { 
  print(i)
  temp <- unique.fn[cluster.fn == i, ]
  temp$id <- 1:nrow(temp)
  
  out <- fastLink(temp, temp, varnames = "first_name", stringdist.match = "first_name",  
                  cut.a = 0.92)
  matches <- data.table(cbind(out$matches$inds.a, out$matches$inds.b))
  pasteT <- function(x) {
    x = sort(x)
    x = paste(x, collapse = ",")
    x
  }
  matches[, `:=`(V3, pasteT(V2)), by = "V1"]
  
  ans <- matches[, .(id_2 = unique(V3)), by = "V1"]
  ans$id_2 <- paste0("C", i, "_", as.numeric(as.factor(ans$id_2)))
  colnames(ans) <- c("id", "id_2")
  
  temp <- merge(temp, ans, by = "id", all.x = T)
  if(length(temp$id_2[is.na(temp$id_2)]) > 0) {
    temp$id_2[is.na(temp$id_2)] <- paste0("CU_", i, "_", 1:length(temp$id_2[is.na(temp$id_2)]))
  }
  results.names[[i]] <- temp
  rm(temp); gc()
}

data.fn <- rbindlist(results.names)
length(unique(data.fn$id_2))

results.last.names <- list()
for(i in 1:nclu.lnames) {
  print(i)
  temp <- unique.ln[cluster.ln == i, ]
  temp$id <- 1:nrow(temp)
  
  out <- fastLink(temp, temp, varnames = "last_name", stringdist.match = "last_name",  
                  cut.a = 0.92)
  matches <- data.table(cbind(out$matches$inds.a, out$matches$inds.b))
  pasteT <- function(x) {
    x = sort(x)
    x = paste(x, collapse = ",")
    x
  }
  matches[, `:=`(V3, pasteT(V2)), by = "V1"]
  
  ans <- matches[, .(id_2 = unique(V3)), by = "V1"]
  ans$id_2 <- paste0("C", i, "_", as.numeric(as.factor(ans$id_2)))
  colnames(ans) <- c("id", "id_2")
  
  temp <- merge(temp, ans, by = "id", all.x = T)
  if(length(temp$id_2[is.na(temp$id_2)]) > 0) {
    temp$id_2[is.na(temp$id_2)] <- paste0("CU_", i, "_", 1:length(temp$id_2[is.na(temp$id_2)]))
  }
  results.last.names[[i]] <- temp
  rm(temp); gc()
}

data.ln <- rbindlist(results.last.names)
length(unique(data.ln$id_2))

data1 <- merge(data1, data.fn, by = c("first_name"), all.x = T)
data1$first_name_id <- data1$id_2
data1$id_2 <- NULL

data1 <- merge(data1, data.ln, by = c("last_name"), all.x = T)
data1$last_name_id <- data1$id_2
data1$id_2 <- NULL

data2 <- merge(data2, data.fn, by = c("first_name"), all.x = T)
data2$first_name_id <- data2$id_2
data2$id_2 <- NULL

data2 <- merge(data2, data.ln, by = c("last_name"), all.x = T)
data2$last_name_id <- data2$id_2
data2$id_2 <- NULL

data1 <- data1[, c("last_name", "first_name", "race", "first_name_id", "last_name_id"), with = F]
data2 <- data2[, c("last_name", "first_name", "race", "first_name_id", "last_name_id"), with = F]

write.csv(data1, file = "../../Data/NameRaceData/FL_UID.csv", row.names = F)
write.csv(data2, file = "../../Data/NameRaceData/NC_UID.csv", row.names = F)




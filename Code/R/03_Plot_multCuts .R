rm(list=ls())
library(data.table)

list.files <- list.files("../../Data/FinalDataSet_Combos/FLGAtrain_NCtest_cuts/", pattern = "*.RData")

container <- list()
for(i in 1:length(list.files)) {
  load(paste0("../../Data/FinalDataSet_Combos/FLGAtrain_NCtest_cuts/", list.files[i]))
  container[[i]] <- out
}

data <- data.table(do.call('rbind', container))
colnames(data) <- c("x", "y", "w", "z")
data <- data[order(x, y), ]

library(plotly)

x <- data$x
y <- data$y
z <- data$z

f1 <- list(
  family = "Arial, sans-serif",
  size = 23
)

fig1 <- plot_ly(
  x = ~x, 
  y = ~y, 
  z = ~z, 
  type = "contour",
  contours = list(showlabels = TRUE, labelfont = list(size = 20, color = 'white'))
)

fig1 <- fig1 %>% colorbar(title = "Number of\nIndistinguishables", titlefont = f1, tickfont = list(size = 20)) 
fig1 <- fig1 %>% layout(xaxis = list(title = "Closeness", titlefont = f1, tickfont = list(size = 20)),
               yaxis = list(title = "Minimum Frequency", titlefont = f1, tickfont = list(size = 20)))
fig1 

export(fig1, file = '../../Visualizations/contour_params.pdf')

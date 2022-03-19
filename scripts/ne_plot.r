args = commandArgs(TRUE)
input = args[1] ## Ne output of MSMC
output = args[2] ## prefix of the output files
mu = as.numeric(args[3]) ## mutation rate [1.25e-8]
g = as.numeric(args[4]) ## years per generation [25]
color = as.character(args[5]) ## line color

read.table(input, head = T) -> data
newdata = data.frame(time_index = data$time_index)
newdata$left_time_boundary = data$left_time_boundary / mu * g ## in years
newdata$right_time_boundary = data$right_time_boundary / mu * g ## in years
newdata$ne = 1 / data$lambda / 2 / mu

write.table(newdata, file = paste(output, ".converted.txt", sep = ""), row.names = F, quote = F)

pdf(paste(output,".pdf", sep = ""), width = 10, height = 8)
newdata=newdata[newdata$right_time_boundary>=1000&newdata$left_time_boundary<=1000000,]
t1 = newdata$left_time_boundary
t1[1] = 1000
t2 = newdata$right_time_boundary
ne = newdata$ne
plot(c(t1, t2), c(ne, ne), cex=0, ylab = "Effective Population Size", xlab = "Years ago", log = "xy", xlim=c(1000, 1000000), ylim=c(1000, 30000), cex.lab = 1.2, cex.axis = 1)
segments(t1, ne, t2, ne, lwd=1.5, col = color[1])
segments(t2[1:(length(t2)-1)], ne[1:(length(ne)-1)], t2[1:(length(t2)-1)], ne[2:length(ne)], lwd=1.5, col = color[1])
dev.off()


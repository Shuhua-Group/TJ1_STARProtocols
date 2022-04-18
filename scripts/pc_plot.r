args = commandArgs(TRUE)
input_pc = args[1]
input_color = args[2]
output_pdf = args[3]

library("hash")

read.table(input_color) -> colorlist
h_colorlist = hash(keys = colorlist[,1], values = colorlist[,2])

read.table(input_pc, head = T) -> pc
color = c()
for (i in c(1 : length(pc[,1]))) {
	id = as.vector(pc$IID)[i]
	color = c(color, as.vector(h_colorlist[[id]]))
}

pdf(output_pdf)
plot(pc$PC1, pc$PC2, pch = 19, cex = 1.5, col = color, xlab = "PC 1", ylab = "PC 2", cex.lab = 1.2, cex.axis = 1)
dev.off()

# Load required libraries
library(GEOquery)
library(affy)
library(limma)
library(ggplot2)
library(biomaRt)
library(WGCNA)

# Download GEO data
gse <- getGEO("GSE_ID", GSEMatrix =TRUE, getGPL=FALSE) 
datMeta <- pData(gse[[1]])
rownames(datMeta) <- datMeta[,2]

# Read GEO data
getGEOSuppFiles("GSE_ID")
setwd("directory")
untar("GSE_ID/GSE_ID_RAW.tar", exdir = "GSE_ID/CEL")
data.affy <- ReadAffy(celfile.path = "directory")
datExpr <- exprs(data.affy)

# Data preprocessing
GSM <- rownames(pData(data.affy))
GSM <- substr(GSM,1,9)
idx <- match(GSM, datMeta$geo_accession)
datMeta <- datMeta[idx,] 
colnames(datExpr) = rownames(datMeta) 

# Metadata cleaning and formatting
idx_source_name_ch1 <- which(colnames(datMeta) == "source_name_ch1")
colnames(datMeta)[idx_source_name_ch1] <- "Dx"
datMeta$Dx <- gsub("pattern_control","CTL",datMeta$Dx)
datMeta$Dx <- gsub("pattern_disease","DS",datMeta$Dx)
datMeta$Dx <- as.factor(datMeta$Dx)

# Quality control of raw data
datExpr <- log2(datExpr)

# Boxplot
boxplot(datExpr, range = 0, col = c('red', 'green')[as.numeric(datMeta$Dx)], xaxt = 'n', xlab = "Array", main = "Boxplot", ylab = "Intensity")

# Multidimensional Scaling (MDS)
mds = cmdscale(dist(t(datExpr)), eig = TRUE)
plot(mds$points, col = c('green', 'red')[as.numeric(datMeta$Dx)], pch = 19, main = "MDS")

# Normalization and batch correction
datExpr <- rma(data.affy, background=T, normalize=T, verbose=T)
datExpr <- exprs(datExpr)

# Outlier detection
outliersCount <- apply(datExpr, 1, function(x) sum(is.na(x)))
outliersSummary <- data.frame(Gene = rownames(datExpr), Count = outliersCount)
outliersSummary <- outliersSummary[order(outliersSummary$Count, decreasing = TRUE), ]

# Annotating Probes   
ensembl <- useMart(biomart="ENSEMBL_MART_ENSEMBL",dataset="hsapiens_gene_ensembl",host="www.ensembl.org")
identifier <- "affy_ID"
getinfo <- c("affy_ID", "ensembl_gene_id", "entrezgene_id", "external_gene_name")
geneDat <- getBM(attributes = getinfo, filters=identifier, values = rownames(datExpr),mart=ensembl)
idx <- match(rownames(datExpr),geneDat$affy_ID)
geneDat <- geneDat[idx,]
exprsData <- datExpr[!is.na(geneDat$ensembl_gene_id), ]

# Collapsing multiple probes into a single value per gene
CR <- collapseRows(exprsData, rowGroup = geneDat$ensembl_gene_id, rowID = geneDat$affy_ID)
exprsData <- CR$datETcollapsed

# Differential Expression Analysis
datMeta$Dx <- as.factor(datMeta$Dx)
mod <- model.matrix(~ Dx, data = datMeta)   
fit <- lmFit(exprsData,mod)
fit <- eBayes(fit)
tt <- topTable(fit,coef = 2,n = Inf,genelist = geneDat)

# Save results
write.csv(tt, "Differential_Expression_Results.csv", row.names = FALSE)

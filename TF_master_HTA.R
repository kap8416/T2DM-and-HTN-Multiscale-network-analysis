##Preparar la matrix de expresion para los genes el modulo significativo a la patología
library(GEOquery)
library(affy)
library(limma)

gse <- getGEO("GSE24752", GSEMatrix =TRUE,getGPL=FALSE) #or# gse <- setwd("C:/Users/lcz/Documents/GSE24572")
datMeta <- pData(gse[[1]])
rownames(datMeta) <- datMeta[,2]

setwd("/Users/lorandacalderonzamora/Respaldo/LORANDA/microarreglo/Conjuto de datos/Hipertensión/GSE24752/")
data.affy <- ReadAffy(celfile.path = "./")
datExpr <- exprs(data.affy)

#check datMeta/datExpr ordering and reformat as necessary
GSM <- rownames(pData(data.affy))
GSM <- substr(GSM,1,9)
idx <- match(GSM, datMeta$geo_accession)
datMeta <- datMeta[idx,] 
colnames(datExpr)=rownames(datMeta)   

datMeta <- datMeta[,-c(3:7,14:36)]
colnames(datMeta)[2] <- c("Dx")
datMeta$Dx[rownames(datMeta) %in% c("GSM609529", "GSM609530")] <- "CTL"
datMeta$Dx[rownames(datMeta) %in% c("GSM609525", "GSM609526")] <- "HTA"
datMeta <- datMeta[!rownames(datMeta) %in% c("GSM609527", "GSM609528"), ]
datMeta$Dx <- as.factor(datMeta$Dx)

# QC on Raw Data

datExpr <- log2(datExpr)
dim(datExpr)


##Normalization 

datExpr <- rma(data.affy, background=T, normalize=T, verbose=T)
datExpr <- exprs(datExpr)


#Annotating Probes   
library(ensembldb)
library(biomaRt)

ensembl <- useMart(biomart = "ENSEMBL_MART_ENSEMBL", 
                   dataset = "hsapiens_gene_ensembl", 
                   host = "https://www.ensembl.org")

f <- listFilters(ensembl)
a <- listAttributes(ensembl)

identifier <- "affy_hg_u133_plus_2"
getinfo <- c("affy_hg_u133_plus_2", "ensembl_gene_id", "entrezgene_id", "external_gene_name")

if (is.null(rownames(datExpr))) {
  stop("Error: ‘datExpr’ does not have row names. They are required for annotation")
}

geneDat <- getBM(attributes = getinfo, 
                 filters = identifier, 
                 values = rownames(datExpr),  # Aquí se usa directamente rownames(datExpr)
                 mart = ensembl)

idx <- match(rownames(datExpr),geneDat$affy_hg_u133_plus_2)
geneDat <- geneDat[idx,]
table(is.na(geneDat$ensembl_gene_id)) 

to_keep <- (is.na(geneDat$ensembl_gene_id) == FALSE)
geneDat <- geneDat[to_keep,]
samples_to_remove <- c("GSM609527.CEL.gz", "GSM609528.CEL.gz")
datExpr <- datExpr[, !(colnames(datExpr) %in% samples_to_remove)]

dim(datExpr)
dim(geneDat)

#Collapse Rows

table(duplicated(geneDat$affy_hg_u133a_2)) 
table(duplicated(geneDat$ensembl_gene_id)) 
library(WGCNA)

CR <- collapseRows(datExpr, rowGroup = geneDat$ensembl_gene_id, rowID = geneDat$affy_hg_u133_plus_2, method = "MaxMean")
CR$datETcollapsed
idx <- match(CR$group2row[,"selectedRowID"], geneDat$"affy_hg_u133_plus_2")
geneDat <- geneDat[idx,]
rownames(geneDat) <- geneDat$ensembl_gene_id 

dim(CR$datETcollapsed)
dim(geneDat)

CR$datETcollapsed <- as.data.frame(CR$datETcollapsed)
CR$datETcollapsed$ensembl_gene_id <- rownames(CR$datETcollapsed)

expr_matrix <- merge(CR$datETcollapsed, geneDat, 
                     by = "ensembl_gene_id", 
                     all.x = TRUE)

expr_matrix <- expr_matrix[!duplicated(expr_matrix$external_gene_name), ]
expr_matrix_numeric <- expr_matrix[, grep("GSM", colnames(expr_matrix))]
expr_matrix_unique <- aggregate(expr_matrix_numeric, 
                                by = list(expr_matrix$external_gene_name), 
                                FUN = mean)

colnames(expr_matrix_unique)[1] <- "external_gene_name"
rownames(expr_matrix_unique) <- expr_matrix_unique$external_gene_name
expr_matrix_unique <- expr_matrix_unique[, -1]


library(dplyr)
library(viper)      
library(dorothea) 

# 1) Cargar la información de DoRothEA para humano
data(dorothea_hs, package="dorothea")  # data.frame con columnas: tf, target, confidence, etc.

# 2) Filtrar por nivel de evidencia (opcional, A y B suelen ser los más confiables)
dorothea_regulons <- dorothea_hs %>%
  dplyr::filter(confidence %in% c("A", "B"))

# Crear un regulón compatible con VIPER
my_regulon <- dorothea_regulons %>%
  group_by(tf) %>%
  summarise(
    targets = list(setNames(mor, target)),  # mor = modo de regulación (+1, -1)
    .groups = "drop"
  )

# Convertir el data frame en una lista de regulones
my_regulon <- setNames(my_regulon$targets, my_regulon$tf)

# Revisar la estructura del regulón creado
str(my_regulon, max.level = 2)

# Crear la estructura correcta para VIPER
my_regulon_viper <- lapply(my_regulon, function(targets) {
  list(
    tfmode = targets,  # Modos de regulación (+1 activador, -1 represor)
    likelihood = rep(1, length(targets))  # Probabilidad uniforme
  )
})


tf_activity <- viper(
  eset = expr_matrix_unique, 
  regulon = my_regulon_viper, 
  method = "scale", 
  nes = TRUE
)

# Agregar etiquetas de condición
condition_labels <- datMeta$Dx
names(condition_labels) <- colnames(tf_activity)

# Boxplot de actividad de un TF clave
library(ggplot2)

tf_to_plot <- "FOXA1"  # Cambiar por TFs relevantes

df <- data.frame(
  Sample = colnames(tf_activity),
  Activity = tf_activity[tf_to_plot, ],
  Condition = condition_labels
)

ggplot(df, aes(x = Condition, y = Activity, fill = Condition)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, alpha = 0.5) +
  labs(title = paste("", tf_to_plot), y = "Enrichment Score") +
  scale_fill_manual(values = c("red", "blue")) +
  theme_minimal()

# Crear los grupos de muestras
hta_samples <- c("GSM609525.CEL.gz", "GSM609526.CEL.gz")  # Diabéticos
ctl_samples <- c("GSM609529.CEL.gz", "GSM609530.CEL.gz")  # Controles

# Calcular la media para cada TF en los grupos HTA y CTL
tf_means <- data.frame(
  TF = rownames(tf_activity),
  HTA_mean = rowMeans(tf_activity[, hta_samples]),
  CTL_mean = rowMeans(tf_activity[, ctl_samples]),
  stringsAsFactors = FALSE
)

# Aplicar la prueba t para comparar las medias de los grupos
p_values <- apply(tf_activity, 1, function(x) t.test(x[hta_samples], x[ctl_samples])$p.value)
tf_means$p_value <- p_values
tf_means <- tf_means[order(tf_means$p_value), ]


head(tf_means)
write.csv(tf_means, "TF_activity_comparison.csv", row.names = FALSE)

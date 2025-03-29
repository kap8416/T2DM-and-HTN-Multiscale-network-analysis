# GEO Data Processing and Differential Expression Analysis

## Overview  
This pipeline automates the retrieval, preprocessing, normalization, and **differential expression analysis** of **GEO microarray datasets** using R. The workflow includes **data normalization, batch correction, probe annotation, and differential gene expression analysis** with **limma**.

## Features  
- **Automatic retrieval of GEO datasets** using GEOquery  
- **Preprocessing and quality control** including boxplots and MDS visualization  
- **RMA normalization and batch correction**  
- **Probe annotation using biomaRt**  
- **Collapsing multiple probes per gene**  
- **Differential expression analysis** using limma  
- **Outputs a list of differentially expressed genes (DEGs) in CSV format**

## Dependencies  
Ensure you have R installed and the following packages installed:  
```r
install.packages(c("GEOquery", "affy", "limma", "ggplot2", "biomaRt", "WGCNA"))
```

## Usage  

### 1. Clone the Repository (or manually download the script)
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Open R and Load Required Libraries  
```r
library(GEOquery)
library(affy)
library(limma)
library(ggplot2)
library(biomaRt)
library(WGCNA)
```

### 3. Run the Script  
Modify the **GSE_ID** and **directory** parameters in `GEO_Data_Processing.R`, then execute:
```r
source("GEO_Data_Processing.R")
```

### 4. Expected Output  
- **Boxplots and MDS plots** for quality control  
- **Normalized and batch-corrected expression data**  
- **Annotated gene expression matrix**  
- **List of differentially expressed genes (DEGs) in `Differential_Expression_Results.csv`**  

### Example of the Output Format (Differential Expression Results)  
| Gene | logFC | adj.P.Val | External Gene Name |  
|------|------:|----------:|--------------------|  
| ENSG000001 | 2.15 | 0.0001 | TP53 |  
| ENSG000002 | -1.98 | 0.0025 | VEGFA |  

## Citation  
If you use this pipeline for your research, please cite:  
```
Loranda Calderón-Zamora and Katia Avina-Padilla "GEO Data Processing and Differential Expression Analysis in R", GitHub, 2025.
```



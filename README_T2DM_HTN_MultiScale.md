# Multi-Scale Network Analysis of T2DM and HTN

This repository contains the full codebase and associated resources used in the study **"Inflammatory and Vascular Remodeling Pathways link Type 2 Diabetes and Hypertension: A Multi-Scale Network Analysis"**, created on 29 March 2025. The analysis integrates transcriptomic data and interactome-based approaches to identify predictive hub genes and regulatory mechanisms shared between type 2 diabetes mellitus (T2DM) and hypertension (HTN).

## Overview

We employed a multi-scale network framework combining transcriptomic profiling, co-expression networks, transcription factor (TF) activity inference, protein-protein interaction (PPI) analysis, and tissue-specific validation. This comprehensive strategy enabled the identification of key regulatory modules and predictive hub genes involved in vascular and inflammatory processes common to both diseases.

## Workflow Summary

The workflow is composed of six main stages (also illustrated in **Figure 1** of the manuscript):


<img width="1199" alt="Screenshot 2025-04-05 at 10 38 15 AM" src="https://github.com/user-attachments/assets/68e36f84-8fda-49c9-b5dd-2d8c44ccf409" />




1. **Data Preprocessing**  
   - Transcriptomic dataset acquisition  
   - Normalization, batch correction, and construction of expression matrices

2. **Differential Expression Analysis**  
   - Conducted with the `limma` package in R  
   - Includes gene annotation, outlier detection, and statistical testing

3. **Co-expression Network Construction (WGCNA)**  
   - Identification of disease-associated modules  
   - Detection of top eigengenes and module-trait relationships

4. **Functional Enrichment Analysis**  
   - Performed using Gene Ontology (GO) and KEGG pathway databases  
   - Highlighting immune and vascular remodeling pathways

5. **Transcription Factor Activity Inference**  
   - Inferred using `DoRothEA` and `VIPER` in R  
   - Identification of key regulatory TFs and their target genes

6. **PPI Network Construction and Hub Gene Identification**  
   - Networks built with STRING v11.5  
   - Visualized using Python scripts (networkx, matplotlib)  
   - Community detection and enrichment performed for topological modules  
   - In-silico validation using GTEx for tissue-specific expression

## Repository Structure

```
├── data/
│   ├── raw/                  # Raw expression data files
│   └── processed/            # Preprocessed and normalized datasets
├── scripts/
│   ├── 01_limma_dge.R        # Differential expression analysis
│   ├── 02_wgcna_network.R    # WGCNA module construction
│   ├── 03_functional_enrich.R# GO and KEGG enrichment
│   ├── 04_dorothea_viper.R   # Transcription factor inference
│   └── 05_ppi_network.py     # STRING-based PPI construction and visualization
├── results/
│   ├── figures/              # High-resolution figures for the manuscript
│   └── tables/               # Key output files (DEGs, modules, hubs)
└── README.md
```

## Dependencies

This project requires the following tools and packages:

- **R (≥ 4.2.0)**  
  - `limma`, `WGCNA`, `clusterProfiler`, `org.Hs.eg.db`, `VIPER`, `DoRothEA`
- **Python (≥ 3.8)**  
  - `pandas`, `networkx`, `matplotlib`, `seaborn`, `requests`
- **External Tools**  
  - [STRING](https://string-db.org/) (for PPI data)
  - [GTEx Portal](https://gtexportal.org/) (for validation)

## Citation

If you use this repository or adapt the scripts for your own work, please cite the following study:

> *Inflammatory and Vascular Remodeling Pathways link Type 2 Diabetes and Hypertension: A Multi-Scale Network Analysis*. (In preparation, 2025).


## Contact

For questions, suggestions, or collaboration opportunities, please contact:

**Katia Aviña Padilla**  
CINVESTAV - Irapuato  
[ResearchGate](https://www.researchgate.net/profile/Katia-Avina-Padilla) | [Email](mailto:katia.avinap@cinvestav.mx)

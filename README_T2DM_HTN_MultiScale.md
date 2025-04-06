# Multi-Scale Network Analysis of T2DM and HTN

This repository contains the full codebase and associated resources used in the study **"Inflammatory and Vascular Remodeling Pathways link Type 2 Diabetes and Hypertension: A Multi-Scale Network Analysis"**, created on 29 March 2025. The analysis integrates transcriptomic data and interactome-based approaches to identify predictive hub genes and regulatory mechanisms shared between type 2 diabetes mellitus (T2DM) and hypertension (HTN).

## Overview

We employed a multi-scale network framework combining transcriptomic profiling, co-expression networks, transcription factor (TF) activity inference, protein-protein interaction (PPI) analysis, and tissue-specific validation. This comprehensive strategy enabled the identification of key regulatory modules and predictive hub genes involved in vascular and inflammatory processes common to both diseases.

## Workflow Summary

The workflow is composed of six main stages (also illustrated in **Figure 1** of the manuscript):


<img width="1199" alt="![WhatsApp Image 2025-04-06 at 12 10 38 (1)](https://github.com/user-attachments/assets/e8d310e1-06a5-4467-ae4d-030c73a5a933)
" />




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

7. **Rewiring and Focused Hub Subnetwork Analysis**  
   - **Dataset acquisition**: Gene expression datasets GSE25724 (T2DM) and GSE24752 (HTN) were retrieved from the [Gene Expression Omnibus (GEO)](https://www.ncbi.nlm.nih.gov/geo/).  
   - **Platform mapping**: Probe-to-gene mapping was performed using platform annotation files GPL96 and GPL570.  
   - **Probe aggregation**: Redundant probes mapping to the same gene were averaged to produce a single expression value per gene.  
   - **Normalization**: Quantile normalization was applied using the `limma` package in R to reduce technical variability.  
   - **Gene selection**: The top 100 genes with the highest absolute expression differences between T2DM and HTN were retained.  
   - **Network construction**: Pearson correlation coefficients were computed between all gene pairs to construct condition-specific co-expression networks.  
   - **Network representation**:  
     - Nodes: genes  
     - Edges: significant co-expression relationships  
   - **Connectivity metric**: Each gene’s connectivity was defined as the sum of its absolute Pearson correlation coefficients with all other genes.  
   - **Rewiring Score calculation**:  
     ```
     Rewiring Score = Connectivity in Diabetes − Connectivity in Hypertension
     ```  
   - **Hub prioritization**: Genes with the highest absolute rewiring scores were considered rewired hubs.  
   - **Global rewiring network**: Constructed to represent gene pairs with significant correlation changes across conditions.  

   - **Focused subnetwork extraction**:  
     - Script: `Focused_HubSubnetwork_T2D_HTN.py`  
     - Input:  
       - Tab-delimited list of hub genes  
       - PPI interaction matrix (e.g., from STRING)  
     - Core features:  
       - Extracts condition-specific subnetworks  
       - Computes local connectivity metrics  
       - Visualizes using `networkx` and `matplotlib`  
     - Output:  
       - Annotated visualizations of subnetworks  
       - Exportable node and edge tables for downstream enrichment  
     - Requirements:  
       ```bash
       pip install pandas networkx matplotlib
       ```  
     - Execution:  
       ```bash
       python Focused_HubSubnetwork_T2D_HTN.py
       ```



## Tool Summary by Analysis Step

| Step | Analysis Component                             | Tool(s) Used                                 | Language     | Output                                |
|------|------------------------------------------------|----------------------------------------------|--------------|----------------------------------------|
| 1    | Data Preprocessing                             | GEOquery, limma                              | R            | Expression matrices                    |
| 2    | Differential Expression Analysis               | limma                                        | R            | List of DEGs                           |
| 3    | Co-expression Network Construction             | WGCNA                                        | R            | Modules, module-trait relationships    |
| 4    | Functional Enrichment Analysis                 | clusterProfiler, org.Hs.eg.db                | R            | GO/KEGG pathway enrichment             |
| 5    | Transcription Factor Activity Inference        | DoRothEA, VIPER                              | R            | TF activity matrices                   |
| 6    | PPI Network and Hub Gene Identification        | STRING, networkx, matplotlib                 | Python       | PPI networks, hub gene list            |
| 7    | Rewiring Analysis                              | limma, Pearson correlation, custom   script  | R/Python     | Rewiring scores, global rewiring graph |
| 8    | Focused Hub Subnetwork Visualization           | networkx, matplotlib                         | Python       | Subnetwork figures, exportable tables  |



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

> *Inflammatory and Vascular Remodeling Pathways link Type 2 Diabetes and Hypertension: A Multi-Scale Network Analysis*. (In preparation, Frontiers in Bioscience 2025).


## Contact

For questions, suggestions, or collaboration opportunities, please contact:

**Katia Aviña Padilla**  
CINVESTAV - Irapuato  
[ResearchGate](https://www.researchgate.net/profile/Katia-Avina-Padilla) | [Email](mailto:katia.avinap@cinvestav.mx)

# PPI Network Analysis for Type 2 Diabetes Mellitus (T2DM)

## Overview
This repository contains a **Protein-Protein Interaction (PPI) Network Analysis** for **Type 2 Diabetes Mellitus (T2DM)**. The study aims to identify **key hub genes, functional clusters, and biological pathways** associated with T2DM using **high-confidence interactions** from the STRING database.

## Features
- **PPI Network Construction** using STRING database interactions with a confidence score > 0.9.
- **Hub Gene Identification** based on degree centrality.
- **Community Detection** using modularity optimization to identify major functional clusters.
- **Visualization** of the network with highlighted hubs and top three communities.
- **Statistical Metrics** including network size, hub interactions, and community structures.

## Files
- `protein_network_T2D.py`: Python script to generate the PPI network and perform analysis.
- `string_interactions_T2D.tsv`: Input data containing STRING interactions for T2DM.
- `output_network.png`: Visualization of the constructed PPI network.
- `README.md`: This file describing the project.

## Installation
To run the analysis, ensure you have **Python 3.x** installed along with the required dependencies:

```bash
pip install pandas networkx matplotlib
```

## Usage
Run the Python script to generate the network:

```bash
python protein_network_T2D.py
```

This will create a **network visualization** and print **statistical metrics** related to hub genes and community structures.

## Results Summary
- The **network consists of 613 proteins and 812 interactions**.
- **Hub genes** (*TP53, UBB, RPL3, RPL4*) were identified, with *TP53* being the most connected node (29 interactions).
- **Community analysis** revealed **95 distinct functional clusters**, with the top three containing **54, 50, and 41 proteins**, respectively.
- Functional clusters highlight the roles of **metabolic regulation, oxidative stress, and translational control** in T2DM.


## Contact
For inquiries, contact Katia Aviña Padilla.

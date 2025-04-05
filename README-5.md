# 🔄 Rewiring Analysis in Type 2 Diabetes and Hypertension

This repository contains a Python script for analyzing gene coexpression network *rewiring* between two conditions: Type 2 Diabetes (GSE25724) and Hypertension (GSE24752), using publicly available microarray data from GEO.

## 📁 Files

- `rewiring_analysis_script.py`: Main script to preprocess data, normalize expression, compute gene-gene correlation networks, and quantify rewiring scores.
- `GSE25724_series_matrix.txt`: Expression matrix for T2DM samples.
- `GSE24752_series_matrix.txt`: Expression matrix for Hypertension samples.
- `GPL96.annot`: Probe-to-gene annotation file for platform GPL96 (Affymetrix HG-U133A).
- `GPL570.annot`: Probe-to-gene annotation file for platform GPL570 (Affymetrix HG-U133 Plus 2.0).

## ⚙️ Requirements

Make sure you have the following Python packages installed:

```bash
pip install pandas numpy scikit-learn matplotlib networkx
```

## 🚀 How to Run

1. Clone this repository or download the files manually.

2. Place all input files in the same directory as the script:
   - `GSE25724_series_matrix.txt`
   - `GSE24752_series_matrix.txt`
   - `GPL96.annot`
   - `GPL570.annot`

3. Run the script:

```bash
python rewiring_analysis_script.py
```

This will:
- Normalize and filter the expression data
- Construct correlation matrices for both conditions
- Calculate gene-level rewiring scores
- Visualize the top rewired genes as a network

## 📊 Output

- Printed rewiring scores for all genes
- Network graph highlighting the top 30 rewired genes with strongest changes in connectivity between diabetes and hypertension conditions

## 📚 Citation

If you use this script in your research, please cite:

> Aviña-Padilla, K. et al. "Inflammatory and Vascular Remodeling Pathways link Type 2 Diabetes and Hypertension: A Multi-Scale Network Analysis." *In preparation.*

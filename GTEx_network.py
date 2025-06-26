#!/usr/bin/env python3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load GTEx v10 data
gtex_df = pd.read_csv("GTEx_Analysis_2022-06-06_v10_RNASeQCv2.4.2_gene_median_tpm.gct", sep="\t", skiprows=2)
gtex_df["ENSG_ID"] = gtex_df["Name"].str.replace(r"\.\d+$", "", regex=True)
gtex_df["Gene_Symbol"] = gtex_df["Description"].str.upper()

# 2. List of selected genes
selected_genes = [
    "ATP5MC3", "RRAGA", "GCA", "PTMAP9", "RNF11", "SLC16A7", "ST18", "RPS7", "NRBF2",
    "CREB1", "BACH1", "AMN", "IL3", "ATRAID", "NIPBL", "CASP3", "PPP1R14D", "ANKRD2",
    "PEX2", "SPINK1", "ANPEP", "MT1G", "NR4A1", "PRSS2", "SCD5", "QPCT"
]

# 3. Selected tissues of interest
tissues_t2dm = ["Adipose_Subcutaneous", "Adipose_Visceral_Omentum", "Liver", "Muscle_Skeletal", "Pancreas"]
tissues_htn = ["Adrenal_Gland", "Artery_Aorta", "Artery_Coronary", "Heart_Atrial_Appendage", "Heart_Left_Ventricle", "Kidney_Cortex", "Lung"]
selected_tissues = tissues_t2dm + tissues_htn

# 4. Filter TPM matrix for selected genes
heatmap_df = gtex_df[gtex_df["Gene_Symbol"].isin([g.upper() for g in selected_genes])]
heatmap_df = heatmap_df.set_index("Gene_Symbol")[selected_tissues]

# 5. Log2(TPM + 1) transformation
heatmap_log2 = heatmap_df.applymap(lambda x: np.log2(x + 1))

# 6. Normalize per gene (row-wise z-score)
heatmap_scaled = heatmap_log2.sub(heatmap_log2.mean(axis=1), axis=0)
heatmap_scaled = heatmap_scaled.div(heatmap_log2.std(axis=1), axis=0)

# 7. Color annotations for T2DM and HTN
col_colors = ["#8c564b" if t in tissues_t2dm else "#FFD700" for t in selected_tissues]

# 8. Generate heatmap
sns.set(font_scale=0.9)
cg = sns.clustermap(
    heatmap_scaled,
    cmap=sns.color_palette("GnBu", as_cmap=True),
    row_colors=None,
    col_colors=col_colors,
    xticklabels=True,
    yticklabels=True,
    col_cluster=False,
    row_cluster=True,
    figsize=(14, 22),
    cbar_kws={"label": "Z-score (log2 TPM)"}
)

# 9. Adjust labels
for label in cg.ax_heatmap.get_yticklabels():
    label.set_rotation(0)
    label.set_color("black")
    label.set_fontsize(16)  # Gene labels enlarged
    label.set_fontweight("normal")
for label in cg.ax_heatmap.get_xticklabels():
    label.set_fontsize(16)  # Tissue labels slightly smaller
    label.set_rotation(90)
    label.set_fontweight("bold")
# 10. No main title
cg.fig.suptitle("")
cg.savefig("/Users/lorandacalderonzamora/Downloads/GTEx/heatmap_GTEx_genes_tissues.png", dpi=300, bbox_inches='tight')  # PNG
plt.show()
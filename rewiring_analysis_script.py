
# ============================
# SCRIPT: Análisis de Rewiring Transcriptómico
# ============================

import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# ============================
# FUNCIONES
# ============================

# Extrae la tabla de anotación desde archivos GPL
def extract_annotation_table(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = next(i for i, line in enumerate(lines) if '!platform_table_begin' in line) + 1
    table_data = lines[start_index:]
    
    df = pd.read_csv(StringIO(''.join(table_data)), sep='\t', dtype=str)
    
    cols = ['ID', 'Gene symbol', 'Gene ID']
    df = df[[col for col in cols if col in df.columns]].dropna()
    return df

# Carga la matriz de expresión desde un archivo de GEO
def load_expression_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = next(i for i, line in enumerate(lines) if "!series_matrix_table_begin" in line) + 1
    end_index = next(i for i, line in enumerate(lines) if "!series_matrix_table_end" in line)
    table_data = lines[start_index:end_index]
    
    df = pd.read_csv(StringIO(''.join(table_data)), sep='\t', dtype=str)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    return df

# Calcula matriz de correlación entre muestras
def compute_correlation_matrix(df):
    expr_data = df.iloc[:, 1:].astype(float)
    corr_matrix = expr_data.corr(method='pearson')
    return corr_matrix

# Visualiza matriz de correlación con seaborn
def plot_correlation_matrix(corr_matrix, title):
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', fmt=".2f", square=True)
    plt.title(title)
    plt.tight_layout()
    plt.show()

# ============================
# RUTAS A LOS ARCHIVOS
# ============================

gpl96_path = "GPL96.annot"
gpl570_path = "GPL570.annot"
gse25724_path = "GSE25724_series_matrix.txt"
gse24752_path = "GSE24752_series_matrix.txt"

# ============================
# PROCESAMIENTO
# ============================

print("Cargando anotaciones...")
gpl96_genes = extract_annotation_table(gpl96_path)
gpl570_genes = extract_annotation_table(gpl570_path)

print("Cargando datos de expresión...")
gse25724_expr = load_expression_matrix(gse25724_path)
gse24752_expr = load_expression_matrix(gse24752_path)

print("Calculando correlaciones...")
gse25724_corr = compute_correlation_matrix(gse25724_expr)
gse24752_corr = compute_correlation_matrix(gse24752_expr)

print("Visualizando matriz de correlación GSE25724")
plot_correlation_matrix(gse25724_corr, "Matriz de correlación - GSE25724")

print("Visualizando matriz de correlación GSE24752")
plot_correlation_matrix(gse24752_corr, "Matriz de correlación - GSE24752")

print("Script finalizado con éxito.")

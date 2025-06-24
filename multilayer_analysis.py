#!/usr/bin/env python3

# ───────────── 1) LOAD FILES ─────────────
annotation = pd.read_csv("annotation.csv")
tf_t2dm    = pd.read_csv("tf_activity_T2DM.csv")
tf_htn     = pd.read_csv("tf_activity_HTN.csv")
me7        = pd.read_csv("ME7_merge_T2Dm-HTN.csv")
deg        = pd.read_csv("DE_merge_T2DM-HTN.csv")
rewiring   = pd.read_csv("Rewiring_results.csv")

# ───────────── 2) CLEAN COLUMN NAMES ─────────────
annotation.columns = [col.strip().lower() for col in annotation.columns]
tf_t2dm.columns    = tf_t2dm.columns.str.strip()
tf_htn.columns     = tf_htn.columns.str.strip()
me7.columns        = me7.columns.str.strip()
deg.columns        = deg.columns.str.strip()
rewiring.columns   = rewiring.columns.str.strip()

# ───────────── 3) FUNCTION TO CREATE NODE DATAFRAME ─────────────
def build_node_df(ids, layer, color):
    return pd.DataFrame({
        "Node": ids,
        "Label": ids,
        "Layer": layer,
        "Color": color,
        "Size": 1
    })

# ───────────── 4) CREATE NODE TABLES BY LAYER ─────────────
nodes_tf_t2dm  = build_node_df(tf_t2dm['TF'].unique(),              'TF_T2DM',  'blue')
nodes_tf_htn   = build_node_df(tf_htn['TF'].unique(),               'TF_HTN',   'green')
nodes_me7      = build_node_df(me7['x'].unique(),                   'ME7',      'red')
nodes_deg      = build_node_df(deg['external_gene_name'].dropna().unique(), 'DEG', 'purple')
nodes_rewiring = build_node_df(pd.concat([rewiring['Gene1'], rewiring['Gene2']]).unique(), 'REW', 'orange')

# ───────────── 5) MAP SYMBOL TO ENSEMBL ID (AND VICE VERSA) ─────────────
symbol_to_ensg = dict(zip(annotation['gene_symbol'], annotation['ensembl_id']))
ensembl_to_symbol = {v: k for k, v in symbol_to_ensg.items()}

# Add Ensembl IDs to TFs
tf_t2dm['ensembl_id'] = tf_t2dm['TF'].map(symbol_to_ensg)
tf_htn['ensembl_id']  = tf_htn['TF'].map(symbol_to_ensg)

# ───────────── 6) CREATE EDGES BETWEEN LAYERS ─────────────
edges = []

# TF_T2DM → ME7 (if target in module)
for _, row in tf_t2dm.dropna(subset=['ensembl_id']).iterrows():
    if row['ensembl_id'] in set(me7['x']):
        edges.append(['TF_T2DM', row['TF'], 'ME7', row['ensembl_id']])

# TF_HTN → ME7
for _, row in tf_htn.dropna(subset=['ensembl_id']).iterrows():
    if row['ensembl_id'] in set(me7['x']):
        edges.append(['TF_HTN', row['TF'], 'ME7', row['ensembl_id']])

# ME7 → DEG (map Ensembl → gene symbol)
for gene in me7['x']:
    symbol = ensembl_to_symbol.get(gene)
    if symbol and symbol in set(deg['external_gene_name']):
        edges.append(['ME7', gene, 'DEG', symbol])

# REW layer (co-expression rewiring)
for _, row in rewiring.iterrows():
    edges.append(['REW', row['Gene1'], 'REW', row['Gene2']])

# ───────────── 7) COMBINE ALL NODES ─────────────
all_nodes = pd.concat([
    nodes_tf_t2dm,
    nodes_tf_htn,
    nodes_me7,
    nodes_deg,
    nodes_rewiring
]).drop_duplicates(subset=['Node'])

# ───────────── 8) CREATE EDGE DATAFRAME ─────────────
edges_df = pd.DataFrame(edges, columns=['Layer1', 'Node1', 'Layer2', 'Node2'])

# ───────────── 9) EXPORT TO TSV FOR Arena3Dweb ─────────────
all_nodes.to_csv("multilayer_nodes.tsv", sep="\t", index=False)
edges_df.to_csv("multilayer_edges.tsv", sep="\t", index=False)
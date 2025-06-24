#!/usr/bin/env python3
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
from pathlib import Path

# 1. Paths
file_path = "string_interactions_T2DM.tsv"   # Your STRING interactions file
out_png   = Path("ppi_network_hubs_T2DM.png")    

# 2. Load data
# If the file has no header, set column names manually
df = pd.read_csv(file_path, sep="\t")
if "#node1" not in df.columns:
    df = pd.read_csv(
        file_path, sep="\t", header=None,
        names=["#node1", "node2", "combined_score", *range(3, 100)])
df["combined_score"] = pd.to_numeric(df["combined_score"], errors="coerce")

# 3. Filter high-confidence interactions
# STRING scores are 0–1000 (or 0–1 if already scaled)
threshold = 900 if df["combined_score"].max() > 1 else 0.9
high_conf = df[df["combined_score"] > threshold]
print("Interactions after filtering:", len(high_conf)
)
if high_conf.empty:
    raise ValueError("No interactions left after filtering; lower the threshold.")

# 4. Build the graph
G = nx.from_pandas_edgelist(
    high_conf, source="#node1", target="node2", edge_attr="combined_score")

score_by_node = pd.concat([
    high_conf[["#node1", "combined_score"]].rename(columns={"#node1": "node"}),
    high_conf[["node2", "combined_score"]].rename(columns={"node2": "node"})
])
mean_score = score_by_node.groupby("node")["combined_score"].mean()

# Seleccionar los 200 nodos con mayor interacción promedio
top200_nodes = mean_score.sort_values(ascending=False).head(200).index.tolist()

# 5. Identify hubs (top‑10 by degree centrality)
degree_cent = nx.degree_centrality(G)
hub_nodes   = sorted(degree_cent, key=degree_cent.get, reverse=True)[:10]
non_hubs    = [n for n in G.nodes if n not in hub_nodes]

# 6. Detect communities
communities      = list(greedy_modularity_communities(G))
community_lookup = {n: i for i, c in enumerate(communities) for n in c}
top_comms        = sorted(communities, key=len, reverse=True)[:3]
top_comm_nodes   = {n for c in top_comms for n in c}

# 7. Compute layout
pos = nx.spring_layout(G, seed=42, k=0.4)
# Offset hub nodes slightly so they stand out
for n in hub_nodes:
    pos[n] = (pos[n][0] + 0.3, pos[n][1] + 0.3)

# 8. Colors and sizes
palette      = [plt.cm.tab20(i / 3) for i in range(3)]
node_colors  = [
    "yellow" if n in hub_nodes
    else palette[community_lookup[n]] if n in top_comm_nodes
    else "lightgray"
    for n in G.nodes
]
node_sizes   = [600 if n in hub_nodes else 200 for n in G.nodes]

# 9. Plot
plt.figure(figsize=(16, 16))
nx.draw_networkx_edges(G, pos, alpha=0.35, edge_color="grey")

# Non‑hub nodes first (background)
nx.draw_networkx_nodes(
    G, pos,
    nodelist=non_hubs,
    node_color=[
        palette[community_lookup[n]] if n in top_comm_nodes else "lightgray"
        for n in non_hubs
    ],
    node_size=200,
    linewidths=0
)

# Hub nodes on top
nx.draw_networkx_nodes(
    G, pos,
    nodelist=hub_nodes,
    node_color="yellow",
    node_size=600,
    linewidths=0  # No border
)

# Labels: normal for regular nodes, bold for hubs
regular_labels = {n: n for n in top200_nodes if n not in hub_nodes}
nx.draw_networkx_labels(
    G, pos,
    labels=regular_labels,
    font_size=6,
    font_weight="normal"
)
hub_labels = {n: n for n in hub_nodes}
nx.draw_networkx_labels(
    G, pos,
    labels=hub_labels,
    font_size=6,
    font_weight="bold"
)

plt.title("PPI Network — Top‑10 hubs (yellow) and 3 largest communities", fontsize=18)
plt.axis("off")

# 10. Save figure
plt.savefig(out_png, dpi=600, bbox_inches="tight", facecolor="white")

print("PNG saved to:", out_png.resolve())


plt.show()

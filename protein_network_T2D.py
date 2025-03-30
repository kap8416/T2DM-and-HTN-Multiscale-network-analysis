import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the interaction data file
file_path = 'string_interactions_HTA.tsv'  # Replace with the correct path if needed
network_data = pd.read_csv(file_path, sep='\t')

# Filter high-confidence interactions (combined_score > 0.9)
high_confidence_data = network_data[network_data['combined_score'] > 0.9]

# Create a graph with the filtered interactions
G = nx.Graph()
for _, row in high_confidence_data.iterrows():
    G.add_edge(row['#node1'], row['node2'], weight=row['combined_score'])

# Compute degree centrality to identify hub nodes
degree_centrality = nx.degree_centrality(G)
sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
hub_nodes = [node for node, _ in sorted_degree[:10]]  # Select the top 10 hubs

# Detect communities using greedy modularity optimization
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))

# Assign each node to its community
community_map = {}
for i, community in enumerate(communities):
    for node in community:
        community_map[node] = i

# Select the top 3 largest communities
top_communities = sorted(communities, key=len, reverse=True)[:3]
top_community_nodes = {node for community in top_communities for node in community}

# Define colors for communities and hubs
num_communities = len(top_communities)
community_colors = [plt.cm.tab20(i / num_communities) for i in range(num_communities)]
node_colors = []
for node in G.nodes:
    if node in hub_nodes:
        node_colors.append("yellow")  # Hubs in yellow
    elif node in top_community_nodes:
        node_colors.append(community_colors[community_map[node]])  # Community colors
    else:
        node_colors.append("lightgray")  # Other nodes in gray

# Adjust layout to emphasize hub nodes
pos = nx.spring_layout(G, seed=42, k=0.4)
hub_offset = 0.3  # Offset to separate hub nodes
for node in hub_nodes:
    if node in pos:
        pos[node] = (pos[node][0] + hub_offset, pos[node][1] + hub_offset)

# Define node sizes (larger for hubs)
node_sizes = [600 if node in hub_nodes else 200 for node in G.nodes]

# Plot the enhanced network visualization
plt.figure(figsize=(16, 16))
nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="gray")
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

# Add title
plt.title("Enhanced Protein Interaction Network: Highlighted Hubs and Top 3 Communities", fontsize=18)
plt.axis("off")
plt.show()

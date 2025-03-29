import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths for enrichment results
files = {
    "Module 3": "enrichment_results_GO_module3.csv",
    "Module 4": "enrichment_results_GO_module4.csv"
}

# Loop through each file to generate publication-ready bar plots
for module, file_path in files.items():
    try:
        # Load enrichment results
        enrichment_data = pd.read_csv(file_path)

        # Select the top enriched terms based on FDR
        top_terms = enrichment_data.nsmallest(10, 'fdr')

        # Create a publication-quality bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=-top_terms['fdr'], 
            y=top_terms['description'], 
            palette="Blues_r"
        )

        # Formatting for scientific presentation
        plt.xlabel('-log10(FDR)', fontsize=12, fontweight='bold')
        plt.ylabel('GO Biological Process', fontsize=12, fontweight='bold')
        plt.title(f'Top 10 Enriched GO Terms in {module}', fontsize=14, fontweight='bold')

        # Adjust tick labels for better readability
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.gca().invert_yaxis()  # Invert y-axis for better visualization

        # Remove unnecessary grid lines for a clean, professional look
        sns.despine()

        # Save the figure in high resolution
        output_filename = f"GO_enrichment_barplot_{module.replace(' ', '_')}.png"
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")

        # Show the figure
        plt.show()

        print(f"Plot saved: {output_filename}")

    except Exception as e:
        print(f"Error processing {module}: {e}")

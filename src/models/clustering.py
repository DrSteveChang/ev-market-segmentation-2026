# src/models/clustering.py
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def execute_market_clustering(X: pd.DataFrame) -> dict:
    """
    Executes K-Means clustering and applies Principal Component Analysis (PCA) 
    for dimensionality reduction. Generates a 2D scatter plot for strategic presentations.
    """
    logging.info("Initializing K-Means clustering algorithm...")
    
    # Define the number of clusters based on business strategy (e.g., Budget, Mid, Premium)
    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    
    sil_score = silhouette_score(X, labels)
    logging.info(f"[K-Means] Silhouette Score: {sil_score:.4f}")
    
    # --- PCA Dimensionality Reduction & Visualization ---
    logging.info("Applying PCA to reduce feature dimensions for 2D visualization...")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    # Construct a temporary DataFrame for Seaborn plotting
    df_pca = pd.DataFrame(data=X_pca, columns=['Principal Component 1', 'Principal Component 2'])
    df_pca['Market Segment'] = [f"Cluster {label}" for label in labels]
    
    # Ensure the reporting directory exists
    output_dir = "data/processed/reports/charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure and generate the scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='Principal Component 1', 
        y='Principal Component 2',
        hue='Market Segment',
        palette='viridis',
        data=df_pca,
        alpha=0.7,
        edgecolor=None
    )
    plt.title("EV Market Segmentation Landscape (PCA Reduced)", fontsize=14, weight='bold')
    plt.xlabel(f"Principal Component 1 (Explains {pca.explained_variance_ratio_[0]:.1%} of variance)")
    plt.ylabel(f"Principal Component 2 (Explains {pca.explained_variance_ratio_[1]:.1%} of variance)")
    
    # Save the visualization for presentation use
    pca_path = os.path.join(output_dir, "kmeans_pca_clusters.png")
    plt.savefig(pca_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"K-Means PCA scatter plot saved to: {pca_path}")
    
    # Prepare textual profiles for the LLM report
    cluster_profiles = {
        f"Cluster_{i}": f"Market Segment {i} (Awaiting LLM qualitative interpretation based on centroids)" 
        for i in range(optimal_k)
    }
    
    # Strictly return the structured dictionary
    return {
        "model": "K-Means",
        "optimal_clusters_k": optimal_k,
        "silhouette_score": float(sil_score),
        "pca_variance_explained": [float(v) for v in pca.explained_variance_ratio_],
        "cluster_profiles": cluster_profiles
    }
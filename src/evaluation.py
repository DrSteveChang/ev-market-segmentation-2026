# src/evaluation.py
import os
import logging
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay

def evaluate_classification_with_cost(y_true, y_pred, model_name="Classifier"):
    """
    Evaluates the model statistically and applies an asymmetric cost matrix 
    to quantify the projected financial risk of misclassification.
    Also automatically saves the Confusion Matrix visualization to disk.
    """
    logging.info(f"Initiating evaluation sequence for {model_name}...")
    
    # 1. Statistical Evaluation
    acc = accuracy_score(y_true, y_pred)
    logging.info(f"[{model_name}] Statistical Accuracy: {acc:.4f}")
    
    # 2. Financial Risk Assessment (Asymmetric Cost Matrix)
    # Penalties reflect varying degrees of business impact (e.g., brand damage vs. lost margin)
    cost_matrix = {
        ('Luxury', 'Budget'): 1000,
        ('Luxury', 'Mid-range'): 500,
        ('Premium', 'Budget'): 300,
        ('Budget', 'Luxury'): 800,
        ('Mid-range', 'Premium'): 50
    }
    
    total_risk_cost = 0
    for true_val, pred_val in zip(y_true, y_pred):
        if true_val != pred_val:
            penalty = cost_matrix.get((true_val, pred_val), 10) # Default penalty base
            total_risk_cost += penalty
            
    logging.info(f"[{model_name}] Total Projected Financial Risk Score: {total_risk_cost}")
    
    # 3. Export Visualization (Defensive directory creation)
    output_dir = "data/processed/figures"
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax, cmap="Blues")
    plt.title(f"Confusion Matrix: Actual vs Predicted ({model_name})")
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, f"CM_{model_name.replace(' ', '_')}.png")
    plt.savefig(save_path, dpi=300)
    plt.close() # Crucial: Frees memory and prevents blocking the CI/CD pipeline
    logging.info(f"Confusion matrix visualization saved to {save_path}")
    
    return total_risk_cost
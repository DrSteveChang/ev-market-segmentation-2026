# src/models/classifiers.py
import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

def calculate_commercial_loss(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """
    Calculates the expected commercial loss based on an asymmetric cost matrix.
    This simulates the real-world financial penalty of misclassification.
    """
    labels = np.unique(y_true)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Define asymmetric commercial penalties (in USD)
    penalty_fp = 50000 
    penalty_fn = 15000 
    
    # Extract False Positives and False Negatives
    false_positives = np.sum(cm, axis=0) - np.diag(cm)
    false_negatives = np.sum(cm, axis=1) - np.diag(cm)
    
    # Calculate the total expected commercial loss in USD
    total_expected_loss = np.sum(false_positives * penalty_fp) + np.sum(false_negatives * penalty_fn)
    
    return float(total_expected_loss)

def execute_classification_suite(X: pd.DataFrame, y: pd.Series) -> dict:
    """
    Executes SVM and Random Forest classifiers. Extracts feature importance, evaluates 
    commercial cost, and exports a Confusion Matrix visualization for presentation.
    """
    logging.info("Performing train-test split for the classification task...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    results = {}
    output_dir = "data/processed/reports/charts"
    os.makedirs(output_dir, exist_ok=True)

    # --- Lab 3: Support Vector Machines (SVM) ---
    logging.info("Training Support Vector Machine (SVM)...")
    svm = SVC(kernel='linear', C=1.0, random_state=42)
    svm.fit(X_train, y_train)
    svm_pred = svm.predict(X_test)
    
    # Calculate financial risk for SVM
    svm_commercial_loss = calculate_commercial_loss(y_test, svm_pred)
    
    # --- SVM Confusion Matrix Visualization ---
    logging.info("Generating SVM Confusion Matrix for presentation...")
    cm = confusion_matrix(y_test, svm_pred)
    plt.figure(figsize=(8, 6))
    
    # Configure the heatmap for clarity in slides
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, 
                xticklabels=np.unique(y), yticklabels=np.unique(y))
    plt.title("SVM Classification Confusion Matrix", fontsize=14, weight='bold')
    plt.xlabel("Predicted Market Segment")
    plt.ylabel("Actual Market Segment")
    
    svm_cm_path = os.path.join(output_dir, "svm_confusion_matrix.png")
    plt.savefig(svm_cm_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"SVM Confusion Matrix saved to: {svm_cm_path}")
    
    results['svm'] = {
        "accuracy": float(accuracy_score(y_test, svm_pred)),
        "f1_score": float(f1_score(y_test, svm_pred, average='weighted')),
        "expected_commercial_loss_usd": svm_commercial_loss
    }

    # --- Lab 2: Decision Trees & Random Forests ---
    logging.info("Training Random Forest for feature importance and cost evaluation...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    
    rf_commercial_loss = calculate_commercial_loss(y_test, rf_pred)
    
    # Extract top 5 important features to identify key business drivers
    importances = rf.feature_importances_
    feature_names = X.columns
    feature_importance_dict = {
        feature_names[i]: float(importances[i]) 
        for i in importances.argsort()[::-1][:5]
    }

    results['random_forest'] = {
        "accuracy": float(accuracy_score(y_test, rf_pred)),
        "f1_score": float(f1_score(y_test, rf_pred, average='weighted')),
        "expected_commercial_loss_usd": rf_commercial_loss,
        "top_business_drivers": feature_importance_dict
    }

    logging.info(f"[Commercial Eval] SVM Loss: ${svm_commercial_loss:,.2f} | RF Loss: ${rf_commercial_loss:,.2f}")

    return results
# main.py
import logging
import argparse
import sys
import os
import json

# Import data engineering modules
from src.data_pipeline import fetch_data, preprocess_for_modeling

# Import independent mathematical modeling engines mapping to the curriculum
from src.models import (
    execute_classification_suite,    # Covers Lab 2 (Decision Tree/RF) & Lab 3 (SVM)
    execute_market_clustering,       # Covers Lab 4 (Unsupervised Learning + PCA)
    execute_risk_factor_regression   # Covers Lab 1 (Regression)
)

# Import the LLM deployment and visualization modules
from src.deployment.llm_reporter import generate_headless_strategic_insight # Covers Lab 6 (NLP/Prompting)
from src.deployment.visualizer import generate_business_charts

def setup_logging():
    """
    Configures standard output logging with ISO timestamps and severity levels.
    """
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def export_metrics_to_txt(metrics: dict, output_dir: str = "data/processed/reports"):
    """
    Exports the comprehensive quantitative metrics (Score Report) to a local .txt file
    for audit trails and offline review.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "model_evaluation_scores.txt")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("========== COMPREHENSIVE MODEL EVALUATION SCORES ==========\n\n")
            # Serialize the dictionary to a beautifully formatted JSON/Text structure
            f.write(json.dumps(metrics, indent=4))
        logging.info(f"Quantitative score report successfully saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save score report: {e}")

def save_final_report_to_disk(report_content: str, output_dir: str = "data/processed/reports"):
    """
    Saves the final LLM-generated strategic report to a Markdown file.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "strategic_insight_report.md")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        logging.info(f"Final strategic report successfully saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save final report: {e}")

def main():
    """
    Main orchestrator for the EV Market Strategic Segmentation Pipeline.
    """
    # 1. Parse command-line arguments for pipeline execution control
    parser = argparse.ArgumentParser(description="Automated ML Pipeline for EV Strategy")
    parser.add_argument(
        '--step', 
        type=str, 
        default='all', 
        choices=['ml_only', 'all'], 
        help="Determine execution mode: 'ml_only' bypasses the LLM API call."
    )
    args = parser.parse_args()

    setup_logging()
    logging.info("========== INITIATING FULL CURRICULUM ML PIPELINE ==========")

    # 2. Data Ingestion & Preprocessing Phase
    logging.info("Virtualizing and preprocessing data...")
    try:
        raw_data = fetch_data()
        X_clf, y_clf, X_cluster, X_reg, y_reg = preprocess_for_modeling(raw_data)
        logging.info("Data successfully mapped to multi-task matrices.")
    except Exception as e:
        logging.error(f"Data pipeline initialization failed: {e}")
        sys.exit(1)

    # 3. Core Model Matrix Execution Phase (Aggregator Pattern)
    comprehensive_metrics = {}

    try:
        logging.info("Executing Classification Suite (Lab 2: RF & Lab 3: SVM)...")
        comprehensive_metrics["classification"] = execute_classification_suite(X_clf, y_clf)

        logging.info("Executing Unsupervised Clustering (Lab 4: K-Means & PCA)...")
        comprehensive_metrics["clustering"] = execute_market_clustering(X_cluster)

        logging.info("Executing Factor Regression (Lab 1: OLS)...")
        comprehensive_metrics["regression"] = execute_risk_factor_regression(X_reg, y_reg)

        logging.info("All quantitative modeling completed successfully.")
        
    except Exception as e:
        logging.error(f"Mathematical modeling execution failed: {e}")
        sys.exit(1)

    # 4. Data Persistence & Visualization Phase
    logging.info("========== INITIATING DATA EXPORT & VISUALIZATION ==========")
    # Save the raw numbers to a txt file
    export_metrics_to_txt(comprehensive_metrics)
    
    try:
        # Export static charts to the local directory
        generate_business_charts(comprehensive_metrics)
    except Exception as e:
        logging.error(f"Visualization export failed: {e}")

    # 5. Conditional LLM Reporting Phase
    if args.step == 'ml_only':
        logging.info("Execution mode is set to 'ml_only'. Pipeline halted gracefully.")
        sys.exit(0)

    logging.info("========== INITIATING STRATEGIC LLM REPORTING ==========")
    
    business_scenario = (
        "Core Business Problem: The client faces declining margins and needs to restructure "
        "its 2026 EV product matrix. Identify high-risk segments and blue-ocean opportunities "
        "using the provided empirical data. Conclude with a 3-step actionable strategy."
    )
    
    model_ensemble_name = "Full Curriculum Analytics Engine (OLS, SVM, RF, K-Means, PCA)"
    
    final_report = generate_headless_strategic_insight(
        model_name=model_ensemble_name,
        metrics=comprehensive_metrics,
        scenario_focus=business_scenario
    )

    if final_report:
        # Save the AI-generated text to a local markdown file
        save_final_report_to_disk(final_report)
        logging.info("========== PIPELINE COMPLETED SUCCESSFULLY ==========")
    else:
        logging.error("========== PIPELINE TERMINATED WITH API ERRORS ==========")
        sys.exit(1)

if __name__ == "__main__":
    main()
# EV Market Strategic Segmentation 2026
**Full Curriculum Analytics Engine (OLS, SVM, RF, K-Means, PCA)**

## 📖 Project Overview
This repository contains a production-grade, end-to-end Machine Learning pipeline designed to address margin erosion in the 2026 Electric Vehicle (EV) market. Following the complete **CRISP-DM** framework, the system ingests raw market data, executes a multi-paradigm mathematical modeling suite, and deploys an LLM-driven automated reporting engine to generate actionable business strategies and quantify financial risks.

## 🏗️ Architecture & Modules
The pipeline is fully modularized and covers the core machine learning curriculum:

* **Data Engineering (`src/data_pipeline.py`)**
  * Automated data ingestion via Kaggle API.
  * Virtualization, cleaning, and matrix preparation for multi-task learning.
* **Supervised Classification (`src/models/classifiers.py`)**
  * **Algorithms:** Random Forest (Lab 2) & Support Vector Machines (Lab 3).
  * **Business Logic:** Implements an **Asymmetric Cost Matrix** to evaluate models based on *Expected Commercial Loss (USD)* rather than pure statistical accuracy, prioritizing financial risk minimization.
* **Unsupervised Clustering (`src/models/clustering.py`)**
  * **Algorithms:** K-Means Clustering & Principal Component Analysis (PCA) (Lab 4).
  * **Business Logic:** Identifies continuous market personas and applies PCA for dimensionality reduction to visualize market fragmentation.
* **Financial Risk Regression (`src/models/linear_regression.py`)**
  * **Algorithms:** Ordinary Least Squares (OLS) (Lab 1).
  * **Business Logic:** Isolates significant causal factors to quantify brand equity premiums and supply chain penalties.
* **MLOps & Deployment (`src/deployment/`)**
  * `visualizer.py`: Generates presentation-ready static charts (Feature Importance, PCA Scatter, Confusion Matrix, OLS Risk).
  * `llm_reporter.py` (Lab 6): Interfaces with GPT models to synthesize quantitative metrics into a formal, English-language strategic consulting report.

## 🚀 Execution Guide

### 1. Environment Setup
Ensure all dependencies are installed. It is recommended to use a virtual environment (`tfm_intel`).
```bash
python -m pip install -r requirements.txt

2. Run the Pipeline
The orchestrator (main.py) controls the entire flow. You must provide your LLM API key as an environment variable.

To run the complete pipeline (Modeling + Visualization + LLM Report):

Bash
MIMO_API_KEY="sk-your-real-api-key" python main.py --step all
To run only the mathematical models and bypass the LLM API call:

Bash
python main.py --step ml_only
📊 Deliverables & Output
Upon successful execution, the pipeline automatically generates an audit trail and strategic deliverables in the data/processed/reports/ directory:

strategic_insight_report.md: The final, LLM-generated executive strategy report.

model_evaluation_scores.txt: A serialized JSON ledger containing all exact floating-point metrics, p-values, and commercial loss calculations for compliance audits.

charts/: High-resolution PNGs ready for executive presentations:

rf_feature_importance.png: Top 5 business drivers.

ols_risk_exposure.png: Top 20 positive/negative price coefficients.

svm_confusion_matrix.png: Visual misclassification heatmap.

kmeans_pca_clusters.png: 2D market landscape scatter plot.

🛡️ Model Evolution & Data Drift
This system includes a strict decay monitoring protocol (CRISP-DM Phase 6). The current Random Forest model is considered invalidated and requires full retraining if:

The 90th percentile of charging_speed_kw exceeds 350kW in new market data (indicating solid-state battery adoption).

The median battery_capacity shifts by >25% from the training baseline.
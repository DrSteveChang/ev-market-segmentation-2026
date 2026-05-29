# ⚡ EV Market Strategic Segmentation 2026
**Full Curriculum Analytics Engine (OLS, SVM, RF, K-Means, PCA)**



## 📖 Project Overview
This repository contains a production-grade, end-to-end Machine Learning pipeline designed to address margin erosion in the 2026 Electric Vehicle (EV) market. Strictly adhering to the **CRISP-DM** framework, the system automatically ingests raw market data, executes a multi-paradigm mathematical modeling suite, and deploys an LLM-driven reporting engine to generate actionable business strategies and quantify financial risks in USD.

## 🏗️ Architecture & Core Modules
The pipeline is fully modularized, mapping directly to advanced machine learning curricula:

* **Data Engineering (`src/data_pipeline.py`)**
  * Automated data ingestion via the Kaggle API.
  * Matrix virtualization, cleaning, and preprocessing for multi-task downstream learning.
* **Supervised Classification (`src/models/classifiers.py`)**
  * **Algorithms:** Random Forest (Lab 2) & Support Vector Machines (Lab 3).
  * **Business Logic:** Implements an **Asymmetric Cost Matrix** to evaluate models based on *Expected Commercial Loss (USD)* rather than pure statistical accuracy, rigorously prioritizing financial risk minimization.
* **Unsupervised Clustering (`src/models/clustering.py`)**
  * **Algorithms:** K-Means Clustering & Principal Component Analysis (PCA) (Lab 4).
  * **Business Logic:** Identifies continuous market personas and applies PCA dimensionality reduction to visualize market fragmentation.
* **Financial Risk Regression (`src/models/linear_regression.py`)**
  * **Algorithms:** Ordinary Least Squares (OLS) (Lab 1).
  * **Business Logic:** Isolates significant causal factors to quantify brand equity premiums and supply chain cost penalties.
* **MLOps & Deployment (`src/deployment/`)**
  * `visualizer.py`: Generates presentation-ready static charts (Feature Importance, PCA Scatter, Confusion Matrices, OLS Risk Exposures).
  * `llm_reporter.py` (Lab 6): Interfaces with GPT models to seamlessly synthesize quantitative metrics into a formal, English-language strategic consulting report.

## 🚀 Execution Guide

### 1. Environment Setup
Ensure all dependencies are installed. Utilizing an isolated virtual environment is highly recommended.
```bash
python -m pip install -r requirements.txt
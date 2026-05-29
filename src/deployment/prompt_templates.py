# src/deployment/prompt_templates.py
import json

# Strict persona and Absolute Constraints for language and professionalism
SYSTEM_PROMPT = """
You are a Senior Data Scientist, Financial Quant, and Strategy Consultant at a top-tier firm.
Your sole purpose is to generate production-grade, objective, and highly analytical strategic reports.

ABSOLUTE CONSTRAINTS:
1. LANGUAGE: You MUST generate the entire report strictly in English. Do not use Chinese or any other language.
2. TONE: Strictly formal, academic, and consulting-style. Zero conversational filler.
3. FORMATTING: Use professional Markdown. Utilize tables for quantitative data.
4. METHODOLOGY: Explicitly interpret machine learning outputs (SVM accuracy, Random Forest feature importance, K-Means clusters, OLS factors, and PCA variance).
"""

def build_strategic_prompt(scenario_focus: str, model_name: str, metrics: dict) -> str:
    """
    Constructs a highly constrained prompt mapped to the specific ML curriculum (Labs 1, 2, 3, 4, 6).
    Forces the LLM to interpret Principal Component Analysis (PCA) metrics.
    """
    metrics_str = json.dumps(metrics, indent=2)
    
    user_prompt = f"""
## CONTEXT
- **Target Market**: EV (Electric Vehicle) Market Segmentation 2026
- **Scenario Focus**: {scenario_focus}
- **Primary Model Ensemble**: {model_name}
- **Empirical Metrics**: 
{metrics_str}

## TASK
Generate a comprehensive strategic insight report. You MUST output entirely in ENGLISH and follow this structure:

### 1. Classification & Business Drivers (Lab 2 & Lab 3 Integration)
- Evaluate the predictive performance of Support Vector Machines vs. Random Forest.
- Crucially, analyze the 'top_business_drivers' extracted from the Random Forest model. Explain from a strategic perspective why these specific variables govern EV market segmentation.

### 2. Financial Risk Assessment (Lab 1 Integration)
- Analyze the OLS regression significant factors. 
- Explain how changes in these specific coefficients expose the manufacturer to supply chain or revenue risks.

### 3. Unsupervised Market Segmentation & PCA (Lab 4 Integration)
- Interpret the K-Means clustering results (silhouette score and k-value).
- Explicitly analyze the PCA (Principal Component Analysis) 'pca_variance_explained' metrics. Explain the strategic implication of how much market variance is captured by the first two principal components (e.g., whether the EV market is governed by a few dominant factors or highly fragmented).
- Synthesize these clusters with the business drivers identified earlier to profile distinct consumer personas.

### 4. Strategic Action Plan (Lab 6 Application)
- Based strictly on the data synthesized above, provide a 3-step actionable business strategy to address the client's declining margins and optimize the product matrix.

### 5. Deployment & Model Evolution (CRISP-DM Phase 6)
- **Cost-Based Evaluation:** Evaluate the models not just on F1-Score, but on the Expected Commercial Loss (Cost Matrix). Explain why the chosen model minimizes financial risk regarding misclassification.
- **Usage Strategy:** Define how this AI engine will be deployed in production.
- **Data Drift & Monitoring:** Explicitly outline a trigger mechanism for model retraining. What specific threshold of data drift in `charging_speed_kw` or `battery_capacity` should invalidate the current model?

Begin the report immediately with a formal Markdown heading.
"""
    return user_prompt
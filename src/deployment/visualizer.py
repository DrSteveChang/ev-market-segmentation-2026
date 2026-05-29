# src/deployment/visualizer.py
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_business_charts(metrics: dict):
    """
    Generates production-grade static visualizations based on the model ensemble output.
    Applies strategic filtering to prevent chart clutter in executive presentations.
    Saves high-resolution PNG files to the local reports directory.
    """
    logging.info("Initiating automated chart generation sequence...")
    
    # Ensure the output directory exists
    output_dir = "data/processed/reports/charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure global styling for professional business presentation
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'figure.autolayout': True, 'font.size': 12})

    try:
        # 1. Feature Importance Chart (Random Forest)
        rf_drivers = metrics.get('classification', {}).get('random_forest', {}).get('top_business_drivers', {})
        if rf_drivers:
            df_rf = pd.DataFrame(list(rf_drivers.items()), columns=['Feature', 'Importance'])
            df_rf = df_rf.sort_values(by='Importance', ascending=False)
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Importance', y='Feature', data=df_rf, color="#2C3E50")
            plt.title("Top Strategic Market Drivers (Random Forest)", fontsize=14, weight='bold')
            plt.xlabel("Gini Importance Score")
            plt.ylabel("")
            
            rf_path = os.path.join(output_dir, "rf_feature_importance.png")
            plt.savefig(rf_path, dpi=300)
            plt.close()
            logging.info(f"Feature importance chart saved to: {rf_path}")

        # 2. Risk Exposure Chart (OLS Regression) - OPTIMIZED FOR PRESENTATION
        ols_factors = metrics.get('regression', {}).get('significant_factors', {})
        if ols_factors:
            factor_data = [{'Factor': k, 'Coefficient': v['coefficient']} for k, v in ols_factors.items()]
            df_ols = pd.DataFrame(factor_data)
            
            # --- Strategic Filtering Logic ---
            # Isolate the Top 10 highest premiums (positive impact)
            top_positive = df_ols[df_ols['Coefficient'] > 0].nlargest(10, 'Coefficient')
            # Isolate the Top 10 highest risks (negative impact)
            top_negative = df_ols[df_ols['Coefficient'] < 0].nsmallest(10, 'Coefficient')
            
            # Combine and sort for a clean, highly readable chart
            df_filtered = pd.concat([top_positive, top_negative]).sort_values(by='Coefficient', ascending=False)
            
            # Use a slightly taller figure for perfect label spacing
            plt.figure(figsize=(12, 10))
            
            # Differentiate positive (premium) and negative (risk) values visually
            colors = ["#27AE60" if val > 0 else "#C0392B" for val in df_filtered['Coefficient']]
            
            sns.barplot(
                x='Coefficient', 
                y='Factor', 
                data=df_filtered, 
                hue='Factor', 
                palette=colors, 
                legend=False
            )
            
            plt.title("Top 20 Financial Risk & Premium Exposures (OLS Coefficients)", fontsize=15, weight='bold')
            plt.xlabel("Impact on Vehicle Price (USD)", fontsize=12)
            plt.ylabel("")
            plt.axvline(0, color='black', linewidth=1.5) # Emphasize zero baseline
            
            ols_path = os.path.join(output_dir, "ols_risk_exposure.png")
            plt.savefig(ols_path, dpi=300)
            plt.close()
            logging.info(f"Risk exposure chart saved to: {ols_path}")

    except Exception as e:
        logging.error(f"Chart generation encountered an error: {e}")
# src/models/linear_regression.py
import logging
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from src.config import RANDOM_STATE

def train_ridge_regression(X_train, y_train):
    """Trains a Ridge Regression model to mitigate multicollinearity risks."""
    logging.info("Optimizing Ridge Regression model...")
    ridge = Ridge(random_state=RANDOM_STATE)
    param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}
    
    grid_search = GridSearchCV(
        estimator=ridge, param_grid=param_grid, cv=5, n_jobs=-1, scoring='neg_mean_squared_error'
    )
    grid_search.fit(X_train, y_train)
    
    logging.info(f"Optimal Ridge Parameters: {grid_search.best_params_}")
    return grid_search.best_estimator_

# src/models/linear_regression.py
import statsmodels.api as sm
# ... other imports and model training logic ...

def execute_risk_factor_regression(X_reg, y_reg):
    # Add constant for OLS regression
    X_reg = sm.add_constant(X_reg)
    model = sm.OLS(y_reg, X_reg).fit()
    
    # Extract significant factors (p-value < 0.05)
    p_values = model.pvalues
    coefficients = model.params
    
    significant_factors = {}
    for feature in p_values.index:
        if feature != 'const' and p_values[feature] < 0.05:
            significant_factors[feature] = {
                "coefficient": float(coefficients[feature]),
                "p_value": float(p_values[feature])
            }
            
    # Return structured dictionary matching the blueprint
    return {
        "model": "Ordinary Least Squares (OLS)",
        "r_squared": float(model.rsquared),
        "significant_factors": significant_factors
    }
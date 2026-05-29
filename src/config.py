# src/config.py

# ==========================================
# DATA & FILE SETTINGS
# ==========================================
DATASET_NAME = "patelris/electric-vehicle-market-and-pricing-dataset-2026"
FILE_NAME = "ev_market_2026.csv"

# ==========================================
# MACHINE LEARNING PARAMETERS
# ==========================================
RANDOM_STATE = 42
TEST_SIZE = 0.25

# Features used for predictive modeling
FEATURES = [
    'battery_capacity_kwh', 
    'range_miles', 
    'horsepower', 
    'charging_speed_kw'
]

# Target variables for dual-scenario execution
TARGET_REGRESSION = 'price_usd'
TARGET_CLASSIFICATION = 'market_segment'

# ==========================================
# HYPERPARAMETER GRIDS (GridSearchCV)
# ==========================================
RF_PARAM_GRID = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}

SVM_PARAM_GRID = {
    'C': [0.1, 1, 10],
    'gamma': ['scale', 'auto'],
    'kernel': ['rbf', 'linear']
}
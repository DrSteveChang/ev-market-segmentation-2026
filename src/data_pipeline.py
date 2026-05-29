# src/data_pipeline.py
import os
import glob
import shutil
import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler
import kagglehub

def fetch_data() -> pd.DataFrame:
    """
    Automated data ingestion pipeline.
    Downloads the dataset via Kaggle API, persists a copy into the local 'data/' 
    directory for project consistency, and loads it into memory.
    """
    logging.info("Initiating Kaggle API dataset download...")
    
    # 1. Download via Kagglehub using your exact dataset ID
    dataset_id = "patelris/electric-vehicle-market-and-pricing-dataset-2026"
    
    try:
        cache_path = kagglehub.dataset_download(dataset_id)
        logging.info(f"Dataset successfully downloaded to system cache: {cache_path}")
    except Exception as e:
        logging.error(f"Kaggle API download failed. Please check your network or Kaggle credentials: {e}")
        raise

    # 2. Locate the target CSV file within the downloaded cache directory
    csv_files_in_cache = glob.glob(os.path.join(cache_path, "*.csv"))
    if not csv_files_in_cache:
        logging.error("No CSV file found in the downloaded Kaggle dataset.")
        raise FileNotFoundError("Missing CSV in Kaggle cache.")
        
    source_file = csv_files_in_cache[0]
    file_name = os.path.basename(source_file)
    
    # 3. Persist the file into the project's 'data/' directory
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True) # Safely create 'data/' if it doesn't exist
    destination_file = os.path.join(data_dir, file_name)
    
    # Copy the file from cache to our project folder
    shutil.copy2(source_file, destination_file)
    logging.info(f"Dataset securely copied to project workspace: {destination_file}")
    
    # 4. Load the DataFrame and return to the main pipeline
    df = pd.read_csv(destination_file)
    logging.info(f"Successfully loaded data into memory. Matrix shape: {df.shape}")
    
    return df


def preprocess_for_modeling(df: pd.DataFrame):
    """
    Cleans raw data and features an intelligent target-variable sniffer.
    Automatically identifies target columns for Classification and Regression 
    based on business semantics and data types to prevent hardcoding.
    """
    # 1. Base Data Cleaning: Drop rows with missing values to ensure matrix integrity
    df = df.dropna().copy()
    
    # 2. Intelligent Target Variable Detection (Semantic Sniffing)
    target_class_col = None
    target_numeric_col = None
    
    # Define semantic keyword dictionaries for target identification
    classification_keywords = ['segment', 'class', 'category', 'risk', 'label', 'type', 'group']
    regression_keywords = ['price', 'cost', 'score', 'revenue', 'margin', 'sales', 'value', 'amount']
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Sniff for classification targets (Discrete categorical variables)
        if any(keyword in col_lower for keyword in classification_keywords):
            # Ensure the cardinality is low enough to be a classification target (e.g., < 20 unique labels)
            if df[col].nunique() < 20:
                target_class_col = col
                
        # Sniff for regression targets (Continuous numeric variables)
        elif any(keyword in col_lower for keyword in regression_keywords):
            # Ensure the column's data type is strictly numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                target_numeric_col = col

    # Fallback Mechanism: If semantic keywords fail, extract based purely on column data types
    if not target_class_col:
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        target_class_col = cat_cols[-1] if len(cat_cols) > 0 else df.columns[-1]
        
    if not target_numeric_col:
        num_cols = df.select_dtypes(include=['number']).columns
        # Exclude the classification column if it happens to be numerically encoded
        num_cols = [c for c in num_cols if c != target_class_col]
        target_numeric_col = num_cols[-1] if len(num_cols) > 0 else df.columns[-2]

    logging.info(f"[Auto-Detect] Classification Target locked to: '{target_class_col}'")
    logging.info(f"[Auto-Detect] Regression Target locked to: '{target_numeric_col}'")

    # 3. Target Extraction and Matrix Splitting
    y_clf = df[target_class_col]
    y_reg = df[target_numeric_col]
    
    # Drop the identified targets from the main feature matrix to prevent data leakage
    df_features = df.drop(columns=[target_class_col, target_numeric_col], errors='ignore')
    
    # Apply One-Hot Encoding to the remaining categorical features
    X_raw = pd.get_dummies(df_features, drop_first=True)

    # 4. Feature Standardization
    # Essential mathematical prerequisite for SVM, K-Means, and Ridge/Lasso Regression
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X_raw.columns)

    # 5. Pipeline Matrix Generation
    # Isolate matrices for specific modeling paradigms
    X_clf = X_scaled_df
    X_cluster = X_scaled_df  # Unsupervised learning requires no target vector (y)
    X_reg = X_scaled_df

    # Strictly return the 5 required structures for the main orchestrator
    return X_clf, y_clf, X_cluster, X_reg, y_reg
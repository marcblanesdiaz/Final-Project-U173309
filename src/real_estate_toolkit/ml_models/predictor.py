from typing import List, Dict, Any
# Modules you can use (not all are mandatory):
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)
import polars as pl  # Polars should be used for data handling.


class HousePricePredictor:
    def __init__(self, train_data_path: str, test_data_path: str):
        """
        Initialize the predictor class with paths to the training and testing datasets.
        
        Args:
            train_data_path (str): Path to the training dataset CSV file.
            test_data_path (str): Path to the testing dataset CSV file.
        
        Attributes to Initialize:
            - self.train_data: Polars DataFrame for the training dataset.
            - self.test_data: Polars DataFrame for the testing dataset.
        """
        self.train_data = pl.read_csv("train.csv")
        self.test_data = pl.read_csv("test.csv")
    
    def clean_data(self):
        """
        Perform comprehensive data cleaning on the training and testing datasets.
        
        Tasks:
        1. Handle Missing Values:
            - Use a strategy for each column: drop, fill with mean/median/mode, or create a separate category.
        2. Ensure Correct Data Types:
            - Convert numeric columns to float/int.
            - Convert categorical columns to string.
        3. Drop Unnecessary Columns:
            - Identify and remove columns with too many missing values or irrelevant information.
        
        Tips:
            - Use Polars for data manipulation.
            - Implement a flexible design to allow column-specific cleaning strategies.
        """
    
    def prepare_features(self, target_column: str = 'SalePrice', selected_predictors: List[str] = None):
        """
        Prepare the dataset for machine learning by separating features and the target variable, 
        and preprocessing them for training and testing.

        Args:
            target_column (str): Name of the target variable column. Default is 'SalePrice'.
            selected_predictors (List[str]): Specific columns to use as predictors. 
                                            If None, use all columns except the target.

        Tasks:
        1. Separate Features and Target:
            - Split the dataset into predictors (`X`) and target variable (`y`).
            - Use `selected_predictors` if provided; otherwise, use all columns except the target.
        2. Split Numeric and Categorical Features:
            - Identify numeric and categorical columns.
        3. Create a Preprocessing Pipeline:
            - Numeric Data: Impute missing values with the mean and standard scale the features.
            - Categorical Data: Impute missing values with a new category and apply one-hot encoding.
            - Use `ColumnTransformer` to combine both pipelines.
        4. Split Data:
            - Split the data into training and testing sets using `train_test_split`.

        Returns:
            - X_train, X_test, y_train, y_test: Training and testing sets.
        """

    def train_baseline_models(self) -> Dict[str, Dict[str, float]]:
        """
        Train and evaluate baseline machine learning models for house price prediction.
        
        Models:
        1. Linear Regression
        2. Choose One Advanced Model:
            - RandomForestRegressor
            - GradientBoostingRegressor

        Tasks:
        1. Create a Pipeline for Each Model:
            - Combine preprocessing and the estimator into a single pipeline.
        2. Train Models:
            - Train each model on the training set.
        3. Evaluate Models:
            - Use metrics: Mean Squared Error (MSE), Mean Absolute Error (MAE), R-squared (R²), 
            and Mean Absolute Percentage Error (MAPE).
            - Compute metrics on both training and test sets for comparison.
        4. Summarize Results:
            - Return a dictionary of model names and their evaluation metrics and the model itself.

        Returns:
            A dictionary structured like:
                {
                    "Linear Regression": 
                        { 
                            "metrics": {"MSE": ..., "R2": ..., "MAE": ..., "MAPE": ...},
                            "model": (model object)
                        },
                    "Advanced Model":
                        { 
                            "metrics": {"MSE": ..., "R2": ..., "MAE": ..., "MAPE": ...},
                            "model": (model object)
                        }
                }
        """
    
    def forecast_sales_price(self, model_type: str = 'LinearRegression'):
        """
        Use the trained model to forecast house prices on the test dataset.
        
        Args:
            model_type (str): Type of model to use for forecasting. Default is 'LinearRegression'. Other option is 'Advanced'.
        
        Tasks:
            1. Select the Desired Model:
                - Ensure the model type is trained and available.
            2. Generate Predictions:
                - Use the selected model to predict house prices for the test set.
            3. Create a Submission File:
                - Save predictions in the required format:
                    - A CSV with columns: "Id" (from test data) and "SalePrice" (predictions).
                - Example:
                    
                    Id,SalePrice
                    1461,200000
                    1462,175000
                
            4. Save the File:
                - Name the file `submission.csv` and save it in the `src/real_estate_toolkit/ml_models/outputs/` folder.

        Tips:
            - Ensure preprocessing steps are applied to the test data before making predictions.
        """
from typing import List, Dict
import polars as pl
import plotly.express as px
import plotly.graph_objects as go


class MarketAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data from a CSV file.
        
        Args:
            data_path (str): Path to the Ames Housing dataset
        """
        self.real_state_data = pl.read_csv(data_path)
        self.real_state_clean_data = None
    
    def clean_data(self) -> None:
        """
        Perform comprehensive data cleaning:
        
        Tasks to implement:
        1. Identify and handle missing values
            - Decide strategy for each column (drop, fill with mean/median, no change)
        2. Convert columns to appropriate data types if needed.
            - Ensure numeric columns are numeric
            - Ensure categorical columns are categorized
        
        Returns:
            Cleaned and preprocessed dataset assigned to self.real_state_clean_data
        """
    
    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        """
        Analyze sale price distribution using clean data.
        
        Tasks to implement:
        1. Compute basic price statistics and generate another data frame called price_statistics:
            - Mean
            - Median
            - Standard deviation
            - Minimum and maximum prices
        2. Create an interactive histogram of sale prices using Plotly.
            
        Returns:
            - Statistical insights dataframe
            - Save Plotly figures for price distribution in src/real_estate_toolkit/analytics/outputs/ folder.
        """
       #We use polar to compute basic statistics and use ".alias" to name the statistics.
        price_stats = self.real_state_clean_data.select(
            pl.col("SalePrice").mean().alias("mean"),
            pl.col("SalePrice").median().alias("median"),
            pl.col("SalePrice").std().alias("std_dev"),
            pl.col("SalePrice").min().alias("min"),
            pl.col("SalePrice").max().alias("max")
        )

        # Create histogram with the packages imported above
        fig = px.histogram(
            self.real_state_clean_data.to_pandas(),
            x="SalePrice",
            title="Sale Price Distribution",
            labels={"SalePrice": "Sale Price"},
            nbins=50
    


    def neighborhood_price_comparison(self) -> pl.DataFrame:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        
        Tasks to implement:
        1. Group data by neighborhood
        2. Calculate price statistics for each neighborhood
        3. Create Plotly boxplot with:
            - Median prices
            - Price spread
            - Outliers
        
        Returns:
            - Return neighborhood statistics dataframe
            - Save Plotly figures for neighborhood price comparison in src/real_estate_toolkit/analytics/outputs/ folder.
        """
    
    def feature_correlation_heatmap(self, variables: List[str]) -> None:
        """
        Generate a correlation heatmap for variables input.
        
        Tasks to implement:
        1. Pass a list of numerical variables
        2. Compute correlation matrix and plot it
        
        Args:
            variables (Lis[str]): List of variables to correlate
        
        Returns:
            Save Plotly figures for correlation heatmap in src/real_estate_toolkit/analytics/outputs/ folder.
        """
    
    def create_scatter_plots(self) -> Dict[str, go.Figure]:
        """
        Create scatter plots exploring relationships between key features.
        
        Scatter plots to create:
        1. House price vs. Total square footage
        2. Sale price vs. Year built
        3. Overall quality vs. Sale price
        
        Tasks to implement:
        - Use Plotly Express for creating scatter plots
        - Add trend lines
        - Include hover information
        - Color-code points based on a categorical variable
        - Save them in in src/real_estate_toolkit/analytics/outputs/ folder.
        
        Returns:
            Dictionary of Plotly Figure objects for different scatter plots. 
        """
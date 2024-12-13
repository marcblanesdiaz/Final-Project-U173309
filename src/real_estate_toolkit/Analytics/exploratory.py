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
        self.real_state_data = pl.read_csv(data_path, infer_schema_length=10000)
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
        # We identify and handle missing values we use "fill_null" and determine "mean" as the best strategy (0 would create bias)
        self.real_state_clean_data = self.real_state_data.fill_null(strategy = "mean")

        #We want to convert columns to appropriate data types, that is, numeric columns being numeric and categorical being categorical
        numeric_cols = [col for col in self.real_state_clean_data.columns if self.real_state_clean_data[col].dtype in [pl.Int64, pl.Float64]]
        
        #We create a loop to convert integers to floats
        for col in numeric_cols:
                self.real_state_clean_data = self.real_state_clean_data.with_columns(
                    self.real_state_clean_data[col].cast(pl.Float64)
                )

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
         # Compute basic statistics using polar package
        price_stats = self.real_state_clean_data.select(
            pl.col("SalePrice").mean().alias("mean"),
            pl.col("SalePrice").median().alias("median"),
            pl.col("SalePrice").std().alias("std_dev"),
            pl.col("SalePrice").min().alias("min"),
            pl.col("SalePrice").max().alias("max")
        )

        # Create histogram using packaged imported and create a output with the image (using best practices naming)
        fig = px.histogram(
            self.real_state_clean_data.to_pandas(),
            x="SalePrice",
            title="Sale Price Distribution",
            labels={"SalePrice": "Frequenci"},
            nbins=50
        )
        fig.write_image("real_estate_toolkit/analytics/outputs/sale_price_distribution.png")
       
        return price_stats

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
        # First we group by neighborhood and calculate statistics
        neighborhood_stats = self.real_state_clean_data.group_by("Neighborhood").agg(
            [
                pl.col("SalePrice").median().alias("median_price"),
                pl.col("SalePrice").mean().alias("mean_price"),
                pl.col("SalePrice").std().alias("price_std_dev")
            ]
        )

        # Create boxplot
        fig = px.box(
            self.real_state_clean_data.to_pandas(),
            x="Neighborhood",
            y="SalePrice",
            title="Neighborhood Price Comparison",
            labels={"Neighborhood": "Neighborhood", "SalePrice": "Sale Price"}
        )
        fig.update_xaxes(tickangle=45)
        fig.write_image("real_estate_toolkit/analytics/outputs/price_comparison_by_neighborhood.png")

        return neighborhood_stats

    
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
        # Compute correlation matrix only with numerical varaibles
        numeric_cols = [col for col in self.real_state_clean_data.columns if self.real_state_clean_data[col].dtype in [pl.Int64, pl.Float64]]

        variables = [var for var in variables if var in numeric_cols]
        
        correlation_matrix = self.real_state_clean_data.select(variables).to_pandas().corr()

        # Create heatmap
        fig = px.imshow(
            correlation_matrix,
            title="Feature Correlation Heatmap",
            labels=dict(color="Correlation"),
            x=variables,
            y=variables
        )
        fig.write_image("real_estate_toolkit/analytics/outputs/feature_correlation_heatmap.png")




    
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
        scatter_plots = {}

        # We are creating a scatter plot comparing house price and total square footage
        scatter_plots["price_vs_sqft"] = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="GrLivArea",
            y="SalePrice",
            title="Sale Price vs. Total Square Footage",
            trendline="ols",
            labels={"GrLivArea": "Total Square Footage", "SalePrice": "Sale Price"}
        )
        scatter_plots["price_vs_sqft"].write_image("real_estate_toolkit/analytics/outputs/price_vs_sqft.png")

        # We are creating a scatter plot comparing Sale price and Year built
        scatter_plots["price_vs_year_built"] = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="YearBuilt",
            y="SalePrice",
            title="Sale Price vs. Year Built",
            trendline="ols",
            labels={"YearBuilt": "Year Built", "SalePrice": "Sale Price"}
        )
        scatter_plots["price_vs_year_built"].write_image("real_estate_toolkit/analytics/outputs/price_vs_year_built.png")

        # We are creating a scatter plot comparing Overall quality and Sale price
        scatter_plots["quality_vs_price"] = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="OverallQual",
            y="SalePrice",
            title="Overall Quality vs. Sale Price",
            trendline="ols",
            labels={"OverallQual": "Overall Quality", "SalePrice": "Sale Price"}
        )
        scatter_plots["quality_vs_price"].write_image("real_estate_toolkit/analytics/outputs/quality_vs_price.png")

        return scatter_plots


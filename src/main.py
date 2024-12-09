"Main module for running tests"
from pathlib import Path
from typing import List, Dict, Any
import polars as pl
import plotly.graph_objects as go

from real_estate_toolkit.data.loader import DataLoader
from real_estate_toolkit.data.cleaner import Cleaner
from real_estate_toolkit.data.descriptor import Descriptor, DescriptorNumpy
#from real_estate_toolkit.agent_based_model.houses import House, QualityScore
#from real_estate_toolkit.agent_based_model.house_market import HousingMarket
#from real_estate_toolkit.agent_based_model.consumers import Consumer, Segment
#from real_estate_toolkit.agent_based_model.simulation import (
#3#    Simulation, 
#   CleaningMarketMechanism, 
   # AnnualIncomeStatistics,
   # ChildrenRange
#)
#from real_estate_toolkit.analytics.exploratory import MarketAnalyzer
#from real_estate_toolkit.ml_models.predictor import HousePricePredictor

def is_valid_snake_case(string: str) -> bool:
    """
    Check if a given string is in valid snake_case.
    
    Snake case is a naming convention where:
    - The string is all lowercase
    - Words are separated by underscores
    - The string doesn't start or end with an underscore
    - The string doesn't contain double underscore
    """
    if not string:
        # If the string is empty, it's not valid snake case
        return False
    if not all(
        # Check that each character is a lowercase letter, digit, or underscore
        char.islower() or char.isdigit() or char == '_' for char in string
    ):
        return False
    if string.startswith('_') or string.endswith('_'):
        # If the string starts or ends with an underscore, it's not valid snake case
        return False
    if '__' in string:
        # If the string contains double underscore, it's not valid snake case
        return False
    # If all checks pass, the string is valid snake case
    return True

def test_data_loading_and_cleaning():
    """Test data loading and cleaning functionality"""
    # Test data loading
    data_path = Path("files/train.csv")
    loader = DataLoader(data_path)
    # Test column validation
    required_columns = ["Id", "SalePrice", "LotArea", "YearBuilt", "BedroomAbvGr"]
    assert loader.validate_columns(required_columns), "Required columns missing from dataset"
    # Load and test data format
    data = loader.load_data_from_csv()
    assert isinstance(data, list), "Data should be returned as a list"
    assert all(isinstance(row, dict) for row in data), "Each row should be a dictionary"
    # Test data cleaning
    cleaner = Cleaner(data)
    cleaner.rename_with_best_practices()
    cleaned_data = cleaner.na_to_none()
    # Verify cleaning results
    assert all(is_valid_snake_case(key) for key in cleaned_data[0].keys()), "Column names should be in snake_case"
    assert all(val is None or isinstance(val, (str, int, float)) for row in cleaned_data for val in row.values()), \
        "Values should be None or basic types"
    return cleaned_data

def test_descriptive_statistics(cleaned_data: List[Dict[str, Any]]):
    """Test descriptive statistics functionality"""
    descriptor = Descriptor(cleaned_data)
    descriptor_numpy = DescriptorNumpy(cleaned_data)
    # Test none ratio calculation
    none_ratios = descriptor.none_ratio()
    none_ratios_numpy = descriptor_numpy.none_ratio()
    assert isinstance(none_ratios, dict), "None ratios should be returned as dictionary"
    assert set(none_ratios.keys()) == set(none_ratios_numpy.keys()), "Both implementations should handle same columns"
    # Test numeric calculations
    numeric_columns = ["sale_price", "lot_area"]  # Assuming these are the cleaned names
    averages = descriptor.average(numeric_columns)
    medians = descriptor.median(numeric_columns)
    percentiles = descriptor.percentile(numeric_columns, 75)
    # Test numpy implementation
    averages_numpy = descriptor_numpy.average(numeric_columns)
    medians_numpy = descriptor_numpy.median(numeric_columns)
    percentiles_numpy = descriptor_numpy.percentile(numeric_columns, 75)
    # Compare results
    for col in numeric_columns:
        assert abs(averages[col] - averages_numpy[col]) < 1e-6, f"Average calculations differ for {col}"
        assert abs(medians[col] - medians_numpy[col]) < 1e-6, f"Median calculations differ for {col}"
        assert abs(percentiles[col] - percentiles_numpy[col]) < 1e-6, f"Percentile calculations differ for {col}"
    # Test type and mode
    type_modes = descriptor.type_and_mode()
    type_modes_numpy = descriptor_numpy.type_and_mode()
    assert set(type_modes.keys()) == set(type_modes_numpy.keys()), "Both implementations should handle same columns"
    return numeric_columns

def test_house_functionality():
    """Test House class implementation"""
    house = House(
        id=1,
        price=200000.0,
        area=2000.0,
        bedrooms=3,
        year_built=2010,
        quality_score=QualityScore.GOOD,
        available=True
    )
    # Test basic calculations
    price_per_sqft = house.calculate_price_per_square_foot()
    assert isinstance(price_per_sqft, float), "Price per square foot should be float"
    assert price_per_sqft == 100.0, "Incorrect price per square foot calculation"
    # Test new construction logic
    assert house.is_new_construction(2024) is False, "House should not be considered new construction"
    assert house.is_new_construction(2012) is True, "House should be considered new construction"
    # Test quality score generation
    house.quality_score = None
    house.get_quality_score()
    assert house.quality_score is not None, "Quality score should be generated"
    # Test house sale
    house.sell_house()
    assert house.available is False, "House should be marked as unavailable after sale"
    return house

def test_market_functionality(cleaned_data: List[Dict[str, Any]]):
    """Test HousingMarket class implementation"""
    houses: List[House] = []
    for idx, data in enumerate(cleaned_data):
        quality_score = QualityScore(max(1, min(5, int(data['overall_qual']) // 2)))
        house = House(
            id=idx,
            price=float(data['sale_price']),
            area=float(data['gr_liv_area']),
            bedrooms=int(data['bedroom_abv_gr']),
            year_built=int(data['year_built']),
            quality_score=quality_score,
            available=True
        )
        houses.append(house)
    # Create market with single house
    market = HousingMarket(houses)
    # Test house retrieval
    retrieved_house = market.get_house_by_id(1)
    assert isinstance(retrieved_house, House), "Check if retrieved a house"
    # Test average price calculation
    avg_price = market.calculate_average_price(bedrooms=3)
    assert abs(avg_price - 181056.87064676618) < 1e-6, "Incorrect average price calculation"
    # Test requirements filtering
    matching_houses = market.get_houses_that_meet_requirements(
        max_price=250000,
        segment=Segment.AVERAGE
    )
    assert isinstance(matching_houses, list), "Should return list of matching houses"
    assert len(matching_houses) > 0, "Should find at least one matching house"
    return market

def main():
    """Main function to run all tests"""
    try:
        # Run all tests sequentially
        cleaned_data = test_data_loading_and_cleaning()
        test_descriptive_statistics(cleaned_data)
        test_house_functionality()
        market = test_market_functionality(cleaned_data)
        #test_consumer_functionality(market)
        #test_simulation(cleaned_data)
        #test_market_analyzer()
        #test_house_price_predictor()
        print("All tests passed successfully!")
        return 0
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return 2

if __name__ == "__main__":
    main()
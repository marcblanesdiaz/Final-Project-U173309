from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    dataset: List[Dict[str, Any]]
    
    def rename_with_best_practices(self) -> None:
        """Rename the columns with best practices (e.g. snake_case very descriptive name)."""
        column_mapping = {
            "MSSubClass": "main_structure_sub_classification",
            "MSZoning": "main_structure_zoning",
            "LotFrontage": "lot_frontage",
            "LotArea": "lot_area",
            "Street": "street",
            "Alley": "alley",
            "LotShape": "lot_shape",
            "LandContour": "land_contour",
            "Utilities": "utilities",
            "LotConfig": "lot_configuration",
            "LandSlope": "land_slope",
            "Neighborhood": "neighborhood",
            "Condition1": "condition_1",
            "Condition2": "condition_2",
            "BldgType": "building_type",
            "HouseStyle": "house_style",
            "OverallQual": "overall_quality",
            "OverallCond": "overall_condition",
            "YearBuilt": "year_built",
            "YearRemodAdd": "year_remodelation_date",
            "RoofStyle": "roof_style",
            "RoofMatl": "roof_material",
            "Exterior1st": "exterior_first",
            "Exterior2nd": "exterior_second",
            "MasVnrType": "masonry_veneer_type",
            "MasVnrArea": "masonry_veneer_area",
            "ExterQual": "exterior_quality",
            "ExterCond": "exterior_condition",
            "Foundation": "foundation",
            "BsmtExposure": "basement_exposure",
            "BsmtFinType1": "basement_finished_type_1",
            "BsmtFinSF1": "basement_finished_square_feet_1",
            "BsmtFinType2": "basement_finished_type_2",
            "BsmtFinSF2": "basement_finished_square_feet_2",
            "BsmtUnfSF": "basement_unfinished_square_feet",
            "TotalBsmtSF": "total_basement_square_feet",
            "Heating": "heating",
            "HeatingQC": "heating_quality_and_condition",
            "CentralAir": "central_air",
            "Electrical": "electrical",
            "1stFlrSF": "first_floor_square_feet",
            "2ndFlrSF": "second_floor_square_feet",
            "LowQualFinSF": "low_quality_finished_square_feet",
            "GrLivArea": "ground_living_area",
            "BsmtFullBath": "basement_full_bathrooms",
            "BsmtHalfBath": "basement_half_bathrooms",
            "FullBath": "full_bathrooms",
            "HalfBath": "half_bathrooms",
            "Bedroom": "bedroom",
            "Kitchen": "kitchen",
            "KitchenQual": "kitchen_quality",
            "TotRmsAbvGrd": "total_rooms_above_grade",
            "Functional": "functional",
            "Fireplaces": "fireplaces",
            "FireplaceQu": "fireplace_quality",
            "GarageType": "garage_type",
            "GarageYrBlt": "garage_year_built",
            "GarageFinish": "garage_finish",
            "GarageCars": "garage_cars",
            "GarageArea": "garage_area",
            "GarageQual": "garage_quality",
            "GarageCond": "garage_condition",
            "PavedDrive": "paved_driveway",
            "WoodDeckSF": "wood_deck_square_feet",
            "OpenPorchSF": "open_porch_square_feet",
            "EnclosedPorch": "enclosed_porch",
            "3SsnPorch": "three_season_porch",
            "ScreenPorch": "screen_porch",
            "PoolArea": "pool_area",
            "PoolQC": "pool_quality",
            "Fence": "fence",
            "MiscFeature": "miscellaneous_feature",
            "MiscVal": "miscellaneous_value",
            "MoSold": "month_sold",
            "YrSold": "year_sold",
            "SaleType": "sale_type",
            "SaleCondition": "sale_condition"
        }
        
        self.dataset = self.dataset.rename(column_mapping)

    def na_to_none(self) -> List[Dict[str, Any]]:
        """Replace NA to None in all values with NA in the dictionary."""
        for row in self.dataset:
            for key, value in row.items():
                if value == "NA":
                    row [key] = None
        
        return self.dataset

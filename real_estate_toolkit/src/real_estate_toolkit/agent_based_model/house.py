from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict

class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore]
    available: bool = True
    
    def calculate_price_per_square_foot(self) -> float:
        """
        Calculate and return the price per square foot.
        
        Implementation tips:
        - Divide price by area
        - Round to 2 decimal places
        - Handle edge cases (e.g., area = 0)
        """
        if self.area <= 0:
            raise ValueError("Area must be greater than zero to calculate price per square foot")
        else:
            price_per_square_foot = round(self.price / self.area, 2)
        
        return price_per_square_foot

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if house is considered new construction (< 5 years old).
        
        Implementation tips:
        - Compare current_year with year_built
        - Consider edge cases for very old houses
        """
        return (current_year - self.year_built < 5)
        
    def get_quality_score(self) -> None:
        """
        Generate a quality score based on house attributes.
        
        Implementation tips:
        - Consider multiple factors (age, size, bedrooms)
        - Create meaningful score categories
        - Handle missing quality_score values
        """




    def sell_house(self) -> None:
        """
        Mark house as sold.
        
        Implementation tips:
        - Update available status 
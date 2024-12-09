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
        
        elif self.price <= 0:
            raise ValueError("Price cannot be lower or equal to zero to calculate price per square foot")

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
        if self.year_built > current_year:
            raise Exception("Year built cannot be greater than current year")
        
        return (current_year - self.year_built < 5)
    
        
    def get_quality_score(self) -> None:
        """
        Generate a quality score based on house attributes.
        
        Implementation tips:
        - Consider multiple factors (age, size, bedrooms)
        - Create meaningful score categories
        - Handle missing quality_score values
        """
        if self.quality_score is not None: 
            return self.quality_score
        
        
        current_year = 2024
        age_score = max(5 - (current_year - self.year_built) // 10, 1) #higher score for newest houses
        size_score = min(self.area // 500, 5) # bigger houses score higher with a maximum of 5 points
        bedroom_score = min(self.bedrooms, 5) #more bedrooms with a maximum of 5 points

        overall_score = round((age_score + size_score + bedroom_score) / 3)

        if overall_score >= 5:
            self.quality_score = QualityScore.EXCELLENT
        elif overall_score >= 4:
            self.quality_score = QualityScore.GOOD
        elif overall_score >= 3:
            self.quality_score = QualityScore.AVERAGE
        elif overall_score >= 2:
            self.quality_score = QualityScore.FAIR
        else:
            self.quality_score = QualityScore.POOR
            

    def sell_house(self) -> None:
        """
        Mark house as sold.
        
        Implementation tips:
        - Update available status"""
        
        if self.available:
            self.available = False
            print(f"House with ID {self.id} has been marked as sold.")
        else:
            raise Exception(f"House with ID {self.id} is already sold.")
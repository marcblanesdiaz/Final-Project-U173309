from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List, Dict
from .house import House, QualityScore
from .house_market import HousingMarket

class Segment(Enum):
    FANCY = auto() # House is new construction and house score is the highest
    OPTIMIZER = auto() # Price per square foot is less than monthly salary
    AVERAGE = auto() # House price is below the average housing market price

@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House]
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    
    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time.
        
        Implementation tips:
        - Use compound interest formula
        - Consider annual calculations
        - Account for saving_rate
        """
        annual_savings = self.annual_income * self.saving_rate
        total_savings = self.savings

        for year in range(years):
            total_savings += annual_savings
            total_savings *= (1 + self.interest_rate)
        
        self.savings = round(total_savings, 2)


    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house.
        
        Implementation tips:
        - Check savings against house prices
        - Consider down payment requirements
        - Match house to family size needs
        - Apply segment-specific preferences
        """
        available_houses = [house for house in housing_market.houses if house.available]

        # Filter by family size (number of bedrooms needed)
        suitable_houses = [
            house for house in available_houses if house.bedrooms >= self.children_number + 1
        ]


        #TODO: Añadir filtro max price

        # Apply segment-specific preferences
        if self.segment == Segment.FANCY:
            suitable_houses = [
                house for house in suitable_houses
                if house.is_new_construction() and house.quality_score == QualityScore.EXCELLENT
            ]
        elif self.segment == Segment.OPTIMIZER:
            suitable_houses = [
                house for house in suitable_houses
                if house.calculate_price_per_square_foot() <= (self.annual_income / 12)
            ]
        elif self.segment == Segment.AVERAGE:
            average_price = housing_market.calculate_average_price()
            suitable_houses = [
                house for house in suitable_houses if house.price <= average_price
            ]


        if not suitable_houses:
            raise Exception(f"Consumer {self.id}: No houses match segment preferences.")



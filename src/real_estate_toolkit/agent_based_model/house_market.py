from typing import List, Optional
from .houses import House, QualityScore
from numpy import mean

class HousingMarket:
    def __init__(self, houses: List[House]):
        self.houses: List[House] = houses
    
    def get_house_by_id(self, house_id: int) -> House:
        """
        Retrieve specific house by ID.
        
        Implementation tips:
        - Use efficient search method
        - Handle non-existent IDs
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        
        raise Exception(f"No house found with ID {house_id}.")

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate average house price, optionally filtered by bedrooms.
        
        Implementation tips:
        - Handle empty lists
        - Consider using statistics module
        - Implement bedroom filtering efficiently
        """
        if bedrooms is not None:
            filtered_houses = [house.price for house in self.houses if house.bedrooms == bedrooms and house.available]
        else:
            filtered_houses = [house.price for house in self.houses if house.available]
        
        if not filtered_houses:
            raise Exception("No houses match the criteria for calculating the average price.")
        
        return mean(filtered_houses)
    
    def get_houses_that_meet_requirements(self, max_price: int, segment: str) -> Optional[List[House]]:
        """
        Filter houses based on buyer requirements.
        
        Implementation tips:
        - Consider multiple filtering criteria
        - Implement efficient filtering
        - Handle case when no houses match
        """
        from .consumers import Segment
        matching_houses = []

        for house in self.houses:
            if not house.available or house.price > max_price:
                continue
            
            if segment == Segment.FANCY:
                if house.is_new_construction() and house.quality_score == QualityScore.EXCELLENT:
                    matching_houses.append(house)
            elif segment == Segment.OPTIMIZER:
                price_per_sqft = house.calculate_price_per_square_foot()
                if price_per_sqft <= max_price / house.area:
                    matching_houses.append(house)
            elif segment == Segment.AVERAGE:
                if house.price < self.calculate_average_price():
                    matching_houses.append(house)

        if len(matching_houses) == 0:
            raise Exception(f"No houses found that meet the requirements for segment {segment} with max price {max_price}.")

        return matching_houses
from typing import List, Dict, Optional
from .house import House

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
            else: 
                print(f"No house found with ID {house_id}.")

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
            print("No houses match the criteria for calculating the average price.")
            return 0.0
        
        return round(mean(filtered_houses), 2)
    
    def get_houses_that_meet_requirements(self, max_price: int, segment: str) -> Optional[List[House]]:
        """
        Filter houses based on buyer requirements.
        
        Implementation tips:
        - Consider multiple filtering criteria
        - Implement efficient filtering
        - Handle case when no houses match
        """
        matching_houses = []

        for house in self.houses:
            if not house.available or house.price > max_price:
                continue
            
            if segment == "FANCY":
                if house.is_new_construction() and house.quality_score == "EXCELLENT":
                    matching_houses.append(house)
            elif segment == "OPTIMIZER":
                price_per_sqft = house.calculate_price_per_square_foot()
                if price_per_sqft <= max_price / house.area:
                    matching_houses.append(house)
            elif segment == "AVERAGE":
                matching_houses.append(house)

        if not matching_houses:
            print(f"No houses found that meet the requirements for segment {segment} with max price {max_price}.")
            return None

        return matching_houses
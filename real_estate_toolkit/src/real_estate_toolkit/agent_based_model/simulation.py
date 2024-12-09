from enum import Enum, auto
from dataclasses import dataclass
from random import gauss, randint
from typing import Optional, List, Dict
from .house import House
from .house_market import HousingMarket
from .consumers import Segment, Consumer

class CleaningMarketMechanism(Enum):
    INCOME_ORDER_DESCENDANT = auto()
    INCOME_ORDER_ASCENDANT = auto()
    RANDOM = auto()

@dataclass
class AnnualIncomeStatistics:
    minimum: float
    average: float
    standard_deviation: float
    maximum: float

@dataclass
class ChildrenRange:
    minimum: float = 0
    maximum: float = 5

@dataclass
class Simulation:
    housing_market_data: List[Dict[str, Any]]
    consumers_number: int
    years: int
    annual_income: AnnualIncomeStatistics
    children_range: ChildrenRange
    cleaning_market_mechanism: CleaningMarketMechanism
    down_payment_percentage: float = 0.2
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    
    def create_housing_market(self):
        """
        Initialize market with houses.
        
        Implementation tips:
        - Convert raw data to House objects
        - Validate input data
        - Use a for loop for create the List[Consumers] object needed to use the housing market.
        - Assign self.housing_market to the class.
        """
        self.housing_market = HousingMarket([
            House(
                id=house_data['id'],
                price=house_data['price'],
                area=house_data['area'],
                bedrooms=house_data['bedrooms'],
                year_built=house_data['year_built'],
                quality_score=house_data['quality_score'],
                available=house_data.get('available', True)
            )
            for house_data in self.housing_market_data
        ])

    def create_consumers(self) -> None:
        """
        Generate consumer population.

        Implementation instructions:
        1. Create a list of consumers with length equal to consumers_number. Make it a property of the class simulation (self.consumers = ...).
        2. Assign a randomly generated annual income using a normal distribution (gauss from random) truncated by maximum and minimum (while value > maximum or value < min sample again) considering AnnualIncomeStatistics
        3. Assign a randomly generated children number using a random integer generator (randint from random)
        4. Assign randomly a segment (Segment value from consumer). All segments have the same probability of being assigned.
        5. Assign the simulation saving rate (simulated economy saving rate).
        
        Implementation tips:
        - Use provided statistical distributions
        - Ensure realistic attribute values
        - Assign segments appropriately
        """

    
    def compute_consumers_savings(self) -> None:
        """
        Calculate savings for all consumers.
        
        Implementation tips:
        - Apply saving rate consistently to all consumers.
        - Handle edge cases
        """

    def clean_the_market(self) -> None:
        """
        Execute market transactions.
        
        Implementation tips:
        - Use buy_a_house function for each consumer
        - Implement ordering mechanisms (CleaningMarketMechanism)
        - Track successful purchases
        - Handle market clearing
        """
    
    def compute_owners_population_rate(self) -> float:
        """
        Compute the owners population rate after the market is clean. 
        
        Implementation tips:
        - Total consumers who bought a house over total consumers number
        """
    
    def compute_houses_availability_rate(self) -> float:
        """
        Compute the houses availability rate after the market is clean. 
        
        Implementation tips:
        - Houses available over total houses number
        """
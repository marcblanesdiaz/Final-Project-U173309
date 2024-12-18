from enum import Enum, auto
from dataclasses import dataclass
from random import gauss, randint, shuffle
from typing import List, Dict, Any
from .houses import House
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
                price=house_data['sale_price'],
                area=house_data['lot_area'],
                bedrooms=house_data['bedroom_abv_gr'],
                year_built=house_data['year_built'],
                quality_score=house_data["overall_qual"]
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

        self.consumers: List[Consumer] = []
        for consumer_idx in range(self.consumers_number):
            while True:
                income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
                if self.annual_income.minimum <= income <= self.annual_income.maximum:
                    break
            
            children = randint(self.children_range.minimum, self.children_range.maximum)

            segment = Segment(randint(1, len(Segment)))
        
            self.consumers.append(
                Consumer(
                    id = consumer_idx,
                    annual_income = income, 
                    children_number = children, 
                    segment = segment,
                    house = None,
                    savings = 0,
                    saving_rate = self.saving_rate,
                    interest_rate = self.interest_rate
                )
            )
    
    def compute_consumers_savings(self) -> None:
        """
        Calculate savings for all consumers.
        
        Implementation tips:
        - Apply saving rate consistently to all consumers.
        - Handle edge cases
        """
        for consumer in self.consumers:
            consumer.compute_savings(self.years)

    def clean_the_market(self) -> None:
        """
        Execute market transactions.
        
        Implementation tips:
        - Use buy_a_house function for each consumer
        - Implement ordering mechanisms (CleaningMarketMechanism)
        - Track successful purchases
        - Handle market clearing
        """

        if self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_DESCENDANT:
            self.consumers.sort(key=lambda consumer: consumer.annual_income, reverse=True)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_ASCENDANT:
            self.consumers.sort(key=lambda consumer: consumer.annual_income)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.RANDOM:
            shuffle(self.consumers)

        for consumer in self.consumers:
            try:
                consumer.buy_a_house(self.housing_market)
            except:
                break


    def compute_owners_population_rate(self) -> float:
        """
        Compute the owners population rate after the market is clean. 
        
        Implementation tips:
        - Total consumers who bought a house over total consumers number
        """
        owners = sum(1 for consumer in self.consumers if consumer.house is not None)
        return round(owners / self.consumers_number, 2)
    
    def compute_houses_availability_rate(self) -> float:
        """
        Compute the houses availability rate after the market is clean. 
        
        Implementation tips:
        - Houses available over total houses number
        """
        available_houses = sum(1 for house in self.housing_market.houses if house.available)
        total_houses = len(self.housing_market.houses)
        return round(available_houses / total_houses, 2)


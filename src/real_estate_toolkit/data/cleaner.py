from dataclasses import dataclass
from typing import Dict, List, Union, Any
import re

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]
    
    def rename_with_best_practices(self) -> None:
        """Rename the columns with best practices (e.g. snake_case very descriptive name)."""
    
        def to_snake_case(name: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z])', r'\1_\2', name)
            return s1.lower()

        self.data = [
            {f"{to_snake_case(key)}":value for key, value in row.items()}
            for row in self.data
        ]


    def na_to_none(self) -> List[Dict[str, Any]]:
        """Replace NA to None in all values with NA in the dictionary."""
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row [key] = None
        
        return self.data

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union, Any
import polars as pl

@dataclass
class DataLoader:
    """Class for loading and basic processing of real estate data."""
    data_path: Path
    
    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        """Load data from CSV file into a list of dictionaries."""
        try:
            df = pl.read_csv(self.data_path, infer_schema_length=10000)
            data_as_dicts = df.to_dicts()

            return data_as_dicts
        
        except Exception as e:
            raise RuntimeError(f"Error loading CSV: {e}")
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """Validate that all required columns are present in the dataset."""

        dataset = self.load_data_from_csv()
        existing_columns = dataset[0].keys()

        return all(column in existing_columns for column in required_columns)

    


from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Union
import numpy as np
import statistics
import math

@dataclass
class Descriptor:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: List[str] = "all"):
        """Compute the ratio of None value per column.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as the ratio.
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        else: 
            for column in columns:
                if column not in self.data[0]:
                    raise Exception("Invalid column")


        none_ratios = {}
        for col in columns:
            total = len(self.data)
            none_count = sum(1 for row in self.data if row[col] is None)
            none_ratios[col] = none_count / total if total > 0 else 0
        return none_ratios
    
    
    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        """Compute the average value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the average
        """
        if columns == "all":
            columns = [column for column in self.data[0] if isinstance(self.data[0][column], (int, float))]
            if len(columns) != len(self.data[0].keys()):
                raise Exception("Some columns does not correspond to numeric variables")
        else:
            for column in columns:
                if column not in self.data[0]:
                    raise Exception("Invalid column")
            if len(columns) != len([column for column in columns if isinstance(self.data[0][column], (int, float))]):
                raise Exception("Some columns does not correspond to numeric variables")


        result = {}
        for col in columns:
            values = [row[col] for row in self.data if row[col] is not None]
            result[col] = statistics.mean(values) if values else None

        return result



    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        """Compute the median value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the average
        """
        if columns == "all":
            columns = [column for column in self.data[0] if isinstance(self.data[0][column], (int, float))]
            if len(columns) != len(self.data[0].keys()):
                raise Exception("Some columns does not correspond to numeric variables")
        else:
            for column in columns:
                if column not in self.data[0]:
                    raise Exception("Invalid column")
            if len(columns) != len([column for column in columns if isinstance(self.data[0][column], (int, float))]):
                raise Exception("Some columns does not correspond to numeric variables")


        result = {}
        for col in columns:
            values = [row[col] for row in self.data if row[col] is not None]
            result[col] = statistics.median(values) if values else None

        return result


    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        """Compute the percentile value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the average
        """
        if columns == "all":
            columns = [column for column in self.data[0] if isinstance(self.data[0][column], (int, float))]
            if len(columns) != len(self.data[0].keys()):
                raise Exception("Some columns does not correspond to numeric variables")
        else:
            for column in columns:
                if column not in self.data[0]:
                    raise Exception("Invalid column")
            if len(columns) != len([column for column in columns if isinstance(self.data[0][column], (int, float))]):
                raise Exception("Some columns does not correspond to numeric variables")

        result = {}
        for col in columns:
            values = sorted([row[col] for row in self.data if row[col] is not None])
            if values:
                index = math.ceil(percentile / 100 * len(values))
                result[col] = values[index]
            else:
                result[col] = None

        return result

    
    def type_and_mode(self, columns: List[str] = "all") -> Dict[str, Union[Tuple[str, float], Tuple[str, str]]]:
        """Compute the mode for variables. Omit None values.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as a tuple of the variable type and the mode.
        If the variable is categorical
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        else: 
            for column in columns:
                if column not in self.data[0]:
                    raise Exception("Invalid column")

        result = {}
        for col in columns:
            values = [row[col] for row in self.data if row[col] is not None]

            if not values:
                result[col] = ("Unknown", None)
                continue
            
            if isinstance(values[0], (int, float)):
                result[col] = ("Numeric", statistics.mode(values))
            else:
                result[col] = ("Categorical", statistics.mode(values))
            
        
        return result
    

@dataclass
class DescriptorNumpy: 
    data: List[Dict[str, Any]]

    def _post_init_(self):
        keys = list(self.data[0].keys())
        dtype = [(key, '0') for key in keys()]
        structured_data = [tuple(row.get(key, None) for key in keys) for row in self.data]
        self.array = np.array(structured_data, dtype=type)

    def none_ratio(self, columns: List[str] = "all") -> Dict[str, np.float64]:
        if columns == "all":
            columns = self.array.dtypes.names
        else:
            self.data(columns)

        none_ratios = {}
        total_rows = len(self.array)
        for col in columns:
            none_count = np.sum(self.array[col] == None)
            none_ratios[col] = none_count / total_rows if total_rows > 0 else np.float64(0)
        return none_ratios

    def average(self, columns: List[str] = "all") -> Dict[str, np.float64]:
        """Compute the average value for numeric variables."""
        if columns == "all":
            columns = [col for col in self.array.dtype.names if np.issubdtype(self.array[col].dtype, np.number)]
        else:
            self.data(columns)
            columns = [col for col in columns if np.issubdtype(self.array[col].dtype, np.number)]

        if not columns:
            raise ValueError("No numeric columns specified.")
        
        averages = {}
        for col in columns:
            values = self.array[col][self.array[col] != None]
            averages[col] = np.mean(values) if len(values) > 0 else np.nan
        return averages

    def median(self, columns: List[str] = "all") -> Dict[str, np.float64]:
        """Compute the median value for numeric variables."""
        if columns == "all":
            columns = [col for col in self.array.dtype.names if np.issubdtype(self.array[col].dtype, np.number)]
        else:
            self.data(columns)
            columns = [col for col in columns if np.issubdtype(self.array[col].dtype, np.number)]

        if not columns:
            raise ValueError("No numeric columns specified.")
        
        medians = {}
        for col in columns:
            values = self.array[col][self.array[col] != None]
            medians[col] = np.median(values) if len(values) > 0 else np.nan
        return medians

    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, np.float64]:
        """Compute a specific percentile for numeric variables."""
        if columns == "all":
            columns = [col for col in self.array.dtype.names if np.issubdtype(self.array[col].dtype, np.number)]
        else:
            self.data(columns)
            columns = [col for col in columns if np.issubdtype(self.array[col].dtype, np.number)]

        if not columns:
            raise ValueError("No numeric columns specified.")

        percentiles = {}
        for col in columns:
            values = self.array[col][self.array[col] != None] 
            percentiles[col] = np.percentile(values, percentile) if len(values) > 0 else np.nan
        return percentiles

    def type_and_mode(self, columns: List[str] = "all") -> Dict[str, Tuple[str, Any]]:
        """Compute the mode and type for variables."""
        if columns == "all":
            columns = self.array.dtype.names
        else:
            self.data(columns)

        type_and_modes = {}
        for col in columns:
            values = self.array[col][self.array[col] != None]  
            if len(values) == 0:
                type_and_modes[col] = ("unknown", None)
                continue

            variable_type = str(self.array[col].dtype)
            most_common = np.unique(values, return_counts=True)
            mode = most_common[0][np.argmax(most_common[1])]
            type_and_modes[col] = (variable_type, mode)
        return type_and_modes
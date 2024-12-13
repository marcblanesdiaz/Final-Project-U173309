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
    
        percentiles = {}
        for col in columns:
            values = sorted([row[col] for row in self.data if row[col] is not None])
            n = len(values)
            if n == 1:
                percentiles[col] = float(values[0])
                continue
            i = (percentile / 100.0) * (n - 1)
            lower = int(i)
            upper = lower + 1
    
            if upper >= n:
                p_value = float(values[-1])
            else:
                fraction = i - lower
                p_value = float(values[lower] + fraction * (values[upper] - values[lower]))
            percentiles[col] = p_value
        return percentiles

    
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
 
    def __post_init__(self):
        # Asumimos que todas las filas tienen las mismas claves
        # Si no fuera el caso, habría que normalizar.
        keys = list(self.data[0].keys())
        # Creación de un dtype basado en objetos para flexibilidad
        # Esto permite que las columnas tengan valores mixtos (None, str, float, etc.)
        dtype = [(key, object) for key in keys]
        # Construimos una lista de tuplas con el orden de las keys
        structured_data = [
            tuple(row.get(key, None) for key in keys) 
            for row in self.data
        ]
 
        # Creamos el array estructurado
        self.array = np.array(structured_data, dtype=dtype)
 
    def _filter_columns(self, columns: Union[List[str], str]) -> List[str]:
        """Filtra las columnas según el parámetro columns y verifica su existencia."""
        if columns == "all":
            return list(self.array.dtype.names)
        else:
            # Filtramos las columnas que existen en el array
            valid_columns = [col for col in columns if col in self.array.dtype.names]
            if not valid_columns:
                raise ValueError("No se encontraron columnas válidas.")
            return valid_columns
 
    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Calcula la proporción de valores None en las columnas seleccionadas."""
        columns = self._filter_columns(columns)
        none_ratios = {}
        total_rows = len(self.array)
        if total_rows == 0:
            return {col: 0.0 for col in columns}
 
        for col in columns:
            col_data = self.array[col]
            # Contamos cuantos None hay
            none_count = np.sum(col_data == None)
            none_ratios[col] = none_count / total_rows
        return none_ratios
 
    def _get_numeric_columns(self, columns: List[str]) -> List[str]:
        """Devuelve sólo las columnas numéricas de la lista proporcionada."""
        numeric_cols = []
        for col in columns:
            # Intentamos convertir la columna a float ignorando None
            col_data = self.array[col]
            # Filtramos None
            filtered = [x for x in col_data if x is not None]
            if not filtered:
                # Columna vacía después de filtrar None
                continue
            # Probamos conversión a float
            try:
                _ = np.array(filtered, dtype=float)
                numeric_cols.append(col)
            except ValueError:
                # Si no se puede convertir a numérico, ignoramos esta columna
                pass
        return numeric_cols
 
    def average(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Computa el valor promedio para columnas numéricas."""
        all_cols = self._filter_columns(columns)
        numeric_cols = self._get_numeric_columns(all_cols)
 
        if not numeric_cols:
            raise ValueError("No se especificaron columnas numéricas válidas.")
        averages = {}
        for col in numeric_cols:
            col_data = self.array[col]
            filtered = [x for x in col_data if x is not None]
            if len(filtered) > 0:
                filtered_arr = np.array(filtered, dtype=float)
                averages[col] = float(np.mean(filtered_arr))
            else:
                averages[col] = np.nan
        return averages
 
    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Computa la mediana para columnas numéricas."""
        all_cols = self._filter_columns(columns)
        numeric_cols = self._get_numeric_columns(all_cols)
 
        if not numeric_cols:
            raise ValueError("No se especificaron columnas numéricas válidas.")
        medians = {}
        for col in numeric_cols:
            col_data = self.array[col]
            filtered = [x for x in col_data if x is not None]
            if filtered:
                filtered_arr = np.array(filtered, dtype=float)
                medians[col] = float(np.median(filtered_arr))
            else:
                medians[col] = np.nan
        return medians
 
    def percentile(self, columns: Union[List[str], str] = "all", percentile: float = 50.0) -> Dict[str, float]:
        """Computa un percentil específico para columnas numéricas."""
        all_cols = self._filter_columns(columns)
        numeric_cols = self._get_numeric_columns(all_cols)
 
        if not numeric_cols:
            raise ValueError("No se especificaron columnas numéricas válidas.")
        percentiles = {}
        for col in numeric_cols:
            col_data = self.array[col]
            filtered = [x for x in col_data if x is not None]
            if filtered:
                filtered_arr = np.array(filtered, dtype=float)
                percentiles[col] = float(np.percentile(filtered_arr, percentile))
            else:
                percentiles[col] = np.nan
        return percentiles
 
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Any]]:
        """Determina el tipo y la moda para las columnas."""
        columns = self._filter_columns(columns)
        type_and_modes = {}
        for col in columns:
            col_data = self.array[col]
            filtered = [x for x in col_data if x is not None]
 
            # Determinamos el tipo predominante mirando el dtype del array estructurado.
            # Como es object, el tipo no está claro. Intentamos inferir del primer valor filtrado.
            if not filtered:
                # Sin datos
                type_and_modes[col] = ("unknown", None)
                continue
            # Inferir tipo:
            sample = filtered[0]
            var_type = type(sample).__name__
 
            # Moda:
            unique_vals, counts = np.unique(filtered, return_counts=True)
            mode = unique_vals[np.argmax(counts)]
            type_and_modes[col] = (var_type, mode)
        return type_and_modes
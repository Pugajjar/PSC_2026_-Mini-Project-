import numpy as np
import pandas as pd

class DataAnalyzer:
    @staticmethod
    def calculate_column_stats(df, column):
        """
        Calculates basic statistical metrics for a numerical column using NumPy.
        Handles missing values by removing them from the calculation.
        """
        if df is None or column not in df.columns:
            return None
        
        # Extract series and drop NaNs
        clean_series = df[column].dropna()
        if clean_series.empty:
            return None
        
        # Convert to NumPy array
        arr = clean_series.to_numpy()
        
        # Calculate using NumPy functions
        stats = {
            "Mean": float(np.mean(arr)),
            "Median": float(np.median(arr)),
            "Minimum": float(np.min(arr)),
            "Maximum": float(np.max(arr)),
            "Std Dev": float(np.std(arr)),
            "Count": int(len(arr)),
            "Sum": float(np.sum(arr))
        }
        return stats

    @staticmethod
    def generate_describe_summary(df):
        """
        Generates summary statistics for all numerical columns using Pandas describe().
        """
        if df is None:
            return None
        
        # Only select numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return None
        
        summary_df = numeric_df.describe()
        return summary_df

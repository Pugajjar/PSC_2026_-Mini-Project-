import pandas as pd
import numpy as np

class DataManager:
    def __init__(self):
        self.df = None
        self.file_name = ""
        self.numeric_cols = []
        self.text_cols = []
        self.date_cols = []

    def load_csv(self, file_path):
        """Loads a CSV file into a Pandas DataFrame and parses columns."""
        try:
            # Load CSV, let pandas handle basic parsing
            self.df = pd.read_csv(file_path)
            # Normalize column names by stripping trailing/leading whitespaces
            self.df.columns = [col.strip() for col in self.df.columns]
            # Store filename
            import os
            self.file_name = os.path.basename(file_path)
            # Detect columns
            self._classify_columns()
            return True, "Loaded successfully"
        except Exception as e:
            self.df = None
            self.file_name = ""
            self.numeric_cols = []
            self.text_cols = []
            self.date_cols = []
            return False, str(e)

    def clear(self):
        """Resets the state of the data manager."""
        self.df = None
        self.file_name = ""
        self.numeric_cols = []
        self.text_cols = []
        self.date_cols = []

    def _classify_columns(self):
        """Dynamically classifies columns into Numeric, Date, or Text/Categorical."""
        self.numeric_cols = []
        self.text_cols = []
        self.date_cols = []

        if self.df is None:
            return

        for col in self.df.columns:
            series = self.df[col]
            
            # 1. Check if numeric
            if pd.api.types.is_numeric_dtype(series):
                # Ensure it's not all NaNs
                self.numeric_cols.append(col)
                continue

            # 2. Check if date-like (not numeric, try to parse)
            # We try parsing. If at least 70% of non-null values parse as datetime, we treat it as Date.
            non_null_series = series.dropna()
            if len(non_null_series) > 0:
                try:
                    # pd.to_datetime can be slow on large text, so we parse with errors='coerce'
                    parsed = pd.to_datetime(non_null_series, errors='coerce')
                    valid_date_count = parsed.notna().sum()
                    if valid_date_count / len(non_null_series) >= 0.7:
                        self.date_cols.append(col)
                        continue
                except Exception:
                    pass

            # 3. Otherwise, treat as Text/Categorical
            self.text_cols.append(col)

    def get_summary_info(self):
        """Returns basic summary metrics about the dataset."""
        if self.df is None:
            return {
                "rows": 0, "cols": 0, "numeric_count": 0, 
                "text_count": 0, "date_count": 0, 
                "missing": 0, "duplicates": 0
            }
        
        rows, cols = self.df.shape
        missing_count = self.df.isna().sum().sum()
        duplicate_count = self.df.duplicated().sum()

        return {
            "rows": rows,
            "cols": cols,
            "numeric_count": len(self.numeric_cols),
            "text_count": len(self.text_cols),
            "date_count": len(self.date_cols),
            "missing": int(missing_count),
            "duplicates": int(duplicate_count)
        }

    def get_preview_data(self, limit=100):
        """Returns a list of column names, and a list of lists containing the preview rows."""
        if self.df is None:
            return [], []
        
        cols = list(self.df.columns)
        # Limit rows to first N and convert NaN to empty string for clean display
        preview_df = self.df.head(limit).replace({np.nan: ''})
        rows = preview_df.values.tolist()
        return cols, rows

    def get_column_quality(self):
        """Returns missing value count per column, plus duplicates."""
        if self.df is None:
            return {}, 0
        
        missing = self.df.isna().sum().to_dict()
        duplicates = self.df.duplicated().sum()
        return missing, int(duplicates)

    def search_data(self, column, search_value):
        """
        Searches the dataset for a value in a specific column.
        Returns a Pandas DataFrame of matching rows.
        """
        if self.df is None or column not in self.df.columns:
            return pd.DataFrame()

        series = self.df[column]
        search_str = str(search_value).strip().lower()

        if search_str == "":
            return self.df.copy()

        # If it's a numeric column
        if column in self.numeric_cols:
            try:
                val = float(search_value)
                return self.df[series == val]
            except ValueError:
                # If they entered non-numeric, fallback to string matching
                pass

        # String matching (case-insensitive contains)
        return self.df[series.astype(str).str.lower().str.contains(search_str, na=False)]

    def filter_data(self, column, operator, value):
        """
        Filters the dataset by applying a condition on a column.
        operator: '>', '<', '==', '>=', '<=', 'contains'
        Returns a Pandas DataFrame of filtered rows.
        """
        if self.df is None or column not in self.df.columns:
            return pd.DataFrame()

        series = self.df[column]

        # For numeric column
        if column in self.numeric_cols:
            try:
                val = float(value)
            except ValueError:
                raise ValueError("Filter value must be numerical for a numeric column.")

            if operator == '>':
                return self.df[series > val]
            elif operator == '<':
                return self.df[series < val]
            elif operator == '==':
                return self.df[series == val]
            elif operator == '>=':
                return self.df[series >= val]
            elif operator == '<=':
                return self.df[series <= val]
            else:
                raise ValueError(f"Operator {operator} not supported for numeric columns.")
        
        # For non-numeric column (Text/Date)
        else:
            val_str = str(value).lower()
            if operator == '==':
                return self.df[series.astype(str).str.lower() == val_str]
            elif operator == 'contains':
                return self.df[series.astype(str).str.lower().str.contains(val_str, na=False)]
            elif operator in ['>', '<', '>=', '<=']:
                # Support lexicographical / string date comparisons
                return self.df[self._apply_lexicographical_filter(series, operator, val_str)]
            else:
                raise ValueError(f"Operator {operator} not supported for text columns.")

    def _apply_lexicographical_filter(self, series, operator, value):
        """Helper for string inequality filtering (useful for Date strings)."""
        s_str = series.astype(str).str.lower()
        if operator == '>':
            return s_str > value
        elif operator == '<':
            return s_str < value
        elif operator == '>=':
            return s_str >= value
        elif operator == '<=':
            return s_str <= value
        return pd.Series(False, index=series.index)

    def sort_data(self, column, ascending=True):
        """
        Sorts the dataset by the given column.
        Modifies self.df in-place or returns a copy?
        For a prototype, we modify in-place or sort the view?
        Let's modify in-place or return the sorted DataFrame to display.
        The prompt says: "Display the sorted dataset. For the FIRST PROTOTYPE, Pandas sorting is acceptable."
        Let's perform the sort in-place so that subsequent analyses, plots, etc., 
        reflect the sorted order, or allow sorting as an operation.
        Let's modify self.df in-place and return the sorted dataframe.
        """
        if self.df is None or column not in self.df.columns:
            return pd.DataFrame()
        
        # In-place sort
        self.df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)
        return self.df

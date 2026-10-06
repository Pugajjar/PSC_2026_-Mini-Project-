import matplotlib
matplotlib.use("TkAgg")  # Ensure we use TkAgg backend for Tkinter integration
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

class DataVisualizer:
    @staticmethod
    def _create_clean_figure():
        """Creates a Figure and an axes with styling applied."""
        # Use a modern, clean figure style
        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        # Apply style adjustments
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cccccc')
        ax.spines['bottom'].set_color('#cccccc')
        ax.tick_params(colors='#555555')
        return fig, ax

    @staticmethod
    def plot_line(df, x_col, y_col, title=None):
        """Generates a line plot of X vs Y."""
        fig, ax = DataVisualizer._create_clean_figure()
        
        # Sort values by x_col if it contains dates/categories to make the line continuous
        temp_df = df[[x_col, y_col]].dropna().copy()
        # Try sorting if x_col is sortable
        try:
            temp_df = temp_df.sort_values(by=x_col)
        except Exception:
            pass

        ax.plot(temp_df[x_col].astype(str), temp_df[y_col], marker='o', color='#1f77b4', linewidth=2, markersize=5)
        
        ax.set_xlabel(x_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_ylabel(y_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_title(title or f"{y_col} vs {x_col} (Line Graph)", fontsize=12, fontweight='bold', color='#222222', pad=15)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Rotate x labels if there are many labels
        if len(temp_df) > 5:
            fig.autofmt_xdate(rotation=45, ha='right')

        fig.tight_layout()
        return fig

    @staticmethod
    def plot_bar(df, x_col, y_col, title=None):
        """Generates a bar plot. If there are duplicates in X, aggregates using sum."""
        fig, ax = DataVisualizer._create_clean_figure()
        
        temp_df = df[[x_col, y_col]].dropna().copy()
        
        # Aggregate by x_col to sum y_col if there are duplicate category records
        try:
            temp_df = temp_df.groupby(x_col)[y_col].sum().reset_index()
        except Exception:
            pass
            
        ax.bar(temp_df[x_col].astype(str), temp_df[y_col], color='#2ca02c', edgecolor='#1e751e', alpha=0.85)
        
        ax.set_xlabel(x_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_ylabel(f"Sum of {y_col}" if len(df) > len(temp_df) else y_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_title(title or f"{y_col} by {x_col} (Bar Graph)", fontsize=12, fontweight='bold', color='#222222', pad=15)
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)

        # Rotate labels
        if len(temp_df) > 5:
            fig.autofmt_xdate(rotation=45, ha='right')

        fig.tight_layout()
        return fig

    @staticmethod
    def plot_scatter(df, x_col, y_col, title=None):
        """Generates a scatter plot of X vs Y."""
        fig, ax = DataVisualizer._create_clean_figure()
        
        temp_df = df[[x_col, y_col]].dropna().copy()
        
        ax.scatter(temp_df[x_col], temp_df[y_col], color='#d62728', alpha=0.7, edgecolors='none', s=40)
        
        ax.set_xlabel(x_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_ylabel(y_col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_title(title or f"{y_col} vs {x_col} (Scatter Plot)", fontsize=12, fontweight='bold', color='#222222', pad=15)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        fig.tight_layout()
        return fig

    @staticmethod
    def plot_histogram(df, col, bins=10, title=None):
        """Generates a histogram plot for a single numerical column."""
        fig, ax = DataVisualizer._create_clean_figure()
        
        clean_series = df[col].dropna()
        
        ax.hist(clean_series, bins=bins, color='#9467bd', edgecolor='#6d4b8c', alpha=0.8)
        
        ax.set_xlabel(col, fontsize=10, fontweight='bold', color='#333333')
        ax.set_ylabel("Frequency", fontsize=10, fontweight='bold', color='#333333')
        ax.set_title(title or f"Distribution of {col} (Histogram)", fontsize=12, fontweight='bold', color='#222222', pad=15)
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)
        
        fig.tight_layout()
        return fig

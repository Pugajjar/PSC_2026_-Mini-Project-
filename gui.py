import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np

# Import our modules
from data_manager import DataManager
from analyzer import DataAnalyzer
from visualizer import DataVisualizer
from report_generator import ReportGenerator

# Matplotlib integration
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class ScientificDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Data Analyzer & Visualizer")
        self.root.geometry("700x550")
        self.root.minsize(650, 500)
        
        # Color palette & styling config
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', foreground='#333333', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=1)
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50', background='#f5f5f5')
        self.style.configure('Title.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#34495e', background='#f5f5f5')
        self.style.configure('Status.TLabel', font=('Segoe UI', 9), background='#e0e0e0', foreground='#333333')
        
        # Instantiate model components
        self.data_manager = DataManager()
        
        # UI components list for enabling/disabling
        self.action_buttons = []
        
        self._build_ui()
        self.set_status("Ready. Load a CSV dataset to begin.")
        self.update_ui_state()

    def _build_ui(self):
        # Main background container
        self.main_container = ttk.Frame(self.root, padding="15")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # ----------------------------------------------------
        # 1. HEADER SECTION
        # ----------------------------------------------------
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_lbl = ttk.Label(header_frame, text="Scientific Data Analyzer & Visualizer", style="Header.TLabel")
        title_lbl.pack(anchor=tk.W)
        
        desc_lbl = ttk.Label(header_frame, text="Welcome to Scientific Data Analyzer & Visualizer. Load a CSV dataset to begin.", font=('Segoe UI', 9, 'italic'))
        desc_lbl.pack(anchor=tk.W, pady=(2, 0))

        # ----------------------------------------------------
        # 2. FILE CONTROLS SECTION
        # ----------------------------------------------------
        file_frame = ttk.LabelFrame(self.main_container, text=" File Access Control ", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_load = ttk.Button(file_frame, text="Load CSV Dataset", command=self.load_dataset)
        btn_load.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_clear = ttk.Button(file_frame, text="Clear Dataset", command=self.clear_dataset)
        btn_clear.pack(side=tk.LEFT)
        
        self.lbl_loaded_file = ttk.Label(file_frame, text="Dataset: No file loaded", font=('Segoe UI', 10, 'bold'), foreground='#c0392b')
        self.lbl_loaded_file.pack(side=tk.RIGHT, padx=10)

        # ----------------------------------------------------
        # 3. DATASET INFORMATION SECTION
        # ----------------------------------------------------
        info_frame = ttk.LabelFrame(self.main_container, text=" Dataset Information Dashboard ", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create a grid for displaying stats
        info_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        ttk.Label(info_frame, text="Total Rows:", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lbl_rows = ttk.Label(info_frame, text="--")
        self.lbl_rows.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Total Columns:", style="Title.TLabel").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.lbl_cols = ttk.Label(info_frame, text="--")
        self.lbl_cols.grid(row=0, column=3, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Numerical Columns:", style="Title.TLabel").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.lbl_numeric = ttk.Label(info_frame, text="--")
        self.lbl_numeric.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Text/Categorical:", style="Title.TLabel").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.lbl_text = ttk.Label(info_frame, text="--")
        self.lbl_text.grid(row=1, column=3, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Date Columns:", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.lbl_date = ttk.Label(info_frame, text="--")
        self.lbl_date.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Missing Values:", style="Title.TLabel").grid(row=2, column=2, sticky=tk.W, pady=2)
        self.lbl_missing = ttk.Label(info_frame, text="--")
        self.lbl_missing.grid(row=2, column=3, sticky=tk.W, pady=2)

        ttk.Label(info_frame, text="Duplicate Rows:", style="Title.TLabel").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.lbl_duplicates = ttk.Label(info_frame, text="--")
        self.lbl_duplicates.grid(row=3, column=1, sticky=tk.W, pady=2)

        # ----------------------------------------------------
        # 4. ACTION PANEL
        # ----------------------------------------------------
        actions_frame = ttk.LabelFrame(self.main_container, text=" Analysis & Operations Panel ", padding="15")
        actions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        actions_frame.columnconfigure((0, 1), weight=1)
        actions_frame.rowconfigure((0, 1, 2, 3), weight=1)
        
        # Grid buttons
        self.btn_view = ttk.Button(actions_frame, text="Preview Dataset (View)", command=self.open_view_window)
        self.btn_view.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_view)
        
        self.btn_summary = ttk.Button(actions_frame, text="Dataset Summary (Describe)", command=self.open_summary_window)
        self.btn_summary.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_summary)
        
        self.btn_analyze = ttk.Button(actions_frame, text="Single Column Analysis", command=self.open_analyze_window)
        self.btn_analyze.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_analyze)
        
        self.btn_search = ttk.Button(actions_frame, text="Search Dataset", command=self.open_search_window)
        self.btn_search.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_search)
        
        self.btn_filter = ttk.Button(actions_frame, text="Filter Dataset", command=self.open_filter_window)
        self.btn_filter.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_filter)
        
        self.btn_sort = ttk.Button(actions_frame, text="Sort Dataset", command=self.open_sort_window)
        self.btn_sort.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_sort)
        
        self.btn_visualize = ttk.Button(actions_frame, text="Data Visualization", command=self.open_visualize_window)
        self.btn_visualize.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_visualize)
        
        self.btn_report = ttk.Button(actions_frame, text="Generate Text Report", command=self.generate_report)
        self.btn_report.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.action_buttons.append(self.btn_report)

        # ----------------------------------------------------
        # 5. STATUS BAR
        # ----------------------------------------------------
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W, style="Status.TLabel", padding=(5, 3))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------
    def set_status(self, text):
        self.status_bar.config(text=f" STATUS: {text}")
        self.root.update_idletasks()

    def update_ui_state(self):
        """Disables action buttons if no CSV is loaded."""
        if self.data_manager.df is None:
            # Disable
            for btn in self.action_buttons:
                btn.config(state='disabled')
            self.lbl_loaded_file.config(text="Dataset: No file loaded", foreground='#c0392b')
            
            # Reset indicators
            self.lbl_rows.config(text="--")
            self.lbl_cols.config(text="--")
            self.lbl_numeric.config(text="--")
            self.lbl_text.config(text="--")
            self.lbl_date.config(text="--")
            self.lbl_missing.config(text="--")
            self.lbl_duplicates.config(text="--")
        else:
            # Enable
            for btn in self.action_buttons:
                btn.config(state='normal')
            self.lbl_loaded_file.config(text=f"Dataset: {self.data_manager.file_name}", foreground='#27ae60')
            
            # Update info
            info = self.data_manager.get_summary_info()
            self.lbl_rows.config(text=str(info["rows"]))
            self.lbl_cols.config(text=str(info["cols"]))
            self.lbl_numeric.config(text=str(info["numeric_count"]))
            self.lbl_text.config(text=str(info["text_count"]))
            self.lbl_date.config(text=str(info["date_count"]))
            self.lbl_missing.config(text=str(info["missing"]))
            self.lbl_duplicates.config(text=str(info["duplicates"]))

    # --------------------------------------------------------
    # BUTTON OPERATIONS
    # --------------------------------------------------------
    def load_dataset(self):
        file_path = filedialog.askopenfilename(
            title="Open CSV Dataset",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return
        
        self.set_status("Loading dataset...")
        success, msg = self.data_manager.load_csv(file_path)
        
        if success:
            self.update_ui_state()
            self.set_status(f"Dataset '{self.data_manager.file_name}' loaded successfully.")
            messagebox.showinfo("Success", f"Loaded dataset successfully!\nDetected:\n- {len(self.data_manager.numeric_cols)} Numerical columns\n- {len(self.data_manager.date_cols)} Date columns\n- {len(self.data_manager.text_cols)} Text columns")
        else:
            self.update_ui_state()
            self.set_status("Failed to load dataset.")
            messagebox.showerror("Error Loading CSV", f"Could not load the file:\n{msg}")

    def clear_dataset(self):
        if self.data_manager.df is None:
            return
        if messagebox.askyesno("Clear Dataset", "Are you sure you want to unload the current dataset?"):
            self.data_manager.clear()
            self.update_ui_state()
            self.set_status("Dataset cleared.")

    # --------------------------------------------------------
    # SUB-WINDOWS
    # --------------------------------------------------------
    def open_view_window(self):
        """Displays data in a Treeview."""
        if self.data_manager.df is None:
            return
        
        cols, rows = self.data_manager.get_preview_data(100)
        total_rows = len(self.data_manager.df)
        
        view_win = tk.Toplevel(self.root)
        view_win.title(f"Dataset Preview - {self.data_manager.file_name}")
        view_win.geometry("800x450")
        view_win.transient(self.root)
        
        # Frame
        frame = ttk.Frame(view_win, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Header Label
        lbl_preview = ttk.Label(
            frame, 
            text=f"Displaying first {len(rows)} rows of {total_rows} total rows.", 
            font=('Segoe UI', 11, 'bold'), 
            foreground='#2c3e50'
        )
        lbl_preview.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview & Scrollbars Container
        tree_container = ttk.Frame(frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_container, columns=cols, show='headings')
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Configure columns
        for c in cols:
            tree.heading(c, text=c)
            # Adjust column width based on column name length
            tree.column(c, width=max(100, len(c)*10), anchor=tk.W)
            
        # Add values
        for r in rows:
            tree.insert("", "end", values=r)
            
        # Pack layouts
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def open_summary_window(self):
        """Generates describe() output and shows it in a table."""
        if self.data_manager.df is None:
            return
        
        self.set_status("Generating dataset summary statistics...")
        summary_df = DataAnalyzer.generate_describe_summary(self.data_manager.df)
        
        if summary_df is None:
            self.set_status("Failed to generate summary statistics.")
            messagebox.showerror("Error", "No numerical columns found in the dataset to calculate summaries.")
            return

        summary_win = tk.Toplevel(self.root)
        summary_win.title(f"Dataset Summary (describe) - {self.data_manager.file_name}")
        summary_win.geometry("750x350")
        summary_win.transient(self.root)
        
        frame = ttk.Frame(summary_win, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        lbl = ttk.Label(frame, text="Pandas describe() summary statistics for numerical columns:", style="Title.TLabel")
        lbl.pack(anchor=tk.W, pady=(0, 10))
        
        # Describe df columns: features as columns, metrics (count, mean, std, etc.) as index
        # Let's pivot it so columns in the UI represent columns, and metrics are on the left
        cols = ["Statistic"] + list(summary_df.columns)
        
        tree_container = ttk.Frame(frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_container, columns=cols, show='headings')
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Configure columns
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)
            
        # Add values (index name + cell values for index row)
        for stat_name in summary_df.index:
            row_vals = [stat_name]
            for col in summary_df.columns:
                val = summary_df.loc[stat_name, col]
                # Format to a readable string
                if pd.isna(val):
                    row_vals.append("")
                elif val.is_integer() if hasattr(val, 'is_integer') else False:
                    row_vals.append(str(int(val)))
                else:
                    row_vals.append(f"{val:.4f}".rstrip('0').rstrip('.'))
            tree.insert("", "end", values=row_vals)
            
        # Pack layouts
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.set_status("Summary generated.")

    def open_analyze_window(self):
        """NumPy statistics for selected numeric column."""
        if self.data_manager.df is None:
            return
        
        numeric_cols = self.data_manager.numeric_cols
        if not numeric_cols:
            messagebox.showerror("Error", "No numeric columns in this dataset to analyze.")
            return

        analyze_win = tk.Toplevel(self.root)
        analyze_win.title("Single Column Numeric Analysis")
        analyze_win.geometry("450x400")
        analyze_win.resizable(False, False)
        analyze_win.transient(self.root)
        
        frame = ttk.Frame(analyze_win, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Select Numerical Column:", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        col_select = ttk.Combobox(frame, values=numeric_cols, state="readonly", font=('Segoe UI', 10))
        col_select.pack(fill=tk.X, pady=(0, 15))
        col_select.current(0)
        
        # Results frame
        res_frame = ttk.LabelFrame(frame, text=" NumPy Summary Output ", padding="10")
        res_frame.pack(fill=tk.BOTH, expand=True)
        
        stats_labels = {}
        metrics = ["Mean", "Median", "Minimum", "Maximum", "Std Dev", "Count", "Sum"]
        
        for i, metric in enumerate(metrics):
            lbl_m = ttk.Label(res_frame, text=f"{metric}:", font=('Segoe UI', 10, 'bold'))
            lbl_m.grid(row=i, column=0, sticky=tk.W, pady=3, padx=(0, 20))
            
            lbl_v = ttk.Label(res_frame, text="--", foreground='#106ebe')
            lbl_v.grid(row=i, column=1, sticky=tk.W, pady=3)
            stats_labels[metric] = lbl_v
            
        def calculate_stats():
            col = col_select.get()
            if not col:
                return
            
            self.set_status(f"Calculating NumPy stats for {col}...")
            stats = DataAnalyzer.calculate_column_stats(self.data_manager.df, col)
            
            if stats is None:
                messagebox.showerror("Error", "Could not calculate statistics (the column might contain only missing values).")
                self.set_status("Stats calculation failed.")
                return
            
            for m in metrics:
                val = stats[m]
                if m == "Count":
                    stats_labels[m].config(text=str(val))
                else:
                    stats_labels[m].config(text=f"{val:.4f}".rstrip('0').rstrip('.'))
                    
            self.set_status(f"Stats calculated for {col}.")
            
        btn_calc = ttk.Button(frame, text="Calculate Statistics", command=calculate_stats)
        btn_calc.pack(fill=tk.X, pady=(15, 0))

    def open_search_window(self):
        """Dynamically search matching records."""
        if self.data_manager.df is None:
            return
            
        search_win = tk.Toplevel(self.root)
        search_win.title(f"Search - {self.data_manager.file_name}")
        search_win.geometry("750x450")
        search_win.transient(self.root)
        
        frame = ttk.Frame(search_win, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Search Inputs
        inputs_frame = ttk.Frame(frame)
        inputs_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(inputs_frame, text="Column:").pack(side=tk.LEFT, padx=(0, 5))
        col_select = ttk.Combobox(inputs_frame, values=list(self.data_manager.df.columns), state="readonly", width=15)
        col_select.pack(side=tk.LEFT, padx=(0, 15))
        col_select.current(0)
        
        ttk.Label(inputs_frame, text="Search Value:").pack(side=tk.LEFT, padx=(0, 5))
        ent_search = ttk.Entry(inputs_frame, width=25)
        ent_search.pack(side=tk.LEFT, padx=(0, 15))
        
        # Grid View
        cols = list(self.data_manager.df.columns)
        tree_container = ttk.Frame(frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_container, columns=cols, show='headings')
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.W)
            
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        lbl_results_info = ttk.Label(frame, text="Matches: Enter criteria and click search.", font=('Segoe UI', 9, 'italic'))
        lbl_results_info.pack(anchor=tk.W, pady=(5, 0))

        def execute_search():
            col = col_select.get()
            term = ent_search.get()
            self.set_status(f"Searching for '{term}' in column '{col}'...")
            
            # Clear old rows
            for item in tree.get_children():
                tree.delete(item)
                
            res_df = self.data_manager.search_data(col, term)
            
            if res_df.empty:
                lbl_results_info.config(text="No matching rows found.")
                self.set_status("Search completed - 0 matches.")
                return
                
            # Preview first 100 results
            preview_res = res_df.head(100).replace({np.nan: ''})
            for r in preview_res.values.tolist():
                tree.insert("", "end", values=r)
                
            lbl_results_info.config(text=f"Found {len(res_df)} matches. Showing first {len(preview_res)} rows.")
            self.set_status(f"Search completed - {len(res_df)} matches found.")
            
        btn_search = ttk.Button(inputs_frame, text="Search", command=execute_search)
        btn_search.pack(side=tk.LEFT)
        
        # Bind Enter key to search
        ent_search.bind("<Return>", lambda e: execute_search())

    def open_filter_window(self):
        """Filter dataset by dynamic condition."""
        if self.data_manager.df is None:
            return
            
        filter_win = tk.Toplevel(self.root)
        filter_win.title(f"Filter Data - {self.data_manager.file_name}")
        filter_win.geometry("800x480")
        filter_win.transient(self.root)
        
        frame = ttk.Frame(filter_win, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Filters Controls
        ctrl_frame = ttk.Frame(frame)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(ctrl_frame, text="Column:").pack(side=tk.LEFT, padx=(0, 5))
        col_select = ttk.Combobox(ctrl_frame, values=list(self.data_manager.df.columns), state="readonly", width=15)
        col_select.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(ctrl_frame, text="Operator:").pack(side=tk.LEFT, padx=(0, 5))
        op_select = ttk.Combobox(ctrl_frame, values=['==', 'contains', '>', '<', '>=', '<='], state="readonly", width=10)
        op_select.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(ctrl_frame, text="Value:").pack(side=tk.LEFT, padx=(0, 5))
        ent_val = ttk.Entry(ctrl_frame, width=15)
        ent_val.pack(side=tk.LEFT, padx=(0, 15))
        
        # Default choices
        col_select.current(0)
        op_select.current(0)
        
        # Grid View
        cols = list(self.data_manager.df.columns)
        tree_container = ttk.Frame(frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_container, columns=cols, show='headings')
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.W)
            
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        lbl_results_info = ttk.Label(frame, text="Results: Define condition and click Apply Filter.", font=('Segoe UI', 9, 'italic'))
        lbl_results_info.pack(anchor=tk.W, pady=(5, 0))

        def apply_filter():
            col = col_select.get()
            op = op_select.get()
            val = ent_val.get().strip()
            
            if not val:
                messagebox.showwarning("Empty Value", "Please enter a value to filter on.")
                return
                
            self.set_status(f"Applying filter: {col} {op} '{val}'...")
            
            # Clear old rows
            for item in tree.get_children():
                tree.delete(item)
                
            try:
                res_df = self.data_manager.filter_data(col, op, val)
                
                if res_df.empty:
                    lbl_results_info.config(text="No rows match this filter criteria.")
                    self.set_status("Filter applied - 0 matches.")
                    return
                    
                preview_res = res_df.head(100).replace({np.nan: ''})
                for r in preview_res.values.tolist():
                    tree.insert("", "end", values=r)
                    
                lbl_results_info.config(text=f"Filtered {len(res_df)} rows. Showing first {len(preview_res)} rows.")
                self.set_status(f"Filter completed - {len(res_df)} matches found.")
            except Exception as e:
                lbl_results_info.config(text="Filtering Error.")
                self.set_status("Filter error.")
                messagebox.showerror("Filter Error", f"Failed to apply filter:\n{str(e)}")
            
        btn_apply = ttk.Button(ctrl_frame, text="Apply Filter", command=apply_filter)
        btn_apply.pack(side=tk.LEFT)
        
        # Add quick helper to suggest operators depending on column classification
        def on_column_change(event):
            col = col_select.get()
            if col in self.data_manager.numeric_cols:
                # Suggest numeric filters
                op_select.config(values=['>', '<', '==', '>=', '<='])
                op_select.current(0)
            else:
                # Suggest text/date filters
                op_select.config(values=['==', 'contains', '>', '<', '>=', '<='])
                op_select.current(1)
                
        col_select.bind("<<ComboboxSelected>>", on_column_change)
        # Run once to set initial values
        on_column_change(None)

    def open_sort_window(self):
        """Sort the dataset in-place."""
        if self.data_manager.df is None:
            return
            
        sort_win = tk.Toplevel(self.root)
        sort_win.title("Sort Dataset")
        sort_win.geometry("400x250")
        sort_win.resizable(False, False)
        sort_win.transient(self.root)
        
        frame = ttk.Frame(sort_win, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Choose Sort Column:", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        cols = list(self.data_manager.df.columns)
        col_select = ttk.Combobox(frame, values=cols, state="readonly", font=('Segoe UI', 10))
        col_select.pack(fill=tk.X, pady=(0, 15))
        col_select.current(0)
        
        ttk.Label(frame, text="Sort Direction:", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        sort_order = tk.StringVar(value="Ascending")
        r_asc = ttk.Radiobutton(frame, text="Ascending (Low to High)", variable=sort_order, value="Ascending")
        r_asc.pack(anchor=tk.W, pady=2)
        r_desc = ttk.Radiobutton(frame, text="Descending (High to Low)", variable=sort_order, value="Descending")
        r_desc.pack(anchor=tk.W, pady=2)
        
        def run_sort():
            col = col_select.get()
            asc = (sort_order.get() == "Ascending")
            
            self.set_status(f"Sorting dataset by '{col}'...")
            self.data_manager.sort_data(col, ascending=asc)
            self.set_status(f"Dataset sorted by '{col}' ({sort_order.get()}).")
            messagebox.showinfo("Success", f"Dataset sorted by '{col}' successfully!")
            sort_win.destroy()
            
        btn_run = ttk.Button(frame, text="Apply Sorting", command=run_sort)
        btn_run.pack(fill=tk.X, pady=(15, 0))

    def open_visualize_window(self):
        """Universal plot generator."""
        if self.data_manager.df is None:
            return
            
        vis_win = tk.Toplevel(self.root)
        vis_win.title("Create Data Visualization")
        vis_win.geometry("450x380")
        vis_win.resizable(False, False)
        vis_win.transient(self.root)
        
        frame = ttk.Frame(vis_win, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Type
        ttk.Label(frame, text="Select Graph Type:", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 5))
        graph_types = ["Line Graph", "Bar Graph", "Scatter Plot", "Histogram"]
        type_select = ttk.Combobox(frame, values=graph_types, state="readonly")
        type_select.pack(fill=tk.X, pady=(0, 15))
        type_select.current(0)
        
        # X-Axis
        ttk.Label(frame, text="Select X-Axis Column:", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 5))
        all_cols = list(self.data_manager.df.columns)
        x_select = ttk.Combobox(frame, values=all_cols, state="readonly")
        x_select.pack(fill=tk.X, pady=(0, 15))
        x_select.current(0)
        
        # Y-Axis (only needed for Line, Bar, Scatter)
        lbl_y = ttk.Label(frame, text="Select Y-Axis Column:", style="Title.TLabel")
        lbl_y.pack(anchor=tk.W, pady=(0, 5))
        y_select = ttk.Combobox(frame, values=all_cols, state="readonly")
        y_select.pack(fill=tk.X, pady=(0, 15))
        # Find first numeric column as default for Y-Axis if possible
        if self.data_manager.numeric_cols:
            y_select.set(self.data_manager.numeric_cols[0])
        else:
            y_select.current(0)

        # Toggle Y-Axis based on type selection
        def on_type_change(event):
            gtype = type_select.get()
            if gtype == "Histogram":
                # Disable Y-Axis selection
                lbl_y.pack_forget()
                y_select.pack_forget()
            else:
                # Show Y-Axis selection
                lbl_y.pack(anchor=tk.W, pady=(0, 5), before=btn_plot)
                y_select.pack(fill=tk.X, pady=(0, 15), before=btn_plot)
                
        type_select.bind("<<ComboboxSelected>>", on_type_change)

        def make_plot():
            gtype = type_select.get()
            xcol = x_select.get()
            ycol = y_select.get()
            
            self.set_status(f"Generating {gtype}...")
            
            # Validations
            if gtype != "Histogram" and xcol == ycol:
                if not messagebox.askyesno("Warning", "X and Y axis columns are identical. Continue?"):
                    return
            
            try:
                # Call visualizer
                fig = None
                title = f"{gtype}: "
                
                if gtype == "Histogram":
                    # For Histogram, must select a numerical column
                    if xcol not in self.data_manager.numeric_cols:
                        messagebox.showerror("Invalid Column Selection", "Histograms require a numerical column for the distribution.")
                        return
                    fig = DataVisualizer.plot_histogram(self.data_manager.df, xcol, bins=12)
                else:
                    # Y-Axis validation (must be numerical for Line, Bar, Scatter plots in standard cases)
                    # Let's show warning if Y-axis is not numeric, but allow it if it works
                    if ycol not in self.data_manager.numeric_cols:
                        if not messagebox.askyesno("Non-Numeric Y Column", f"Column '{ycol}' is non-numeric. Plotting categorical values on Y-axis might look crowded or throw errors. Continue?"):
                            return
                            
                    if gtype == "Line Graph":
                        fig = DataVisualizer.plot_line(self.data_manager.df, xcol, ycol)
                    elif gtype == "Bar Graph":
                        fig = DataVisualizer.plot_bar(self.data_manager.df, xcol, ycol)
                    elif gtype == "Scatter Plot":
                        fig = DataVisualizer.plot_scatter(self.data_manager.df, xcol, ycol)

                if fig is not None:
                    # Open canvas viewer window
                    self.show_plot_window(fig, f"{gtype} Viewer")
                    self.set_status(f"{gtype} generated successfully.")
                else:
                    self.set_status("Failed to generate plot.")
                    messagebox.showerror("Error", "Visualizer did not return a valid figure object.")
            except Exception as e:
                self.set_status("Plotting error.")
                messagebox.showerror("Visualizer Error", f"An error occurred while generating the graph:\n{str(e)}")

        btn_plot = ttk.Button(frame, text="Generate Plot", command=make_plot)
        btn_plot.pack(fill=tk.X, pady=(15, 0))

    def show_plot_window(self, fig, window_title):
        """Displays a Matplotlib figure embedded in a new Tkinter window with controls."""
        plot_win = tk.Toplevel(self.root)
        plot_win.title(window_title)
        plot_win.geometry("750x550")
        plot_win.transient(self.root)
        
        # Frame
        frame = ttk.Frame(plot_win)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Embed Figure canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add Toolbar at the bottom
        toolbar_frame = ttk.Frame(frame)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    def generate_report(self):
        """Formats and saves the analysis text report."""
        if self.data_manager.df is None:
            return
            
        self.set_status("Formatting dataset report...")
        
        # We need to compile statistics for each numeric column
        column_stats = {}
        for col in self.data_manager.numeric_cols:
            stats = DataAnalyzer.calculate_column_stats(self.data_manager.df, col)
            if stats:
                column_stats[col] = stats
                
        # Generate raw text using report generator
        summary_info = self.data_manager.get_summary_info()
        report_text = ReportGenerator.generate_report_text(
            self.data_manager.file_name,
            summary_info,
            self.data_manager.numeric_cols,
            self.data_manager.text_cols,
            self.data_manager.date_cols,
            column_stats
        )
        
        # Request file path from user
        save_path = filedialog.asksaveasfilename(
            title="Save Text Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"report_{self.data_manager.file_name.replace('.csv', '')}.txt"
        )
        
        if not save_path:
            self.set_status("Report generation cancelled.")
            return
            
        try:
            self.set_status("Writing report to disk...")
            ReportGenerator.write_report_to_file(save_path, report_text)
            self.set_status("Report generated successfully.")
            messagebox.showinfo("Report Saved", f"Statistical report successfully saved to:\n{save_path}")
        except Exception as e:
            self.set_status("Failed to save report.")
            messagebox.showerror("Error Saving Report", f"An error occurred while saving the report:\n{str(e)}")

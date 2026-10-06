import datetime

class ReportGenerator:
    @staticmethod
    def generate_report_text(file_name, summary_info, numeric_cols, text_cols, date_cols, column_stats_dict):
        """
        Formats a detailed analysis report as plain text.
        
        :param file_name: Name of the dataset file.
        :param summary_info: Dict returned by DataManager.get_summary_info().
        :param numeric_cols: List of numeric columns.
        :param text_cols: List of text/categorical columns.
        :param date_cols: List of date columns.
        :param column_stats_dict: Dictionary mapping column names to their computed statistics.
        :return: String containing the formatted text report.
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = []
        
        report.append("==================================================")
        report.append("SCIENTIFIC DATA ANALYSIS REPORT")
        report.append("==================================================")
        report.append(f"Generated on: {now}")
        report.append(f"Dataset File: {file_name}")
        report.append("")
        report.append("--------------------------------------------------")
        report.append("DATASET OVERVIEW")
        report.append("--------------------------------------------------")
        report.append(f"Total Rows:               {summary_info['rows']}")
        report.append(f"Total Columns:            {summary_info['cols']}")
        report.append(f"Missing Values (Total):   {summary_info['missing']}")
        report.append(f"Duplicate Rows:           {summary_info['duplicates']}")
        report.append("")
        report.append("COLUMN CLASSIFICATION:")
        report.append(f"- Numerical ({len(numeric_cols)}): {', '.join(numeric_cols) if numeric_cols else 'None'}")
        report.append(f"- Date ({len(date_cols)}):      {', '.join(date_cols) if date_cols else 'None'}")
        report.append(f"- Text/Categorical ({len(text_cols)}): {', '.join(text_cols) if text_cols else 'None'}")
        report.append("")
        report.append("--------------------------------------------------")
        report.append("STATISTICAL SUMMARY (NUMERICAL COLUMNS)")
        report.append("--------------------------------------------------")
        
        if not numeric_cols:
            report.append("No numerical columns found in the dataset.")
        else:
            for col in numeric_cols:
                stats = column_stats_dict.get(col)
                if stats:
                    report.append(f"Column Name: {col}")
                    report.append(f"  Count:              {stats['Count']}")
                    report.append(f"  Sum:                {stats['Sum']:.4f}".rstrip('0').rstrip('.'))
                    report.append(f"  Mean:               {stats['Mean']:.4f}".rstrip('0').rstrip('.'))
                    report.append(f"  Median:             {stats['Median']:.4f}".rstrip('0').rstrip('.'))
                    report.append(f"  Minimum:            {stats['Minimum']:.4f}".rstrip('0').rstrip('.'))
                    report.append(f"  Maximum:            {stats['Maximum']:.4f}".rstrip('0').rstrip('.'))
                    report.append(f"  Standard Deviation: {stats['Std Dev']:.4f}".rstrip('0').rstrip('.'))
                    report.append("")
                else:
                    report.append(f"Column Name: {col} (No calculations available - contains only null values)")
                    report.append("")
                    
        report.append("--------------------------------------------------")
        report.append("REPORT GENERATED SUCCESSFULLY")
        report.append("==================================================")
        
        return "\n".join(report)

    @staticmethod
    def write_report_to_file(file_path, report_content):
        """Writes the report content to the designated filepath."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

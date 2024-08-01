import pandas as pd
import os

def analyze_report(file_path):
    """
    Analyze the financial report CSV file.
    
    Args:
    file_path (str): Path to the CSV file.
    
    Returns:
    tuple: (year_month, total_amount)
    """
    # Extract year and month from filename
    filename = os.path.splitext(os.path.basename(file_path))[0]
    year_month = '-'.join(filename.split('-')[1:3])  # Extract 'YYYY-MM'
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Calculate total amount
    total_amount = df['amount'].sum()
    
    return year_month, total_amount

def analyze_all_reports(reports_dir):
    """
    Analyze all reports in the given directory.
    
    Args:
    reports_dir (str): Path to the directory containing CSV files.
    
    Returns:
    pd.DataFrame: Processed and analyzed data for all months.
    """
    data = []
    for filename in os.listdir(reports_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(reports_dir, filename)
            month, total_amount = analyze_report(file_path)
            data.append({'month': month, 'total_amount': total_amount})
    
    return pd.DataFrame(data)

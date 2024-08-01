import pandas as pd
import os

def analyze_report(file_path):
    """
    Analyze the financial report CSV file.
    
    Args:
    file_path (str): Path to the CSV file.
    
    Returns:
    tuple: (year_month, total_amount, df)
    """
    # Extract year and month from filename
    filename = os.path.splitext(os.path.basename(file_path))[0]
    year_month = '-'.join(filename.split('-')[1:3])  # Extract 'YYYY-MM'
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # Process installments
    def extract_installment_info(title):
        import re
        match = re.search(r'(\d+)/(\d+)$', title)
        if match:
            current, total = map(int, match.groups())
            base_title = title[:match.start()].strip()
            return base_title, current, total
        return title, None, None

    df['base_title'], df['current_installment'], df['total_installments'] = zip(*df['title'].apply(extract_installment_info))

    # Group by base_title and sum amounts for installments
    grouped = df.groupby('base_title').agg({
        'amount': 'sum',
        'date': 'first',
        'current_installment': 'max',
        'total_installments': 'max'
    }).reset_index()

    # Recreate title for installments
    grouped['title'] = grouped.apply(lambda row: 
        f"{row['base_title']} {row['current_installment']}/{row['total_installments']}"
        if pd.notnull(row['total_installments']) else row['base_title'], axis=1)

    # Keep only necessary columns
    df = grouped[['date', 'title', 'amount']]
    
    # Calculate total amount
    total_amount = df['amount'].sum()
    
    return year_month, total_amount, df

def analyze_all_reports(reports_dir):
    """
    Analyze all reports in the given directory.
    
    Args:
    reports_dir (str): Path to the directory containing CSV files.
    
    Returns:
    pd.DataFrame: Processed and analyzed data for all months.
    """
    data = []
    all_purchases = pd.DataFrame()
    
    for filename in os.listdir(reports_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(reports_dir, filename)
            month, total_amount, df = analyze_report(file_path)
            data.append({
                'month': month, 
                'total_amount': total_amount
            })
            all_purchases = pd.concat([all_purchases, df])
    
    result = pd.DataFrame(data)
    
    # Get top 10 most expensive purchases from all files
    top_10_purchases = all_purchases.nlargest(10, 'amount')[['date', 'amount', 'title']]
    result['top_10_purchases'] = [top_10_purchases] * len(result)
    
    return result

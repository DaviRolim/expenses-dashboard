import os
from data_analysis import analyze_report
from dashboard import create_dashboard

def main():
    reports_dir = "reports"
    for filename in os.listdir(reports_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(reports_dir, filename)
            data = analyze_report(file_path)
            create_dashboard(data)

if __name__ == "__main__":
    main()

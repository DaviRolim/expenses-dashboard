from data_analysis import analyze_all_reports
from dashboard import create_dashboard

def main():
    reports_dir = "reports"
    data = analyze_all_reports(reports_dir)
    create_dashboard(data)

if __name__ == "__main__":
    main()

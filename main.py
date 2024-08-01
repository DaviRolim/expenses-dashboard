from data_analysis import analyze_all_reports
from dashboard import create_dashboard

def main():
    reports_dir = "reports"
    data, top_10_purchases = analyze_all_reports(reports_dir)
    app = create_dashboard(data, top_10_purchases)
    app.run_server(debug=True)

if __name__ == "__main__":
    main()

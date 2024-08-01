# Financial Report Analyzer

This project analyzes financial reports from CSV files and creates interactive dashboards to visualize the data.

## Setup

1. Ensure you have Python 3.9 or later installed.
2. Install Poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository and navigate to the project directory.
4. Install dependencies:
   ```
   poetry install
   ```

## Usage

1. Place your CSV financial reports in the `reports` folder.
2. Run the main script:
   ```
   poetry run python main.py
   ```
3. The script will analyze all CSV files in the `reports` folder and create interactive dashboards for each.

## Project Structure

- `main.py`: The entry point of the application.
- `data_analysis.py`: Contains functions for analyzing the financial reports.
- `dashboard.py`: Handles the creation of interactive dashboards using Dash and Plotly.
- `reports/`: Directory to store CSV financial reports.
- `pyproject.toml`: Poetry configuration file for managing dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

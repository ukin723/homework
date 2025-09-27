# Hong Kong Weather Visualization

This project is designed to scrape, process, and visualize weather data from the Hong Kong Observatory website. It provides a comprehensive analysis of recent weather trends in Hong Kong.

## Project Structure

```
hk-weather-visualization
├── src
│   ├── fetch_weather.py      # Functions to scrape weather data from the HKO website
│   ├── parse_hko.py          # Functions to parse the fetched HTML content
│   ├── visualize.py           # Functions to create visualizations of the weather data
│   ├── utils.py               # Utility functions for data processing
│   └── config.py             # Configuration settings and constants
├── data
│   ├── raw                   # Directory for storing raw weather data
│   └── processed             # Directory for storing processed weather data
├── notebooks
│   └── analysis.ipynb        # Jupyter notebook for exploratory data analysis
├── tests
│   └── test_fetch.py         # Unit tests for the data fetching functions
├── requirements.txt          # List of Python dependencies
├── .gitignore                # Files and directories to ignore by Git
└── README.md                 # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd hk-weather-visualization
pip install -r requirements.txt
```

## Usage

1. **Fetch Weather Data**: Run `fetch_weather.py` to scrape the latest weather data from the Hong Kong Observatory.
2. **Parse Data**: Use `parse_hko.py` to extract relevant information from the fetched HTML content.
3. **Visualize Data**: Utilize `visualize.py` to create visual representations of the weather trends.
4. **Analysis**: Open `notebooks/analysis.ipynb` for exploratory data analysis and further insights.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
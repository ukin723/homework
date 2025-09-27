# Sunspot Data Visualization

This project is designed to fetch, process, and visualize sunspot data. It provides a comprehensive analysis of historical sunspot activity and solar cycles.

## Project Structure

```
sunspot-visualization
├── src
│   ├── data_processing.py    # Functions to fetch and process sunspot data
│   ├── visualize.py          # Functions to create visualizations of sunspot activity
│   ├── utils.py              # Utility functions for data processing
│   └── config.py             # Configuration settings and constants
├── data
│   ├── raw                   # Directory for storing raw sunspot data
│   └── processed             # Directory for storing processed sunspot data
├── notebooks
│   └── analysis.ipynb        # Jupyter notebook for exploratory data analysis
├── tests
│   └── test_data_processing.py # Unit tests for the data processing functions
├── requirements.txt          # List of Python dependencies
├── .gitignore                # Files and directories to ignore by Git
└── README.md                 # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd sunspot-visualization
pip install -r requirements.txt
```

## Usage

1. **Fetch Sunspot Data**: Run `data_processing.py` to fetch the latest sunspot data from SILSO or generate simulated data if fetching fails.
2. **Process Data**: Use `data_processing.py` to preprocess the data and annotate solar cycles.
3. **Visualize Data**: Utilize `visualize.py` to create visual representations of sunspot activity and solar cycles.
4. **Analysis**: Open `notebooks/analysis.ipynb` for exploratory data analysis and further insights.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

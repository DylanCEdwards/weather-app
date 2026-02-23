# Weather Data App

## Description

An iteratively-written weather app project as part of CS3270's curriculum. The finished project will fetch, process, analyze, and visualize weather data from various sources.



---

## Purpose
Provide utilities to safely read weather datasets into pandas, wrap the data in a purpose-built dataset class, and compute common summary statistics. The code is organized for clarity, testability, and reuse.

---

## Design & OOP Principles
The package weather_stats is organized by single-responsibility 
classes: WeatherDataLoader handles CSV I/O, WeatherDataset wraps 
a pandas.DataFrame (stored in a private _data attribute) and offers 
dataset helpers, and WeatherStats composes a WeatherDataset to compute 
statistics. Constructors inject dependencies, instance methods 
operate on self, and input checks raise explicit exceptions 
for predictable failures. Type hints plus docstrings are used to make 
the API clear and easy to test.</city>

---
## Recent Changes
### Phase 5
- Added automated unit tests using pytest.
- Added doctest examples in selected methods to validate expected outputs directly from docstrings.
- Created a dedicated tests/ directory to separate test logic from application code.

### Phase 4
- Refactored code to use generators & iterators for creating & processing the dataset, improving memory efficiency.
- Implemented a logger to track data loading and processing steps, aiding in debugging and monitoring.

---

## Project Files
- `Module1.py` – Main Python script containing the CSV loading logic
- `WeatherPredictionData/weather_prediction_dataset.csv` – Input data file
- `Module1.html` – Auto-generated documentation created with `pydoc`
- `README.md` – Project documentation
- `weather_stats/loader.py` - Module for loading & processing weather data from CSV
- `weather_stats/stats.py` - Module for calculating statistics on weather data
- `weather_stats/dataset.py` - Module for holding weather data and returning non-numerical data from the set
- `tests/` - Directory containing pytest unit tests

---

## Requirements
- Python 3.x
- pandas
- pytest
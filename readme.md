# Weather Data App

## Description

An iteratively-written weather app project as part of CS3270's curriculum. The finished project will fetch, process, analyze, and visualize weather data from various sources.



---

## Purpose
Provide utilities to safely read weather datasets into `pandas`, wrap the data in a purpose-built dataset class, and compute common summary statistics. The code is organized for clarity, testability, and reuse.

---

## Design & OOP Principles
The package weather_stats is organized by single-responsibility 
classes: WeatherDataLoader handles CSV I/O, WeatherDataset wraps 
a `pandas` DataFrame (stored in a private _data attribute) and offers 
dataset helpers, and WeatherStats composes a WeatherDataset to compute 
statistics. Constructors inject dependencies, instance methods 
operate on self, and input checks raise explicit exceptions 
for predictable failures. Type hints plus docstrings are used to make 
the API clear and easy to test.</city>

---
## Recent Changes
### Phase 6
- Added various filtering capabilities to WeatherDataset, allowing users to create subsets of data by specific time periods.
  - `filter_by_month` - filters dataset to include only rows from a specified month (across all years).
  - `filter_by_year` - filters dataset to include all rows from a specified year.
  - `filter_by_month_and_year` - filters dataset to include only rows from specified month and year.
  - `filter_by_date_range` - filters dataset to include only rows between specified start and end dates (inclusive).
  - `filter_by_season` - filters dataset to include only rows from a specified season (e.g., 'spring', 'summer', 'fall', 'winter') across all years.
- Extracted the majority of CLI logic out of Module1.py to reduce clutter and refactored it via lambda expressions and helper functions.
  - `ask_until_valid` - a dynamic helper function that repeatedly prompts the user for input until a valid response is given, using a provided validation function and error message.
  - `run_cli` - the main function extracted from the main method that orchestrates the command-line interface and facilitates user interaction.
- Utilized `matplotlib` to add a simple visualization feature that allows user to see a visual representation of their temperature statistics summary. 

### Phase 5
- Added automated unit tests using pytest.
- Added doctest examples in selected methods to validate expected outputs directly from docstrings.
- Created a dedicated tests/ directory to separate test logic from application code.

### Phase 4
- Refactored code to use generators & iterators for creating & processing the dataset, improving memory efficiency.
- Implemented a logger to track data loading and processing steps, aiding in debugging and monitoring.

---
## Automated Tests

Automated test suite located in `tests/` exercises dataset loading, dataset helpers, loader behavior, and statistical computations.

- `tests/test_dataset.py`
  - `test_get_data` - verifies `WeatherDataset.get_data()` returns the original DataFrame.
  - `test_get_columns` - ensures `get_columns()` lists all columns.
  - `test_has_column` - checks `has_column()` for existing and missing columns.
  - `test_get_cities` - validates extraction of city identifiers from column names.
  - `test_has_city` - checks `has_city()` for present and missing city identifiers.
  - `test_special_case_de_bilt` - ensures `DE` is normalized to `DE_BILT` per special-case logic.

- `tests/test_loader.py`
  - `test_load_success` - creates a temporary CSV and asserts `WeatherDataLoader.load()` returns a `WeatherDataset`.
  - `test_load_file_not_found` - verifies loading a nonexistent file raises `FileNotFoundError`.

- `tests/test_stats.py`
  - `test_mean` - validates `WeatherStats.mean()` computation.
  - `test_validate_column` - ensures `_validate_column()` raises `ValueError` for missing columns.
  - `test_median` - validates `median()` computation.
  - `test_min` - validates `min()` computation.
  - `test_max` - validates `max()` computation.
  - `test_std_dev` - validates `std_dev()` computation.
  - `test_range` - validates `range()` calculation using `max()` - `min()`.
  - `test_mode` - validates `mode()` computation.
  - `test_temperature_summary` - confirms `temperature_summary()` yields all expected summary statistics and values.

- `tests/test_ws_helper.py`
  - `test_ask_until_valid_success` - verifies `ask_until_valid` parses and returns a valid value.
  - `test_ask_until_valid_retries` - ensures invalid input is retried and error message is shown.
  - `test_run_cli_all_time_summary` - simulates an all-time CLI flow (city selection, summary) and completes without error.
  - `test_run_cli_date_range_filter` - simulates a date-range filter CLI flow and verifies completion (uses monkeypatch/stubbed plotting to avoid GUI).

---

## Project Files
- `Module1.py` – Main Python script
- `weather_stats/ws_helper.py` - Module for helper functions related to weather data processing and CLI interaction
- `weather_stats/loader.py` - Module for loading & processing weather data from CSV
- `weather_stats/stats.py` - Module for calculating statistics on weather data
- `weather_stats/dataset.py` - Module for holding weather data and returning non-numerical data from the set
- `tests/` - Directory containing pytest unit tests
- `logs/weather.log` - Log file generated by the logger during data loading and processing
- `README.md` – Project documentation
- `WeatherPredictionData/weather_prediction_dataset.csv` – Input data file
- `Module1.html` – Auto-generated documentation created with `pydoc`

---

## Requirements
- Python 3.x
- pandas
- pytest
- matplotlib
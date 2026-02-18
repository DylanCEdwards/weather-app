# Module 1 - Phase 3 - Weather Data

## Description

This project practices reading CSV files
and documenting code using Python docstrings, while following
Pythonic coding standards. An understanding of modularization 
has been introduced since the last version. 

---

## Purpose
This project was created as part of CS 3270 to practice
working with pandas DataFrames, modularization and
documentation.

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

## Project Files
- `Module1.py` – Main Python script containing the CSV loading logic
- `WeatherPredictionData/weather_prediction_dataset.csv` – Input data file
- `Module1.html` – Auto-generated documentation created with `pydoc`
- `README.md` – Project documentation
- `weather_stats/loader.py` - Module for loading & processing weather data from CSV
- `weather_stats/stats.py` - Module for calculating statistics on weather data
- `weather_stats/dataset.py` - Module for holding weather data and returning non-numerical data from the set


---

## Requirements
- Python 3.x
- pandas
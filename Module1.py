"""
Filename: Module1.py
Author: Dylan Edwards
Date: 02/07/2026
Version: Phase 3
Description: This script loads weather prediction data from a CSV file and stores it
in Python data structures via pandas. Documentation is done through docstrings
to be used with pydoc. Demonstrates modularity by separating data loading and statistical
calculations into different modules.
"""

from weather_stats.loader import WeatherDataset, WeatherDataLoader
from weather_stats.stats import WeatherStats

def main():
    """
    Main entry point for the script.

    Loads the CSV dataset, presents available cities, and prompts the
    user to request a temperature summary until they quit.
    """
    file_name = "WeatherPredictionData/weather_prediction_dataset.csv"
    loader = WeatherDataLoader(file_name)
    dataset = loader.load()
    stats = WeatherStats(dataset)

    for city in dataset:
        print(city)

    while True:
        user_choice = input("Enter a city name for weather data (Enter 'Q' to quit): ").upper()

        if user_choice == "Q":
            print("Goodbye")
            break

        if not dataset.has_city(user_choice):
            print("City not found. Please try again.")
            continue

        print(f"Temperature statistics for {user_choice}:")
        for stat, value in stats.temperature_summary(user_choice):
            print(f"{stat}: {value}")

if __name__ == '__main__':
    main()
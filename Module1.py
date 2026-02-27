"""
Filename: Module1.py
Author: Dylan Edwards
Date: 02/25/2026
Version: Phase 6
Description: This script loads weather prediction data from a CSV file and stores it
in Python data structures via pandas. Documentation is done through docstrings
to be used with pydoc. Demonstrates modularity by separating data loading and statistical
calculations into different modules.
"""

from weather_stats.loader import WeatherDataLoader
from weather_stats.stats import WeatherStats
import logging
from weather_stats.ws_helper import run_cli

logging.basicConfig(filename='logs/weather.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)

def main():
    """
    Main entry point for the script.

    Loads the CSV dataset, presents available cities, and prompts the
    user to request a temperature summary until they quit.
    """
    logging.debug("Program started")
    wd_file_name = "WeatherPredictionData/weather_prediction_dataset.csv"
    loader = WeatherDataLoader(wd_file_name)
    dataset = loader.load()
    stats = WeatherStats(dataset)

    run_cli(dataset, stats)

if __name__ == '__main__':
    main()
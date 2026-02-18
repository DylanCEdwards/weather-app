"""
Functions and classes to load weather data from CSV files.

Provides a simple `WeatherDataLoader` class that reads a CSV file with
pandas and wraps the result in a `WeatherDataset`.
"""
import pandas as pd
from weather_stats.dataset import WeatherDataset

class WeatherDataLoader:
    """
    Loader class responsible for reading CSV weather data and returning
    a `WeatherDataset`.
    """

    def __init__(self, file_path: str):
        """
        Initialize the loader.

        Args:
            file_path: Path to the CSV file to load.
        """
        self.file_path = file_path

    def load(self) -> WeatherDataset:
        """
        Read the CSV file and return a `WeatherDataset`.

        Returns:
            A WeatherDataset containing the loaded data.
        """
        data = pd.read_csv(self.file_path)
        return WeatherDataset(data)


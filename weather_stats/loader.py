"""
Functions and classes to load weather data from CSV files.

Provides a simple `WeatherDataLoader` class that reads a CSV file with
pandas and wraps the result in a `WeatherDataset`.
"""
import pandas as pd
from weather_stats.dataset import WeatherDataset
import logging

logger = logging.getLogger(__name__)

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
        logger.debug("Reading CSV %s", self.file_path)
        try:
            data = pd.read_csv(self.file_path)
            logger.info("Loaded CSV %s (rows=%d, cols=%d)", self.file_path, data.shape[0], data.shape[1])
            return WeatherDataset(data)
        except Exception:
            logger.error("Failed to load CSV %s", self.file_path)
            raise


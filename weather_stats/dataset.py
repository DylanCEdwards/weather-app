import pandas as pd
import logging

logger = logging.getLogger(__name__)

class WeatherDataset:
    """
    Wrapper around a pandas DataFrame that represents weather data.

    Attributes:
        _data: The underlying pandas DataFrame containing weather data.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize a WeatherDataset.

        Args:
            data: A pandas DataFrame containing weather measurements.
        """
        self._data = data
        self.cities = self.get_cities()

    def __iter__(self):
        for city in self.cities:
            yield city

    def get_data(self) -> pd.DataFrame:
        """
        Return the underlying pandas DataFrame.

        Returns:
            The stored pandas DataFrame.
        """
        return self._data

    def get_columns(self) -> list[str]:
        """
        Return a list of column names present in the dataset.

        Returns:
            A list of column name strings.
        """
        return list(self._data.columns)

    def has_column(self, column: str) -> bool:
        """
        Check whether a column exists in the dataset.

        Args:
            column: Name of the column to check.

        Returns:
            True if the column exists, False otherwise.
        """
        return column in self._data.columns

    def get_cities(self) -> list[str]:
        """
        Extract unique city names from the dataset based on column naming.

        The dataset columns use a naming convention such as
        `<CITY>_temp_mean`. This method extracts the `<CITY>`
        portion (before the first underscore) and returns the
        unique list of cities.

        Returns:
            A list of unique city identifiers (strings).
        """
        cities = self._data.columns[self._data.columns.str.contains("_")].str.split("_").str[0].unique().tolist()
        for i in range(len(cities)):
            # Special case since this is the only city name with two words.
            # Prevents second half from being cut off.
            if cities[i] == "DE":
                cities[i] = "DE_BILT"

        logger.info("Detected cities: %s", cities)
        return cities

    def has_city(self, city_name) -> bool:
        return city_name in self.cities

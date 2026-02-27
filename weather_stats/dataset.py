import pandas as pd
import logging

logger = logging.getLogger(__name__)

class WeatherDataset:
    """
    Wrapper around a pandas DataFrame that represents weather data.

    Attributes:
        _data: The underlying pandas DataFrame containing weather data.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"UT_temp_mean": [30, 40]})
        >>> dataset = WeatherDataset(df)
        >>> dataset.get_column_names()
        ['UT_temp_mean']
        >>> dataset.has_city("UT")
        True
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize a WeatherDataset.

        Args:
            data: A pandas DataFrame containing weather measurements.
        """
        self._data = data
        self._data['DATE'] = pd.to_datetime(data['DATE'], format='%Y%m%d')
        self._data = self._data.set_index('DATE')
        self._cities = self.get_cities()

    def __iter__(self):
        for city in self._cities:
            yield city

    def get_data(self) -> pd.DataFrame:
        """
        Return the underlying pandas DataFrame.

        Returns:
            The stored pandas DataFrame.
        """
        return self._data

    def get_column_names(self) -> list[str]:
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

        Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"UT_temp_mean": [30]})
        >>> dataset = WeatherDataset(df)
        >>> dataset.has_column("UT_temp_mean")
        True
        >>> dataset.has_column("CA_temp_mean")
        False
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

        Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     "UT_temp_mean": [30],
        ...     "CA_temp_mean": [60]
        ... })
        >>> dataset = WeatherDataset(df)
        >>> sorted(dataset.get_cities())
        ['CA', 'UT']
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
        """
        Check whether a given city identifier is present in the dataset.

        Args:
            city_name: The city identifier to check (for example ``'UT'`` or ``'DE_BILT'``).

        Returns:
            True if the city is present in the dataset's detected cities, False otherwise.

        Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"UT_temp_mean": [30], "DE_temp_mean": [40]})
        >>> dataset = WeatherDataset(df)
        >>> dataset.has_city("UT")
        True
        >>> dataset.has_city("NO_SUCH_CITY")
        False
        """
        return city_name in self._cities

    def filter_by_month(self, month: int) -> pd.DataFrame:
        """
        Filter the dataset to include only rows from a specific month across all years.

        Args:
            month: The month to filter by (1-12).

        Returns:
            A new DataFrame containing only rows from the specified month.
        """
        return self._data[self._data.index.month == month]

    def filter_by_year(self, year: int) -> pd.DataFrame:
        """
        Filter the dataset to include only rows from a specific year.

        Args:
            year: The year to filter by (e.g., 2020).
        Returns:
            A new DataFrame containing only rows from the specified year.
        """
        return self._data[self._data.index.year == year]

    def filter_by_month_and_year(self, month: int, year: int) -> pd.DataFrame:
        """
        Filter the dataset to include only rows from a specific month and year.

        Args:
            month: The month to filter by (1-12).
            year: The year to filter by (e.g., 2020).

        Returns:
            A new DataFrame containing only rows from the specified month and year.
        """
        return self._data[(self._data.index.month == month) & (self._data.index.year == year)]

    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter the dataset to include only rows within a specific date range.

        Args:
            start_date: The start date of the range (inclusive) in 'YYYY-MM-DD' format.
            end_date: The end date of the range (inclusive) in 'YYYY-MM-DD' format.

        Returns:
            A new DataFrame containing only rows within the specified date range.
        """

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self._data.loc[start:end]

    def filter_by_season(self, season: str) -> pd.DataFrame:
        """
        Filter the dataset to include only rows from a specific season.

        Seasons are defined as follows:
            - Spring: March 1 to May 31
            - Summer: June 1 to August 31
            - Fall: September 1 to November 30
            - Winter: December 1 to February 28/29

        Args:
            season: The season to filter by ('spring', 'summer', 'fall', 'winter').

        Returns:
            A new DataFrame containing only rows from the specified season.
        """
        season = season.lower()
        if season == 'spring':
            return self._data[(self._data.index.month >= 3) & (self._data.index.month <= 5)]
        elif season == 'summer':
            return self._data[(self._data.index.month >= 6) & (self._data.index.month <= 8)]
        elif season == 'fall':
            return self._data[(self._data.index.month >= 9) & (self._data.index.month <= 11)]
        elif season == 'winter':
            return self._data[(self._data.index.month == 12) | (self._data.index.month <= 2)]
        else:
            raise ValueError("Invalid season. Must be one of: 'spring', 'summer', 'fall', 'winter'.")






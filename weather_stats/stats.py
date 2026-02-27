"""
Statistical helpers for weather datasets.

Provides the `WeatherStats` class which computes descriptive statistics
for numeric columns in a `WeatherDataset`.
"""
from typing import Iterator

import pandas as pd
from typing import Optional
from weather_stats.dataset import WeatherDataset
import logging

logger = logging.getLogger(__name__)

class WeatherStats:
    """
    Compute descriptive statistics for a WeatherDataset.

    The class caches the underlying DataFrame for repeated computations.

    Example:
        >>> import pandas as pd
        >>> from weather_stats.dataset import WeatherDataset
        >>> df = pd.DataFrame({"UT_temp_mean": [10, 20, 30]})
        >>> dataset = WeatherDataset(df)
        >>> stats = WeatherStats(dataset)
        >>> stats.mean("UT_temp_mean")
        20.0
    """

    def __init__(self, dataset: WeatherDataset):
        """
        Create a WeatherStats instance.

        Args:
            dataset: The WeatherDataset to compute statistics on.
        """
        self._dataset = dataset
        self._data = dataset.get_data()

    def mean(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the mean of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The mean as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        mean = df[column].mean()
        logger.debug(f"{column}: {mean}")
        return mean

    def median(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the median of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.


        Returns:
            The median as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        return df[column].median()

    def min(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the minimum of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The minimum as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        return df[column].min()

    def max(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the maximum of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The maximum as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        return df[column].max()

    def std_dev(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the standard deviation of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The standard deviation as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        return df[column].std()

    def range(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the range of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The range as a float.

        Example:
                >>> import pandas as pd
                >>> from weather_stats.dataset import WeatherDataset
                >>> df = pd.DataFrame({"UT_temp_mean": [10, 30]})
                >>> stats = WeatherStats(WeatherDataset(df))
                >>> stats.range("UT_temp_mean")
                20
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        return self.max(column, df) - self.min(column, df)

    def mode(self, column: str, data: Optional[pd.DataFrame] = None) -> float:
        """
        Compute the mode of a column.

        Args:
            column: Column name.
            data: Optional DataFrame to use for computation. If None, uses the dataset's DataFrame.

        Returns:
            The mode as a float.
        """
        self._validate_column(column, data)
        df = data if data is not None else self._data
        modes = df[column].mode()
        if modes.empty:
            logger.warning("No mode found for column %s (empty or all-NaN series)", column)
            return float("nan")
        try:
            return float(modes.iloc[0])
        except (TypeError, ValueError):
            # fallback if mode value can't be converted to float
            return float("nan")

    def _validate_column(self, column: str, data: Optional[pd.DataFrame] = None):
        """
        Ensure the requested column exists in the dataset.

        Args:
            column: Column name to validate.

        Raises:
            ValueError: If the column does not exist.
        """
        df = data if data is not None else self._data
        if column not in df.columns:
            logger.error("Column %s does not exist in provided data", column)
            raise ValueError(f"Column '{column}' not found in dataset")

    def temperature_summary(self, city: str, data: Optional[pd.DataFrame] = None) -> Iterator[tuple[str, float]]:
        """
        Produce a temperature summary for a given city.

        Columns follow the pattern `<CITY>_temp_mean`.

        Args:
            city: The city identifier.
            data: Optional DataFrame. If provided, this will be used for all computations.

        Returns:
            Tuples of (statistic name, value).

        Example:
        >>> import pandas as pd
        >>> from weather_stats.dataset import WeatherDataset
        >>> df = pd.DataFrame({"UT_temp_mean": [10, 20, 30]})
        >>> stats = WeatherStats(WeatherDataset(df))
        >>> summary = dict(stats.temperature_summary("UT"))
        >>> summary["Mean"]
        20.0
        >>> summary["Range"]
        20
        """
        base = f"{city}_temp_mean"

        yield "Mean", self.mean(base, data)
        yield "Median", self.median(base, data)
        yield "Min", self.min(base, data)
        yield "Max", self.max(base, data)
        yield "Standard deviation", self.std_dev(base, data)
        yield "Range", self.range(base, data)
        yield "Mode", self.mode(base, data)

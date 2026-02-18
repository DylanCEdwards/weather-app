"""
Statistical helpers for weather datasets.

Provides the `WeatherStats` class which computes descriptive statistics
for numeric columns in a `WeatherDataset`.
"""
from typing import Iterator

class WeatherStats:
    """
    Compute descriptive statistics for a WeatherDataset.

    The class caches the underlying DataFrame for repeated computations.
    """

    def __init__(self, dataset):
        """
        Create a WeatherStats instance.

        Args:
            dataset: The WeatherDataset to compute statistics on.
        """
        self.dataset = dataset
        self.data = dataset.get_data()

    def mean(self, column: str) -> float:
        """
        Compute the mean of a column.

        Args:
            column: Column name.

        Returns:
            The mean as a float.
        """
        self._validate_column(column)
        return self.data[column].mean()

    def median(self, column: str) -> float:
        """
        Compute the median of a column.

        Args:
            column: Column name.

        Returns:
            The median as a float.
        """
        self._validate_column(column)
        return self.data[column].median()

    def min(self, column: str) -> float:
        """
        Compute the minimum of a column.

        Args:
            column: Column name.

        Returns:
            The minimum as a float.
        """
        self._validate_column(column)
        return self.data[column].min()

    def max(self, column: str) -> float:
        """
        Compute the maximum of a column.

        Args:
            column: Column name.

        Returns:
            The maximum as a float.
        """
        self._validate_column(column)
        return self.data[column].max()

    def std_dev(self, column: str) -> float:
        """
        Compute the standard deviation of a column.

        Args:
            column: Column name.

        Returns:
            The standard deviation as a float.
        """
        self._validate_column(column)
        return self.data[column].std()

    def range(self, column: str) -> float:
        """
        Compute the range of a column.

        Args:
            column: Column name.

        Returns:
            The range as a float.
        """
        self._validate_column(column)
        return self.max(column) - self.min(column)

    def mode(self, column: str) -> float:
        """
        Compute the mode of a column.

        Args:
            column: Column name.

        Returns:
            The mode as a float.
        """
        self._validate_column(column)
        return self.data[column].mode()[0]

    def _validate_column(self, column: str):
        """
        Ensure the requested column exists in the dataset.

        Args:
            column: Column name to validate.

        Raises:
            ValueError: If the column does not exist.
        """
        if not self.dataset.has_column(column):
            raise ValueError(f"Column '{column}' not found in dataset")

    def temperature_summary(self, city: str) -> Iterator[tuple[str, float]]:
        """
        Produce a temperature summary for a given city.

        Columns follow the pattern `<CITY>_temp_mean`.

        Args:
            city: The city identifier.

        Returns:
            Tuples of (statistic name, value).
        """
        base = f"{city}_temp_mean"
        yield "Mean", self.mean(base)
        yield "Median", self.median(base)
        yield "Min", self.min(base)
        yield "Max", self.max(base)
        yield "Standard deviation", self.std_dev(base)
        yield "Range", self.range(base)
        yield "Mode", self.mode(base)


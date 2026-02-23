import pandas as pd
import pytest
from weather_stats.loader import WeatherDataLoader
from weather_stats.dataset import WeatherDataset


def test_load_success(tmp_path):
    """
    Ensure that a valid CSV file is loaded and wrapped
    in a WeatherDataset.
    """
    # Create a temporary CSV file
    file_path = tmp_path / "sample.csv"
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02"],
        "temperature": [30, 40]
    })
    df.to_csv(file_path, index=False)

    # Load using WeatherDataLoader
    loader = WeatherDataLoader(str(file_path))
    dataset = loader.load()

    # Assertions
    assert isinstance(dataset, WeatherDataset)

    # Optional: if WeatherDataset exposes data
    assert dataset._data.shape == (2, 2)


def test_load_file_not_found():
    """
    Ensure that loading a nonexistent file raises FileNotFoundError.
    """
    loader = WeatherDataLoader("does_not_exist.csv")

    with pytest.raises(FileNotFoundError):
        loader.load()
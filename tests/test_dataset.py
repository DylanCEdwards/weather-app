import pytest
from weather_stats.dataset import WeatherDataset
import pandas as pd

def sample_dataframe():
    return pd.DataFrame({
        "SLC_temp_mean":[30, 40],
        "SLC_temp_max":[35, 45],
        "LA_temp_mean":[60, 65],
        "other_column":[1, 2]
    })

def test_get_data():
    df = sample_dataframe()
    dataset = WeatherDataset(df)
    assert dataset.get_data().equals(df)

def test_get_columns():
    df = sample_dataframe()
    dataset = WeatherDataset(df)

    columns = dataset.get_column_names()

    assert "SLC_temp_mean" in columns
    assert "LA_temp_mean" in columns
    assert len(columns) == 4

def test_has_column():
    df = sample_dataframe()
    dataset = WeatherDataset(df)

    assert dataset.has_column("SLC_temp_mean") is True
    assert dataset.has_column("nonexistent_column") is False

def test_get_cities():
    df = sample_dataframe()
    dataset = WeatherDataset(df)

    cities = dataset.get_cities()

    assert "SLC" in cities
    assert "LA" in cities

def test_has_city():
    df = sample_dataframe()
    dataset = WeatherDataset(df)

    assert dataset.has_city("SLC") is True
    assert dataset.has_city("NYC") is False

def test_special_case_de_bilt():
    df = pd.DataFrame({
        "DE_temp_mean": [10, 12],
        "UT_temp_mean": [30, 40]
    })

    dataset = WeatherDataset(df)
    cities = dataset.get_cities()

    assert "DE_BILT" in cities
    assert "DE" not in cities
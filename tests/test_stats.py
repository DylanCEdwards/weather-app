import pytest
from weather_stats.stats import WeatherStats
from weather_stats.dataset import WeatherDataset
import pandas as pd

def sample_dataframe():
    df = pd.DataFrame({
        "SLC_temp_mean":[30, 40, 50],
        "SLC_temp_max":[35, 45, 40],
        "LA_temp_mean":[70, 75, 70],
        "other_column":[1, 2, 1]
    })
    return WeatherDataset(df)

def test_mean():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.mean("SLC_temp_mean") == 40

def test_validate_column():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    with pytest.raises(ValueError):
        stats._validate_column("nonexistent_column")


def test_median():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.median("SLC_temp_max") == 40

def test_min():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.min("SLC_temp_mean") == 30

def test_max():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.max("SLC_temp_max") == 45

def test_std_dev():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.std_dev("SLC_temp_mean") == 10

def test_range():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.range("LA_temp_mean") == 5

def test_mode():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    assert stats.mode("LA_temp_mean") == 70

def test_temperature_summary():
    ds = sample_dataframe()
    stats = WeatherStats(ds)

    summary = dict(stats.temperature_summary("SLC"))

    assert summary["Mean"] == 40
    assert summary["Median"] == 40
    assert summary["Min"] == 30
    assert summary["Max"] == 50
    assert summary["Standard deviation"] == 10
    assert summary["Range"] == 20
    assert summary["Mode"] == 30
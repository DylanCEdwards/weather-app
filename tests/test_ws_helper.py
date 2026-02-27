import builtins
import pandas as pd
import pytest
from weather_stats.ws_helper import ask_until_valid, run_cli
from weather_stats.dataset import WeatherDataset
from weather_stats.stats import WeatherStats
from matplotlib import pyplot as plt


def test_ask_until_valid_success(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "5")
    val = ask_until_valid("Prompt: ", int, lambda v: 1 <= v <= 10, "bad")
    assert isinstance(val, int) and val == 5


def test_ask_until_valid_retries(monkeypatch, capsys):
    inputs = iter(["bad", "7"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    val = ask_until_valid("Prompt: ", int, lambda v: 1 <= v <= 10, "bad")
    assert val == 7
    captured = capsys.readouterr()
    assert "bad" in captured.out


def make_dataset():
    df = pd.DataFrame({
        "DATE": ["20200101", "20200201", "20200601"],
        "UT_temp_mean": [10.0, 20.0, 15.0]
    })
    return WeatherDataset(df)


def stub_plot(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    monkeypatch.setattr(plt, "close", lambda *a, **k: None)


def test_run_cli_all_time_summary(monkeypatch):
    dataset = make_dataset()
    stats = WeatherStats(dataset)
    # Inputs: select city UT, choose all-time summary (1), return to city (0), quit (Q)
    inputs = iter(["UT", "1", "0", "Q"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    stub_plot(monkeypatch)
    # Should complete without raising
    run_cli(dataset, stats)


def test_run_cli_date_range_filter(monkeypatch):
    dataset = make_dataset()
    stats = WeatherStats(dataset)
    # Inputs: UT, choose date-range (5), start, end, return to city, quit
    inputs = iter(["UT", "5", "2020-01-01", "2020-12-31", "0", "Q"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    stub_plot(monkeypatch)
    run_cli(dataset, stats)

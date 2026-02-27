"""
Command-line helper utilities for the weather_stats package.

Provides:
- `ask_until_valid` - prompt loop that parses and validates user input.
- `run_cli` - interactive CLI loop to pick a city, apply filters and display statistics.
"""
import logging
from typing import Callable, Optional, Any
import pandas as pd
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

def ask_until_valid(prompt: str,
                    parser: Callable[[str], Any],
                    validator: Optional[Callable[[Any], bool]] = None,
                    error_msg: str = "Invalid input.") -> Any:
    """
    Prompt the user until the input can be parsed and (optionally) validated.

    Args:
        prompt: Text shown to the user.
        parser: Callable that converts the raw string into the desired type.
        validator: Optional callable that returns True for acceptable parsed values.
        error_msg: Message printed and logged on failure.

    Returns:
        The parsed value when parsing and validation succeed.

    Example:
        >>> # parse integer between 1 and 12
        >>> val = ask_until_valid("Month: ", int, lambda v: 1 <= v <= 12, "Month must be 1-12")
        >>> isinstance(val, int)
        True
    """
    while True:
        raw = input(prompt)
        try:
            val = parser(raw)
        except Exception:
            logger.error(error_msg)
            print(error_msg)
            continue
        if validator and not validator(val):
            logger.warning(error_msg)
            print(error_msg)
            continue
        return val


def run_cli(dataset, stats):
    """
    Run the interactive command-line loop to select a city, apply filters and show statistics.

    The function lists available cities, prompts the user to choose a city (or 'Q' to quit),
    offers a set of filters (month, year, month+year, date-range, season), passes the
    filtered DataFrame to `stats.temperature_summary` and plots the results.

    Args:
        dataset: An object providing the same public interface as `WeatherDataset`
                 (get_cities, has_city, filter_by_*, get_data).
        stats: A `WeatherStats` instance used to compute statistics.

    Returns:
        None

    Example:
        >>> # called from main with proper dataset and stats objects
        >>> run_cli(dataset, stats)
    """
    results = []
    x_labels = []
    for city in dataset.get_cities():
        print(city)

    while True:
        user_choice = ask_until_valid("Enter a city name for weather data (Enter 'Q' to quit): ", lambda s: s.upper(), lambda s: s == "Q" or dataset.has_city(s), "City not found. Please try again.")
        if user_choice == "Q":
            print("Goodbye")
            break

        while True:
            print("Options:\n"
                  "     1. All-time summary\n"
                  "     2. Filter by month\n"
                  "     3. Filter by year\n"
                  "     4. Filter by month and year\n"
                  "     5. Filter by date range\n"
                  "     6. Filter by season\n"
                  "     0. Return to city selection\n")

            filter_choice = ask_until_valid("Choose a filter option (0-6): ", int, lambda v: 0 <= v <= 6,
                                            "Enter a number between 0 and 6.")

            filtered_dataframe = None
            graph_title = "All-time"
            try:
                # Skip #1 since the filters will default to using the full dataset if None is passed.
                # Filtering by month (all years)
                if filter_choice == 2:
                    month = ask_until_valid("Enter month (1-12): ", int, lambda m: 1 <= m <= 12, "Month must be 1-12")
                    filtered_dataframe = dataset.filter_by_month(month)
                    graph_title = f"{month} (all years)"
                # Filtering by year (all months)
                elif filter_choice == 3:
                    year = ask_until_valid("Enter year (2000 - 2010): ", int, lambda y: 2000 <= y <= 2010,
                                           "Year must be between 2000 and 2010")
                    filtered_dataframe = dataset.filter_by_year(year)
                    graph_title = f"{year}"
                # Filtering by month and year
                elif filter_choice == 4:
                    month = ask_until_valid("Enter month (1-12): ", int, lambda m: 1 <= m <= 12, "Month must be 1-12")
                    year = ask_until_valid("Enter year (2000 - 2010): ", int, lambda y: 2000 <= y <= 2010,
                                           "Year must be between 2000 and 2010")
                    filtered_dataframe = dataset.filter_by_month_and_year(month, year)
                    graph_title = f"{month}/{year}"
                # Filtering by date range
                elif filter_choice == 5:
                    start_date = ask_until_valid("Enter start date (YYYY-MM-DD): ",
                                                 lambda s: pd.to_datetime(s, format="%Y-%m-%d", errors="raise"),
                                                 None,
                                                 "Invalid date format")
                    end_date = ask_until_valid("Enter end date (YYYY-MM-DD): ",
                                               lambda s: pd.to_datetime(s, format="%Y-%m-%d", errors="raise"),
                                               None,
                                               "Invalid date format")
                    filtered_dataframe = dataset.filter_by_date_range(start_date, end_date)
                    graph_title = f"{start_date.date()} to {end_date.date()}"
                # Filtering by season (all years)
                elif filter_choice == 6:
                    season = ask_until_valid("Enter season (Winter, Spring, Summer, Fall): ",
                                             lambda s: s.title(),
                                             lambda s: s in {"Winter", "Spring", "Summer", "Fall"},
                                             "Invalid season")
                    filtered_dataframe = dataset.filter_by_season(season)
                    graph_title = f"{season} (all years)"
                # Return to city selection
                elif filter_choice == 0:
                    break

            except ValueError as e:
                # dataset methods can raise on invalid ranges; handle centrally
                print(f"Filter error: {e}")
                logger.error("Filter error: %s", e)
                continue

            filtered_weather_data = stats.temperature_summary(user_choice, filtered_dataframe)
            print(f"Temperature statistics for {user_choice}:")
            for stat, value in filtered_weather_data:
                print(f"{stat}: {value}")
                results.append(value)
                x_labels.append(stat if stat != "Standard deviation" else "Std Dev")

            plt.plot(results, 'o')
            plt.grid(True)
            plt.xticks(range(len(x_labels)), x_labels)
            plt.title(f"Weather trends: {user_choice} - {graph_title}")
            plt.ylabel("Temperature (°C)")
            plt.show()

            results.clear()
            x_labels.clear()
            plt.close()


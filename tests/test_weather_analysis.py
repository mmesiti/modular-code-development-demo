from os import path, remove
import filecmp
from weather_analysis.main import main, arithmetic_mean
import pytest

def test_pngs_produced():
    periods = ["2024-01","2024-02","2024-03"]
    plot_types = ["precipitation","temperature"]
    outputs = [f"{period}-{plot_type}.png" for period in periods for plot_type in plot_types]
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    main("./tests/reference_data/weather_data.csv")
    for filename in outputs:
        assert path.exists(filename)


def test_output_bit_equality():
    outputs = ["2024-01-precipitation.png", "2024-01-temperature.png"]
    main("./tests/reference_data/weather_data.csv")
    for filename in outputs:
        assert filecmp.cmp(filename,path.join("tests","reference_data",filename))


def test_mean():
    arr = [1.0,2.0,3.0,4.0]
    assert arithmetic_mean(arr) == pytest.approx(2.5)
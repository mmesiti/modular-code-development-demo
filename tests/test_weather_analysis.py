from os import path, remove
import filecmp
from weather_analysis.main import main, arithmetic_mean
import pytest

def get_filename(period,plot_type):
    return f"{period}-{plot_type}.png"

plot_types = ["precipitation","temperature"]
periods = ["2024-01","2024-02","2024-03"]

@pytest.fixture(scope="session")
def png_files():
    for filename in [get_filename(p,t) for p in periods for t in plot_types]:
        if path.exists(filename):
            remove(filename)
    main("./tests/reference_data/weather_data.csv")

@pytest.mark.parametrize("period",periods)
@pytest.mark.parametrize("plot_type",plot_types)
def test_png_produced(png_files,period,plot_type):    
    assert path.exists(get_filename(period,plot_type))

outputs_regression = ["2024-01-precipitation.png", "2024-01-temperature.png"]
@pytest.mark.parametrize("filename",outputs_regression)
def test_output_bit_equality(png_files,filename):
    assert filecmp.cmp(filename,path.join("tests","reference_data",filename))


def test_mean():
    arr = [1.0,2.0,3.0,4.0]
    assert arithmetic_mean(arr) == pytest.approx(2.5)


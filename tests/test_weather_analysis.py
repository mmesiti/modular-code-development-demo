from os import path, remove
import filecmp
from weather_analysis.main import main, arithmetic_mean, iterate_on_periods
import pytest
from subprocess import run

    
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

def test_pngs_produced_periods_by_args():
    periods = ["2024-05","2024-07"]
    plot_types = ["precipitation","temperature"]

    outputs = [f"{period}-{plot_type}.png" for period in periods for plot_type in plot_types]
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    run(["python","./weather_analysis/main.py","./tests/reference_data/weather_data.csv",",".join(periods)])
    for filename in outputs:
        assert path.exists(filename)

def test_single_pngs_produced_when_single_plot_active():
    periods = ["2024-01","2024-02","2024-03"]
    outputs = [f"{period}-combined.png" for period in periods]
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    main("./tests/reference_data/weather_data.csv",single_plots=True)
    for filename in outputs:
        assert path.exists(filename)

def test_pngs_single_png_produced_when_single_plot_by_args():
    periods = ["2024-05","2024-07"]
    outputs = [f"{period}-combined.png" for period in periods]
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    run(["python","./weather_analysis/main.py","./tests/reference_data/weather_data.csv",",".join(periods), "--single-plots"])
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


def test_iterate_on_periods():
    periods = ["A","B","C"]
    data =  {"A":"dataA","B":"dataB","C":"dataC"}
    def get_period_data(data,period):
        return data[period]

    periods_and_data_iterated_over = []

    def plot_function_spy(data,period):
        periods_and_data_iterated_over.append((data,period))

    iterate_on_periods(data,plot_function=plot_function_spy, periods=periods, get_period_data=get_period_data)

    assert len(periods_and_data_iterated_over) == len(periods)
    for p in periods:
        assert (data[p],p) in periods_and_data_iterated_over
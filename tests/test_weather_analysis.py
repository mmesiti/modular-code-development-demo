from os import path, remove
import filecmp
from weather_analysis.main import main

def test_png_produced():
    outputs = ["2024-01-precipitation.png", "2024-01-temperature.png"]
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
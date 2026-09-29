from os import path, remove
from weather_analysis.main import main

def test_png_produced():
    outputs = ["2024-01-precipitation.png", "2024-01-temperature.png"]
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    main("data/weather_data.csv")
    for filename in outputs:
        assert path.exists(filename)

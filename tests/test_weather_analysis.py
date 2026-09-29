from os import path, remove
import filecmp
from weather_analysis.main import main
import pytest

outputs = ["2024-01-precipitation.png", "2024-01-temperature.png"]

@pytest.fixture(scope="session")
def png_files():
    for filename in outputs:
        if path.exists(filename):
            remove(filename)
    main("./tests/reference_data/weather_data.csv")

@pytest.mark.parametrize("filename",outputs)
def test_png_produced(png_files,filename):
    assert path.exists(filename)

@pytest.mark.parametrize("filename",outputs)
def test_output_bit_equality(png_files,filename):
    assert filecmp.cmp(filename,path.join("tests","reference_data",filename))
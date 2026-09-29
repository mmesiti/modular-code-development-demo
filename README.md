# Weather data Analysis


## Installation

Use conda:
```bash
conda env create -f "weather-analysis.yml
```

Activate the environment.

## Usage

Make sure that a file with name `weather_data.csv`
is present in the current directory. 

Then:

```bash
python ./weather_analysis/main.py
```

will produce some plots.


## Testing

Test with pytest, with
```bash
python -m pytest ./tests
```

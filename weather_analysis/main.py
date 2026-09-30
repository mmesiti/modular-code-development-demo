#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt

def main(filename):

    data = read_and_index_data(filename)
    # keep only january data using datetime period indexing
    january = data.loc["2024-01"]

    make_temperature_plot(january)
    make_precipitation_plot(january)

def read_and_index_data(filename):
    # read data
    data = pd.read_csv(filename)
    
    # combine 'date' and 'time' into a single column 'recorded_at' as type datetime
    data["recorded_at"] = pd.to_datetime(data["date"] + " " + data["time"])
    
    # set 'recorded_at' as index for convenience
    data = data.set_index("recorded_at")
    return data

def make_temperature_plot(january):
    make_timeseries_plot(january,
                         column="air_temperature_celsius",
                         label="air temperature (C)",
                         color="red",
                         title="air temperature (C) at Helsinki airport",
                         filename="2024-01-temperature.png",
                         show_mean=True)
    

def make_precipitation_plot(january):
    make_timeseries_plot(january,
                         column="precipitation_mm",
                         label="precipitation (mm)",
                         color="blue",
                         title="precipitation (mm) at Helsinki airport",
                         filename="2024-01-precipitation.png")
    


def make_timeseries_plot(january,column,label,color,title,filename,show_mean=False):
    fig, ax = plt.subplots()
    
    ax.plot(
        january.index,
        january[column],
        label=label,
        color=color,
    )

    if show_mean:
        mean_value = january[column].mean()
    
        # mean value (as horizontal dashed line)
        ax.axhline(
                y=mean_value,
                label=f"mean {label}: {mean_value:.1f}",
                color=color,
                linestyle="--",
            )
        
    
    ax.set_title(title)
    ax.set_xlabel("date and time")
    ax.set_ylabel(label)
    ax.legend()
    ax.grid(True)
    
    # format x-axis for better date display
    fig.autofmt_xdate()

    fig.savefig(filename)
    
    


def arithmetic_mean(values):
    return sum(values)/len(values)

if __name__ == "__main__":
    main("weather_data.csv")

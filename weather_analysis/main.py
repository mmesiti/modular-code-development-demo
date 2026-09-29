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
    fig, ax = plt.subplots()
    
    # temperature time series
    ax.plot(
        january.index,
        january["air_temperature_celsius"],
        label="air temperature (C)",
        color="red",
    )
    
    mean_temp = arithmetic_mean(january["air_temperature_celsius"].values)
    
    # mean temperature (as horizontal dashed line)
    ax.axhline(
        y=mean_temp,
        label=f"mean air temperature (C): {mean_temp:.1f}",
        color="red",
        linestyle="--",
    )
    
    ax.set_title("air temperature (C) at Helsinki airport")
    ax.set_xlabel("date and time")
    ax.set_ylabel("air temperature (C)")
    ax.legend()
    ax.grid(True)
    
    # format x-axis for better date display
    fig.autofmt_xdate()
    
    fig.savefig("2024-01-temperature.png")
    

def make_precipitation_plot(january):
    make_timeseries_plot(january,
                         column="precipitation_mm",
                         label="precipitation (mm)",
                         color="blue",
                         title="precipitation (mm) at Helsinki airport",
                         filename="2024-01-precipitation.png")
    


def make_timeseries_plot(january,column,label,color,title,filename):
    fig, ax = plt.subplots()
    
    ax.plot(
        january.index,
        january[column],
        label=label,
        color=color,
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
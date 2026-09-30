#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from sys import argv

def main(data_filename,periods=["2024-01","2024-02","2024-03"]):

    data = read_and_index_data(data_filename)
    iterate_on_periods(
        data,
        plot_function=make_temperature_and_precipitation_plots,
        periods = periods)


def iterate_on_periods(data,plot_function, periods, get_period_data= lambda d,p: d.loc[p]):
    for period in periods:    
        month_data = get_period_data(data,period)
        plot_function(month_data,period)

    
def read_and_index_data(filename):
    # read data
    data = pd.read_csv(filename)
    
    # combine 'date' and 'time' into a single column 'recorded_at' as type datetime
    data["recorded_at"] = pd.to_datetime(data["date"] + " " + data["time"])
    
    # set 'recorded_at' as index for convenience
    data = data.set_index("recorded_at")
    return data

def make_temperature_and_precipitation_plots(month_data,period):
    make_temperature_plot(month_data,period)
    make_precipitation_plot(month_data,period)


def make_temperature_plot(month_data,period):
    make_timeseries_plot(month_data,
                         column="air_temperature_celsius",
                         label="air temperature (C)",
                         color="red",
                         title="air temperature (C) at Helsinki airport",
                         filename=f"{period}-temperature.png",
                         show_mean=True)
    

def make_precipitation_plot(month_data,period):
    make_timeseries_plot(month_data,
                         column="precipitation_mm",
                         label="precipitation (mm)",
                         color="blue",
                         title="precipitation (mm) at Helsinki airport",
                         filename=f"{period}-precipitation.png")
    


def make_timeseries_plot(period_data,column,label,color,title,filename,show_mean=False):
    fig, ax = plt.subplots()
    
    ax.plot(
        period_data.index,
        period_data[column],
        label=label,
        color=color,
    )

    if show_mean:
        mean_value = period_data[column].mean()
    
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
    main(argv[1], periods=argv[2:])

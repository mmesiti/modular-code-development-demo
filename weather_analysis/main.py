#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt

def main(data_filename):

    data = read_and_index_data(data_filename)
    # keep only january data using datetime period indexing


    periods = ["2024-01","2024-02","2024-03"]
  
    for period in periods:    
        month_data = data.loc[period]
        make_temperature_plot(month_data,period)
        make_precipitation_plot(month_data,period)

    

def read_and_index_data(filename):
    # read data
    data = pd.read_csv(filename)
    
    # combine 'date' and 'time' into a single column 'recorded_at' as type datetime
    data["recorded_at"] = pd.to_datetime(data["date"] + " " + data["time"])
    
    # set 'recorded_at' as index for convenience
    data = data.set_index("recorded_at")
    return data

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
        mean_temp = period_data[column].mean()
    
        # mean temperature (as horizontal dashed line)
        ax.axhline(
                y=mean_temp,
                label=f"mean {label}: {mean_temp:.1f}",
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

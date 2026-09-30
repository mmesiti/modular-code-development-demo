#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import argparse as ap

def main(data_filename,periods=["2024-01","2024-02","2024-03"],single_plots=False):

    data = read_and_index_data(data_filename)
    iterate_on_periods(
        data,
        plot_function=lambda md, p : make_temperature_and_precipitation_plots(md,p,single_plots),
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

def make_temperature_and_precipitation_plots(month_data,period,single_plot=False):
    if single_plot:
        fig,axes = plt.subplots(nrows=2,ncols=1,sharex=True)
        ax_temp, ax_prec = axes
    else:
        fig_temp,ax_temp = plt.subplots()
        fig_prec,ax_prec = plt.subplots()

    axes = {"temperature" : ax_temp, "precipitation": ax_prec}

    make_temperature_plot(month_data,period,axes["temperature"])
    make_precipitation_plot(month_data,period,axes["precipitation"])
    
    if single_plot:
        fig.autofmt_xdate()
        fig.savefig(f"{period}-combined.png")
    else:
        fig_temp.autofmt_xdate()
        fig_temp.savefig(f"{period}-temperature.png")
        fig_prec.autofmt_xdate()
        fig_prec.savefig(f"{period}-precipitation.png")
        
        



def make_temperature_plot(month_data,period,ax):
    make_timeseries_plot(month_data,
                         column="air_temperature_celsius",
                         label="air temperature (C)",
                         color="red",
                         title="air temperature (C) at Helsinki airport",
                         filename=f"{period}-temperature.png",
                         ax=ax,
                         show_mean=True)
    

def make_precipitation_plot(month_data,period,ax):
    make_timeseries_plot(month_data,
                         column="precipitation_mm",
                         label="precipitation (mm)",
                         color="blue",
                         title="precipitation (mm) at Helsinki airport",
                         ax=ax,
                         filename=f"{period}-precipitation.png")
    


def make_timeseries_plot(period_data,column,label,color,title,filename,ax,show_mean=False):
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

    
def arithmetic_mean(values):
    return sum(values)/len(values)

def parse_args():
    parser = ap.ArgumentParser("Plot weather data")
    parser.add_argument("data_file",type=str)
    parser.add_argument("periods",type=str,
                        default="2024-01",
                        help="Comma-separated list of months. Example: 2024-01,2024-02")
    parser.add_argument("--single-plots",
                        action="store_true",
                        help="Produce a combined plot for each month")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(data_filename=args.data_file,periods=args.periods.split(","),single_plots=args.single_plots)

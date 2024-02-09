"""module datetime to get format object and colored to get colored object for console"""

import os
from datetime import datetime
import argparse
import calendar
from termcolor import colored

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = []

def yearly_weather_data(year, folderpath):
    """Function to read yearly data"""
    for i in months:
        file_path = os.path.join(folderpath, f"lahore_weather_{year}_{i}.txt")
        if not os.path.exists(file_path):
            return None

        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()[2:-1]
            for line in lines:
                temp = line.split(",")
                if temp[1] and temp[3] and temp[7]:
                    data.append({
                        'date': datetime.strptime(temp[0], '%Y-%m-%d').strftime('%B %d'),
                        'temp_max': int(temp[1]),
                        'temp_min': int(temp[3]),
                        'humidity': int(temp[7])
                    })

def monthly_weather_data(year, month, folderpath):
    """Function to read monthly data"""
    month_name = calendar.month_abbr[int(month)]
    file_path = os.path.join(folderpath, f"lahore_weather_{year}_{month_name}.txt")
    if not os.path.exists(file_path):
        return None
    monthly_data = []
    with open(file_path, encoding="utf-8") as file:
        lines = file.readlines()[2:-1]
        for line in lines:
            temp = line.split(",")
            if month and temp[0].split("-")[1].lower() != month:
                continue
            if temp[1] and temp[3] and temp[7]:
                monthly_data.append({
                    'date': datetime.strptime(temp[0], '%Y-%m-%d').strftime('%d'),
                    'temp_max': int(temp[1]),
                    'temp_min': int(temp[3]),
                    'humidity': int(temp[7])
                })
    return monthly_data

def highest_lowest_temperature(d):
    """Function to find highest and lowest temperature data"""
    if not d:
        return None

    highest_temp = d[0]
    lowest_temp = d[0]

    for i in d:
        if i['temp_max'] > highest_temp['temp_max']:
            highest_temp = i
        if i['temp_min'] < lowest_temp['temp_min']:
            lowest_temp = i

    return highest_temp, lowest_temp

def highest_humidity(d):
    """Function to get highest humidity data"""
    if not d:
        return None

    high_humidity = d[0]

    for i in d:
        if i['humidity'] > high_humidity['humidity']:
            high_humidity = i

    return high_humidity

def average_data(d):
    """Function to get average temperature and humidity data"""
    if not d:
        return None

    temp_max = 0
    temp_min = 0
    humidity = 0

    for i in d:
        temp_max += i['temp_max']
        temp_min += i['temp_min']
        humidity += i['humidity']

    data_points = len(d)
    avg_temp_max = temp_max / data_points
    avg_temp_min = temp_min / data_points
    avg_humidity = humidity / data_points

    return avg_temp_max, avg_temp_min, avg_humidity

def draw_bar_chart(chart_data):
    """Function to get chart data"""
    for d in chart_data:
        print(f"{d['date']} {colored('+' * d['temp_max'], 'red')} {d['temp_max']}C")
        print(f"{d['date']} {colored('+' * d['temp_min'], 'blue')} {d['temp_min']}C")

def draw_singleline_bar_chart(chart_data):
    """Function to get singleline chart data"""
    for d in chart_data:
        print(f"{d['date']} {colored('+' * d['temp_min'], 'blue')}"
        f"{colored('+' * d['temp_max'], 'red')} {d['temp_min']}C - {d['temp_max']}C")

def main():
    """Main function defines arguments and its use cases"""
    parser = argparse.ArgumentParser(description="Generate weather reports.")
    parser.add_argument("-e", "--year", type=int,
    help="Get highest, lowest temperature, and humidity for a given year")
    parser.add_argument("-a", "--avg", metavar=("year/month"),
    help="Get average temperature and humidity for a given month")
    parser.add_argument("-c", "--chart", metavar=("year/month"),
    help="Draw a horizontal bar chart for a given month")
    parser.add_argument("-cb", "--chartbar", metavar=("year/month"),
    help="Draw a horizontal bar chart for a given month")
    parser.add_argument("path", type=str, help="Path to the weather data folder")

    args = parser.parse_args()

    if args.year:
        yearly_weather_data(args.year, args.path)
        yearly_data = data
        if yearly_data:
            highest_temp, lowest_temp = highest_lowest_temperature(yearly_data)
            highest_humid= highest_humidity(yearly_data)
            print(f"Highest: {highest_temp['temp_max']}C on {highest_temp['date']}")
            print(f"Lowest: {lowest_temp['temp_min']}C on {lowest_temp['date']}")
            print(f"Humid: {highest_humid['humidity']}% on {highest_humid['date']}")
        else:
            print("No data available for the specified year.")

    elif args.avg:
        year, month = args.avg.split('/')
        month = '{:01d}'.format(int(month))
        monthly_data = monthly_weather_data(year, month, args.path)
        if monthly_data:
            avg_temp_max, avg_temp_min, avg_humidity = average_data(monthly_data)
            print(f"Highest Average: {avg_temp_max:.0f}C")
            print(f"Lowest Average: {avg_temp_min:.0f}C")
            print(f"Average Humidity: {avg_humidity:.0f}%")
        else:
            print(f"No data available for {month}/{year}.")

    elif args.chart:
        year, month = args.chart.split('/')
        month = '{:01d}'.format(int(month))
        chart_data = monthly_weather_data(year, month, args.path)
        if chart_data:
            print(f"{datetime.strptime(month, '%m').strftime(f'%B {year}')}")
            draw_bar_chart(chart_data)
        else:
            print(f"No data available for {month}/{year}.")

    elif args.chartbar:
        year, month = args.chartbar.split('/')
        month = '{:01d}'.format(int(month))
        chart_data = monthly_weather_data(year, month, args.path)
        if chart_data:
            print(f"{datetime.strptime(month, '%m').strftime(f'%B {year}')}")
            draw_singleline_bar_chart(chart_data)
        else:
            print(f"No data available for {month}/{year}.")

if __name__ == "__main__":
    main()

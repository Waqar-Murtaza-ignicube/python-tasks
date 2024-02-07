"""module datetime to get format object and colored to get colored object for console"""
import os
from datetime import datetime
import argparse
import calendar
from termcolor import colored

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = []

def yearly_weather_data(year):
    for i in months:
        file_path = f"weatherdata/lahore_weather_{year}_{i}.txt"
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

def monthly_weather_data(year, month):
    month_name = calendar.month_abbr[int(month)]
    file_path = f"weatherdata/lahore_weather_{year}_{month_name}.txt"
    print(file_path)
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
    highest_temp = max(d, key=lambda x: x['temp_max'])
    lowest_temp = min(d, key=lambda x: x['temp_min'])
    return highest_temp, lowest_temp

def highest_lowest_humidity(d):
    highest_humidity = max(d, key=lambda x: x['humidity'])
    return highest_humidity

def average_data(d):
    if not d:
        return None, None, None
    avg_temp_max = sum(d['temp_max'] for d in d) / len(d)
    avg_temp_min = sum(d['temp_min'] for d in d) / len(d)
    avg_humidity = sum(d['humidity'] for d in d) / len(d)
    return avg_temp_max, avg_temp_min, avg_humidity

def draw_bar_chart(chart_data):
    for d in chart_data:
        print(f"{d['date']} {colored('+' * d['temp_max'], 'red')} {d['temp_max']}C")
        print(f"{d['date']} {colored('+' * d['temp_min'], 'blue')} {d['temp_min']}C")

    for d in chart_data:
        print(f"{d['date']} {colored('+' * d['temp_min'], 'blue')}"
        f"{colored('+' * d['temp_max'], 'red')} {d['temp_min']}C - {d['temp_max']}C")

def main():
    parser = argparse.ArgumentParser(description="Generate weather reports.")
    parser.add_argument("-e", "--year", type=int,
    help="Get highest, lowest temperature, and humidity for a given year")
    parser.add_argument("-a", "--avg", metavar=("year/month"),
    help="Get average temperature and humidity for a given month")
    parser.add_argument("-c", "--chart", metavar=("year/month"),
    help="Draw a horizontal bar chart for a given month")
    #parser.add_argument("path", help="give a folderpath")

    args = parser.parse_args()

    if args.year:
        yearly_weather_data(args.year)
        yearly_data = data
        if yearly_data:
            highest_temp, lowest_temp = highest_lowest_temperature(yearly_data)
            highest_humidity= highest_lowest_humidity(yearly_data)
            print(f"Highest: {highest_temp['temp_max']}C on {highest_temp['date']}")
            print(f"Lowest: {lowest_temp['temp_min']}C on {lowest_temp['date']}")
            print(f"Humid: {highest_humidity['humidity']}% on {highest_humidity['date']}")
        else:
            print("No data available for the specified year.")

    elif args.avg:
        year, month = args.avg.split('/')
        monthly_data = monthly_weather_data(year, month)
        if monthly_data:
            avg_temp_max, avg_temp_min, avg_humidity = average_data(monthly_data)
            print(f"Highest Average: {avg_temp_max:.0f}C")
            print(f"Lowest Average: {avg_temp_min:.0f}C")
            print(f"Average Humidity: {avg_humidity:.0f}%")
        else:
            print(f"No data available for {month}/{year}.")

    elif args.chart:
        year, month = args.chart.split('/')
        chart_data = monthly_weather_data(year, month)
        if chart_data:
            print(f"{datetime.strptime(month, '%m').strftime(f'%B {year}')}")
            draw_bar_chart(chart_data)
        else:
            print(f"No data available for {month}/{year}.")

if __name__ == "__main__":
    main()

"""module used for app are defined on top"""

import os
import csv
from datetime import datetime
import argparse
import calendar
from termcolor import colored

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class WeatherReport:
    """class to pair up similar set of functionality"""
    def __init__(self, year, folderpath, month):
        self.year = year
        self.folderpath = folderpath
        self.month = month

    def read_weather_data(self, file_path):
        """method to read data from file"""
        if not os.path.exists(file_path):
            return None

        data = []
        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()[1:-1]
            report_file = csv.DictReader(lines)
            for row in report_file:
                if row["Max TemperatureC"] == '':
                    continue
                if row["Min TemperatureC"] == '':
                    continue
                if row["Max Humidity"] == '':
                    continue
                row['Max TemperatureC'] = int(row['Max TemperatureC'])
                row['Min TemperatureC'] = int(row['Min TemperatureC'])
                row['Max Humidity'] = int(row['Max Humidity'])
                data.append(row)
        return data

    def data_filepath(self, file_type):
        """method to get data"""
        data = []
        if file_type == 'yearly':
            for index in self.month:
                file_path = os.path.join(self.folderpath, f"lahore_weather_{self.year}_{index}.txt")
                weather_data = self.read_weather_data(file_path)
                if weather_data:
                    data.extend(weather_data)
            return data

        if file_type == 'monthly':
            month = calendar.month_abbr[int(self.month)]
            file_path = os.path.join(self.folderpath, f"lahore_weather_{self.year}_{month}.txt")
            data.extend(self.read_weather_data(file_path))
        return data

    def high_low_temp(self, data):
        """method to find highest and lowest temperature and humidity data"""
        if not data:
            return None

        highest_temp = data[0]
        lowest_temp = data[0]
        high_humidity = data[0]

        for index in data:
            if index['Max TemperatureC'] > highest_temp['Max TemperatureC']:
                highest_temp = index
            if index['Min TemperatureC'] < lowest_temp['Min TemperatureC']:
                lowest_temp = index
            if index['Max Humidity'] > high_humidity['Max Humidity']:
                high_humidity = index

        return highest_temp, lowest_temp, high_humidity

    def average_data(self, data):
        """method to get average temperature and humidity data"""
        if not data:
            return None

        temp_max = 0
        temp_min = 0
        humidity = 0

        for index in data:
            temp_max += index['Max TemperatureC']
            temp_min += index['Min TemperatureC']
            humidity += index['Max Humidity']

        data_points = len(data)
        avg_temp_max = temp_max / data_points
        avg_temp_min = temp_min / data_points
        avg_humidity = humidity / data_points

        return avg_temp_max, avg_temp_min, avg_humidity

    def draw_bar_chart(self, chart_data, chart_type):
        """method to get bar chart data"""
        for index in chart_data:
            date = datetime.strptime(index['PKT'], '%Y-%m-%d').strftime('%d')
            if chart_type == "double-line":
                print(f"{date} {colored('+' * index['Max TemperatureC'], 'red' )}"
                f" {index['Max TemperatureC']}C")
                print(f"{date} {colored('+' * index['Min TemperatureC'], 'blue')}"
                f" {index['Min TemperatureC']}C")

            elif chart_type == "single-line":
                print(f"{date} {colored('+' * index['Min TemperatureC'], 'blue')}"
                f"{colored('+' * index['Max TemperatureC'], 'red')}"
                f" {index['Min TemperatureC']}C - {index['Max TemperatureC']}C")

def main():
    """Main function defines arguments and its use cases"""
    parser = argparse.ArgumentParser(description="Generate weather reports.")
    parser.add_argument("-e", "--year", type=int)
    parser.add_argument("-a", "--avg", metavar="year/month")
    parser.add_argument("-c", "--chart", metavar="year/month")
    parser.add_argument("-cb", "--chartbar", metavar="year/month")
    parser.add_argument("path", type=str, help="Path to the weather data folder")

    args = parser.parse_args()
    add_zero = '{:01d}'

    if args.year:
        data = WeatherReport(args.year, args.path, months)
        if data:
            cal_data = data.data_filepath("yearly")
            highest_temp, lowest_temp, highest_humid = data.high_low_temp(cal_data)
            max_date = datetime.strptime(highest_temp['PKT'], '%Y-%m-%d').strftime('%B %d')
            low_date = datetime.strptime(lowest_temp['PKT'], '%Y-%m-%d').strftime('%B %d')
            high_date = datetime.strptime(highest_humid['PKT'], '%Y-%m-%d').strftime('%B %d')
            print(f"Highest: {highest_temp['Max TemperatureC']}C on {max_date}")
            print(f"Lowest: {lowest_temp['Min TemperatureC']}C on {low_date}")
            print(f"Humid: {highest_humid['Max Humidity']}% on {high_date}")
        else:
            print("No data available for the specified year.")

    elif args.avg:
        year, month = args.avg.split('/')
        month = add_zero.format(int(month))
        data = WeatherReport(year, args.path, month)
        if data:
            cal_data = data.data_filepath("monthly")
            avg_temp_max, avg_temp_min, avg_humidity = data.average_data(cal_data)
            print(f"Highest Average: {avg_temp_max:.0f}C")
            print(f"Lowest Average: {avg_temp_min:.0f}C")
            print(f"Average Humidity: {avg_humidity:.0f}%")
        else:
            print(f"No data available for {month}/{year}.")

    elif args.chart:
        year, month = args.chart.split('/')
        month = add_zero.format(int(month))
        data = WeatherReport(year, args.path, month)
        if data:
            print(f"{datetime.strptime(month, '%m').strftime(f'%B {year}')}")
            data.draw_bar_chart(data.data_filepath("monthly"), chart_type="double-line")
        else:
            print(f"No data available for {month}/{year}.")

    elif args.chartbar:
        year, month = args.chartbar.split('/')
        month = add_zero.format(int(month))
        data = WeatherReport(year, args.path, month)
        if data:
            print(f"{datetime.strptime(month, '%m').strftime(f'%B {year}')}")
            data.draw_bar_chart(data.data_filepath("monthly"), chart_type="single-line")
        else:
            print(f"No data available for {month}/{year}.")

if __name__ == "__main__":
    main()

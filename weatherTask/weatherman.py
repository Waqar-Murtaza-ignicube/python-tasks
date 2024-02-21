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
    def __init__(self, year, folder_path, month):
        self.year = year
        self.folder_path = folder_path
        self.month = month

    def read_weather_data(self, file_path):
        """method to read data from file"""
        if not os.path.exists(file_path):
            return None

        data = []
        with open(file_path, encoding="utf-8") as file:
            lines = []
            for line in file:
                stripped_line = line.strip()
                if stripped_line:
                    lines.append(stripped_line)

            report_file = csv.DictReader(lines)
            for row in report_file:
                fields = ["Max TemperatureC", "Min TemperatureC", "Max Humidity"]
                date_key = 'PKT' if 'PKT' in row else 'PKST'
                # Skip the row if any of its fields have a None value or are empty strings
                if any(row[field] is None or row[field] == '' for field in fields):
                    continue

                row['Max TemperatureC'] = int(row['Max TemperatureC'])
                row['Min TemperatureC'] = int(row['Min TemperatureC'])
                row['Max Humidity'] = int(row['Max Humidity'])
                row[date_key] = datetime.strptime(row[date_key], '%Y-%m-%d')
                data.append(row)
        return data

    def data_filepath(self, file_type):
        """method to get data"""
        data = []
        if file_type == 'yearly':
            for month in self.month:
                file_path = os.path.join(self.folder_path, f"lahore_weather_{self.year}"
                                                           f"_{month}.txt")
                weather_data = self.read_weather_data(file_path)
                if weather_data:
                    data.extend(weather_data)
            return data

        if file_type == 'monthly':
            month = calendar.month_abbr[int(self.month)]
            file_path = os.path.join(self.folder_path, f"lahore_weather_{self.year}_{month}.txt")
            data.extend(self.read_weather_data(file_path))
        return data

    def high_low_temp(self, data):
        """method to find highest and lowest temperature and humidity data"""
        if not data:
            return None

        highest_temp = data[0]
        lowest_temp = data[0]
        high_humidity = data[0]

        for temp in data:
            if temp['Max TemperatureC'] > highest_temp['Max TemperatureC']:
                highest_temp = temp
            if temp['Min TemperatureC'] < lowest_temp['Min TemperatureC']:
                lowest_temp = temp
            if temp['Max Humidity'] > high_humidity['Max Humidity']:
                high_humidity = temp

        return highest_temp, lowest_temp, high_humidity

    def average_data(self, data):
        """method to get average temperature and humidity data"""
        if not data:
            return None

        temp_max = 0
        temp_min = 0
        humidity = 0

        for temp in data:
            temp_max += temp['Max TemperatureC']
            temp_min += temp['Min TemperatureC']
            humidity += temp['Max Humidity']

        data_points = len(data)
        avg_temp_max = temp_max / data_points
        avg_temp_min = temp_min / data_points
        avg_humidity = humidity / data_points

        return avg_temp_max, avg_temp_min, avg_humidity


class PrintReport:
    """method to pair up all prints"""
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def print_maxmin_temp(self, highest_temp, lowest_temp, highest_humid):
        """method to print max,min temp and humidity"""
        date_key = 'PKT' if 'PKT' in highest_temp else 'PKST'
        max_date = highest_temp[date_key].strftime('%B %d')
        low_date = lowest_temp['PKT'].strftime('%B %d')
        high_date = highest_humid['PKT'].strftime('%B %d')
        print(f"Highest: {highest_temp['Max TemperatureC']}C on {max_date}")
        print(f"Lowest: {lowest_temp['Min TemperatureC']}C on {low_date}")
        print(f"Humid: {highest_humid['Max Humidity']}% on {high_date}")

    def print_avg_temp(self, avg_temp_max, avg_temp_min, avg_humidity):
        """method to print avg temp and humidity"""
        print(f"Highest Average: {avg_temp_max:.0f}C")
        print(f"Lowest Average: {avg_temp_min:.0f}C")
        print(f"Average Humidity: {avg_humidity:.0f}%")

    def print_temp_chart(self, chart_data, chart_type):
        """method to print bar chart data"""
        print(f"{datetime.strptime(self.month, '%m').strftime(f'%B {self.year}')}")
        for temp in chart_data:
            date_key = 'PKT' if 'PKT' in temp else 'PKST'
            date = temp[date_key].strftime('%d')
            if chart_type == "double-line":
                print(f"{date} {colored('+' * temp['Max TemperatureC'], 'red' )}"
                      f" {temp['Max TemperatureC']}C")
                print(f"{date} {colored('+' * temp['Min TemperatureC'], 'blue')}"
                      f" {temp['Min TemperatureC']}C")

            elif chart_type == "single-line":
                print(f"{date} {colored('+' * temp['Min TemperatureC'], 'blue')}"
                      f"{colored('+' * temp['Max TemperatureC'], 'red')}"
                      f" {temp['Min TemperatureC']}C - {temp['Max TemperatureC']}C")

    def print_no_data_avail(self):
        """method to print if data is not available"""
        print(f"No data available for {self.month}/{self.year}.")


def main():
    """Main function defines arguments and its use cases"""
    parser = argparse.ArgumentParser(description="Generate weather reports.")
    parser.add_argument("-e", "--year", type=int)
    parser.add_argument("-a", "--avg", metavar="year/month")
    parser.add_argument("-c", "--chart", metavar="year/month")
    parser.add_argument("-cb", "--chart_bar", metavar="year/month")
    parser.add_argument("path", type=str, help="Path to the weather data folder")

    args = parser.parse_args()

    if args.year:
        yearly_data = WeatherReport(args.year, args.path, months)
        cal_data = yearly_data.data_filepath("yearly")
        highest_temp, lowest_temp, highest_humid = yearly_data.high_low_temp(cal_data)
        # making an instance of a printing class and calling its method
        maxmin_temp = PrintReport(args.year, None)
        maxmin_temp.print_maxmin_temp(highest_temp, lowest_temp, highest_humid)

    elif args.avg:
        year, month = args.avg.split('/')
        monthly_avg = WeatherReport(year, args.path, month)
        cal_data = monthly_avg.data_filepath("monthly")
        if cal_data:
            avg_temp_max, avg_temp_min, avg_humidity = monthly_avg.average_data(cal_data)
            # making an instance of a printing class and calling its method
            avg_temp = PrintReport(year, month)
            avg_temp.print_avg_temp(avg_temp_max, avg_temp_min, avg_humidity)
        else:
            not_available = PrintReport(year, month)
            not_available.print_no_data_avail()

    elif args.chart:
        year, month = args.chart.split('/')
        chart_data = WeatherReport(year, args.path, month)
        chart_report = chart_data.data_filepath("monthly")
        if chart_report:
            # making an instance of a printing class and calling its method
            draw_chart = PrintReport(year, month)
            draw_chart.print_temp_chart(chart_report, "double-line")
        else:
            not_available = PrintReport(year, month)
            not_available.print_no_data_avail()

    elif args.chart_bar:
        year, month = args.chart_bar.split('/')
        chart_data = WeatherReport(year, args.path, month)
        chart_report = chart_data.data_filepath("monthly")
        if chart_report:
            # making an instance of a printing class and calling its method
            draw_chart = PrintReport(year, month)
            draw_chart.print_temp_chart(chart_report, "single-line")
        else:
            not_available = PrintReport(year, month)
            not_available.print_no_data_avail()


if __name__ == "__main__":
    main()

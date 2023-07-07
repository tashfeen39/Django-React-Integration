from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import plotly.graph_objects as go
import json
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


def convert_price(price_str):
    if 'Crore' in price_str:
        value = float(price_str.split()[0]) * 10000000
    elif 'Lakh' in price_str:
        value = float(price_str.split()[0]) * 100000
    elif 'Arab' in price_str:
        value = float(price_str.split()[0]) * 1000000000
    else:
        value = float(price_str)
    return value


def convert_size(size_str):
    if 'Kanal' in size_str:
        value = float(size_str.split()[0]) * 20
    elif 'Marla' in size_str:
        value = float(size_str.split()[0])
    else:
        value = float(size_str)
    return value


def read_csv_data(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            price = convert_price(row['Price'])
            size = convert_size(row['Size'])
            data.append({'Price': price, 'Size': size})
    return data


def scrape(request):
    if request.method == 'GET':

        url1 = "https://www.zameen.com/Homes/Multan-15-1.html"
        url2 = "https://www.zameen.com/Homes/Lahore-1-1.html"

        data_m = []
        data_l = []

        html_text1 = requests.get(url1).text
        html_text2 = requests.get(url2).text

        soup1 = BeautifulSoup(html_text1)
        soup2 = BeautifulSoup(html_text2)

        houses_multan = soup1.find_all('li', class_='ef447dde')
        for house_multan in houses_multan:
            title_m = house_multan.find('h2', class_='c0df3811').text
            short_description_m = house_multan.find(
                'div', class_='cf36e19e').text
            location_m = house_multan.find('div', class_='_162e6469').text
            price_m = house_multan.find('span', class_='f343d9ce').text
            timestamp_m = house_multan.find('span', class_='d77ff1d8').text
            size_m = house_multan.find_all('div', class_='_1e0ca152 _026d7bff')

            data_m.append({
                'Title': title_m,
                'Short Description': short_description_m,
                'Location': location_m,
                'Price': price_m,
                'Timestamp': timestamp_m,
                'Size': size_m[1].text
            })

        houses_lahore = soup2.find_all('li', class_='ef447dde')
        for house_lahore in houses_lahore:
            title_l = house_lahore.find('h2', class_='c0df3811').text
            short_description_l = house_lahore.find(
                'div', class_='cf36e19e').text
            location_l = house_lahore.find('div', class_='_162e6469').text
            price_l = house_lahore.find('span', class_='f343d9ce').text
            timestamp_l = house_lahore.find('span', class_='d77ff1d8').text
            size_l = house_lahore.find_all('div', class_='_1e0ca152 _026d7bff')

            data_l.append({
                'Title': title_l,
                'Short Description': short_description_l,
                'Location': location_l,
                'Price': price_l,
                'Timestamp': timestamp_l,
                'Size': size_l[1].text
            })

        # Writing data in csv files
        csv_file_path = 'houses_multan.csv'
        fieldnames = ['Title', 'Short Description',
                      'Location', 'Price', 'Timestamp', 'Size']

        with open(csv_file_path, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_m)

        csv_file_path = 'houses_lahore.csv'

        with open(csv_file_path, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_l)

        csv_file_path1 = 'houses_multan.csv'
        data1 = read_csv_data(csv_file_path1)

        csv_file_path2 = 'houses_lahore.csv'
        data2 = read_csv_data(csv_file_path2)

        context = {
            'url1': url1,
            'url2': url2,
            'data1': data1,
            'data2': data2,
        }

        return JsonResponse(context, safe=False)
    else:
        return render(request, 'home.html')

#!/usr/bin/env python3
import os
import time
import xml.etree.ElementTree as ET
import sys
import json

try:
    import requests
except ImportError:
    print(json.dumps({"items": [{
        "title": "Please install Python requests",
        "subtitle": "Click to open the README of the repo",
        "arg": "README"}]}))
    sys.exit(1)

XML_URL = 'http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml'
XML_FILE = 'eurofxref-daily.xml'
TIME_FILE = 'last_fetch_time.txt'


def fetch_xml():
    response = requests.get(XML_URL)
    with open(XML_FILE, 'wb') as f:
        f.write(response.content)
    with open(TIME_FILE, 'w') as f:
        f.write(str(time.time()))


def is_data_stale():
    if not os.path.exists(XML_FILE) or not os.path.exists(TIME_FILE):
        return True
    with open(TIME_FILE, 'r') as f:
        last_fetch_time = float(f.read().strip())
    return (time.time() - last_fetch_time) >= 86400


def parse_xml():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    namespace = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    time_element = root.find(".//ns:Cube[@time]", namespace)
    update_time = time_element.attrib['time'] if time_element is not None else "Unknown"

    rates = {'EUR': 1.0}
    for cube in root.findall('.//ns:Cube/ns:Cube/ns:Cube', namespace):
        currency = cube.attrib['currency']
        rate = float(cube.attrib['rate'])
        rates[currency] = rate
    return rates, update_time


def convert_currency(base_currency, target_currencies, amount, rates):
    if base_currency not in rates:
        print(f"Base currency {base_currency} is not available.")
        sys.exit(1)

    base_rate = rates[base_currency]
    items = []

    for target_currency in target_currencies:
        if target_currency not in rates:
            print(f"Target currency {target_currency} is not available.")
            continue

        target_rate = rates[target_currency]
        converted_amount = (amount / base_rate) * target_rate

        if converted_amount >= 1:
            formatted_amount = f"{round(converted_amount, 2):.2f}"
        else:
            formatted_amount = f"{converted_amount:.2g}"

        items.append({
            "title": f"{target_currency} {formatted_amount}",
            "arg": formatted_amount
        })

    return items


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <base_currency> <target_currencies> [amount]")
        sys.exit(1)

    base_currency = sys.argv[1].upper()
    target_currencies = sys.argv[2].upper().split(',')
    amount = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    if is_data_stale():
        fetch_xml()
    rates, update_time = parse_xml()

    conversion_results = convert_currency(base_currency, target_currencies, amount, rates)

    # Append the data update time as the last item
    conversion_results.append({
        "title": f"Data Update time: {update_time}",
        "subtitle": "Select this to refresh the data next time",
        "arg": "refresh"
    })

    json_output = json.dumps({"items": conversion_results}, indent=4)
    print(json_output)

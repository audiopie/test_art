from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen


def get_root():
    try:
        url = urlopen('http://www.cbr.ru/scripts/XML_valFull.asp')
        return ET.parse(url)
    except ET.ParseError:
        print('Probably the page not found')


def get_list_currency():
    root = get_root()
    names = root.findall('.//Name')
    codes = root.findall('.//ISO_Char_Code')
    results = []
    for key, value in zip(names, codes):
        if value.text:
            row = {value.text: key.text}
            results.append(row)
    return results


def parse_id():
    root = get_root()
    item_ids = root.findall('./Item')
    codes = root.findall('.//ISO_Char_Code')
    currency_values = {}
    for k, v in zip(item_ids, codes):
        for i in k.attrib.values():
            currency_values[v.text] = i
    return currency_values


def get_day(date, code, data):
    item_id = ''
    currency_date = {'date': date, 'currency_rate': None}
    for key, value in data.items():
        if key == code:
            item_id = value
            break
    year, month, day = date.split('-')
    try:
        response = ET.parse(urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'))
        root = response.getroot()
        try:
            currency = root.find(f"./Valute[@ID='{item_id}']/Value").text.replace(',', '.')
            currency_date['date'] = date
            currency_date['currency_rate'] = currency
            return currency_date
        except AttributeError:
            print("No Attribute")
        finally:
            return currency_date
    except ET.ParseError:
        print('Error')


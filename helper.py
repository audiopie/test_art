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

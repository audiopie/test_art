from datetime import datetime
from urllib.request import urlopen
import xml.etree.ElementTree as ET


class CurrencyApi:

    def __init__(self):
        self.url = urlopen('http://www.cbr.ru/scripts/XML_valFull.asp')
        self.list_of_currencies = ET.parse(self.url)
        self.names = self.list_of_currencies.findall('.//Name')
        self.codes = self.list_of_currencies.findall('.//ISO_Char_Code')
        self.ids = self.list_of_currencies.findall('./Item')
        self.list_result = []
        self.currency_values = {}

    def get_list_currency(self):
        """ Парсим дом дерево и находим имя валют, код, сохраняем в массив."""
        for key, value in zip(self.names, self.codes):
            if value.text:
                row = {value.text: key.text}
                self.list_result.append(row)
        return self.list_result

    def parse_id(self):
        """ Парсим дом дерево и находим ID  валют, код."""
        for k, v in zip(self.ids, self.codes):
            for i in k.attrib.values():
                self.currency_values[v.text] = i
        return self.currency_values

    def get_day(self, date, code):
        """ Обрабатываем данные и отправляем запрос на получение значения курса за определенный день
            Возвращает словарь с курсом валюты и датой.
        """
        currency_date = {'date': date, 'currency_rate': None}
        year, month, day = date.split('-')
        try:
            response = ET.parse(urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'))
            root = response.getroot()
            try:
                currency = root.find(f"./Valute[@ID='{code}']/Value").text.replace(',', '.')
                currency_date['date'] = date
                currency_date['currency_rate'] = currency
                return currency_date
            except AttributeError:
                return "No Attribute"
            finally:
                return currency_date
        except ET.ParseError as e:
            return e

    def validate_date(self, date):
        """ Валидации даты, например 2020-02-30 не является корректной датой"""
        try:
            year, month, day = date.split('-')
            return datetime(int(year), int(month), int(day))
        except ValueError as e:
            return False

    def check_code(self, code):
        """ Валидируем код, не должен быть меньше трех символов и должен быть в списке валют"""
        if self.currency_values:
            codes = self.currency_values
        else:
            codes = self.parse_id()
        if len(code) == 3:
            for key, value in codes.items():
                if key == code:
                    return value
            else:
                return False
        else:
            return False

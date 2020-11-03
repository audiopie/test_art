import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen


class CurrencyApi:

    def __init__(self, url):
        self.list_of_currencies = url
        self.names = self.list_of_currencies.findall('.//Name')
        self.codes = self.list_of_currencies.findall('.//ISO_Char_Code')
        self.ids = self.list_of_currencies.findall('./Item')
        self.list_result = []
        self.currency_values = {}
        self.cache = {}

    def get_list_currency(self):
        """ Возвращаем массив валют"""
        for key, value in zip(self.names, self.codes):
            if value.text:
                row = {value.text: key.text}
                self.list_result.append(row)
        return self.list_result

    def parse_id(self):
        """ Возвращаем словарь ID валюты и его код"""
        for k, v in zip(self.ids, self.codes):
            for i in k.attrib.values():
                self.currency_values[v.text] = i
        return self.currency_values

    def get_day(self, date, code):
        """ Обрабатываем данные и отправляем запрос на получение значения курса за определенный день
            Возвращает словарь с курсом валюты и датой.
        """
        currency_date = {'date': date, 'currency_rate': None}
        if date not in self.cache:
            year, month, day = date.split('-')
            response = ET.parse(urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'))
            self.cache[date] = response
            return self.get_data_from_day(date, code, currency_date)
        else:
            return self.get_data_from_day(date, code, currency_date)

    def get_data_from_day(self, date, code, currency):
        currency_date = currency
        root = self.cache[date].getroot()
        currency = root.find(f"./Valute[@ID='{code}']/Value").text.replace(',', '.')
        currency_date['date'] = date
        currency_date['currency_rate'] = currency
        return currency_date

    @staticmethod
    def validate_date(date):
        """ Валидации даты, например 2020-02-30 не является корректной датой"""
        year, month, day = date.split('-')
        current_date = datetime.now()
        date = datetime(int(year), int(month), int(day))

        if date > current_date or date.year < 1992:
            raise AttributeError('Error: input date is future or past')
        return datetime(int(year), int(month), int(day))

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
                raise ValueError
        else:
            raise ValueError

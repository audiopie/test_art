import xml.etree.ElementTree as ET
from flask import Flask
from flask import jsonify, request, make_response
from urllib.request import urlopen
from helper import CurrencyApi

app = Flask(__name__)


@app.route('/currencies/api/v1.0/', methods=['GET'])
def get_currencies_list():
    """ Метод возвращает список валюты и наименование валют """
    return jsonify(helperAPI.get_list_currency())


@app.route('/exchange/api/v1.0/', methods=['GET'])
def exchange_rate_differential():
    """ Метод принимает две даты в формате YYYY-MM-DD и код валюты.
    Пример запроса: /exchange/api/v1.0/?date1=2002-03-02&date2=2020-03-02&code=USD
    Возвращает курсы валют за заданные даты и разницу между ними.
    """
    date1 = request.args.get('date1', type=str)
    date2 = request.args.get('date2', type=str)
    code = request.args.get('code', type=str).upper()
    if date1 == '' or date2 == '' or code == '':  # Если один из параметров пуст возвращается ответ о ошибке запроса
        return jsonify(f'Error: some data in requests is empty'), 400
    try:
        helperAPI.validate_date(date1)  # валидация даты
        helperAPI.validate_date(date2)  # валидация даты
        valid_code = helperAPI.check_code(code)  # валидация кода
    except AttributeError as e:
        return jsonify(str(e)), 400
    except ValueError:
        return jsonify("Error: input date is incorrect"), 400
    currency_date1 = helperAPI.get_day(date1, valid_code)
    currency_date2 = helperAPI.get_day(date2, valid_code)
    rate = float(currency_date1['currency_rate']) - float(currency_date2['currency_rate'])
    difference = f'Difference currency {code} relative to the RUB between ' \
                 f'date {date1} and date {date2} is {rate} RUB'
    return jsonify(currency_date1, currency_date2, difference)


if __name__ == "__main__":
    try:
        url = urlopen('http://www.cbr.ru/scripts/XML_valFull.asp')
        root = ET.parse(url)
        helperAPI = CurrencyApi(root)
        app.run(debug=False)
    except ET.ParseError:
        print("Неправильный URL адрес")
        exit()


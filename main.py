from flask import Flask
from flask import jsonify, request
from helper import CurrencyApi

app = Flask(__name__)


@app.route('/currencies/api/v1.0/', methods=['GET'])
def get_currencies_list():
    """ Метод возвращает список валюты и наименование валют """
    return jsonify(helperApi.get_list_currency())


@app.route('/exchange/api/v1.0/', methods=['GET'])
def exchange_rate_differential():
    """ Метод принимает две даты в формате YYYY-MM-DD и код валюты.
    Пример запроса: /exchange/api/v1.0/?date1=2002-03-02&date2=2020-03-02&code=USD
    Возвращает курсы валют за заданные даты и разницу между ними.
    """
    date1 = request.args.get('date1', type=str)
    date2 = request.args.get('date2', type=str)
    code = request.args.get('code', type=str).upper()
    valid_code = helperApi.check_code(code)
    if helperApi.validate_date(date1) and helperApi.validate_date(date2) and valid_code:
        currency_date1 = helperApi.get_day(date1, valid_code)
        currency_date2 = helperApi.get_day(date2, valid_code)
        rate = float(currency_date1['currency_rate']) - float(currency_date2['currency_rate'])
        difference = f'Difference currency {code} relative to the RUB between ' \
                     f'date {date1} and date {date2} is {rate} RUB'
        return jsonify(currency_date1, currency_date2, difference)
    else:
        return jsonify(f"Please check date {date1} or {date2} or code {code} it's incorrect")


if __name__ == "__main__":
    helperApi = CurrencyApi()
    app.run(debug=False)

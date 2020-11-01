from flask import Flask
from flask import jsonify, request
from helper import get_list_currency, get_day, parse_id, validate_date

app = Flask(__name__)


@app.route('/currencies/api/v1.0/', methods=['GET'])
def get_currencies_list():
    return jsonify(get_list_currency())


@app.route('/exchange/api/v1.0/', methods=['GET'])
def exchange_rate_differential():
    date1 = request.args.get('date1', type=str)
    date2 = request.args.get('date2', type=str)
    code = request.args.get('code', type=str)
    if date1 == '' or date2 == '' or code == '':
        return jsonify("One param of empty")
    if validate_date(date1) and validate_date(date2):
        get_currency_id = parse_id()
        currency_date1 = get_day(date1, code, get_currency_id)
        currency_date2 = get_day(date2, code, get_currency_id)
        rate = float(currency_date1['currency_rate']) - float(currency_date2['currency_rate'])
        difference = f'Difference currency {code} relative to the RUB between ' \
                     f'date {date1} and date {date2} is {rate} RUB'
        return jsonify(currency_date1, currency_date2, difference)
    else:
        return jsonify(f'Please check date {date1} or {date2} is incorrect')


if __name__ == "__main__":
    app.run()

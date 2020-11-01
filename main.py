from flask import Flask
from flask import jsonify, request
from helper import get_list_currency, get_day, parse_id

app = Flask(__name__)


@app.route('/currencies/api/v1.0/', methods=['GET'])
def get_currencies_list():
    return jsonify(get_list_currency())


# http://127.0.0.1:5000/exchange/api/v1.0/?date1=2020-10-30&date2=2020-09-01&code=EUR
@app.route('/exchange/api/v1.0/', methods=['GET'])
def exchange_rate_differential():
    date1 = request.args.get('date1', type=str)
    date2 = request.args.get('date2', type=str)
    code = request.args.get('code', type=str)
    if date1 == '' or date2 == '' or code == '':
        return jsonify("One param of empty")

    else:
        get_currency_id = parse_id()
        currency_date1 = get_day(date1, code, get_currency_id)
        currency_date2 = get_day(date2, code, get_currency_id)
        rate = float(currency_date1['currency_rate']) - float(currency_date2['currency_rate'])
        difference = f'Difference currency {code} relative to the RUB between ' \
                     f'date {date1} and date {date2} is {rate} RUB'
        return jsonify(currency_date1, currency_date2, difference)


if __name__ == "__main__":
    app.run()

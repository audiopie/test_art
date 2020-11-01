from flask import Flask
from flask import jsonify
from helper import get_list_currency

app = Flask(__name__)


@app.route('/currencies/api/v1.0/', methods=['GET'])
def get_currencies_list():
    return jsonify(get_list_currency())


if __name__ == "__main__":
    app.run()

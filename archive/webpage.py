#!/usr/bin/python

from flask import Flask, render_template
import src

app = Flask(__name__)


@app.route('/')
def hello_world():
    ny = src.get_NYISO_prices()

    prices = [("NY", ny)]


    return render_template('rt_prices.html', prices=prices)


if __name__ == '__main__':
    app.run()
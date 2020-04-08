# coding:utf8
import os
from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    #return render_template('index.html')
    return render_template('home.html')


if __name__ == '__main__':
    app.run()

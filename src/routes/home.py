from flask import Flask, Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/index')
def index():
    return render_template('index.html')
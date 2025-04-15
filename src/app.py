from flask import Flask, redirect, request, render_template, url_for
from routes.home import home

app = Flask(__name__)

app.register_blueprint(home, url_prefix='/home')


@app.route('/')
def index():
    return redirect(url_for('home.index'))
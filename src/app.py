from flask import Flask, redirect, request, render_template, url_for
from routes.home import home

app = Flask(__name__)

app.register_blueprint(home, url_prefix='/home')


@app.route('/')
def index():
    return redirect(url_for('home.index'))

@app.route('/sobrenos')
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/jogos')
def jogos():
    return render_template('jogos.html')

@app.route('/nelson-fight')
def nelson_fight():
    return render_template('nelson-fight.html')


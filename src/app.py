from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobrenos')
def sobrenos():
    return render_template('pages/sobrenos.html')

@app.route('/devlog')
def devlog():
    return render_template('pages/devlog.html')

@app.route('/jogos')
def jogos():
    return render_template('pages/jogos.html')

@app.route('/nelson-fight')
def nelsonfight():
    return render_template('pages/nelson-fight.html')


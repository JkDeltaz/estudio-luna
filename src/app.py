import os
from flask import Flask, render_template, request
import json

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        with open('static/dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)['users']
        for info in dados.values():
            if info['nome'].lower() == usuario.lower():
                tipo = info['tipo']
                return render_template('pages/access.html', nome=info['nome'], tipo=tipo)
        return render_template('index.html', nome=None, tipo=None)


if __name__ == '__main__':
    app.run(debug=True)
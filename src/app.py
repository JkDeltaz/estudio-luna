import os
from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "lunasecret" 

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', nome=session['usuario'])

@app.route('/sobrenos')
def sobrenos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/sobrenos.html')

@app.route('/devlog')
def devlog():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/devlog.html')

@app.route('/jogos')
def jogos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/jogos.html')

@app.route('/nelson-fight')
def nelsonfight():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/nelson-fight.html')

@app.route('/conta')
def conta():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        'pages/conta.html',
        nome=session.get('usuario'),
        tipo=session.get('tipo'),
        cargo=session.get('cargo')
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if not usuario or not senha:
            erro = "Preencha todos os campos."
            return render_template('loginpage.html', erro=erro)

        with open('static/dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)['users']

        for info in dados.values():
            if info['nome'].lower() == usuario.lower() and info['senha'] == senha:
                session['usuario'] = info['nome']
                session['tipo'] = info['tipo']
                session['cargo'] = info['cargo']
                return redirect(url_for('home')) 
        erro = "Usuário ou senha incorretos."
        return render_template('loginpage.html', erro=erro)
    # GET → mostra a tela de login
    return render_template('loginpage.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

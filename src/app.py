import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "lunasecret" 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    cargo = db.Column(db.String(50))
    descricao = db.Column(db.Text)  
    redes_sociais = db.Column(db.Text) 

# Rotas principais

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', nome=session['usuario'], theme=session.get('theme', 'light'))

@app.route('/config', methods=['GET', 'POST'])
def config():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_theme = session.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        session['theme'] = new_theme
        
        sucesso = f"{'Dark' if new_theme == 'dark' else 'Light'} mode ativado!"
        return render_template('config.html', sucesso=sucesso, theme=new_theme)
    
    return render_template('config.html', theme=session.get('theme', 'light'))

@app.route('/sobrenos')
def sobrenos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/sobrenos.html', theme=session.get('theme', 'light'))

@app.route('/posts')
def posts():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/posts.html', theme=session.get('theme', 'light'))

@app.route('/jogos')
def jogos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/jogos.html', theme=session.get('theme', 'light'))

@app.route('/nelson-fight')
def nelsonfight():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('pages/nelson-fight.html', theme=session.get('theme', 'light'))

@app.route('/conta')
def conta():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(nome=session['usuario']).first()
    
    if not usuario:
        return redirect(url_for('login'))
    
    return render_template(
        'pages/conta.html',
        nome=usuario.nome,
        tipo=usuario.tipo,
        cargo=usuario.cargo,
        descricao=usuario.descricao,
        redes_sociais=usuario.redes_sociais,
        theme=session.get('theme', 'light')
    )


# Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if not usuario or not senha:
            erro = "Preencha todos os campos."
            return render_template('loginpage.html', erro=erro)

        # Busca o usuário no banco
        user = Usuario.query.filter_by(nome=usuario, senha=senha).first()

        if user:
            session['usuario'] = user.nome
            session['tipo'] = user.tipo
            session['cargo'] = user.cargo
            return redirect(url_for('home'))
        else:
            erro = "Usuário ou senha incorretos."
            return render_template('loginpage.html', erro=erro)

    # GET → mostra a tela de login
    return render_template('loginpage.html')

# Cadastro

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('usuario')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')
        cargo = request.form.get('cargo')

        if not nome or not senha:
            erro = "Preencha todos os campos obrigatórios."
            return render_template('cadastro.html', erro=erro)

        # Verifica se já existe um usuário com esse nome
        existente = Usuario.query.filter_by(nome=nome).first()
        if existente:
            erro = "Esse nome de usuário já está em uso."
            return render_template('cadastro.html', erro=erro)

        # Cria e salva o novo usuário
        novo = Usuario(nome=nome, senha=senha, tipo=tipo, cargo=cargo)
        db.session.add(novo)
        db.session.commit()

        sucesso = "Conta criada com sucesso! Você já pode fazer login."
        return render_template('cadastro.html', sucesso=sucesso)

    return render_template('cadastro.html')

@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(nome=session['usuario']).first()
    
    if not usuario:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nova_descricao = request.form['descricao']
        nova_redes_sociais = request.form['redes_sociais']
        usuario.descricao = nova_descricao
        usuario.redes_sociais = nova_redes_sociais
        db.session.commit()
        return redirect(url_for('conta'))  # volta pro perfil

    return render_template('pages/editar_perfil.html', usuario=usuario, theme=session.get('theme', 'light'))
# Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Inicialização

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from datetime import datetime
from functions.uteis import read_data

app = Flask(__name__, static_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.config['SECRET_KEY'] = 'chave_secreta'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

def page_refresh():
	# Obtém a data e hora atuais
	agora = datetime.now()
	# Formata a data e a hora
	data_hora_formatada = agora.strftime("%Y-%m-%d %H:%M:%S")

	df_dados = read_data()
	# Cria Coluna Farol
	df_dados['farol'] = df_dados['status'] \
		.apply(lambda status: 'green' if status == 0 else 'red')
    
	df_dados['id'] = df_dados.reset_index()['index'] + 1
    
	df_dados.to_sql('cursos', db.engine, if_exists='replace', index=False)
	return (f"{data_hora_formatada}")

# Metodo Construtor 
class cursos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	empresa = db.Column(db.String(50))
	ambiente = db.Column(db.String(100))
	quantidade = db.Column(db.Integer)
	data_ultima_transacao = db.Column(db.String(50))
	hora_ultima_transacao = db.Column(db.String(50))
	gap_time = db.Column(db.String(50))
	status = db.Column(db.String(50))
	farol = db.Column(db.String(50))
     
	def __init__(self, empresa, ambiente, quantidade, data_ultima_transacao, hora_ultima_transacao, gap_time, status, farol):
		self.empresa = empresa
		self.ambiente = ambiente
		self.quantidade = quantidade
		self.data_ultima_transacao = data_ultima_transacao
		self.hora_ultima_transacao = hora_ultima_transacao
		self.gap_time = gap_time
		self.status = status
		self.farol = farol

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/home')
@login_required
def principal():
    date = page_refresh()
    return render_template("index.html", cursos=cursos.query.all(), date=date)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    dados = request.json
    login = dados.get('login')
    senha = dados.get('senha')

    # Verifica se o usuário e a senha existem no banco de dados
    usuario = Usuario.query.filter_by(login=login, senha=senha).first()

    if usuario:
        login_user(usuario)
        return jsonify({'autenticado': True})
    else:
        return jsonify({'autenticado': False})

@app.route('/home', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        # Usuário não autenticado, redireciona para a rota de login
        return redirect(url_for('login'))
    
    # Lógica da rota home
    date = page_refresh()
    return render_template('home.html', user=current_user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run()

from flask import Flask, render_template
from functions.uteis import read_data
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'

db = SQLAlchemy(app)


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


@app.route('/')
def principal():
	date = page_refresh()
	# Substitua o conteúdo da tabela pelo DataFrame
	return render_template("index.html", cursos=cursos.query.all(), date=date)

if __name__ == "__main__":
	
	with app.app_context():
		print("create db")
		db.create_all()
		app.run(debug=True)

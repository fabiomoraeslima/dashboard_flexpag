from flask import Flask, render_template, request, jsonify, redirect, url_for
from functions.uteis import read_querie, conn_producao_utilities, read_data
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flexpag.sqlite3'
app.config['SECRET_KEY'] = 'chave_secreta'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

def page_refresh():
	# Obtém a data e hora atuais
	agora = datetime.now()
	# Formata a data e a hora
	data_hora_formatada = agora.strftime("%Y-%m-%d %H:%M:%S")

	df_dados = read_querie()
	# Cria Coluna Farol

	df_dados['farol'] = df_dados['status'] \
		.apply(lambda status: 'green' if status == 0 else 'red')

	df_dados['id'] = df_dados.reset_index()['index'] + 1
	df_dados.to_sql('transacoes', db.engine, if_exists='replace', index=False)

	return (f"{data_hora_formatada}")

# Metodo Construtor 
class transacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    empresa = db.Column(db.String(50))
    ambiente = db.Column(db.String(100))
    quantidade = db.Column(db.Integer)
    data_ultima_transacao = db.Column(db.String(100))
    hora_ultima_transacao = db.Column(db.String(100))
    gap_time = db.Column(db.String(100))
    status = db.Column(db.String(50))
    farol = db.Column(db.String(50))
    
    def __init__(self, company_id, empresa, ambiente, quantidade, data_ultima_transacao, hora_ultima_transacao, gap_time, status, farol):
                self.company_id = company_id
                self.empresa = empresa
                self.ambiente = ambiente
                self.quantidade = quantidade
                self.data_ultima_transacao = data_ultima_transacao
                self.hora_ultima_transacao = hora_ultima_transacao
                self.gap_time = gap_time
                self.status = status
                self.farol = farol


# Função para formatar timedelta como string
def format_timedelta(value):
    if isinstance(value, timedelta):
        days, seconds = value.days, value.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days} days {hours:02}:{minutes:02}:{seconds:02}"
    return value
    
# Adicione o filtro ao ambiente Jinja do Flask
app.jinja_env.filters['format_timedelta'] = format_timedelta

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(50))


class notificacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/home')
@login_required
def principal():

    if not current_user.is_authenticated:
        # Usuário não autenticado, redireciona para a rota de login
        return redirect(url_for('login'))
    
    date = page_refresh()

    # Consulte a tabela notificacoes para determinar quais clientes foram notificados
    clientes_notificados = notificacoes.query.all()
    clientes_notificados = [cliente.cliente_id for cliente in clientes_notificados]

    user_conectado = current_user.login.split('-')[0]
    user_conectado = user_conectado.capitalize()

    return render_template("index.html", transacoes=transacoes.query.all(), date=date, clientes_notificados = clientes_notificados, user=user_conectado)

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

@app.route('/sobre')
@login_required
def sobre():

    user_conectado = current_user.login.split('-')[0]
    user_conectado = user_conectado.capitalize()
    
    return render_template('sobre.html', usuario={current_user.login}, user=user_conectado)

# Rota para marcar um status como enviado
@app.route('/notificar', methods=['POST'])
def notificar_cliente():
    data = request.json
    cliente_id = data['cliente_id']
    
    # Verificar se o farol do cliente é "red" e se ele ainda não foi notificado
    farol = obter_farol_do_cliente(cliente_id)

    print(cliente_foi_notificado(cliente_id))
    
    if farol == 'red' and cliente_foi_notificado(cliente_id) == False:
        # Inserir uma nova linha no banco de dados para notificar o cliente"
        
        db.session.execute(
            text('INSERT INTO notificacoes (cliente_id, data) VALUES (:cliente_id, CURRENT_TIMESTAMP)'),
            {'cliente_id': cliente_id}
            )
        db.session.commit()

        return jsonify({'message': 'Cliente notificado com sucesso!'}), 200
        
    else:
        return jsonify({'message': 'O cliente já está notificado ou o farol não é vermelho.'}), 200

def obter_farol_do_cliente(cliente_id):
    pass
    return 'red'

def cliente_foi_notificado(cliente_id):
    
    try:
        result = db.session.execute(
            text('select cliente_id from notificacoes where cliente_id = :cliente_id'),
            {'cliente_id': cliente_id}
        )

        # Verifica se há pelo menos uma linha retornada pela consulta
        rows = result.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
    except:
        return 

# Rota para marcar um status como enviado
@app.route('/normalizar', methods=['POST'])
def normalizar_cliente():
    data = request.json
    cliente_id = data['cliente_id']

    db.session.execute(
        text('delete from notificacoes where cliente_id = :cliente_id'),
            {'cliente_id': cliente_id}
        )
    db.session.commit()

    return jsonify({'message': 'Cliente notificado com sucesso!'}), 200

# Rota para marcar um status como enviado
@app.route('/limparNotificacoes', methods=['POST'])
def limparNotificacoes():

    db.session.execute(
        text('delete from notificacoes')
        )
    db.session.commit()

    return jsonify({'message': 'Notificações apagadas com sucesso!'}), 200

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
        app.run(debug=True, host='127.0.0.1', port=500)
import pandas as pd
import os
from sqlalchemy import create_engine

def read_data():
    # Specify the path to your CSV file
    csv_file_path = 'file/estudo_transacoes_web.csv'
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path,  delimiter='^')
    return df 

def conn_producao_utilities():
    url = "postgresql://fabio.monitoramento:M0nitF4b10@monitordb.flexpag.com:55432/producao_utilities_v2"
    engine = create_engine(url)
    
    try:
        conexao_banco = url
        conn = create_engine(conexao_banco)

        print("Database connected successfully")
        return conn

    except:
        return "Database not connected successfully"
        
def read_querie():
    
    # Obtém o caminho absoluto para o diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    sql_file_path = os.path.join(script_dir, 'sql', 'web_transactions.sql')
    
    # Abre o arquivo com a querie
    file = open(sql_file_path)
    sql = file.read()
    file.close()

    # Abre a conexao com o banco
    conn = conn_producao_utilities()
    
    # Executa a querie usando o pandas
    df = pd.read_sql_query(sql, conn)
    
    return df

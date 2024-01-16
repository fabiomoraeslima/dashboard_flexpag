import pandas as pd


def read_data():
    # Specify the path to your CSV file
    csv_file_path = 'file/estudo_transacoes_web.csv'
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path,  delimiter=';')
    return df 
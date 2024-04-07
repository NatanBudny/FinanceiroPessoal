import pandas as pd
import sqlite3
import os

# Função para extrair o mês e o ano do nome do arquivo
def extrair_mes_ano(nome_arquivo):
    partes = nome_arquivo.split('-')
    ano = partes[-1].split('.')[0]
    mes = partes[-2]
    return mes + '-' + ano

# Procurar por arquivos CSV no diretório atual
arquivos_csv = [arquivo for arquivo in os.listdir() if arquivo.endswith('.csv')]

if not arquivos_csv:
    print("Nenhum arquivo CSV encontrado no diretório.")
    exit()

# Escolher o primeiro arquivo encontrado
nome_arquivo = arquivos_csv[0]

# Ler o arquivo CSV
dados = pd.read_csv(nome_arquivo)

# Filtrar valores negativos
dados = dados[dados['amount'] > 0]

# Adicionar a coluna referenceMonth
dados['referenceMonth'] = extrair_mes_ano(nome_arquivo)

# Conectar ao banco de dados SQLite
conexao = sqlite3.connect('fatura_cartao.db')

# Salvar os dados no banco de dados
dados.to_sql('FaturaCartaoCredito', conexao, if_exists='append', index=False)

# Fechar a conexão com o banco de dados
conexao.close()

# Renomear o arquivo CSV para .processed
novo_nome_arquivo = nome_arquivo.replace('.csv', '.processed')
os.rename(nome_arquivo, novo_nome_arquivo)

print("Dados salvos com sucesso no banco de dados SQLite.")

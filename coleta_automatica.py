import requests
import pandas as pd

print("Iniciando a coleta automática de dados via API do IBGE...")

url_ibge = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

try:
    resposta = requests.get(url_ibge)

    if resposta.status_code == 200:
        dados_json = resposta.json()
        
        df_estados = pd.json_normalize(dados_json)
        
        df_estados_limpo = df_estados[['id', 'sigla', 'nome', 'regiao.nome']].copy()
        df_estados_limpo.columns = ['ID_Estado', 'UF', 'Nome_Estado', 'Regiao']
        
        df_estados_limpo = df_estados_limpo.sort_values('UF')
        
        nome_ficheiro = 'dimensao_estados_ibge.csv'
        df_estados_limpo.to_csv(nome_ficheiro, index=False, encoding='utf-8')
        
        print("Coleta concluída com sucesso!")
        print(f"O ficheiro '{nome_ficheiro}' foi gerado e salvo na pasta do projeto.")
        print("\nResumo dos 5 primeiros registos coletados:")
        print(df_estados_limpo.head())
        
    else:
        print(f"Erro ao conectar com a API. Código de erro web: {resposta.status_code}")

except Exception as e:
    print(f"Ocorreu um erro durante a execução do script: {e}")
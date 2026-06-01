import pandas as pd

print("--- 1. INICIANDO A LEITURA DOS ARQUIVOS ---")
caminho_acidentes = 'datatran2023.csv'
caminho_snv = 'SNV_202310A.xls'

print("A ler a base de acidentes...")
df_acidentes = pd.read_csv(caminho_acidentes, sep=';', encoding='latin1')

print("A ler a base de rodovias do DNIT...")
df_snv = pd.read_excel(caminho_snv, header=2)

print("\n--- 2. PREPARAÇÃO DAS CHAVES ESTRANGEIRAS ---")
df_acidentes.columns = df_acidentes.columns.str.lower().str.strip()
df_snv.columns = df_snv.columns.str.lower().str.strip()

df_acidentes['br'] = df_acidentes['br'].astype(str).str.replace(r'\.0$', '', regex=True)
df_snv['br'] = df_snv['br'].astype(str).str.replace(r'\.0$', '', regex=True)

df_acidentes['uf'] = df_acidentes['uf'].astype(str).str.upper().str.strip()
df_snv['uf'] = df_snv['uf'].astype(str).str.upper().str.strip()

df_snv_unica = df_snv.drop_duplicates(subset=['br', 'uf'], keep='first')

print("\n--- 3. INTEGRAÇÃO COM MERGE (LEFT JOIN) ---")
df_completo = pd.merge(df_acidentes, df_snv_unica, on=['br', 'uf'], how='left')

print("\nIntegração (JOIN) concluída com sucesso! 🚀")
print(f"A sua nova base enriquecida possui {df_completo.shape[0]} linhas e {df_completo.shape[1]} colunas.")

print("\n--- PRÉVIA DOS DADOS (Acidente + Detalhes da Via) ---")
print(df_completo[['id', 'uf', 'br', 'tipo de trecho', 'superfície federal']].head())
print("\n--- 4. TRANSFORMAÇÃO DE DADOS ---")
print("A processar datas...")
df_completo['data_inversa'] = pd.to_datetime(df_completo['data_inversa'], format='%Y-%m-%d', errors='coerce')

df_completo['ano'] = df_completo['data_inversa'].dt.year
df_completo['mes'] = df_completo['data_inversa'].dt.month
df_completo['fim_de_semana'] = df_completo['data_inversa'].dt.dayofweek >= 5

print("A padronizar textos...")
df_completo['municipio'] = df_completo['municipio'].astype(str).str.upper().str.strip()
df_completo['causa_acidente'] = df_completo['causa_acidente'].astype(str).str.capitalize().str.strip()

print("Transformações concluídas com sucesso! ✨")

print("\n--- 5. EXPORTAR A BASE FINAL PARA O DASHBOARD ---")
nome_ficheiro_final = 'base_pronta_dashboard.csv'
df_completo.to_csv(nome_ficheiro_final, sep=';', index=False, encoding='latin1')

print(f"Sucesso Total! O seu novo ficheiro '{nome_ficheiro_final}' foi guardado na sua pasta.")
print("Agora temos o motor perfeito para o Dashboard!")
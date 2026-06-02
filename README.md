# Projeto Final - Estudos Avançados de Banco de Dados

**Instituição:** Puc-Campinas 
**Disciplina:** Estudos Avançados de Banco de Dados  
**Grupo 5:** João Lunardini, Felipe Andretta, Gabriel Lopes, Matheus Roçafa

---

## Sobre o Projeto
Este projeto tem como objetivo aplicar, de forma integrada, os conceitos de bases de dados e engenharia de dados para desenvolver uma análise completa sobre os Acidentes nas Rodovias Federais do Brasil (2023). 

O projeto contempla todo o pipeline de Ciência de Dados (ETL): extração de bases públicas, limpeza, transformação, cruzamento de entidades relacionais (JOINs) e, por fim, a construção de dois Dashboards interativos utilizando Python e a biblioteca Dash.

## Arquitetura de Dados
Para garantir uma análise profunda e relacional, o projeto cruza duas fontes de dados governamentais distintas utilizando o Número da Rodovia como Chave Estrangeira:

1. **Tabela de Fatos (Acidentes):** Bases de dados de acidentes de trânsito de 2023, extraídas do portal de dados abertos da Polícia Rodoviária Federal (PRF).
2. **Tabela Dimensional (Rodovias):** Base de dados do Sistema Nacional de Viação (SNV), fornecida pelo DNIT, contendo as características físicas e jurisdicionais das vias brasileiras.

## Estrutura do Repositório
O projeto está dividido em três scripts principais:

`integracao.py`: O "Motor de Preparação". Lê os ficheiros originais, resolve inconsistências (limpeza de nulos, formatação de datas), realiza o cruzamento (LEFT JOIN) entre acidentes e detalhes da via, e exporta a base consolidada `base_pronta_dashboard.csv`.
`dashboard_visao_geral.py`: **Dashboard 1**. Um painel executivo focado em apresentar os principais KPIs (Total de Acidentes, Vítimas Fatais, Total de Feridos) e a evolução temporal das ocorrências.
`dashboard_exploracao.py`: **Dashboard 2**. Um painel analítico avançado e 100% interativo, que permite filtrar os acidentes por Estado (UF) e Fase do Dia. Conta com 5 visualizações dinâmicas: Top 10 Rodovias, Impacto Climático, Distribuição por Horário, Hierarquia de Causas (Treemap) e Gravidade por Tipo de Acidente (Barras Empilhadas).
`coleta_automatica.py:` [BONUS] Script de coleta de dados automatizada (API). Conecta-se à API pública do IBGE, extrai informações de Estados e Regiões em formato JSON e gera automaticamente a tabela dimensional dimensao_estados_ibge.csv

## Como Executar o Projeto Localmente

Para que o projeto funcione na sua máquina, siga as instruções abaixo:

**1. Pré-requisitos**
Certifique-se de que tem o Python instalado. No seu terminal, instale as bibliotecas necessárias:
```bash
pip install pandas dash dash-bootstrap-components plotly xlrd openpyxl

cd Projeto-Final-BD-Grupo-5

python dashboard_visao_geral.py

python dashboard_exploracao.py

python coleta_automatica.py
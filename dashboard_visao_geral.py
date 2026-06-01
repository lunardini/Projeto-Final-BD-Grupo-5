import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

print("A iniciar o servidor do Dashboard...")

df = pd.read_csv('base_pronta_dashboard.csv', sep=';', encoding='latin1')

total_acidentes = len(df)
total_mortos = df['mortos'].sum()
total_feridos = df['feridos_leves'].sum() + df['feridos_graves'].sum()

df_mes = df.groupby('mes').size().reset_index(name='Total')
fig_linha = px.line(df_mes, x='mes', y='Total', markers=True, 
                   title='Evolução Mensal de Acidentes (2023)',
                   labels={'mes': 'Mês do Ano', 'Total': 'Quantidade de Acidentes'},
                   template='plotly_white')
fig_linha.update_xaxes(tickmode='linear')

df_fds = df['fim_de_semana'].value_counts().reset_index()
df_fds['fim_de_semana'] = df_fds['fim_de_semana'].map({True: 'Fim de Semana', False: 'Dias Úteis'})
fig_pizza = px.pie(df_fds, names='fim_de_semana', values='count', 
                   title='Acidentes: Dias Úteis vs. Finais de Semana',
                   hole=0.4, color_discrete_sequence=['#2C3E50', '#E74C3C'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Visão Geral: Acidentes nas Rodovias Federais (2023)", 
                        className="text-center text-primary mt-4 mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total de Acidentes", className="card-title text-muted"),
                html.H2(f"{total_acidentes:,}".replace(',', '.'), className="text-dark fw-bold")
            ])
        ], className="shadow-sm text-center"), width=4),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Vítimas Fatais", className="card-title text-muted"),
                html.H2(f"{total_mortos:,.0f}".replace(',', '.'), className="text-danger fw-bold")
            ])
        ], className="shadow-sm text-center"), width=4),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total de Feridos", className="card-title text-muted"),
                html.H2(f"{total_feridos:,.0f}".replace(',', '.'), className="text-warning fw-bold")
            ])
        ], className="shadow-sm text-center"), width=4),
    ], className="mb-5"),

    # Linha dos Gráficos e Insights
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_linha), width=7),
        dbc.Col(dcc.Graph(figure=fig_pizza), width=5)
    ])
], fluid=True, className="bg-light pb-5")

if __name__ == '__main__':
    print("Dashboard pronto! Abra o seu navegador no endereço: http://127.0.0.1:8050")
    app.run(debug=True)
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv('base_pronta_dashboard.csv', sep=';', encoding='latin1')
df['hora'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.hour

app2 = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

opcoes_uf = [{'label': '🌎 Todos os Estados (Brasil)', 'value': 'Todos'}] + [{'label': str(uf), 'value': str(uf)} for uf in sorted(df['uf'].dropna().unique()) if str(uf) != 'nan']
opcoes_fase = [{'label': '🕒 Qualquer Horário', 'value': 'Todos'}] + [{'label': str(fase), 'value': str(fase)} for fase in sorted(df['fase_dia'].dropna().unique()) if str(fase) != 'nan']

app2.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("Exploração Interativa de Fatores de Risco", className="text-center text-primary mt-4 mb-2"), width=12)]),
    dbc.Row([
        dbc.Col([dcc.Dropdown(id='uf-dropdown', options=opcoes_uf, value='Todos', clearable=False)], width=6),
        dbc.Col([dcc.Dropdown(id='fase-dia-dropdown', options=opcoes_fase, value='Todos', clearable=False)], width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-br'), width=7),
        dbc.Col(dcc.Graph(id='donut-clima'), width=5),
    ]),
    dbc.Row([dbc.Col(dcc.Graph(id='hist-hora'), width=12)]),
], fluid=True)

@app2.callback(
    [Output('bar-br', 'figure'), Output('donut-clima', 'figure'), Output('hist-hora', 'figure')],
    [Input('uf-dropdown', 'value'), Input('fase-dia-dropdown', 'value')]
)
def atualizar_graficos(uf_selecionada, fase_selecionada):
    dff = df.copy()
    if uf_selecionada != 'Todos': dff = dff[dff['uf'] == uf_selecionada]
    if fase_selecionada != 'Todos': dff = dff[dff['fase_dia'] == fase_selecionada]
        
    fig1 = px.bar(dff.groupby('br').size().reset_index(name='Total').sort_values('Total', ascending=False).head(10), x='Total', y='br', orientation='h', title='Top 10 Rodovias')
    fig2 = px.pie(dff.groupby('condicao_meteorologica').size().reset_index(name='Total'), values='Total', names='condicao_meteorologica', title='Clima')
    fig3 = px.histogram(dff, x='hora', nbins=24, title='Distribuição por Hora')
    
    return fig1, fig2, fig3

if __name__ == '__main__':
    app2.run(debug=True, port=8051)
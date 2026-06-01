import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

print("A iniciar o servidor do Dashboard 2 (Exploracao Interativa)...")

df = pd.read_csv('base_pronta_dashboard.csv', sep=';', encoding='latin1')
df['hora'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.hour

app2 = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

opcoes_uf = [{'label': 'Todos os Estados (Brasil)', 'value': 'Todos'}] + [{'label': str(uf), 'value': str(uf)} for uf in sorted(df['uf'].dropna().unique()) if str(uf) != 'nan']
opcoes_fase = [{'label': 'Qualquer Horario', 'value': 'Todos'}] + [{'label': str(fase), 'value': str(fase)} for fase in sorted(df['fase_dia'].dropna().unique()) if str(fase) != 'nan']

app2.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("Exploracao Interativa de Fatores de Risco", className="text-center text-primary mt-4 mb-2"), width=12)]),
    
    dbc.Row([
        dbc.Col([dcc.Dropdown(id='uf-dropdown', options=opcoes_uf, value='Todos', clearable=False)], width=6),
        dbc.Col([dcc.Dropdown(id='fase-dia-dropdown', options=opcoes_fase, value='Todos', clearable=False)], width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-br'), width=7),
        dbc.Col(dcc.Graph(id='donut-clima'), width=5),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='treemap-causas'), width=7),
        dbc.Col(dcc.Graph(id='hist-hora'), width=5),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='stacked-tipo'), width=12)
    ])
], fluid=True)

@app2.callback(
    [Output('bar-br', 'figure'), 
     Output('donut-clima', 'figure'), 
     Output('hist-hora', 'figure'),
     Output('treemap-causas', 'figure'),
     Output('stacked-tipo', 'figure')],
    [Input('uf-dropdown', 'value'), Input('fase-dia-dropdown', 'value')]
)
def atualizar_graficos(uf_selecionada, fase_selecionada):
    dff = df.copy()
    
    if uf_selecionada != 'Todos': 
        dff = dff[dff['uf'] == uf_selecionada]
    if fase_selecionada != 'Todos': 
        dff = dff[dff['fase_dia'] == fase_selecionada]
        
    if dff.empty:
        vazio = px.scatter(title="Nenhum dado encontrado para este filtro.")
        return vazio, vazio, vazio, vazio, vazio

    dados_br = dff.groupby('br').size().reset_index(name='Total')
    dados_br = dados_br.sort_values('Total', ascending=False).head(10)
    dados_br['br'] = 'BR ' + dados_br['br'].astype(str)
    fig1 = px.bar(dados_br, x='Total', y='br', orientation='h', 
                  title='Top 10 Rodovias mais Perigosas', 
                  color='Total', 
                  color_continuous_scale=['#ff7f7f', '#d32f2f', '#8b0000'])
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
    
    dados_clima = dff.groupby('condicao_metereologica').size().reset_index(name='Total')
    fig2 = px.pie(dados_clima, values='Total', names='condicao_metereologica', title='Clima no Momento do Acidente', hole=0.4)
    
    fig3 = px.histogram(dff, x='hora', nbins=24, title='Distribuicao de Acidentes por Hora')
    
    dados_causas = dff.groupby('causa_acidente').size().reset_index(name='Total')
    dados_causas = dados_causas.sort_values('Total', ascending=False).head(12)
    dados_causas['Raiz'] = 'Causas Principais'
    fig4 = px.treemap(dados_causas, path=['Raiz', 'causa_acidente'], values='Total', title='Hierarquia das Causas', color='Total', color_continuous_scale='Blues')
    
    dados_tipo = dff.groupby('tipo_acidente')[['mortos', 'feridos_graves', 'feridos_leves']].sum().reset_index()
    dados_tipo['Total Vitimas'] = dados_tipo['mortos'] + dados_tipo['feridos_graves'] + dados_tipo['feridos_leves']
    dados_tipo = dados_tipo.sort_values('Total Vitimas', ascending=False).head(10)
    
    dados_tipo_melt = dados_tipo.melt(id_vars='tipo_acidente', value_vars=['mortos', 'feridos_graves', 'feridos_leves'], var_name='Gravidade', value_name='Quantidade')
    
    fig5 = px.bar(dados_tipo_melt, x='tipo_acidente', y='Quantidade', color='Gravidade', title='Gravidade por Tipo de Acidente (Top 10)', 
                  color_discrete_map={'mortos': 'black', 'feridos_graves': '#e74c3c', 'feridos_leves': '#f1c40f'})
    fig5.update_layout(xaxis_tickangle=-45)
    
    return fig1, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    app2.run(debug=True, port=8051)
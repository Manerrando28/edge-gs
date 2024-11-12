import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import pandas as pd
from dash.dependencies import Input, Output
import json

app = dash.Dash(__name__)

# Função para obter dados do servidor FIWARE
def obter_dados():
    url = "http://<SEU_ORION_BROKER_IP>:1026/v2/entities/<ID_DO_SEU_DISPOSITIVO>/attrs"
    headers = {
        'Fiware-Service': 'openiot',
        'Fiware-ServicePath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

# Função para criar dataframe com os dados obtidos
def criar_dataframe(dados):
    df = pd.DataFrame(dados)
    df['data'] = pd.to_datetime(df['data'])
    return df

# Layout do dashboard
app.layout = html.Div(children=[
    html.H1(children='Monitoramento de Sistema Solar'),

    dcc.Graph(
        id='grafico-temperatura',
        figure={
            'data': [
                go.Scatter(
                    x=[],
                    y=[],
                    mode='lines+markers'
                )
            ],
            'layout': {
                'title': 'Temperatura'
            }
        }
    ),

    dcc.Graph(
        id='grafico-umidade',
        figure={
            'data': [
                go.Scatter(
                    x=[],
                    y=[],
                    mode='lines+markers'
                )
            ],
            'layout': {
                'title': 'Umidade'
            }
        }
    ),

    dcc.Graph(
        id='grafico-luminosidade',
        figure={
            'data': [
                go.Scatter(
                    x=[],
                    y=[],
                    mode='lines+markers'
                )
            ],
            'layout': {
                'title': 'Luminosidade'
            }
        }
    ),

    dcc.Interval(
        id='intervalo-atualizacao',
        interval=60*1000,  # Atualiza a cada minuto
        n_intervals=0
    )
])

# Callback para atualizar os gráficos
@app.callback(
    [Output('grafico-temperatura', 'figure'),
     Output('grafico-umidade', 'figure'),
     Output('grafico-luminosidade', 'figure')],
    [Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_graficos(n):
    dados = obter_dados()
    df = criar_dataframe(dados)

    figura_temperatura = {
        'data': [go.Scatter(
            x=df['data'],
            y=df['temperatura'],
            mode='lines+markers'
        )],
        'layout': {
            'title': 'Temperatura'
        }
    }

    figura_umidade = {
        'data': [go.Scatter(
            x=df['data'],
            y=df['umidade'],
            mode='lines+markers'
        )],
        'layout': {
            'title': 'Umidade'
        }
    }

    figura_luminosidade = {
        'data': [go.Scatter(
            x=df['data'],
            y=df['luminosidade'],
            mode='lines+markers'
        )],
        'layout': {
            'title': 'Luminosidade'
        }
    }

    return figura_temperatura, figura_umidade, figura_luminosidade

if __name__ == '__main__':
    app.run_server(debug=True)

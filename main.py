import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from functions import ler_arduino
from threading import Thread
from sys import exit
import serial

contador_atualizacoes = 0
line = ler_arduino()
dados = line.split(',')
print(f'Última atualização: {pd.Timestamp.now()}')
print(line)
df_main = {
    'Temp_DHT11': [],
    'Umidade_DHT11': [],
    'Pressao_BMP180': [],
    'QualidadeAr': [],
    'Chuva': [],
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
url_theme2 = dbc.themes.VAPOR


# tema
vapor_template = go.layout.Template(
    layout=dict(
        title=dict(
            font=dict(size=24, color='#4FFBE2')  # Cor verde para o título
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo do gráfico transparente
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Fundo do papel (em torno do gráfico) transparente
        # Cor da linha do gráfico (roxo), Cor do texto no eixo x, Mostrar grade do eixo x, Cor da grade do eixo x
        colorway=['#6829AD'],  # Cor da linha do gráfico (roxo)
        xaxis=dict(color='#4FFBE2', showgrid=True,  gridcolor='#1C1C41'),
        # Cor do texto no eixo y, Mostrar grade do eixo y, Cor da grade do eixo y
        yaxis=dict(color='#4FFBE2', showgrid=True, gridcolor='#1C1C41')
    )
)
# app.layout.template = vapor_template
go.Figure().update_layout(template=vapor_template)
# Layout
app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset', data={'data': df_main}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('☁ Estação Meteorológica', style={'font-weight': 'bold', 'font-size': '26px', 'textAlign': 'center'}),
                        ], sm=12, align="center"),
                    ]),
                ])
            ], style={'height': '100%'})
        ], sm=12, lg=16),
    ], style={'height': '100%'}),
    dbc.Row(style={'margin-bottom': '20px'}), dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3('🌡️  Temperatura', style={'font-weight': 'bold', 'font-size': '14px', 'textAlign': 'center'}),
                                dcc.Graph(id='temp_graph', config={"displayModeBar": False, "showTips": False}),
                            ], sm=4, lg=12, align="center")  # Definindo o alinhamento para "center"
                        ])
                    ])
                ], style={'height': '90%'})
            ], sm=4, lg=6), dbc.Col([dbc.Card([dbc.CardBody([dbc.Row([dbc.Col([
                            html.H3('💧  Umidade', style={'font-weight': 'bold', 'font-size': '14px', 'textAlign': 'center'}),
                            dcc.Graph(id='umidade_graph', config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style={'height': '90%'})], sm=4, lg=6), ], style={'height': '90%'}),


    dbc.Row(style={'margin-bottom': '5px'}), dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3('🌬️  Pressão Atmosférica', style={'font-weight': 'bold', 'font-size': '14px', 'textAlign': 'center'}),
                                dcc.Graph(id='pre_graph', config={"displayModeBar": False, "showTips": False}),
                            ], sm=4, lg=12, align="center")  # Definindo o alinhamento para "center"
                        ])
                    ])
                ], style={'height': '90%'})
            ], sm=4, lg=6), dbc.Col([dbc.Card([dbc.CardBody([dbc.Row([dbc.Col([
                            html.H3('😷  Qualidade do Ar', style={'font-weight': 'bold', 'font-size': '14px', 'textAlign': 'center'}),
                            dcc.Graph(id='qual_ar_graph', config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style={'height': '90%'})], sm=4, lg=6), ], style={'height': '90%'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Temperatura', style={'font-weight': 'bold', 'font-size': '18px', 'textAlign': 'center'}),
                            html.H3(id='last_temp', style={'font-size': '48px', 'color': '#32FBE2', 'font-weight': 'bold', 'textAlign': 'center'}),
                        ])
                    ])
                ])
            ], style={'height': '100%'})
        ], sm=2, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Umidade', style={'font-weight': 'bold', 'font-size': '18px', 'textAlign': 'center'}),
                            html.H3(id='last_umidade', style={'font-weight': 'bold', 'font-size': '48px', 'color': '#32FBE2', 'textAlign': 'center'}),
                        ])
                    ])
                ])
            ], style={'height': '100%'})
        ], sm=2, lg=2),


        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Pressão Atmosférica', style={'font-weight': 'bold', 'font-size': '16px', 'textAlign': 'center'}),
                            html.H3(id='last_pre', style={'font-size': '40px', 'color': '#32FBE2', 'font-weight': 'bold', 'textAlign': 'center'}),
                        ])
                    ])
                ])
            ], style={'height': '100%'})
        ], sm=2, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Qualidade do Ar', style={'font-weight': 'bold', 'font-size': '18px', 'textAlign': 'center'}),
                            html.H3(id='last_quali_Ar', style={'font-weight': 'bold', 'font-size': '40px', 'color': '#32FBE2', 'textAlign': 'center'}),
                        ])
                    ])
                ])
            ], style={'height': '100%'})
        ], sm=2, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Chuva', style={'font-weight': 'bold', 'font-size': '18px', 'textAlign': 'center'}),
                            html.H3(id='last_chuva', style={'font-weight': 'bold', 'font-size': '35px', 'color': '#32FBE2', 'textAlign': 'center'}),
                        ])
                    ])
                ])
            ], style={'height': '100%'})
        ], sm=2, lg=2),
        dbc.Col([
            dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3('Temperatura', style={'font-weight': 'bold', 'font-size': '18px', 'textAlign': 'center'}),
                                html.H3(id='last_temp_f', style={'font-weight': 'bold', 'font-size': '48px', 'color': '#32FBE2', 'textAlign': 'center'}),
                            ])
                        ])
                    ])
                ], style={'height': '100%'})
            ], sm=2, lg=2),
    ], style={'height': '100%'}),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    ),
], fluid=True, style={'height': '100%'})


@app.callback(
    [Output('temp_graph', 'figure'),
     Output('umidade_graph', 'figure'),
     Output('pre_graph', 'figure'),
     Output('qual_ar_graph', 'figure')],
    [Output('last_temp', 'children'),
     Output('last_umidade', 'children'),
     Output('last_pre', 'children'),
     Output('last_quali_Ar', 'children'),
     Output('last_chuva', 'children'),
     Output('last_temp_f', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('dataset', 'data')]
)
def update_graphs(_n_intervals, _data):
    try:
        line_from_arduino = ler_arduino()
        dados_from_arduino = line_from_arduino.split(',')
        print(f'Última atualização: {pd.Timestamp.now()}')
        print(line_from_arduino)
        global contador_atualizacoes
        if line_from_arduino is None:
            raise ValueError("No data received.")

        df_main['Temp_DHT11'].append(float(dados_from_arduino[0]))
        df_main['Umidade_DHT11'].append(float(dados_from_arduino[1]))
        df_main['Pressao_BMP180'].append(float(dados_from_arduino[2]))
        df_main['QualidadeAr'].append(float(dados_from_arduino[3]))
        df_main['Chuva'].append(dados_from_arduino[4])

        last_temp = float(df_main['Temp_DHT11'][-1]) if len(df_main['Temp_DHT11']) > 0 else 'N/A'
        last_umidade = float(df_main['Umidade_DHT11'][-1]) if len(df_main['Umidade_DHT11']) > 0 else 'N/A'
        last_pre = float(df_main['Pressao_BMP180'][-1]) if len(df_main['Pressao_BMP180']) > 0 else 'N/A'
        last_quali_ar = float(df_main['QualidadeAr'][-1]) if len(df_main['QualidadeAr']) > 0 else 'N/A'
        last_chuva = df_main['Chuva'][-1]
        last_temp_f = (float(last_temp) * 9/5) + 32
        # Update the temperature graph
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=list(range(len(df_main['Temp_DHT11']))), y=df_main['Temp_DHT11'],
                                      mode='lines', name='Temperatura',
                                      line=dict(width=2, shape='spline'),
                                      marker=dict(size=10)))
        annotations_temp = []
        for i, y_value in enumerate(df_main['Temp_DHT11']):
            annotations_temp.append(
                dict(
                    x=i,
                    y=y_value,
                    text='',
                    font=dict(color='#4FFBE2'),
                    showarrow=False,
                    xanchor='center',
                    yanchor='bottom'
                )
            )
        fig_temp.update_layout(
            height=160,
            width=690,
            margin=dict(l=40, r=0, t=15, b=40),
            template=vapor_template,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickvals=list(range(len(df_main['Temp_DHT11']))),
                ticktext=[str(i+1) for i in range(len(df_main['Temp_DHT11']))],
                tickangle=-45,
            ),
            yaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickcolor='#1C1C41',
                tickangle=-45,
            ),
            annotations=annotations_temp  # Use the modified annotations
        )

        # Update the humidity graph
        fig_umidade = go.Figure()
        fig_umidade.add_trace(go.Scatter(x=list(range(len(df_main['Umidade_DHT11']))), y=df_main['Umidade_DHT11'], mode='lines', name='Umidade', line=dict(width=2, shape='spline'), marker=dict(size=10)))

        # Modify the annotations for humidity graph
        annotations_umidade = []
        for i, y_value in enumerate(df_main['Umidade_DHT11']):
            annotations_umidade.append(
                dict(
                    x=i,
                    y=y_value,
                    text='',
                    font=dict(color='#4FFBE2'),
                    showarrow=False,
                    xanchor='center',
                    yanchor='bottom'
                )
            )
        fig_umidade.update_layout(
            height=160,
            width=690,
            margin=dict(l=40, r=0, t=15, b=40),
            template=vapor_template,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickvals=list(range(len(df_main['Umidade_DHT11']))),
                ticktext=[str(i+1) for i in range(len(df_main['Umidade_DHT11']))],
                tickangle=-45,
            ),
            yaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickangle=-45,
            ),
            annotations=annotations_umidade
        )

        # grafico de pressao atmferica
        fig_pre = go.Figure()
        fig_pre.add_trace(go.Scatter(x=list(range(len(df_main['Pressao_BMP180']))), y=df_main['Pressao_BMP180'], mode='lines', name='Pressão Atmoférica', line=dict(width=2, shape='spline'), marker=dict(size=10)))
        annotations_temp = []
        for i, y_value in enumerate(df_main['Pressao_BMP180']):
            annotations_temp.append(
                dict(
                    x=i,
                    y=y_value,
                    text='',
                    font=dict(color='#4FFBE2'),
                    showarrow=False,
                    xanchor='center',
                    yanchor='bottom'
                )
            )
        fig_pre.update_layout(
            height=160,
            width=690,
            margin=dict(l=40, r=0, t=15, b=40),
            template=vapor_template,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickvals=list(range(len(df_main['Pressao_BMP180']))),
                ticktext=[str(i+1) for i in range(len(df_main['Pressao_BMP180']))],
                tickangle=-45,
            ),
            yaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickangle=-45,
            ),
            annotations=annotations_temp  # Use the modified annotations
        )

        # Gráfico da qualidade do ar
        fig_qua = go.Figure()
        fig_qua.add_trace(go.Scatter(x=list(range(len(df_main['QualidadeAr']))), y=df_main['QualidadeAr'], mode='lines', name='Qualidade Ar', line=dict(width=2, shape='spline'), marker=dict(size=10)))
        annotations_temp = []
        for i, y_value in enumerate(df_main['QualidadeAr']):
            annotations_temp.append(
                dict(
                    x=i,
                    y=y_value,
                    text='',
                    font=dict(color='#4FFBE2'),
                    showarrow=False,
                    xanchor='center',
                    yanchor='bottom'
                )
            )
        fig_qua.update_layout(
            height=160,
            width=690,
            margin=dict(l=40, r=0, t=15, b=40),
            template=vapor_template,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickvals=list(range(len(df_main['QualidadeAr']))),
                ticktext=[str(i+1) for i in range(len(df_main['QualidadeAr']))],
                tickangle=-45,
            ),
            yaxis=dict(
                color='#4FFBE2',
                showgrid=True,
                gridcolor='#1C1C41',
                tickangle=-45,
            ),
            annotations=annotations_temp  # Use the modified annotations
        )

        return fig_temp, fig_umidade, fig_pre, fig_qua, f'{last_temp:.2f}°C', f'{last_umidade:.2f}%', f'{last_pre}hPa', f'{last_quali_ar:.2f} PPM', f'{last_chuva}', f'{last_temp_f:.2f}°F'
    except serial.SerialException as e:
        print(f"Erro ao ler a porta serial: {e}")
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    dash_thread = Thread(target=app.run_server(debug=True, port=8053))
    dash_thread.start()
    exit()

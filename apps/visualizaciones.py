import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime as dt
import base64
import dash_daq as daq
import pandas as pd
import numpy as np
import json as json
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd
import shapely.geometry
from plotly.subplots import make_subplots


peat = 'assets/peaton.png' # replace with your own image
peat_img = base64.b64encode(open(peat, 'rb').read()).decode('ascii')

hv = 'assets/hv.png' # replace with your own image
hv_img = base64.b64encode(open(hv, 'rb').read()).decode('ascii')

lesionado = 'assets/lesionado.png' # replace with your own image
lesionado_img = base64.b64encode(open(lesionado, 'rb').read()).decode('ascii')

fallecido = 'assets/fallecido.png' # replace with your own image
fallecido_img = base64.b64encode(open(fallecido, 'rb').read()).decode('ascii')


# HEATMAP

hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
hvi_pub = hvi

# Cambiar variables a string
hvi_pub["año"] = hvi_pub["año"].astype(str)
hvi_pub["mes"] = hvi_pub["mes"].astype(str)
hvi_pub["dia"] = hvi_pub["dia"].astype(str)

# Crear variable datetime
hvi_pub["fecha"] = hvi_pub["dia"] +"/"+ hvi_pub["mes"] + "/"+ hvi_pub["año"]
hvi_pub["fecha"]  = pd.to_datetime(hvi_pub["fecha"], dayfirst = True, format ='%d/%m/%Y')

# Duplicar columna de fecha y set index
hvi_pub = hvi_pub.set_index("fecha")
hvi_pub = hvi_pub.sort_index()
hvi_pub

df = hvi_pub.pivot_table(index="hora", columns=["dia_semana"], values=["hechos_viales"], aggfunc=np.sum)
df = df.reset_index()

# Cambiar nombre columnas
df.columns = [" ".join(a) for a in df.columns.to_flat_index()]

strings = df.columns.values
new_strings = []

for string in strings:
    new_string = string.replace("hechos_viales ", '')
    new_strings.append(new_string)

df = df.set_axis(new_strings, axis=1)
df = df[['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']]
df = df.reset_index()
df = df.rename(columns={"index": "Hora"})
df_hp = [df.iloc[0,1:8],df.iloc[1,1:8],df.iloc[2,1:8],df.iloc[3,1:8],df.iloc[4,1:8],df.iloc[5,1:8],df.iloc[6,1:8],df.iloc[7,1:8],df.iloc[8,1:8],df.iloc[9,1:8],df.iloc[10,1:8],df.iloc[11,1:8],df.iloc[12,1:8],df.iloc[13,1:8],df.iloc[14,1:8],df.iloc[15,1:8],df.iloc[16,1:8],df.iloc[17,1:8],df.iloc[18,1:8],df.iloc[19,1:8],df.iloc[20,1:8],df.iloc[21,1:8],df.iloc[21,1:8],df.iloc[23,1:8]]

pub_sem_hora = go.Figure(data=go.Heatmap(
                   name='',
                   z=df_hp,
                   x=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
                   y=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','18','19','20','21','22','23',], 
                   hoverongaps = False,
                   colorscale='Sunset'))
pub_sem_hora.update_traces(hovertemplate="<b>%{x} a las %{y} horas:</b> <br>%{z} hechos viales")
pub_sem_hora.update_layout(barmode='stack',
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right',
            plot_bgcolor='white',
            margin = dict(t=30, l=10, r=10, b=30))



# TIPOS DE HECHOS VIALES Y CAUSAS

hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
hvi_pub = hvi

df = hvi_pub.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum).fillna(0).reset_index()

# Cambiar nombre columnas
df.columns = [" ".join(a) for a in df.columns.to_flat_index()]

strings = df.columns.values
new_strings = []

for string in strings:
    new_string = string.replace("hechos_viales ", '')
    new_strings.append(new_string)

df = df.set_axis(new_strings, axis=1)

df_new = pd.concat([pd.DataFrame(df.iloc[0,1:]/df.iloc[0,1:].sum()*100,).T,pd.DataFrame(df.iloc[1,1:]/df.iloc[1,1:].sum()*100,).T,pd.DataFrame(df.iloc[2,1:]/df.iloc[2,1:].sum()*100,).T,
           pd.DataFrame(df.iloc[3,1:]/df.iloc[3,1:].sum()*100,).T,pd.DataFrame(df.iloc[4,1:]/df.iloc[4,1:].sum()*100,).T,pd.DataFrame(df.iloc[5,1:]/df.iloc[5,1:].sum()*100,).T,
           pd.DataFrame(df.iloc[6,1:]/df.iloc[6,1:].sum()*100,).T,pd.DataFrame(df.iloc[7,1:]/df.iloc[7,1:].sum()*100,).T,pd.DataFrame(df.iloc[8,1:]/df.iloc[8,1:].sum()*100,).T,
           pd.DataFrame(df.iloc[9,1:]/df.iloc[9,1:].sum()*100,).T,pd.DataFrame(df.iloc[10,1:]/df.iloc[10,1:].sum()*100,).T])

df_new = df_new[::-1].astype(float).round(1)

pub_tipycau = go.Figure()
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Viro indevidamente'],
            name='Viro indevidamente',
            orientation='h',
            marker=dict(
            color='#90c6e1',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Sin causa registrada'],
            name='Sin causa registrada',
            orientation='h',
            marker=dict(
            color='#e190d9',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Otros'],
            name='Otros',
            orientation='h',
            marker=dict(
            color='#90e19b',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['No respeto semáforo'],
            name='No respeto semáforo',
            orientation='h',
            marker=dict(
            color='#e1e090',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['No respeto alto'],
            name='No respeto alto',
            orientation='h',
            marker=dict(
            color='#e19090',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['No guardo distancia'],
            name='No guardo distancia',
            orientation='h',
            marker=dict(
            color='#909be1',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Mal Estacionado'],
            name='Mal Estacionado',
            orientation='h',
            marker=dict(
            color='#e1a86c',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Invadir carril'],
            name='Invadir carril',
            orientation='h',
            marker=dict(
            color='#a6a6a6',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Exceso de velocidad'],
            name='Exceso de velocidad',
            orientation='h',
            marker=dict(
            color='#598b4c',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Exceso de dimensiones'],
            name='Exceso de dimensiones',
            orientation='h',
            marker=dict(
            color='#926b58',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Estado alcohólico'],
            name='Estado alcohólico',
            orientation='h',
            marker=dict(
            color='#8f548d',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Dormitando'],
            name='Dormitando',
            orientation='h',
            marker=dict(
                color='#5250af',
            )
))
pub_tipycau.add_trace(go.Bar(
            y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
            x=df_new['Distracción'],
            name='Distracción',
            orientation='h',
            marker=dict(
            color='#af5555',
            )
))
pub_tipycau.update_xaxes(showgrid = False, 
            showline = False, 
            title_text='Porcentaje (%)', 
            tickmode="auto")
pub_tipycau.update_yaxes(showgrid = False, 
            showline = False, 
            title_text='Tipo de hecho vial', 
            )
pub_tipycau.update_layout(barmode='stack',
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right',
            plot_bgcolor='white',
            margin = dict(t=30, l=10, r=10, b=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                x=-0.05,
                itemclick = 'toggleothers',
                )
            )
pub_tipycau.update_traces(hovertemplate="<b>%{y}</b><br> %{x}%")


# App Layout

layout = html.Div([

    html.Br(),

    # Tarjetas Indicadores
    dbc.Row([

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dbc.Row([

                        dbc.Col([

                            html.Div([

                                html.H1('2,554'),
                                html.P('Hechos Viales'),

                            ],style={'float':'left'},),
                            html.Img(src='data:image/png;base64,{}'.format(hv_img), 
                                style={'float':'left', 'width':'14%'},
                                className="pl-3 pt-2 img-fluid"), 

                        ]),

                    ]),
                    
                    html.P('en el 2021'),                    

                ])
            ])

        ]),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dbc.Row([

                        dbc.Col([

                            html.Div([

                                html.H1('40'),
                                html.P('Lesionados'),

                            ],style={'float':'left'},),
                            html.Img(src='data:image/png;base64,{}'.format(lesionado_img), 
                                style={'float':'left', 'width':'14%'},
                                className="pl-3 pt-2 img-fluid"), 

                        ]),

                    ]),
                    
                    html.P('en el 2021'),   

                ])
            ])

        ]),

        dbc.Col([
            dbc.Card([

                dbc.CardBody([

                    dbc.Row([

                        dbc.Col([

                            html.Div([

                                html.H1('3'),
                                html.P('Fatalidades'),

                            ],style={'float':'left'},),
                            html.Img(src='data:image/png;base64,{}'.format(fallecido_img), 
                                style={'float':'left', 'width':'14%'},
                                className="pl-3 pt-2 img-fluid"), 

                        ]),

                    ]),

                    html.P('en el 2021'),   

                ])
            ])

        ]),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dbc.Row([

                        dbc.Col([

                            html.Div([

                                html.H1('40'),
                                html.P('Atropellos'),

                            ],style={'float':'left'},),
                            html.Img(src='data:image/png;base64,{}'.format(peat_img), 
                                style={'float':'left', 'width':'14%'},
                                className="pl-3 pt-2 img-fluid"), 

                        ]),

                    ]),

                    html.P('en el 2021'),   

                ])
            ])

        ]),
    
    ], className='mx-0'),

    html.Br(),

    # Por tipo de usuario // Vulnerabilidad de Usuarios
    dbc.Row([
       
        # Por tipo de usuario
        dbc.Col([

            dbc.Card([
                
                dbc.CardBody([

                    html.H1(['Por tipo de usuario']),
                    html.Hr(),

                    dbc.RadioItems(
                        id = 'pub_gravedad',
                        className = 'radio-group btn-group d-flex justify-content-center',
                        labelClassName = 'btn btn-secondary',
                        labelCheckedClassName = 'active',
                        value = 'todos',
                        options = [
                            {'label': 'Todos', 'value': 'todos'},
                            {'label': 'Lesionados', 'value': 'lesionados'},
                            {'label': 'Fallecidos', 'value': 'fallecidos'},
                        ],
                    ),

                    dcc.Graph(
                        id = 'pub_time',
                        figure = {},
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),

            ], className='p-0')

        ], lg=6, md=6),

        # Vulnerabilidad de Usuarios
        dbc.Col([

            dbc.Card([

                dbc.CardBody([
                    html.H1(['Por vulnerabilidad del usuario']),
                    html.Hr(),

                    dbc.RadioItems(
                        id = 'pub_vul_año',
                        className = 'radio-group btn-group d-flex justify-content-center',
                        labelClassName = 'btn btn-secondary',
                        labelCheckedClassName = 'active',
                        value = '2020',
                        options = [
                            
                            {'label': '2015', 'value': '2015'},
                            {'label': '2016', 'value': '2016'},
                            {'label': '2017', 'value': '2017'},
                            {'label': '2018', 'value': '2018'},
                            {'label': '2019', 'value': '2019'},
                            {'label': '2020', 'value': '2020'},
                        ],
                    ),

                    dcc.Graph(
                        id = 'pub_vulne',
                        figure = {},
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),
            ], className='p-0')

        ], lg=6, md=6),

    ], className='mx-0'),

    html.Br(),

    # Por mes y dia del año // Por día de la semana y hora
    dbc.Row([

        # Por mes y dia del año
        dbc.Col([

            dbc.Card([
                
                dbc.CardBody([

                    html.H1(['Por mes y dia del año']),
                    html.Hr(),

                    html.Div([

                        dbc.RadioItems(
                            id = 'pub_gravedad_2',
                            className = 'radio-group btn-group d-flex justify-content-center',
                            labelClassName = 'btn btn-secondary',
                            labelCheckedClassName = 'active',
                            value = 'todos',
                            options = [
                                {'label': 'Todos', 'value': 'todos'},
                                {'label': 'Lesionados', 'value': 'lesionados'},
                                {'label': 'Fallecidos', 'value': 'fallecidos'},
                            ],
                            style={'float':'left'}
                        ),

                        dbc.RadioItems(
                            id = 'pub_tiempos',
                            className = 'radio-group btn-group d-flex justify-content-center pl-5',
                            labelClassName = 'btn btn-secondary',
                            labelCheckedClassName = 'active',
                            value = 'mes',
                            options = [
                                {'label': 'Mes', 'value': 'mes'},
                                {'label': 'Día del año', 'value': 'dia_año'},
                            ],
                        ),
                    ], className='d-flex justify-content-center'),

                    dcc.Graph(
                        id = 'pub_periodo',
                        figure = {},
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),
                
            ], className='p-0')

        ], lg=6, md=6),

        # Por día de la semana y hora
        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    html.H1(['Por día de la semana y hora']),
                    html.Hr(),

                    dbc.RadioItems(
                            id = 'pub_gravedad_3',
                            className = 'radio-group btn-group d-flex justify-content-center',
                            labelClassName = 'btn btn-secondary',
                            labelCheckedClassName = 'active',
                            value = 'todos',
                            options = [
                                {'label': 'Todos', 'value': 'todos'},
                                {'label': 'Lesionados', 'value': 'lesionados'},
                                {'label': 'Fallecidos', 'value': 'fallecidos'},
                            ],
                        ),

                    dcc.Graph(
                        id = 'pub_sem_hora',
                        figure = pub_sem_hora,
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),
            ], className='p-0')

        ], lg=6, md=6),

    ], className='mx-0'),

    html.Br(),

    # Tipos y causas // Pending
    dbc.Row([

        # Tipos y causas
        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    html.H1(['Por tipo de hecho vial y sus causas']),
                    html.Hr(),

                    dcc.Graph(
                        id = 'pub_tipycau',
                        figure = pub_tipycau,
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),
            ], className='p-0')

        ], lg=6, md=6),

        # Pending
        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    html.H1(['Por lesionados y fallecidos']),
                    html.Hr(),

                    dcc.Graph(
                        id = 'pub_radar',
                        figure = {},
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d','zoom2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )

                ]),
            ], className='p-0')

        ], lg=6, md=6),

    ], className='mx-0'),

    html.Br(),

    # Footer 

    dbc.Row([
        dbc.Col(
            html.H6('Instituto Municipal de Planeación y Gestión Urbana')),
        dbc.Col(
            html.H6('San Pedro Garza García, Nuevo León, México',
                style = {'textAlign': 'right'}))
    ], className='px-3 py-4 mx-0', style={'background-color': 'black','color': 'white'})

], style={'background-color': '#fafafa'}) 

# Por mes y dia del año
def render_pub_periodo(pub_tiempos):

    if pub_tiempos == 'dia_año':
    
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi

        # Cambiar variables a string
        hvi_pub["año"] = hvi_pub["año"].astype(str)
        hvi_pub["mes"] = hvi_pub["mes"].astype(str)
        hvi_pub["dia"] = hvi_pub["dia"].astype(str)

        # Crear variable datetime
        hvi_pub["fecha"] = hvi_pub["dia"] +"/"+ hvi_pub["mes"] + "/"+ hvi_pub["año"]
        hvi_pub["fecha"]  = pd.to_datetime(hvi_pub["fecha"], dayfirst = True, format ='%d/%m/%Y')

        # Duplicar columna de fecha y set index
        hvi_pub = hvi_pub.set_index("fecha")
        hvi_pub = hvi_pub.sort_index()

        #Transformar datos en dias
        hvi_pub = hvi_pub.resample("D").sum()

        hvi_pub['fecha_ind'] = hvi_pub.index 
        hvi_pub["fecha2"] = hvi_pub["fecha_ind"].dt.strftime('%m/%d')
        hvi_pub = hvi_pub.reset_index()
        hvi_pub = hvi_pub.set_index("fecha2")
        hvi_pub['fecha_ind'] = hvi_pub.index 

        fecha = hvi_pub['fecha_ind'].drop_duplicates().sort_index()
        hvi_prom = hvi_pub.groupby(hvi_pub.index)['hechos_viales'].mean().sort_index().round(0)

        pub_tiempo = go.Figure([
            go.Bar(
                name='',
                x=fecha,
                y=hvi_prom,
                #mode='lines',
                #line=dict(color='rgb(54, 117, 101)'),
                showlegend=False
            ),
        ])
        pub_tiempo.update_xaxes(showgrid = False, 
            showline = False, 
            tickmode="auto")
        pub_tiempo.update_yaxes(showgrid = False, 
            showline = False, 
            title_text='Hechos Viales', 
            rangebreaks=[dict(bounds=[0,10])],
            )
        pub_tiempo.update_layout(
                    hoverlabel = dict(font_size = 16),
                    hoverlabel_align = 'right',
                    plot_bgcolor='white',
                    yaxis_range=[0,45],
                    margin = dict(t=30, l=10, r=10, b=30)
                )
        pub_tiempo.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales") #+lines

        return pub_tiempo

    elif pub_tiempos == 'mes':

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        
        # Cambiar variables a string
        hvi_pub["año"] = hvi_pub["año"].astype(str)
        hvi_pub["mes"] = hvi_pub["mes"].astype(str)
        hvi_pub["dia"] = hvi_pub["dia"].astype(str)

        # Crear variable datetime
        hvi_pub["fecha"] = hvi_pub["dia"] +"/"+ hvi_pub["mes"] + "/"+ hvi_pub["año"]
        hvi_pub["fecha"]  = pd.to_datetime(hvi_pub["fecha"], dayfirst = True, format ='%d/%m/%Y')

        # Duplicar columna de fecha y set index
        hvi_pub = hvi_pub.set_index("fecha")
        hvi_pub = hvi_pub.sort_index()

        #Transformar datos en dias
        hvi_pub = hvi_pub.resample("M").sum()

        hvi_pub['fecha_ind'] = hvi_pub.index 
        hvi_pub["fecha2"] = hvi_pub["fecha_ind"].dt.strftime('%B')
        hvi_pub = hvi_pub.reset_index()
        hvi_pub = hvi_pub.set_index("fecha2")
        hvi_pub['fecha_ind'] = hvi_pub.index 

        fecha = hvi_pub['fecha_ind'].drop_duplicates()
        hvi_prom = hvi_pub.groupby(hvi_pub.index)['hechos_viales'].mean().sort_index().round(0)

        pub_tiempo = go.Figure([
            go.Bar(
                name='',
                x=fecha,
                y=hvi_prom,
                #mode='lines',
                #line=dict(color='rgb(54, 117, 101)'),
                showlegend=False
            ),
        ])
        pub_tiempo.update_xaxes(showgrid = False, 
            showline = False, 
            tickmode="auto")
        pub_tiempo.update_yaxes(showgrid = False, 
            showline = False, 
            title_text='Hechos Viales', 
            rangebreaks=[dict(bounds=[0,10])],
            )
        pub_tiempo.update_layout(dragmode = False, 
                    hoverlabel = dict(font_size = 16),
                    hoverlabel_align = 'right',
                    plot_bgcolor='white',
            )
        pub_tiempo.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales")

        return pub_tiempo


# Por vulnerabilidad del usuario
def render_pub_vulne(pub_vul_año):

    if pub_vul_año == '2015':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2015]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne

    elif pub_vul_año == '2016':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2016]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne

    elif pub_vul_año == '2017':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2017]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne

    elif pub_vul_año == '2018':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2018]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne

    elif pub_vul_año == '2019':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2019]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne

    elif pub_vul_año == '2020':
        
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        hvi_pub = hvi
        hvi_pub = hvi_pub[hvi_pub.año == 2020]

        df = hvi_pub.pivot_table(index="tipo_usu_2", values=['hechos_viales',"lesionados","fallecidos"], aggfunc=np.sum).fillna(0).reset_index()

        # Cambiar nombre columnas
        df.columns = ["".join(a) for a in df.columns.to_flat_index()]

        strings = df.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales", '')
            new_strings.append(new_string)

        r_les = df.lesionados/df.hechos_viales
        r_fall = df.fallecidos/df.hechos_viales
        r_iles = 1 - r_les + r_fall
        dif = r_les + r_fall + r_iles -1
        r_iles = r_iles - dif

        df_new = pd.concat([pd.DataFrame(df.iloc[:,0]),pd.DataFrame(r_les).rename(columns={0:'lesionados'})*100,pd.DataFrame(r_fall).rename(columns={0:'fallecidos'})*100,pd.DataFrame(r_iles).rename(columns={0:'sin_les_fall'})*100],axis=1)
        df_new = df_new[::-1].round(1)
        df_new = df_new.sort_values(by='tipo_usu_2', ascending=True)
        df_new = df_new.rename(columns={"lesionados": "p_lesionados","fallecidos": "p_fallecidos","sin_les_fall": "p_sin_les_fall"})
        df_new = pd.concat([df_new, df.fallecidos], axis=1, join="outer")

        pub_vulne = px.scatter(df_new, 
                         x="p_lesionados", 
                         y="p_fallecidos",
                         size="fallecidos", 
                         color="tipo_usu_2",
                         hover_name="tipo_usu_2", 
                         size_max=70,
                         custom_data=['tipo_usu_2','fallecidos'],
                        opacity=1)
        pub_vulne.update_traces(name='',
                          hovertemplate="<b>%{customdata[0]}</b><br>Porcentaje de lesiones: %{x}% <br>Porcentaje de fallecimientos: %{y}% <br>Personas fallecidas %{customdata[1]}",
                          showlegend=False,)
        pub_vulne.update_xaxes(showgrid = True, 
                    showline = True, 
                    zerolinecolor = '#EBF0F8',
                    title_text='Usuarios lesionados (%)')
        pub_vulne.update_yaxes(showgrid = True, 
                    showline = True, 
                    gridcolor = "#EBF0F8",
                    zerolinecolor = '#EBF0F8',
            title_text='Usuarios fallecidos (%)', 
            )
        pub_vulne.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin = dict(t=30, l=0, r=0, b=30),
            xaxis_range=[-3.1,70],
            yaxis_range=[-1.8,9],
        )

        return pub_vulne


# Por mes y dia del año
def render_pub_time(pub_gravedad):

    if pub_gravedad == 'todos':
    
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        hvi_p = hvi.loc[hvi.tipo_usu_2 == 'Peaton']
        hvi_m = hvi.loc[hvi.tipo_usu_2 == 'Motorizado']
        hvi_b = hvi.loc[hvi.tipo_usu_2 == 'Bicicleta']
        hvi_mc = hvi.loc[hvi.tipo_usu_2 == 'Motocicleta']

        #Transformar datos en meses
        hvi_peaton = hvi_p.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_motorizado = hvi_m.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_bici = hvi_b.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_moto = hvi_mc.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

        # Cambiar nombre columnas
        hvi_peaton.columns = ["".join(a) for a in hvi_peaton.columns.to_flat_index()]
        hvi_peaton = hvi_peaton.reset_index()
        hvi_peaton = hvi_peaton.rename(columns={"lesionados": "lesionados_p","fallecidos": "fallecidos_p","hechos_viales": "hechos_viales_p"})


        hvi_motorizado.columns = ["".join(a) for a in hvi_motorizado.columns.to_flat_index()]
        hvi_motorizado = hvi_motorizado.reset_index()
        hvi_motorizado = hvi_motorizado.rename(columns={"lesionados": "lesionados_m","fallecidos": "fallecidos_m","hechos_viales": "hechos_viales_m"})

        hvi_bici.columns = ["".join(a) for a in hvi_bici.columns.to_flat_index()]
        hvi_bici = hvi_bici.reset_index()
        hvi_bici = hvi_bici.rename(columns={"lesionados": "lesionados_b","fallecidos": "fallecidos_b","hechos_viales": "hechos_viales_b"})

        hvi_moto.columns = ["".join(a) for a in hvi_moto.columns.to_flat_index()]
        hvi_moto = hvi_moto.reset_index()
        hvi_moto = hvi_moto.rename(columns={"lesionados": "lesionados_mc","fallecidos": "fallecidos_mc","hechos_viales": "hechos_viales_mc"})

        df = pd.concat([hvi_peaton.fecha, hvi_peaton.hechos_viales_p,hvi_bici.hechos_viales_b,hvi_moto.hechos_viales_mc,hvi_motorizado.hechos_viales_m], axis=1)
        df['fecha_ind'] = df.fecha .dt.strftime('%Y')

        # Graph
        pub_time = px.bar(df,
            x='fecha_ind',
            y=["hechos_viales_m","hechos_viales_p", "hechos_viales_b", "hechos_viales_mc"], 
            labels = {'fecha': ''}, 
            template = 'plotly_white')
        pub_time.update_traces(
            #name='',
            hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
        pub_time.update_xaxes(showgrid = False, 
            title_text='', 
            ticktext=df['fecha_ind'],
            ticklabelmode='period'
            )
        pub_time.update_yaxes(title_text='Hechos viales')
        pub_time.update_layout(
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right',
            legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        x=-0.05,
                        itemclick = 'toggleothers',
                        )
                    )

        return pub_time

    elif pub_gravedad == 'lesionados':

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        hvi = hvi[hvi.lesionados != 0]

        hvi_p = hvi.loc[hvi.tipo_usu_2 == 'Peaton']
        hvi_m = hvi.loc[hvi.tipo_usu_2 == 'Motorizado']
        hvi_b = hvi.loc[hvi.tipo_usu_2 == 'Bicicleta']
        hvi_mc = hvi.loc[hvi.tipo_usu_2 == 'Motocicleta']

        #Transformar datos en meses
        hvi_peaton = hvi_p.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_motorizado = hvi_m.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_bici = hvi_b.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_moto = hvi_mc.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

        # Cambiar nombre columnas
        hvi_peaton.columns = ["".join(a) for a in hvi_peaton.columns.to_flat_index()]
        hvi_peaton = hvi_peaton.reset_index()
        hvi_peaton = hvi_peaton.rename(columns={"lesionados": "lesionados_p","fallecidos": "fallecidos_p","hechos_viales": "hechos_viales_p"})


        hvi_motorizado.columns = ["".join(a) for a in hvi_motorizado.columns.to_flat_index()]
        hvi_motorizado = hvi_motorizado.reset_index()
        hvi_motorizado = hvi_motorizado.rename(columns={"lesionados": "lesionados_m","fallecidos": "fallecidos_m","hechos_viales": "hechos_viales_m"})

        hvi_bici.columns = ["".join(a) for a in hvi_bici.columns.to_flat_index()]
        hvi_bici = hvi_bici.reset_index()
        hvi_bici = hvi_bici.rename(columns={"lesionados": "lesionados_b","fallecidos": "fallecidos_b","hechos_viales": "hechos_viales_b"})

        hvi_moto.columns = ["".join(a) for a in hvi_moto.columns.to_flat_index()]
        hvi_moto = hvi_moto.reset_index()
        hvi_moto = hvi_moto.rename(columns={"lesionados": "lesionados_mc","fallecidos": "fallecidos_mc","hechos_viales": "hechos_viales_mc"})

        df = pd.concat([hvi_peaton.fecha, hvi_peaton.hechos_viales_p,hvi_bici.hechos_viales_b,hvi_moto.hechos_viales_mc,hvi_motorizado.hechos_viales_m], axis=1)
        df['fecha_ind'] = df.fecha .dt.strftime('%Y')

        # Graph
        pub_time = px.bar(df,
            x='fecha_ind',
            y=["hechos_viales_m","hechos_viales_p", "hechos_viales_b", "hechos_viales_mc"], 
            labels = {'fecha': ''}, 
            template = 'plotly_white')
        pub_time.update_traces(
            #name='',
            hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
        pub_time.update_xaxes(showgrid = False, 
            title_text='', 
            ticktext=df['fecha_ind'],
            ticklabelmode='period'
            )
        pub_time.update_yaxes(title_text='Personas lesionadas')
        pub_time.update_layout(
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right',
            legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        x=-0.05,
                        itemclick = 'toggleothers',
                        )
                    )

        return pub_time

    elif pub_gravedad == 'fallecidos':

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        hvi = hvi[hvi.fallecidos != 0]

        hvi_p = hvi.loc[hvi.tipo_usu_2 == 'Peaton']
        hvi_m = hvi.loc[hvi.tipo_usu_2 == 'Motorizado']
        hvi_b = hvi.loc[hvi.tipo_usu_2 == 'Bicicleta']
        hvi_mc = hvi.loc[hvi.tipo_usu_2 == 'Motocicleta']

        #Transformar datos en meses
        hvi_peaton = hvi_p.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_motorizado = hvi_m.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_bici = hvi_b.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
        hvi_moto = hvi_mc.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

        # Cambiar nombre columnas
        hvi_peaton.columns = ["".join(a) for a in hvi_peaton.columns.to_flat_index()]
        hvi_peaton = hvi_peaton.reset_index()
        hvi_peaton = hvi_peaton.rename(columns={"lesionados": "lesionados_p","fallecidos": "fallecidos_p","hechos_viales": "hechos_viales_p"})


        hvi_motorizado.columns = ["".join(a) for a in hvi_motorizado.columns.to_flat_index()]
        hvi_motorizado = hvi_motorizado.reset_index()
        hvi_motorizado = hvi_motorizado.rename(columns={"lesionados": "lesionados_m","fallecidos": "fallecidos_m","hechos_viales": "hechos_viales_m"})

        hvi_bici.columns = ["".join(a) for a in hvi_bici.columns.to_flat_index()]
        hvi_bici = hvi_bici.reset_index()
        hvi_bici = hvi_bici.rename(columns={"lesionados": "lesionados_b","fallecidos": "fallecidos_b","hechos_viales": "hechos_viales_b"})

        hvi_moto.columns = ["".join(a) for a in hvi_moto.columns.to_flat_index()]
        hvi_moto = hvi_moto.reset_index()
        hvi_moto = hvi_moto.rename(columns={"lesionados": "lesionados_mc","fallecidos": "fallecidos_mc","hechos_viales": "hechos_viales_mc"})

        df = pd.concat([hvi_peaton.fecha, hvi_peaton.hechos_viales_p,hvi_bici.hechos_viales_b,hvi_moto.hechos_viales_mc,hvi_motorizado.hechos_viales_m], axis=1)
        df['fecha_ind'] = df.fecha .dt.strftime('%Y')

        # Graph
        pub_time = px.bar(df,
            x='fecha_ind',
            y=["hechos_viales_m","hechos_viales_p", "hechos_viales_b", "hechos_viales_mc"], 
            labels = {'fecha': ''}, 
            template = 'plotly_white')
        pub_time.update_traces(
            #name='',
            hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
        pub_time.update_xaxes(showgrid = False, 
            title_text='', 
            ticktext=df['fecha_ind'],
            ticklabelmode='period'
            )
        pub_time.update_yaxes(title_text='Personas fallecidas')
        pub_time.update_layout(
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right',
            legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        x=-0.05,
                        itemclick = 'toggleothers',
                        )
                    )

        return pub_time
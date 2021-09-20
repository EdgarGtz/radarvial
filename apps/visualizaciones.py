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


# DONAS

# VULNERABILIDAD DE USUARIOS

hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
hvi_pub = hvi

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
df_new = df_new.sort_values(by='fallecidos', ascending=True)

labels = ["Lesionados","Fallecidos","Sin lesiones"]
marker_colors = ['#428DF5','#5D42F5','#42C2F5']
# Create subplots: use 'domain' type for Pie subplot
pub_vulne = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}]])
pub_vulne.add_trace(go.Pie(labels=labels, 
                     values=df_new.iloc[3,1:], 
                     name="",
                     marker_colors = marker_colors),
                      1, 1)
pub_vulne.add_trace(go.Pie(labels=labels, 
                     values=df_new.iloc[2,1:], 
                     name="",
                     marker_colors = marker_colors),
                      1, 2)
pub_vulne.add_trace(go.Pie(labels=labels, 
                     values=df_new.iloc[1,1:], 
                     name="",
                     marker_colors = marker_colors),
                      2, 1)
pub_vulne.add_trace(go.Pie(labels=labels, 
                     values=df_new.iloc[0,1:], 
                     name="",
                     marker_colors = marker_colors),
                      2, 2)

pub_vulne.update_traces(hole=.7, hoverinfo="label+percent+name")
pub_vulne.update_layout(
    annotations=[dict(text='Peatón', x=0.18, y=0.82, font=dict(family='Arial'), font_size=18, showarrow=False),
                 dict(text='Ciclista', x=0.82, y=0.82, font=dict(family='Arial'), font_size=18, showarrow=False),
                 dict(text='Motociclista', x=0.16, y=0.18, font=dict(family='Arial'), font_size=18, showarrow=False),
                 dict(text='Motorizado', x=0.84, y=0.18, font=dict(family='Arial'), font_size=18, showarrow=False),
                 ],
    legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.01,
                x=0.25,
                itemclick = False,
                ),
    margin = dict(t=30, l=0, r=0, b=30)
)

# TIEMPO

# Leer csv
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
hvi_peaton = hvi_p.resample("M").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
hvi_motorizado = hvi_m.resample("M").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
hvi_bici = hvi_b.resample("M").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
hvi_moto = hvi_mc.resample("M").sum().drop(['hora','Lat','Lon','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

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

# Graph
pub_time = px.bar(df, 
    x='fecha',
    y=["hechos_viales_m","hechos_viales_p", "hechos_viales_b", "hechos_viales_mc"], 
    labels = {'fecha': ''}, 
    template = 'plotly_white')
pub_time.update_traces(
    hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
pub_time.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=df['fecha'],
    ticklabelmode='period'
    )
pub_time.update_yaxes(title_text='Hechos viales')
pub_time.update_layout(
    hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right')

indic = go.Figure(go.Indicator(
    mode = "number+delta",
    value = 2950,
    delta = {'position': "bottom", 'reference': 4097,'decreasing':dict(color="green"),'increasing':dict(color="red")},
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Hechos Viales<br><span style='font-size:0.8em;color:gray'>"}
))
indic.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

# App Layout

layout = html.Div([

    # Tarjetas Indicadores
    dbc.Row([

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dcc.Graph(
                        id = 'indic',
                        figure = indic,
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

                ])
            ])

        ]),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([])
            ])

        ]),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([])
            ])

        ]),

        dbc.Col([

            dbc.Card([

                dbc.CardBody([])
            ])

        ]),
    
    ]),

    html.Br(),

    # Periodo // Vulnerabilidad
    dbc.Row([

        # Promedios
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label='Día del año', tab_id='dia_año',
                            disabled = False),
                        dbc.Tab(label = 'Mes', tab_id = 'mes',
                            disabled = False),
                        dbc.Tab(label='Día de la semana', tab_id='dia_semana',
                            disabled = False),
                        dbc.Tab(label='Hora', tab_id='hora',
                            disabled = False),
                        
                    ],
                    id='periodo_pub_tabs',
                    active_tab="dia_año",
                    card=True
                    )
                ]),
                dbc.CardBody([

                    dcc.Graph(
                        id = 'pub_periodo',
                        figure = {},
                        config={
                            'modeBarButtonsToRemove':
                            ['lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d',
                            'resetScale2d', 'hoverClosestCartesian',
                            'hoverCompareCartesian', 'toggleSpikelines',
                            'select2d',],
                            'displaylogo': False
                        },
                    )
                ], className='p-0'),
            ])
        ],lg=6, md=6),

        # Periodo
        dbc.Col([

            dbc.Card([

                dbc.CardHeader([html.B(['Periodo'])]),
                dbc.CardBody([

                    dcc.Graph(
                        id = 'pub_time',
                        figure = pub_time,
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

    ]),

    html.Br(),

    # Promedios // Heatmap
    dbc.Row([

        # Heatmap
        dbc.Col([

            dbc.Card([

                dbc.CardHeader(['Día de la Semana y Hora']),
                dbc.CardBody([

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

        # Vulnerabilidad
        dbc.Col([

            dbc.Card([

                dbc.CardBody([
                    html.B(['Vulnerabilidad de Usuarios']),
                    html.Hr(),

                    dcc.Graph(
                        id = 'pub_vulne',
                        figure = pub_vulne,
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

    ]),

    html.Br(),

    # Tipos y causas // Pending
    dbc.Row([

        # Tipos y causas
        dbc.Col([

            dbc.Card([

                dbc.CardHeader(['Tipos de Hechos Viales y sus Causas']),
                dbc.CardBody([

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

                dbc.CardHeader(['Pending']),
                dbc.CardBody([

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

    ]),


    # Footer 

    dbc.Row([
        dbc.Col(
            html.H6('Instituto Municipal de Planeación y Gestión Urbana')),
        dbc.Col(
            html.H6('San Pedro Garza García, Nuevo León, México',
                style = {'textAlign': 'right'}))
    ], className='px-3 py-4', style={'background-color': 'black','color': 'white'})


])

# Hechos Viales por 
def render_pub_periodo(periodo_pub_tabs):

    if periodo_pub_tabs == 'dia_año':
    
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
            title_text='Día del Año', 
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

    elif periodo_pub_tabs == 'mes':

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
            title_text='Meses', 
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

    elif periodo_pub_tabs == 'dia_semana':

        # Leer csv
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
        hvi_pub = hvi_pub.pivot_table(index="dia_semana", values=["hechos_viales"], aggfunc=np.sum)
        hvi_pub = hvi_pub.reset_index()

        hvi_pub = hvi_pub.reindex([2,3,4,1,6,5,0])

        # Cambiar nombre columnas
        hvi_pub.columns = ["".join(a) for a in hvi_pub.columns.to_flat_index()]

        strings = hvi_pub.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales ", '')
            new_strings.append(new_string)

        pub_tiempo = go.Figure([
            go.Bar(
                name='',
                x=hvi_pub.dia_semana,
                y=hvi_pub.hechos_viales,
                #mode='lines',
                #line=dict(color='rgb(54, 117, 101)'),
                showlegend=False
            ),
        ])
        pub_tiempo.update_xaxes(showgrid = False, 
            showline = False, 
            title_text='Meses')
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

    elif periodo_pub_tabs == 'hora':

        # Leer csv
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
        hvi_pub = hvi_pub.pivot_table(index="hora", values=["hechos_viales"], aggfunc=np.sum)
        hvi_pub = hvi_pub.reset_index()

        # Cambiar nombre columnas
        hvi_pub.columns = ["".join(a) for a in hvi_pub.columns.to_flat_index()]

        strings = hvi_pub.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales ", '')
            new_strings.append(new_string)

        pub_tiempo = go.Figure([
            go.Bar(
                name='',
                x=hvi_pub.hora,
                y=hvi_pub.hechos_viales,
                #mode='lines',
                #line=dict(color='rgb(54, 117, 101)'),
                showlegend=False
            ),
        ])
        pub_tiempo.update_xaxes(showgrid = False, 
            showline = False, 
            title_text='Meses')
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
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
from dash_extensions import Download
from dash_extensions.snippets import send_file
from dash_extensions.snippets import send_data_frame

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

# IMAGENES
img1 = 'assets/down-arrow.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

img3 = 'assets/descargar.png' # replace with your own image
encoded_img3 = base64.b64encode(open(img3, 'rb').read()).decode('ascii')

img4 = 'assets/radarvial_logo_bn.png' # replace with your own image
encoded_img4 = base64.b64encode(open(img4, 'rb').read()).decode('ascii')

img5 = 'assets/expand.png'
encoded_img5 = base64.b64encode(open(img5, 'rb').read()).decode('ascii')

# App Layout

layout = html.Div([

        # Mapa y filtros
        dbc.Row([

            # Controles
            dbc.Col([

                # Fechas
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Fecha",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_fecha",
                                    class_name='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),

                            ], style={'text-align':'center'}, class_name='p-0 d-none d-lg-block'),

                            dbc.Collapse(

                                dbc.CardBody([

                                    html.Div([

                                        dcc.DatePickerRange(
                                            id = 'calendario',
                                            min_date_allowed = dt(2015, 1, 1),
                                            max_date_allowed = dt(2021, 9, 30),
                                            start_date = dt(2015, 1, 1),
                                            end_date = dt(2021, 9, 30),
                                            first_day_of_week = 1,
                                            className="d-flex justify-content-center"
                                        ),

                                    ], className ='d-flex align-items-center justify-content-center'),

                                    html.Br(),

                                    dbc.Checklist(
                                        id = 'checklist_dias',
                                        class_name = 'radio-group btn-group d-flex flex-wrap justify-content-center',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name  = 'active',
                                        options=[
                                            {'label': ' LU', 'value': 'Lunes'},
                                            {'label': ' MA', 'value': 'Martes'},
                                            {'label': ' MI', 'value': 'Miércoles'},
                                            {'label': ' JU', 'value': 'Jueves'},
                                            {'label': ' VI', 'value': 'Viernes'},
                                            {'label': ' SA', 'value': 'Sábado'},
                                            {'label': ' DO', 'value': 'Domingo'},
                                        ],
                                        value=['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
                                        style={'display':'inline-block'}
                                    ),

                                    html.Br(),

                                    dcc.RangeSlider(
                                        id='slider_hora',
                                        min=0,
                                        max=23,
                                        value=[0, 23],
                                        marks={
                                            0: {'label': '0'},
                                            3: {'label': '3'},
                                            6: {'label': '6'},
                                            9: {'label': '9'},
                                            12: {'label': '12'},
                                            15: {'label': '15'},
                                            18: {'label': '18'},
                                            21: {'label': '21'},
                                            23: {'label': '23'}
                                        },
                                        allowCross=False,
                                        dots=True,
                                        tooltip={'always_visible': False , "placement":"bottom"},
                                        updatemode='mouseup'
                                    ),

                                ]),
                                id="collapse_cal",
                                is_open=True,
                            ),

                        ], class_name = 'd-none d-lg-block')

                    ], lg=12, md=12, sm = 12, class_name = 'd-none d-lg-block'),

                ], class_name="d-flex justify-content-between d-none d-lg-block",),

                html.Br(),

                # Hechos Viales
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Hechos Viales",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_hv",
                                    class_name='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),

                            ], style={'text-align':'center'}, class_name='p-0'),

                            dbc.Collapse(
                                dbc.CardBody([

                                    html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_sev", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-sev",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-sev",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Gravedad de Hechos Viales")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Todos:'),' Hechos viales con lesionados + hechos viales con fallecidos + hechos viales sin lesionados y fallecidos.']),
                                                    html.Li([html.B('Lesionados:'),' Hechos viales en los que resultaron personas lesionadas.']),
                                                    html.Li([html.B('Fallecidos:'),' Hechos viales en los que resultaron personas fallecidas.']),
                                                ], style={'list-style-type':'none'}, className="p-1"),

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_sev", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_sev",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Gravedad',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.RadioItems(
                                        id = 'hv_graves_opciones',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Lesionados', 'value': 'lesionados'},
                                            {'label': 'Fallecidos', 'value': 'fallecidos'},
                                        ]
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.Div([

                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_usaf", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-usaf",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-usaf"
                                        ),
                                    
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Usuario")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Auto:'),' Acumulado de personas que conducen auto, camión de pasajeros, camioneta, carga pesada, mini van, pickup, trailer y tren.']),
                                                    html.Li([html.B('Peatón:'),' Personas que caminan.']),
                                                    html.Li([html.B('Ciclista:'),' Personas que utilizan la bicicleta como modo de transporte.']),
                                                    html.Li([html.B('Motociclista:'),' Personas que utilizan la motocicleta como modo de transporte.']),
                                                ], style={'list-style-type':'none'}, className="p-1")

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_usaf", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_usaf",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Usuario', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'hv_usu_opciones',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name  = 'active',
                                        value = ['Motorizado','Peaton','Bicicleta','Motocicleta'],
                                        options = [
                                            {'label': 'Auto', 'value': 'Motorizado'},
                                            {'label': 'Peatón', 'value': 'Peaton'},
                                            {'label': 'Ciclista', 'value': 'Bicicleta'},
                                            {'label': 'Motociclista', 'value': 'Motocicleta'}
                                        ],
                                        style = {'display':'inline-block'}
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.Div([

                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_thv", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-thv",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-thv",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Tipos de Hechos Viales")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Alcance:'),' Sucede cuando un conductor impacta con su vehículo en la parte trasera de otro.']),
                                                    html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad. Es imporante destacar que este tipo de hevho vial se asocia únicamente con peatones.']),
                                                    html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
                                                    html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
                                                    html.Li([html.B('Choque de Reversa:'),' Ocurre cuando un vehículo choca con otro al ir de reversa.']),
                                                    html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
                                                    html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
                                                    html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
                                                    html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.']),
                                                    html.Li([html.B('Incendio:'),' Ocurre cuando existe un incendio por un percance vial.']),
                                                    html.Li([html.B('Volcadura:'),' Ocurre cuando un vehículo pierde completamente el contacto entre llantas y superficie de rodamiento originándose giros verticales o transversales']),

                                                ], style={'list-style-type':'none'}, className="p-1")

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_thv", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_thv",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Tipo de hecho vial', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_hv',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name  = 'active',
                                        style={'display':'inline-block'},
                                        value = [],
                                        options = [],
                                    ),

                                ]),
                                id="collapse_dsem",
                                is_open=True,
                            ),

                        ], class_name = 'd-none d-lg-block'),

                    ],lg=12, md=12, class_name = 'd-none d-lg-block'),

                ], class_name = 'd-none d-lg-block'),

                html.Br(),
                
                # Búsqueda avanzada
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Búsqueda avanzada",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_bavan",
                                    class_name='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),



                            ], style={'text-align':'center'}, class_name='p-0'),

                            dbc.Collapse(
                                dbc.CardBody([

                                    html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_afres", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                                ),

                                            id="tooltip-target-afres",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-afres",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Afectado o Responsable")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Afectado:'),' Sujeto perjudicado del siniestro vial.']),
                                                    html.Li([html.B('Responsable:'),' Sujeto causante del siniestro vial.']),
                                                    html.Br(),
                                                    html.Li([
                                                        html.P([html.B('Nota:'), 
                                                            ' Es importante destacar que, para el caso de los atropellos al momento de registrar la información sólo se captura de manera digital la información sobre el contexto del hecho vial y de los vehículos, mientras que la información del perfil de las personas que no transitan en un vehículo (peatonas) sólo se registra de manera física en el parte vial y no digital, por lo que actualmente no es posible conocer el perfil demográfico (edad, sexo) de las personas atropelladas.',]),
                                                            ])
                                                ], style={'list-style-type':'none'}, className="p-1"),

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_afres", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_afres",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Afectado o responsable',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.RadioItems(
                                        id = 'hv_afres_opciones',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Afectados', 'value': 'afectados'},
                                            {'label': 'Responsables', 'value': 'responsables'},
                                        ]
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P(' Sexo',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    dbc.RadioItems(
                                        id = 'hv_sexo_opciones',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Masculino', 'value': 'Masculino'},
                                            {'label': 'Femenino', 'value': 'Femenino'},
                                        ],
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P(' Edad',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    html.Br(),

                                    dcc.RangeSlider(
                                        id='slider_edad',
                                        min=0,
                                        max=85,
                                        value=[0,85],
                                        step=5,
                                        marks={
                                            1: {'label': '0'},
                                            5: {'label': '5'},
                                            10: {'label': '10'},
                                            15: {'label': '15'},
                                            20: {'label': '20'},
                                            25: {'label': '25'},
                                            30: {'label': '30'},
                                            35: {'label': '35'},
                                            40: {'label': '40'},
                                            45: {'label': '45'},
                                            50: {'label': '50'},
                                            55: {'label': '55'},
                                            60: {'label': '60'},
                                            65: {'label': '65'},
                                            70: {'label': '70'},
                                            75: {'label': '75'},
                                            80: {'label': '80'},
                                            85: {'label': '85+'},
                                        },
                                        allowCross=False,
                                        dots=True,
                                        tooltip={'always_visible': False , "placement":"bottom"},
                                        updatemode='mouseup',
                                        className='px-2 pt-2',
                                    ),

                                    html.Br(),

                                    html.P(' Tipo de vehículo',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_veh',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name  = 'active',
                                        options=[
                                            {'label': ' Auto', 'value': 'Auto'},
                                            {'label': ' Bicicleta', 'value': 'Bicicleta'},
                                            {'label': ' Camión de pasajeros', 'value': 'Camión de pasajeros'},
                                            {'label': ' Camioneta', 'value': 'Camioneta'},
                                            {'label': ' Carga pesada', 'value': 'Carga pesada'},
                                            {'label': ' Mini Van', 'value': 'Mini Van'},
                                            {'label': ' Motocicleta', 'value': 'Motocicleta'},
                                            {'label': ' Pick Up', 'value': 'Pick Up'},
                                            {'label': ' Tracción animal', 'value': 'Tracción animal'},
                                            {'label': ' Trailer', 'value': 'Trailer'},
                                            {'label': ' Tren', 'value': 'Tren'},
                                        ],
                                        value=['Auto', 'Bicicleta','Camión de pasajeros','Camioneta','Carga pesada','Mini Van','Motocicleta','Pick Up','Tracción animal','Trailer','Tren'],
                                        style={'display':'inline-block'}
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P([
                                        html.I([
                                            html.B('Nota:'),
                                            ' Los filtros de "sexo", "edad" y "tipo de vehículo" se activan al seleccionar "Afectados" o "Responsables".'
                                            ])
                                    ]),

                                ]),
                                id="collapse_hora",
                                is_open=False,
                            ),

                        ], class_name = 'd-none d-lg-block'),
                        
                    ], lg=12, md=12, class_name = 'd-none d-lg-block'),

                ], class_name = 'd-none d-lg-block'),

                html.Br(),

                # Botón de descargar datos
                dbc.Row([

                    dbc.Col([
                        dbc.CardBody([
                            dcc.Store(id='mapa_data'),
                            Download(id="download-personal-csv"),
                            html.Button([
                                html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                        style={'width':'3.5%','float':'left'},
                                        className="pt-1"),
                                html.B("Descarga tu búsqueda"),
                                ], 
                                id="btn_perso_csv",
                                className="btn btn-block",
                                n_clicks=None,
                                style={'float':'right','background-color':'#BBC3C8','color':'white'}
                            ),
                        ], class_name='p-0', style={'background-color':'transparent'})#, d-lg-none'
                    ], class_name = 'd-none d-lg-block')
                ], class_name = 'd-none d-lg-block')

            ],lg=4, md=4, class_name = 'd-none d-lg-block'),
            
            # Mapa
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        
                        dbc.Row([

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Hechos Viales ', style={'font-weight':'normal', 'border': '0px'}),
                                        html.Th(id = 'hv_totales', style={'font-weight':'normal', 'border': '0px'}),
                                    ], style = {'border': '0px'}),

                                ], style = {'border': '0px'}),

                            ], class_name='d-flex justify-content-center'),

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Lesionados: ', style={'font-weight':'normal', 'border': '0px'}),
                                        html.Th(id = 'hv_les_totales', style={'font-weight':'normal', 'border': '0px'}),
                                    ], style = {'border': '0px'}),

                                ], style = {'border': '0px'}),

                            ], class_name='d-flex justify-content-center'),

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Fallecidos: ', style={'font-weight':'normal', 'border': '0px'}),
                                        html.Th(id = 'hv_fall_totales', style={'font-weight':'normal', 'border': '0px'}),
                                    ], style = {'border': '0px'}),

                                ], style = {'border': '0px'}),

                            ], class_name='d-flex justify-content-center'),
                        ])

                    ], style={'padding':'8px'})
                ], style={'textAlign':'center','color':'white'}, class_name='tarjeta_arriba_map'),

                dbc.Card([

                    dbc.CardBody(

                        dcc.Loading(

                            dcc.Graph(
                                id = 'mapa_interac',
                                figure = {},
                                config={
                                'displayModeBar': False
                                },
                                style={'height':'85vh'}
                            ),

                        color="#636EFA", 
                        type="cube"),

                    style={'padding':'0px'},),

                ], class_name='tarjeta_map'),

                dbc.Card([

                    dbc.CardBody([

                        dcc.Store(id='mapa_data_top'),
                        dcc.Loading(

                            dcc.Graph(
                                id = 'tabla_mapa_top',
                                figure = {},
                                config={
                                        'modeBarButtonsToRemove':
                                        ['lasso2d', 'pan2d',
                                        'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                        'resetScale2d', 'hoverClosestCartesian',
                                        'hoverCompareCartesian', 'toggleSpikelines',
                                        'select2d',],
                                        'displaylogo': False
                                    },
                            ),

                        color="#636EFA", 
                        type="cube"),

                    ],

                    style={'padding':'0px'},),

                ], class_name='tarjeta_map'), 

            ],lg=8, md=8, class_name = 'd-none d-lg-block'),

        ], style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '10px'}),

        dbc.Row([

            dbc.Col([

                dcc.Loading([
                    
                    dbc.Button(
                    'Filtros',
                    color = 'light',
                    class_name = 'filtros_small'
                    ),

                    dcc.Graph(
                        id = 'mapa_interac_movil',
                        figure = {},
                        config={
                        'displayModeBar': False
                        },
                        style={'position':'relative', 'z-index':'1'},
                        className = 'vh-100'
                    ),
                    
                ], color="#2cdb63", type="cube"),

            ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px'})

        ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px', 'height': '700px'})

    ], className = 'w-100 h-100', style = {'padding': '0px', 'margin': '0px'})



# RADAR VIAL - MAPA: FILTRO COLAPSABLE FECHAS
def render_collapse_button_fecha(n, is_open):
    if n:
        return not is_open
    return collapse_button_fecha

# RADAR VIAL - MAPA: FILTRO COLAPSABLE HECHOS VIALES
def render_collapse_button_hv(n, is_open):
    if n:
        return not is_open
    return collapse_button_hv

# RADAR VIAL - MAPA: MODAL SEVERIDAD HECHOS VIALES 
def toggle_modal_sev(open1_sev, close1_sev, modal_sev):
    if open1_sev or close1_sev:
        return not modal_sev
    return modal_sev

# RADAR VIAL - MAPA: MODAL USUARIOS AFECTADOS
def toggle_modal_usaf(open1_usaf, close1_usaf, modal_usaf):
    if open1_usaf or close1_usaf:
        return not modal_usaf
    return modal_usaf

# RADAR VIAL - MAPA: CHECKLIST TIPOS DE HECHOS VIALES DEPENDIENDO DEL USUARIO
def render_opciones_dos(hv_usu_opciones, hv_graves_opciones):

    # Todos
    
    if hv_usu_opciones == [] and hv_graves_opciones == 'todos':

        return [] 

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]    
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Lesionados

    elif hv_usu_opciones == [] and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ] 
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]        
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Fallecidos

    elif hv_usu_opciones == [] and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ] 
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

# RADAR VIAL - MAPA: CHECKLIST TIPOS DE HECHOS VIALES DEPENDIENDO DEL USUARIO - MOVIL
def render_opciones_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil):

    # Todos
    
    if hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'todos':

        return [] 

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]    
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Lesionados

    elif hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ] 
    
    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]        
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Fallecidos

    elif hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ] 
    
    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]

    elif 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]


# RADAR VIAL - MAPA: CHECKLIST TIPOS DE HECHOS VIALES DEPENDIENDO DEL USUARIO (VALORES)
def render_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones):
    
    # Todos

    if hv_usu_opciones == [] and hv_graves_opciones == 'todos':

       return []

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

       return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Atropello']

    # Lesionados

    elif hv_usu_opciones == [] and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',] 
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Atropello']

    # Fallecidos

    elif hv_usu_opciones == [] and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Choque Diverso']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Atropello']

# RADAR VIAL - MAPA: CHECKLIST TIPOS DE HECHOS VIALES DEPENDIENDO DEL USUARIO (VALORES) -MOVIL
def render_opciones_dos_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil):
    
    # Todos

    if hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'todos':

       return []

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

       return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'todos':

        return ['Atropello']

    # Lesionados

    elif hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']

    elif 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Caida de Persona','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',] 
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',]
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'lesionados':

        return ['Atropello']

    # Fallecidos

    elif hv_usu_opciones_movil == [] and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']
    
    elif 'Peaton' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']

    elif 'Bicicleta' in hv_usu_opciones_movil and 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance', 'Choque Diverso']
    
    elif 'Motocicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones_movil and 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']

    elif 'Motocicleta' in hv_usu_opciones_movil and 'Bicicleta' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones_movil and hv_graves_opciones_movil == 'fallecidos':

        return ['Atropello']


# RADAR VIAL - MAPA: MODAL TIPOS DE HECHOS VIALES
def toggle_modal_thv(open1_thv, close1_thv, modal_thv):
    if open1_thv or close1_thv:
        return not modal_thv
    return modal_thv

# RADAR VIAL - MAPA: FILTRO COLAPSABLE BUSQUEDA AVANZADA
def render_collapse_button_bavan(n, is_open):
    if n:
        return not is_open
    return collapse_button_bavan

# RADAR VIAL - MAPA: MODAL AFECTADOS Y RESPONSABLES
def toggle_modal_afres(open1_afres, close1_afres, modal_afres):
    if open1_afres or close1_afres:
        return not modal_afres
    return modal_afres

# RADAR VIAL - MAPA: HECHOS VIALES TOTALES 
def render_hv_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_hv_les_usules[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_resp_edad_sexo = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_sexo_tveh = hv_les_usu_thv_resp_edad_sexo[hv_les_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv_resp_edad.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# RADAR VIAL - MAPA: HECHOS VIALES TOTALES - MOVIL
def render_hv_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_movil == [] or checklist_tipo_hv_movil == [] or checklist_tipo_veh_movil == [] or hv_usu_opciones_movil == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_hv_les_usules[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_usu_thv_resp_edad_sexo = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_sexo_tveh = hv_les_usu_thv_resp_edad_sexo[hv_les_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]        

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv_resp_edad.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------


# RADAR VIAL - MAPA: LESIONADOS
def render_hv_les_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_usu.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    
    # -------------------------------------------

    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de lesionados
        hv_les_totales = hv_les_thv_resp_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por hechos viales con fallecidos
        hvi_cal_dsm_hora_usu_fall = hvi_cal_dsm_hora_usu[hvi_cal_dsm_hora_usu.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_fall_thv = hvi_cal_dsm_hora_usu_fall[(hvi_cal_dsm_hora_usu_fall['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_fall_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.hv_fall_usu_thv.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# RADAR VIAL - MAPA: LESIONADOS - MOVIL
def render_hv_les_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_movil == [] or checklist_tipo_hv_movil == [] or checklist_tipo_veh_movil == [] or hv_usu_opciones_movil == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_usu.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    
    # -------------------------------------------

    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de lesionados
        hv_les_totales = hv_les_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]        

        # Total de lesionados
        hv_les_totales = hv_les_thv_resp_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por hechos viales con fallecidos
        hvi_cal_dsm_hora_usu_fall = hvi_cal_dsm_hora_usu[hvi_cal_dsm_hora_usu.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_fall_thv = hvi_cal_dsm_hora_usu_fall[(hvi_cal_dsm_hora_usu_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_fall_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.hv_fall_usu_thv.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------


# RADAR VIAL - MAPA: FALLECIDOS
def render_hv_fall_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_usu.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_afect_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_resp_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_thv_afect_edad = hv_fall_thv_afect[(hv_fall_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hvi_cal_dsm_hora_afect_sexo = hv_fall_thv_afect_edad[hv_fall_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_afect_sexo_tveh = hvi_cal_dsm_hora_afect_sexo[hvi_cal_dsm_hora_afect_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_afect_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_thv_resp_edad = hv_fall_thv_resp[(hv_fall_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_edad_sexo = hv_fall_thv_resp_edad[hv_fall_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_edad_sexo_tveh = hv_fall_thv_resp_edad_sexo[hv_fall_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# RADAR VIAL - MAPA: FALLECIDOS - MOVIL
def render_hv_fall_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_movil == [] or checklist_tipo_hv_movil == [] or checklist_tipo_veh_movil == [] or hv_usu_opciones_movil == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_usu.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_afect_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]        

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_resp_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones_movil))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_thv_afect_edad = hv_fall_thv_afect[(hv_fall_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hvi_cal_dsm_hora_afect_sexo = hv_fall_thv_afect_edad[hv_fall_thv_afect_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_afect_sexo_tveh = hvi_cal_dsm_hora_afect_sexo[hvi_cal_dsm_hora_afect_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_afect_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_thv_resp_edad = hv_fall_thv_resp[(hv_fall_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_thv_resp_edad_sexo = hv_fall_thv_resp_edad[hv_fall_thv_resp_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_edad_sexo_tveh = hv_fall_thv_resp_edad_sexo[hv_fall_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------



# RADAR VIAL - MAPA: MAPA
def render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        column_names = ["interseccion", "hechos_viales", "lesionados","fallecidos"]
        mapa_data_top = pd.DataFrame(columns = column_names)
        mapa_data_top = mapa_data_top.to_json(orient='columns')

        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=1, 
            zoom=12.5,
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
        margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1)
    
        return mapa_interac, mapa_data_top

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_thv_usu = hvi_cal_dsm_hora_thv[(hvi_cal_dsm_hora_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')

        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac, mapa_data_top



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_thv_afect_edad = hv_les_thv_afect[(hv_les_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_edad_sexo = hv_les_thv_afect_edad[hv_les_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_edad_sexo_tveh = hv_les_thv_afect_edad_sexo[hv_les_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_thv_resp_edad = hv_les_thv_resp[(hv_les_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_edad_sexo = hv_les_thv_resp_edad[hv_les_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_edad_sexo_tveh = hv_les_thv_resp_edad_sexo[hv_les_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top



    # -------------------------------------------



    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_tveh = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_tveh = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_afect_edad_sexo = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_sexo_tveh = hv_fall_usu_thv_afect_edad_sexo[hv_fall_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top
    
    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_resp_edad_sexo = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_sexo_tveh = hv_fall_usu_thv_resp_edad_sexo[hv_fall_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top = mapa_data_top.to_json(orient='columns')
        
        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac, mapa_data_top


    # -------------------------------------------


# RADAR VIAL - MAPA: MAPA - MOVIL
def render_mapa_interac_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_movil == [] or checklist_tipo_hv_movil == [] or checklist_tipo_veh_movil == [] or hv_usu_opciones_movil == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        column_names = ["interseccion", "hechos_viales", "lesionados","fallecidos"]
        mapa_data_top_movil = pd.DataFrame(columns = column_names)
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')

        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=1, 
            zoom=12.5,
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
        margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1)
    
        return mapa_interac_movil

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por usuario
        hvi_cal_dsm_hora_thv_usu = hvi_cal_dsm_hora_thv[(hvi_cal_dsm_hora_thv['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')

        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'todos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones_movil]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad_movil[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(#marker_color="#565e64",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac_movil



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_thv_afect_edad = hv_les_thv_afect[(hv_les_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_afect_edad_sexo = hv_les_thv_afect_edad[hv_les_thv_afect_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_edad_sexo_tveh = hv_les_thv_afect_edad_sexo[hv_les_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'lesionados' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_thv_resp_edad = hv_les_thv_resp[(hv_les_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_les_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_thv_resp_edad_sexo = hv_les_thv_resp_edad[hv_les_thv_resp_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_edad_sexo_tveh = hv_les_thv_resp_edad_sexo[hv_les_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]        

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil



    # -------------------------------------------



    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_tveh = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_tveh = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'todos' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'afectados' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_usu_thv_afect_edad_sexo = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_sexo_tveh = hv_fall_usu_thv_afect_edad_sexo[hv_fall_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil
    
    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias_movil != [] and hv_graves_opciones_movil == 'fallecidos' and hv_afres_opciones_movil == 'responsables' and hv_sexo_opciones_movil != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_movil)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_movil[0])&(hvi_cal_dsm['hora']<=slider_hora_movil[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones_movil))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad_movil[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_fall_usu_thv_resp_edad_sexo = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_sexo_tveh = hv_fall_usu_thv_resp_edad_sexo[hv_fall_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh_movil)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        mapa_data_top_movil = mapa_data.sort_values(by=['hechos_viales'], ascending=False).iloc[0:10,:]
        mapa_data_top_movil = mapa_data_top_movil.to_json(orient='columns')
        
        #-- Graph
        mapa_interac_movil = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac_movil.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6452, lon=-100.3689),
                style="streets"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac_movil.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac_movil


    # -------------------------------------------


# RADAR VIAL - MAPA: TABLA TOP 10
def render_tabla_mapa_top(datos_tabla_mapa):   

    # Tabla
    datos_tabla_mapa = pd.read_json(datos_tabla_mapa)
    
    tabla_mapa_top = go.Figure(
            [go.Table(
                columnwidth = [100, 50, 50, 50],
                header=dict(values=['Intersección','Hechos viales','Lesionados','Fallecidos'],
                    fill_color='#343332',
                    font=dict(color='white', family='Arial', size = 16),
                    align='center'),
                cells=dict(values=[datos_tabla_mapa.interseccion, datos_tabla_mapa.hechos_viales, datos_tabla_mapa.lesionados, datos_tabla_mapa.fallecidos],
                   fill_color='#F7F7F7',
                   font=dict(color='black', family='Arial', size = 16),
                   align=['left', 'center', 'center', 'center'],
                   height=35))
            ])
    tabla_mapa_top.update_layout(margin = dict(t=20, l=0, r=0, b=10))


    return tabla_mapa_top

# RADAR VIAL - MAPA: MAPA (DATA)
def render_mapa_data(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        # Cambiar a JSON
        mapa_data = mapa_data.reset_index()
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_thv_usu = hvi_cal_dsm_hora_thv[(hvi_cal_dsm_hora_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_thv_usu

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh
        
        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_resp_edad_sexo = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_sexo_tveh = hv_les_usu_thv_resp_edad_sexo[hv_les_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data



    # -------------------------------------------



    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Cambiar nombre
        mapa_data = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_tveh = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_tveh = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
 

    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Cambiar nombre
        mapa_data = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_afect_edad_sexo = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_sexo_tveh = hv_fall_usu_thv_afect_edad_sexo[hv_fall_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_resp_edad_sexo = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_sexo_tveh = hv_fall_usu_thv_resp_edad_sexo[hv_fall_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # Quitar columnas
        mapa_data = mapa_data.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # Cambiar a JSON
    mapa_data = mapa_data.reset_index()
    mapa_data = mapa_data.to_json(orient='columns')

    return mapa_data

    # -------------------------------------------

# RADAR VIAL - MAPA: DESCARGA TU BUSQUEDA
def render_down_data_csv(n_clicks, data):
    
    a_json = json.loads(data)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "hechos_viales_query.csv", index=False, encoding='ISO-8859-1')

    return csv

#----------------------------
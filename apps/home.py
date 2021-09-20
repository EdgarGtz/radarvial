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

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

# App Layout

layout = html.Div([

    # Banner Principal

    dbc.Row(

        style={'background-color':'#2A4A71','color':'white','height':'5vh','padding':'0'},
    ),

        
    dbc.Row([

        # Filtros
        dbc.Col([

            html.Br(),

            # Fecha
            html.Div([
                                    
                html.Span(
                    dbc.Button(
                        html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                style={'float':'right'},
                                className="p-0 img-fluid"), 
                        id="open_fecha", 
                        n_clicks=0, 
                        style={'display':'inline-block',
                                'float':'left','padding':'0', 
                                'width':'15px','background-color':'transparent',
                                'border-color':'transparent','padding-top':'5px'},
                        className='rounded-circle'

                    ),

                    id="tooltip1_fecha",
                ),

                dbc.Tooltip(
                    "Más información",
                    target="tooltip1_fecha",
                ),
                    
                dbc.Modal([

                    dbc.ModalHeader(html.B("Fechas")),

                    dbc.ModalBody([
                        html.P('Blablabalbalba')

                    ],style={"textAlign":"justify",'font-size':'100%'}),

                    dbc.ModalFooter([
                        
                        dbc.Button(
                            "Cerrar", 
                            id="close_fecha", 
                            className="ml-auto btn btn-secondary", 
                            n_clicks=0
                        )
                    ]),

                    ],
                    id="modal_fecha",
                    centered=True,
                    size="lg",
                    is_open=False,
                ),

                html.P(' Fecha',
                    style={'width':'90%','float':'left'}, className='pl-1'),

            ]),

            html.Br(),html.Br(),

            html.Div([

                # Calendario
                html.Div([

                    dcc.DatePickerRange(
                        id = 'calendario_pub',
                        min_date_allowed = dt(2015, 1, 1),
                        max_date_allowed = dt(2020, 12, 31),
                        start_date = dt(2015, 1, 1),
                        end_date = dt(2020, 12, 31),
                        first_day_of_week = 1,
                        className="p-0", #d-flex justify-content-center
                    ),

                ]),

                html.Br(),

                # Días de la semana
                dbc.Checklist(
                    id = 'checklist_dias_pub',
                    className = 'radio-group btn-group p-0', #d-flex justify-content-center
                    labelClassName = 'btn btn-secondary',
                    labelCheckedClassName = 'active',
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

                html.Br(),html.Br(),

                # Hora
                dcc.RangeSlider(
                    id='slider_hora_pub',
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
                    updatemode='mouseup',
                    className='p-2'
                ),

            ]),

            html.Br(),

            html.Hr(className='pb-3'),

            # Gravedad
            html.Div([
                                    
                html.Span(
                    dbc.Button(
                        html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                style={'float':'right'},
                                className="p-0 img-fluid"), 
                        id="open_g", 
                        n_clicks=0, 
                        style={'display':'inline-block',
                                'float':'left','padding':'0', 
                                'width':'15px','background-color':'transparent',
                                'border-color':'transparent','padding-top':'5px'},
                        className='rounded-circle'

                    ),

                    id="tooltip_g",
                ),

                dbc.Tooltip(
                    "Más información",
                    target="tooltip_g",
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
                            id="close_g", 
                            className="ml-auto btn btn-secondary", 
                            n_clicks=0
                        )
                    ]),

                    ],
                    id="modal_g",
                    centered=True,
                    size="lg",
                    is_open=False,
                ),

                html.P(' Gravedad',
                    style={'width':'90%','float':'left'}, className='pl-1'),

            ]),

            dbc.RadioItems(
                id = 'hv_graves_opciones_pub',
                className = 'radio-group btn-group pb-3',
                labelClassName = 'btn btn-secondary',
                labelCheckedClassName = 'active',
                value = 'todos',
                options = [
                    {'label': 'Todos', 'value': 'todos'},
                    {'label': 'Lesionados', 'value': 'lesionados'},
                    {'label': 'Fallecidos', 'value': 'fallecidos'},
                ]
            ),

            html.Br(),

            html.Hr(className='pb-3'),

            # Tipo de Usuario
            html.Div([
                                    
                html.Span(
                    dbc.Button(
                        html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                style={'float':'right'},
                                className="p-0 img-fluid"), 
                        id="open_u", 
                        n_clicks=0, 
                        style={'display':'inline-block',
                                'float':'left','padding':'0', 
                                'width':'15px','background-color':'transparent',
                                'border-color':'transparent','padding-top':'5px'},
                        className='rounded-circle'

                    ),

                    id="tooltip_u",
                ),

                dbc.Tooltip(
                    "Más información",
                    target="tooltip_u",
                ),
                    
                dbc.Modal([

                    dbc.ModalHeader(html.B("Tipo de Vehículo")),

                    dbc.ModalBody([
                        html.Ul([
                            html.Li([html.B('Peatón:'),' Personas que caminan.']),
                            html.Li([html.B('Ciclista:'),' Personas que utilizan la bicicleta como modo de transporte.']),
                            html.Li([html.B('Motociclista:'),' Personas que utilizan la motocicleta como modo de transporte.']),
                            html.Li([html.B('Auto:'),' Personas que conducen auto como modo de transporte.']),
                            html.Li([html.B('Camión de pasajeros:'),' Personas que conducen o transitan en un camión de pasajeros como modo de transporte.']),
                            html.Li([html.B('Camioneta:'),' Personas que conducen camioneta como modo de transporte, inclyendo mini van, pickup.']),
                            html.Li([html.B('Carga pesada:'),' Personas que conducen vehículos de carga pesada o trailer.']),
                            html.Li([html.B('Tren:'),' Personas que conducen el tren.']),
                        ], style={'list-style-type':'none'}, className="p-1")

                    ],style={"textAlign":"justify",'font-size':'100%'}),

                    dbc.ModalFooter([
                        
                        dbc.Button(
                            "Cerrar", 
                            id="close_u", 
                            className="ml-auto btn btn-secondary", 
                            n_clicks=0
                        )
                    ]),

                    ],
                    id="modal_u",
                    centered=True,
                    size="lg",
                    is_open=False,
                ),

                html.P(' Tipo de Usuario',
                    style={'width':'90%','float':'left'}, className='pl-1'),

            ]),

            dbc.Checklist(
                id = 'checklist_tipo_usu_pub',
                className = 'radio-group btn-group pb-3',
                labelClassName = 'btn btn-secondary',
                labelCheckedClassName = 'active',
                options=[
                    {'label': ' 🚶', 'value': 'Peaton'},
                    {'label': ' 🚲', 'value': 'Bicicleta'},
                    {'label': ' 🛵', 'value': 'Motocicleta'},
                    {'label': ' 🚌', 'value': 'Camión de pasajeros'},
                    {'label': ' 🚗', 'value': 'Auto'},
                    {'label': ' 🚙', 'value': 'Camioneta'}, #+ Minivan + Pickup
                    {'label': ' 🚚', 'value': 'Carga pesada'}, #+Trailer
                    {'label': ' 🚂', 'value': 'Tren'},
                ],
                value=['Peaton','Bicicleta','Motocicleta','Camión de pasajeros', 'Auto','Camioneta','Carga pesada','Tren'],
                style={'display':'inline-block'},
            ),

            html.Br(),

            html.Hr(className='pb-3'),

            # Red Vial de Lesiones Graves
            html.Div([
                                    
                html.Span(
                    dbc.Button(
                        html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                style={'float':'right'},
                                className="p-0 img-fluid"), 
                        id="open_rvlg", 
                        n_clicks=0, 
                        style={'display':'inline-block',
                                'float':'left','padding':'0', 
                                'width':'15px','background-color':'transparent',
                                'border-color':'transparent','padding-top':'5px'},
                        className='rounded-circle'

                    ),

                    id="tooltip_rvlg",
                ),

                dbc.Tooltip(
                    "Más información",
                    target="tooltip_rvlg",
                ),
                    
                dbc.Modal([

                    dbc.ModalHeader(html.B("Red Vial de Lesiones Graves")),

                    dbc.ModalBody([
                        html.P(['Blablabalbalba'

                        ], className="p-1"),

                    ],style={"textAlign":"justify",'font-size':'100%'}),

                    dbc.ModalFooter([
                        
                        dbc.Button(
                            "Cerrar", 
                            id="close_rvlg", 
                            className="ml-auto btn btn-secondary", 
                            n_clicks=0
                        )
                    ]),

                    ],
                    id="modal_rvlg",
                    centered=True,
                    size="lg",
                    is_open=False,
                ),

                html.P(' Red Vial de Lesiones Graves',
                    style={'float':'left'},
                    className='pl-1'),

            ]),

            daq.BooleanSwitch(
                id = 'rvlg',
                on=False,
                color="#2A4A71",
                style={'float':'left'}, 
                className='px-4'
            )

        ], className='pl-4',
        lg=4, md=4),

        # Mapa
        dbc.Col([

            #dcc.Loading(
                dcc.Graph(
                    id = 'mapa_pub',
                    figure = {},
                    config={
                    'displayModeBar': False
                    },
                    style={'height':'85vh', 'padding':'0'}
                ),

            #color="#42f581", type="dot"),

        ], style={'padding':'0', 'background-color':'#353433'}
        , lg=8, md=8),
    
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


# Mapa interactivo
def render_mapa_pub(start_date, end_date, slider_hora_pub, checklist_dias_pub, hv_graves_opciones_pub, rvlg, checklist_tipo_usu_pub):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_pub == [] or checklist_tipo_usu_pub == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        #-- Graph
        mapa_pub = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=1, 
            zoom=12.5,
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa_pub.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
        margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_pub.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1)
    
        return mapa_pub


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # 
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'todos' and rvlg == False:

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
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_pub)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_pub[0])&(hvi_cal_dsm['hora']<=slider_hora_pub[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(checklist_tipo_usu_pub))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        #-- Graph
        mapa_pub = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_pub.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_pub.update_traces(marker_color="#42f581",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_pub

    # 
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'todos' and rvlg == True:

        # HIGH INJURY NETWORK

        hni_p1 = gpd.read_file('assets/hin/p1.geojson')
        hni_p2 = gpd.read_file('assets/hin/p2.geojson')
        hni_p3 = gpd.read_file('assets/hin/p3.geojson')
        hni_p4 = gpd.read_file('assets/hin/p4.geojson')
        hni_p5 = gpd.read_file('assets/hin/p5.geojson')
        hin_puntos = pd.read_csv("assets/hin/hin_new.csv", encoding='ISO-8859-1')
        hin_puntos_ex = pd.read_csv("assets/hin/hin_new_comp.csv", encoding='ISO-8859-1')

        lats_p1 = []
        lons_p1 = []
        names_p1 = []

        for feature, name in zip(hni_p1.geometry, hni_p1.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p1 = np.append(lats_p1, y)
                lons_p1 = np.append(lons_p1, x)
                names_p1 = np.append(names_p1, [name]*len(y))
                
                lats_p1 = np.append(lats_p1, None)
                lons_p1 = np.append(lons_p1, None)
                names_p1 = np.append(names_p1, None)

        lats_p2 = []
        lons_p2 = []
        names_p2 = []

        for feature, name in zip(hni_p2.geometry, hni_p2.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p2 = np.append(lats_p2, y)
                lons_p2 = np.append(lons_p2, x)
                names_p2 = np.append(names_p2, [name]*len(y))
                
                lats_p2 = np.append(lats_p2, None)
                lons_p2 = np.append(lons_p2, None)
                names_p2 = np.append(names_p2, None)
                
        lats_p3 = []
        lons_p3 = []
        names_p3 = []

        for feature, name in zip(hni_p3.geometry, hni_p3.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p3 = np.append(lats_p3, y)
                lons_p3 = np.append(lons_p3, x)
                names_p3 = np.append(names_p3, [name]*len(y))
                
                lats_p3 = np.append(lats_p3, None)
                lons_p3 = np.append(lons_p3, None)
                names_p3 = np.append(names_p3, None)
                
        lats_p4 = []
        lons_p4 = []
        names_p4 = []

        for feature, name in zip(hni_p4.geometry, hni_p4.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p4 = np.append(lats_p4, y)
                lons_p4 = np.append(lons_p4, x)
                names_p4 = np.append(names_p4, [name]*len(y))
                
                lats_p4 = np.append(lats_p4, None)
                lons_p4 = np.append(lons_p4, None)
                names_p4 = np.append(names_p4, None)

        lats_p5 = []
        lons_p5 = []
        names_p5 = []

        for feature, name in zip(hni_p5.geometry, hni_p5.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p5 = np.append(lats_p5, y)
                lons_p5 = np.append(lons_p5, x)
                names_p5 = np.append(names_p5, [name]*len(y))
                
                lats_p5 = np.append(lats_p5, None)
                lons_p5 = np.append(lons_p5, None)
                names_p5 = np.append(names_p5, None)

        #-- Graph
        mapa_pub = go.Figure(px.scatter_mapbox(hin_puntos_ex, lat="Lat", lon="Lon",
            size = 'tamaño', 
            size_max = 20,
            color_discrete_sequence = [hin_puntos_ex.color],
            custom_data=['Intersecciones','orden'],
            hover_data={'orden':False, 'Lat':False, 'Lon':False, 'color':False, 'tamaño':False, 'Intersecciones':True},
            opacity=1))
        mapa_pub.update_traces(hovertemplate="<b>%{customdata[1]}° lugar: %{customdata[0]}</b><br>")
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p5,
            lat = lats_p5,
            line = {'color': '#ed7a32','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p4,
            lat = lats_p4,
            line = {'color': '#ed5732','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p3,
            lat = lats_p3,
            line = {'color': '#ed3232','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p2,
            lat = lats_p2,
            line = {'color': '#cf0202','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            lat=lats_p1, 
            lon=lons_p1, 
            mode="lines",
            line = {'color': '#a60000','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "markers",
            lon = hin_puntos.Lon,
            lat = hin_puntos.Lat,
            marker = {'size': list(hin_puntos.tamaño.astype(int)*1.3),'color': list(hin_puntos.color),'opacity':1},
            ))
        mapa_pub.update_layout(
            mapbox=dict(
                center=dict(lat=25.6572, lon=-100.3689),
                accesstoken=mapbox_access_token,
                zoom=12.5,
                style="dark"),
            showlegend=False,
            margin = dict(t=0, l=0, r=0, b=0),
        )

        return mapa_pub


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # 
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'lesionados' and rvlg == False:

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
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_pub)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_pub[0])&(hvi_cal_dsm['hora']<=slider_hora_pub[1])]

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(checklist_tipo_usu_pub))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        #-- Graph
        mapa_pub = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_pub.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_pub.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_pub
       
    #
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'lesionados' and rvlg == True:

        # HIGH INJURY NETWORK

        hni_p1 = gpd.read_file('assets/hin/p1.geojson')
        hni_p2 = gpd.read_file('assets/hin/p2.geojson')
        hni_p3 = gpd.read_file('assets/hin/p3.geojson')
        hni_p4 = gpd.read_file('assets/hin/p4.geojson')
        hni_p5 = gpd.read_file('assets/hin/p5.geojson')
        hin_puntos = pd.read_csv("assets/hin/hin_new.csv", encoding='ISO-8859-1')
        hin_puntos_ex = pd.read_csv("assets/hin/hin_new_comp.csv", encoding='ISO-8859-1')

        lats_p1 = []
        lons_p1 = []
        names_p1 = []

        for feature, name in zip(hni_p1.geometry, hni_p1.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p1 = np.append(lats_p1, y)
                lons_p1 = np.append(lons_p1, x)
                names_p1 = np.append(names_p1, [name]*len(y))
                
                lats_p1 = np.append(lats_p1, None)
                lons_p1 = np.append(lons_p1, None)
                names_p1 = np.append(names_p1, None)

        lats_p2 = []
        lons_p2 = []
        names_p2 = []

        for feature, name in zip(hni_p2.geometry, hni_p2.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p2 = np.append(lats_p2, y)
                lons_p2 = np.append(lons_p2, x)
                names_p2 = np.append(names_p2, [name]*len(y))
                
                lats_p2 = np.append(lats_p2, None)
                lons_p2 = np.append(lons_p2, None)
                names_p2 = np.append(names_p2, None)
                
        lats_p3 = []
        lons_p3 = []
        names_p3 = []

        for feature, name in zip(hni_p3.geometry, hni_p3.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p3 = np.append(lats_p3, y)
                lons_p3 = np.append(lons_p3, x)
                names_p3 = np.append(names_p3, [name]*len(y))
                
                lats_p3 = np.append(lats_p3, None)
                lons_p3 = np.append(lons_p3, None)
                names_p3 = np.append(names_p3, None)
                
        lats_p4 = []
        lons_p4 = []
        names_p4 = []

        for feature, name in zip(hni_p4.geometry, hni_p4.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p4 = np.append(lats_p4, y)
                lons_p4 = np.append(lons_p4, x)
                names_p4 = np.append(names_p4, [name]*len(y))
                
                lats_p4 = np.append(lats_p4, None)
                lons_p4 = np.append(lons_p4, None)
                names_p4 = np.append(names_p4, None)

        lats_p5 = []
        lons_p5 = []
        names_p5 = []

        for feature, name in zip(hni_p5.geometry, hni_p5.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p5 = np.append(lats_p5, y)
                lons_p5 = np.append(lons_p5, x)
                names_p5 = np.append(names_p5, [name]*len(y))
                
                lats_p5 = np.append(lats_p5, None)
                lons_p5 = np.append(lons_p5, None)
                names_p5 = np.append(names_p5, None)

        #-- Graph
        mapa_pub = go.Figure(px.scatter_mapbox(hin_puntos_ex, lat="Lat", lon="Lon",
            size = 'tamaño', 
            size_max = 20,
            color_discrete_sequence = [hin_puntos_ex.color],
            custom_data=['Intersecciones','orden'],
            hover_data={'orden':False, 'Lat':False, 'Lon':False, 'color':False, 'tamaño':False, 'Intersecciones':True},
            opacity=1))
        mapa_pub.update_traces(hovertemplate="<b>%{customdata[1]}° lugar: %{customdata[0]}</b><br>")
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p5,
            lat = lats_p5,
            line = {'color': '#ed7a32','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p4,
            lat = lats_p4,
            line = {'color': '#ed5732','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p3,
            lat = lats_p3,
            line = {'color': '#ed3232','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p2,
            lat = lats_p2,
            line = {'color': '#cf0202','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            lat=lats_p1, 
            lon=lons_p1, 
            mode="lines",
            line = {'color': '#a60000','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "markers",
            lon = hin_puntos.Lon,
            lat = hin_puntos.Lat,
            marker = {'size': list(hin_puntos.tamaño.astype(int)*1.3),'color': list(hin_puntos.color),'opacity':1},
            ))
        mapa_pub.update_layout(
            mapbox=dict(
                center=dict(lat=25.6572, lon=-100.3689),
                accesstoken=mapbox_access_token,
                zoom=12.5,
                style="dark"),
            showlegend=False,
            margin = dict(t=0, l=0, r=0, b=0),
        )

        return mapa_pub


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # 
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'fallecidos' and rvlg == False:

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
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias_pub)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora_pub[0])&(hvi_cal_dsm['hora']<=slider_hora_pub[1])]

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(checklist_tipo_usu_pub))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        #-- Graph
        mapa_pub = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_pub.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_pub.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_pub
   
    #
    elif checklist_dias_pub != [] and hv_graves_opciones_pub == 'fallecidos' and rvlg == True:

        # HIGH INJURY NETWORK

        hni_p1 = gpd.read_file('assets/hin/p1.geojson')
        hni_p2 = gpd.read_file('assets/hin/p2.geojson')
        hni_p3 = gpd.read_file('assets/hin/p3.geojson')
        hni_p4 = gpd.read_file('assets/hin/p4.geojson')
        hni_p5 = gpd.read_file('assets/hin/p5.geojson')
        hin_puntos = pd.read_csv("assets/hin/hin_new.csv", encoding='ISO-8859-1')
        hin_puntos_ex = pd.read_csv("assets/hin/hin_new_comp.csv", encoding='ISO-8859-1')

        lats_p1 = []
        lons_p1 = []
        names_p1 = []

        for feature, name in zip(hni_p1.geometry, hni_p1.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p1 = np.append(lats_p1, y)
                lons_p1 = np.append(lons_p1, x)
                names_p1 = np.append(names_p1, [name]*len(y))
                
                lats_p1 = np.append(lats_p1, None)
                lons_p1 = np.append(lons_p1, None)
                names_p1 = np.append(names_p1, None)

        lats_p2 = []
        lons_p2 = []
        names_p2 = []

        for feature, name in zip(hni_p2.geometry, hni_p2.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p2 = np.append(lats_p2, y)
                lons_p2 = np.append(lons_p2, x)
                names_p2 = np.append(names_p2, [name]*len(y))
                
                lats_p2 = np.append(lats_p2, None)
                lons_p2 = np.append(lons_p2, None)
                names_p2 = np.append(names_p2, None)
                
        lats_p3 = []
        lons_p3 = []
        names_p3 = []

        for feature, name in zip(hni_p3.geometry, hni_p3.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p3 = np.append(lats_p3, y)
                lons_p3 = np.append(lons_p3, x)
                names_p3 = np.append(names_p3, [name]*len(y))
                
                lats_p3 = np.append(lats_p3, None)
                lons_p3 = np.append(lons_p3, None)
                names_p3 = np.append(names_p3, None)
                
        lats_p4 = []
        lons_p4 = []
        names_p4 = []

        for feature, name in zip(hni_p4.geometry, hni_p4.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p4 = np.append(lats_p4, y)
                lons_p4 = np.append(lons_p4, x)
                names_p4 = np.append(names_p4, [name]*len(y))
                
                lats_p4 = np.append(lats_p4, None)
                lons_p4 = np.append(lons_p4, None)
                names_p4 = np.append(names_p4, None)

        lats_p5 = []
        lons_p5 = []
        names_p5 = []

        for feature, name in zip(hni_p5.geometry, hni_p5.NOMBRE):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats_p5 = np.append(lats_p5, y)
                lons_p5 = np.append(lons_p5, x)
                names_p5 = np.append(names_p5, [name]*len(y))
                
                lats_p5 = np.append(lats_p5, None)
                lons_p5 = np.append(lons_p5, None)
                names_p5 = np.append(names_p5, None)

        #-- Graph
        mapa_pub = go.Figure(px.scatter_mapbox(hin_puntos_ex, lat="Lat", lon="Lon",
            size = 'tamaño', 
            size_max = 20,
            color_discrete_sequence = [hin_puntos_ex.color],
            custom_data=['Intersecciones','orden'],
            hover_data={'orden':False, 'Lat':False, 'Lon':False, 'color':False, 'tamaño':False, 'Intersecciones':True},
            opacity=1))
        mapa_pub.update_traces(hovertemplate="<b>%{customdata[1]}° lugar: %{customdata[0]}</b><br>")
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p5,
            lat = lats_p5,
            line = {'color': '#ed7a32','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p4,
            lat = lats_p4,
            line = {'color': '#ed5732','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p3,
            lat = lats_p3,
            line = {'color': '#ed3232','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "lines",
            lon = lons_p2,
            lat = lats_p2,
            line = {'color': '#cf0202','width':4}))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            lat=lats_p1, 
            lon=lons_p1, 
            mode="lines",
            line = {'color': '#a60000','width':4},
            ))
        mapa_pub.add_traces(go.Scattermapbox(
            hoverinfo="skip",
            mode = "markers",
            lon = hin_puntos.Lon,
            lat = hin_puntos.Lat,
            marker = {'size': list(hin_puntos.tamaño.astype(int)*1.3),'color': list(hin_puntos.color),'opacity':1},
            ))
        mapa_pub.update_layout(
            mapbox=dict(
                center=dict(lat=25.6572, lon=-100.3689),
                accesstoken=mapbox_access_token,
                zoom=12.5,
                style="dark"),
            showlegend=False,
            margin = dict(t=0, l=0, r=0, b=0),
        )

        return mapa_pub

    mapa_data = {
       "Lat": pd.Series(25.6572),
       "Lon": pd.Series(-100.3689),
        "hechos_viales" : pd.Series(0),
       }
    mapa_data = pd.DataFrame(mapa_data)

    #-- Graph
    mapa_pub = go.Figure(
        px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
        size = 'hechos_viales',
        size_max=1, 
        zoom=12.5,
        hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
        opacity=0.9))

    mapa_pub.update_layout(clickmode='event+select', 
         mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=25.6572, lon=-100.3689),
            style="dark"
        ),
    margin = dict(t=0, l=0, r=0, b=0)
    )
    mapa_pub.update_traces(marker_color="#c6cc14",
        unselected_marker_opacity=1)

    return mapa_pub

    # -------------------------------------------

#Modal Fecha
def toggle_modal_fecha(open_fecha, close_fecha, modal_fecha):
    if open_fecha or close_fecha:
        return not modal_fecha
    return modal_fecha

#Modal Gravedad
def toggle_modal_g(open_g, close_g, modal_g):
    if open_g or close_g:
        return not modal_g
    return modal_g

#Modal Tipo de Usuario
def toggle_modal_u(open_u, close_u, modal_u):
    if open_u or close_u:
        return not modal_u
    return modal_u

#Modal Red Vial
def toggle_modal_rvlg(open_rvlg, close_rvlg, modal_rvlg):
    if open_rvlg or close_rvlg:
        return not modal_rvlg
    return modal_rvlg
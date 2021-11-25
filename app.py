import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import base64
from datetime import datetime as dt
from dash_extensions import Download
from dash_extensions.snippets import send_file
from dash_extensions.snippets import send_data_frame


app = dash.Dash(__name__, title='Radar Vial',
				external_stylesheets = [dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-2FB009N3XV"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-2FB009N3XV');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server

# Connect to app pages
from apps import home, visualizaciones, radarvial

from apps.home import (render_collapse_button_fecha, render_collapse_button_hv, render_hv_fall_totales_movil, render_hv_les_totales_movil, render_opciones_dos_dos_movil, render_opciones_dos_movil, toggle_modal_sev, toggle_modal_usaf, render_opciones_dos,
  render_opciones_dos_dos, toggle_modal_thv, render_collapse_button_bavan, toggle_modal_afres, render_hv_totales, render_hv_les_totales, 
  render_hv_fall_totales, render_mapa_interac, render_mapa_interac_movil, render_tabla_mapa_top, render_mapa_data, render_down_data_csv)

from apps.visualizaciones import (render_pub_periodo, render_pub_vulne, render_pub_time)

radar_img = "https://cdn-icons-png.flaticon.com/512/188/188595.png"

# IMAGENES
img1 = 'assets/down-arrow.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

img3 = 'assets/descargar.png' # replace with your own image
encoded_img3 = base64.b64encode(open(img3, 'rb').read()).decode('ascii')

img4 = 'assets/radarvial_logo_bn.png' # replace with your own image
encoded_img4 = base64.b64encode(open(img4, 'rb').read()).decode('ascii')

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
# pub_tipycau.add_trace(go.Bar(
#             y=['Volcadura','Incendio','Estrellamiento','Choque de Reversa','Choque de Crucero','Choque de Frente','Choque Lateral','Choque Diverso','Caida de Persona','Atropello','Alcance'],
#             x=df_new['Sin causa registrada'],
#             name='Sin causa registrada',
#             orientation='h',
#             marker=dict(
#             color='#e190d9',
#             )
# ))
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

app.layout = html.Div([

        # TITULO
        html.Span([

            # TITULO DESKTOP
            dbc.Row([

                dbc.Col([

                    html.Img(src='data:image/png;base64,{}'.format(encoded_img4), 
                                className="pt-0",
                                style={'width':'47px', 'height': '47px', 'float':'left', 'margin-right': '15px'}
                        ),

                    html.H2('Radar Vial', 
                        style={'float':'left', 'font-weight':'normal', 'font-size':'28px', 'margin-right': '15px'}, 
                        className='pl-3 pt-1'
                    ),

                    # MODAL
                    # html.Div([

                    #     # BOTÓN
                    #     html.Span(
                    #         dbc.Button(
                    #             html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                    #                     style={'float':'right'},
                    #                     className="p-0 img-fluid"), 
                    #             id="open_titulo", 
                    #             n_clicks=0, 
                    #             style={'display':'inline-block',
                    #                     'float':'left','padding':'0', 
                    #                     'width':'18px','background-color':'transparent',
                    #                     'border-color':'transparent'},
                    #             class_name='rounded-circle ml-4 pb-1'

                    #         ),

                    #         id="tooltip-sidebar-titulo",
                    #     ),

                    #     # TOOLTIP
                    #     dbc.Tooltip(
                    #         "Más información",
                    #         target="tooltip-sidebar-titulo",
                    #         placement = 'auto'
                    #     ),

                    #     # CONTENIDO MODAL
                    #     dbc.Modal([

                    #         dbc.ModalHeader(html.B("Radar Vial")),

                    #         dbc.ModalBody([
                            
                    #             dbc.Row([

                    #                 dbc.Col(['Datos de hechos viales del 2015 en adelante proporcionados por la Secretaría de Seguridad Pública y procesados mensualmente por el IMPLANG.',
                    #                     html.I(' Última actualización: Septiembre 2021')
                    #                     ]),

                    #             ]),

                    #             html.Br(),

                    #             dbc.Row([

                    #                 dbc.Col([
                                    
                    #                     html.Div([

                    #                         html.Span(
                                                
                    #                             html.Button([
                    #                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                    #                                         style={'width':'8%','float':'left'},
                    #                                         className="pt-1"),
                    #                                 html.B("Descargar Excel"),
                    #                                 ], 
                    #                                 id="btn_csv",
                    #                                 className="btn",
                    #                                 n_clicks=None,
                    #                                 style={'float':'right','background-color':'#BBC3C8','color':'white'}
                    #                             ),

                    #                             id="tooltip-target-descbd",
                    #                         ),

                    #                         dbc.Tooltip(
                    #                             "Descarga toda la base de datos",
                    #                             target="tooltip-target-descbd",
                    #                         ),

                                            
                    #                         Download(id="download-dataframe-csv")
                    #                     ], className='d-flex justify-content-center'),

                    #                 ], lg=4, md=4),

                    #                 dbc.Col([

                    #                     html.Div([

                    #                         html.Span(

                    #                             html.Button([
                    #                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                    #                                         style={'width':'8%','float':'left'},
                    #                                         className="pt-1"),
                    #                                 html.B("Descargar SHP"),
                    #                                 ], 
                    #                                 id="btn_shp",
                    #                                 className="btn",
                    #                                 n_clicks=None,
                    #                                 style={'float':'right','background-color':'#BBC3C8','color':'white'}
                    #                             ),
                                                        

                    #                             id="tooltip-target-shp",
                    #                         ),

                    #                         dbc.Tooltip(
                    #                             "Descarga toda la base de datos en SHP",
                    #                             target="tooltip-target-shp",
                    #                         ),

                    #                         Download(id="download-dataframe-shp")
                    #                     ], className='d-flex justify-content-center')

                    #                 ], lg=4, md=4)

                    #             ], class_name='d-flex justify-content-center'),

                    #         ],style={"textAlign":"justify",'font-size':'100%'}),

                    #         dbc.ModalFooter([
                                
                    #             dbc.Button(
                    #                 "Cerrar", 
                    #                 id="close_titulo", 
                    #                 class_name="ml-auto btn btn-secondary", 
                    #                 n_clicks=0
                    #             )
                    #         ]),

                    #         ],
                    #         id="modal_titulo",
                    #         centered=True,
                    #         size="lg",
                    #         is_open=False,
                    #         style={'font-family':'Arial'}
                    #     ),
                    # ]),

                ], class_name='d-flex align-items-center justify-content-center', style={'width':'100%'})

            ], class_name='m-0 pt-3 w-50 d-none d-lg-block'), 

            # TITULO MOVIL
            dbc.Row([

                dbc.Col([

                    html.Img(src='data:image/png;base64,{}'.format(encoded_img4), 
                                className="pt-0",
                                style={'width':'33px', 'height': '33px', 'float':'left', 'margin-right': '15px'}
                        ),

                    html.H2('Radar Vial', 
                        style={'float':'left', 'font-weight':'normal', 'font-size':'24px', 'margin-right': '15px'}, 
                        className='pl-3 pt-1 '
                    ),

                ], class_name='d-flex align-items-center justify-content-center', style={'width': '100%'})

            ], class_name='m-0 pt-3 w-100 d-lg-none'),

            # TITULO MD
            # dbc.Row([

            #     dbc.Col([

            #         html.Img(src='data:image/png;base64,{}'.format(encoded_img4), 
            #                     className="pt-0",
            #                     style={'width':'40px', 'height': '40px', 'float':'left', 'margin-right': '15px'}
            #             ),

            #         html.H2('Radar Vial', 
            #             style={'float':'left', 'font-weight':'normal', 'font-size':'25px', 'margin-right': '15px'}, 
            #             className='pl-3 pt-1 '
            #         ),

            #     ], class_name='d-flex align-items-center', style={'padding-left':'60px'})

            # ], style={'position':'absolute','left':'1px','top':'10px',}, class_name='m-0 pt-3 w-100 d-none d-md-block d-lg-none')

        ], className='d-flex align-items-center justify-content-center', style = {'width': '100%'}),

        # Tabs
        dbc.Row(

            dbc.Col(

                dbc.Card([

                    dbc.CardHeader(

                        dbc.Tabs([
                            dbc.Tab(label='Resumen', 
                                    tab_id='resumen', 
                                    label_style={'color':'#BBC3C8','border-top':'0px','border-bottom':'0px',
                                                'border-left':'0px','border-right':'0px', 'padding-right': '0px',
                                                'padding-left': '0px', 'margin-left': '.60rem'},
                                    active_label_style={'color': '#000000', 'border-bottom': '3px solid #000000',
                                                        'border-top':'0px', 'border-left':'0px', 'border-right':'0px',
                                                        'padding-right': '0px', 'margin-left': '.60rem'},
                                    label_class_name='pl-0 pr-0 pb-0 mb-2 ml-2', 
                                    active_label_class_name ='pl-0 pr-0 pb-0 mb-2 ml-2'),

                            dbc.Tab(label='Mapa', 
                                    tab_id='mapa', 
                                    label_style={'color':'#BBC3C8','border-top':'0px','border-bottom':'0px',
                                                'border-left':'0px','border-right':'0px', 'padding-right': '0px',
                                                'padding-left': '0px', 'margin-left': '2rem'},
                                    active_label_style={'color': '#000000', 'border-bottom': '3px solid #000000',
                                                        'border-top':'0px', 'border-left':'0px', 'border-right':'0px',
                                                        'padding-right': '0px', 'margin-left': '2rem'},
                                    label_class_name='pl-0 pr-0 pb-0 mb-2 ml-4', 
                                    active_label_class_name ='pl-0 pr-0 pb-0 mb-2 ml-4'),

                        ],
                        id='tabs',
                        active_tab="mapa",
                        class_name='d-flex flex-nowrap', #overflow-scroll'
                        style = {'font-size': '16px'}
                        ),
                        style={'background-color':'white', 'white-space': 'nowrap', 'overflow-x': 'auto',
                        'overflow-y': 'hidden', 'height': '44px', 'box-shadow': '0 8px 6px -6px rgba(0, 0, 0, 0.15)'},
                        class_name='d-flex flex-nowrap' #overflow-auto'
                    
                    ),

                    dbc.CardBody([
                    
                        html.Div(id="hechosviales_content")#, style = {'margin': '0px', 'padding': '0px'}, className = 'h-100'),
                        #html.Div(id="hechosviales_content_movil", className='d-block d-sm-none')
                    
                    ], style = {'margin': '0px', 'padding': '0px'}, class_name = 'h-100')

                ], style={'border':'none'}, color = '#F8F9FB'), lg=12, class_name='p-0'

            ), justify = 'center', class_name='m-0'

        ),

], style={'font-family':'Arial'})


#------

# CARGAR CONTENIDO TABS
def render_hechosviales(tab):
    if tab == 'resumen':
        return resumen()

    elif tab == 'mapa':
        return mapa()

    else:
        return mapa()

# CARGAR TABS
@app.callback(
    Output('hechosviales_content', 'children'), 
    [Input('tabs', 'active_tab')])
def get_hechosviales(tab):
    return render_hechosviales(tab)

# TAB RESUMEN
def resumen():

  return html.Div([

            html.Br(),

            # PÁRRAFO RESUMEN
            dbc.Row([

              dbc.Col([

                    dbc.Card([

                        dbc.CardBody([

                            dbc.Row([

                                dbc.Col([

                                    html.P(['Radar Vial es una plataforma de hechos viales del municipio de San Pedro, si quieres conocer más sobre como se obtinen los datos da ', 
                          
                                        html.B('click aquí'),
                                        
                                        '.',

                                        html.Br(),

                                        'Por otro lado el municipio desarrollo el diagnóstico de seguridad vial que es la guía para mejorar la seguridad de la ciudad, conoce el diagnóstico ',

                                        html.B('aquí'),
                                        
                                        '.',

                                    ])  

                                ]),

                            ]),
                            
                        ], style={'background-color':'#BBC3C8'})
                    ])

                ]),

            ], className='mx-0'),

            html.Br(),

            # BOTON MAPA
            dbc.Row([

                dbc.Col([

                      dbc.Card([

                          dbc.CardBody([

                              dbc.Row([

                                  dbc.Col([

                                      html.Img(src='assets/mapa_foto.png', className='img-fluid'),

                                      html.H1('Mapa', )

                                  ]),

                              ]),
                              
                          ])
                      ])

                ]),

            ], className='mx-0'),

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

                ], lg = 3, md = 12, sm = 12),

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

                ], lg = 3, md = 12, sm = 12),

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

                ], lg = 3, md = 12, sm = 12),

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

                ], lg = 3, md = 12, sm = 12),
            
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

                            html.H1(['Por tipo y sus causas']),
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

                # Por lesionados y fallecidos
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

            # FOOTER
            dbc.Row([

                dbc.Col([

                    dbc.Row([

                        dbc.Col([

                            html.Img(src='assets/logo_spgg.png', style={'width':'128.33px', 'height': '70px', 'float':'left'}),
                            html.Img(src='assets/implang_logo.png', style={'width':'121.7px', 'height': '49.2px', 'float':'left'}),

                        ], style={'padding-left': '15px'}, className='d-lg-flex justify-content-between my-3'),

                    ]),

                    dbc.Row([

                        dbc.Col([

                            html.B("Conmutador:"),
                            html.Br(),
                            "81 8400 4400"

                        ]),

                        dbc.Col([

                            html.B("Atención Ciudadana:"),
                            html.Br(),
                            "81 1365 5262"

                        ])

                    ]),

                    dbc.Row([

                        dbc.Col([

                            'atencion@sanpedro.gob.mx',
                            html.Br(),

                            html.B("Dirección:"),
                            html.Br(),
                            "Calle Juárez 101, Centro de San Pedro Garza García, N.L. C.P. 66200"

                        ])

                    ]),

                    dbc.Row([

                        dbc.Col([

                            dbc.Button(
                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                        style={'float':'right'},
                                        className="p-0 img-fluid"), 
                                id="open_titulo", 
                                n_clicks=0, 
                                style={'display':'inline-block',
                                        'float':'left','padding':'0', 
                                        'width':'18px','background-color':'transparent',
                                        'border-color':'transparent'},
                                class_name='rounded-circle ml-4 pb-1'

                            ),

                            dbc.Button(
                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                        style={'float':'right'},
                                        className="p-0 img-fluid"), 
                                id="open_titulo", 
                                n_clicks=0, 
                                style={'display':'inline-block',
                                        'float':'left','padding':'0', 
                                        'width':'18px','background-color':'transparent',
                                        'border-color':'transparent'},
                                class_name='rounded-circle ml-4 pb-1'

                            ),

                        ])

                    ])

                ])

            ], style={'background-color': '#000', 'color':'white'})

        ], style={'background-color': '#fafafa'}) 

# TAB MAPA
def mapa():

  return html.Div([

        # Mapa y filtros DESKTOP
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

                            ], style={'text-align':'center'}, class_name='p-0'),

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

                    ], lg=12, md=12, sm = 12),

                ], class_name="d-flex justify-content-between",),

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

                        ]),

                    ],lg=12, md=12),

                ]),

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

                        ]),
                        
                    ], lg=12, md=12),

                ]),

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
                    ])
                ])

            ],lg=4, md=4, style={'float': 'left'}),
            
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

            ],lg=8, md=8, style={'float': 'left'}),

        ], style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '10px'}, class_name = 'd-none d-lg-block'),

        # Mapa y filtros MÓVIL

        dbc.Row([

            dbc.Col([
                    
                dbc.Button(
                    'Filtros',
                    color = 'light',
                    class_name = 'filtros_small',
                    id = 'collapse-filtros-movil',
                    n_clicks = 0
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

            ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px'})

        ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px', 'height': '700px'}),

        dbc.Row([

            dbc.Col([

                dbc.Offcanvas([

                    # FILTROS FECHA
                    dbc.Card([

                        dbc.CardBody([

                            html.Div([

                                html.P([
                                    'Fecha'
                                ], 
                                style = {
                                    'font-size': '18px', 
                                    'font-weight': 'bold',
                                    'margin-bottom': '5px'
                                    }
                                )
                            ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

                            html.Hr(style = {'margin-top': '0px', 'padding-top': '0px'}),

                            html.Div([

                                dcc.DatePickerRange(
                                    id = 'calendario_movil',
                                    min_date_allowed = dt(2015, 1, 1),
                                    max_date_allowed = dt(2021, 9, 30),
                                    start_date = dt(2015, 1, 1),
                                    end_date = dt(2021, 9, 30),
                                    first_day_of_week = 1,
                                    className="d-flex justify-content-center",
                                    style = {
                                        'padding': '0px', 
                                        'margin': '0px'
                                    }
                                ),

                            ], className ='d-flex align-items-center justify-content-center', style = {'padding': '0px', 'margin': '0px'}),

                            html.Br(),

                            html.Div([

                                            dbc.Checklist(
                                            id = 'checklist_dias_movil',
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
                            ], style = {'padding-left': '10px', 'padding-right': '10px'}),

                            html.Br(),

                            dcc.RangeSlider(
                                            id='slider_hora_movil',
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
                            )
                        
                        ], style = {'padding': '0px', 'margin': '10px'})

                    ], style = {'margin-top': '15px', 'margin-left': '20px', 'margin-right': '20px'}),

                    html.Br(),

                    # FILTROS HECHOS VIALES
                    dbc.Card([

                        dbc.CardBody([

                            # TÍTULO
                            html.Div([

                                html.P([
                                    'Hechos Viales'
                                ], 
                                style = {
                                    'font-size': '18px', 
                                    'font-weight': 'bold',
                                    'margin-bottom': '5px'
                                    }
                                )
                            ], style={'margin-bottom': '0px'}),

                            html.Hr(style = {'margin-top': '0px'}),

                                    html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_sev_movil", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-sev-movil",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-sev-movil",
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
                                                    id="close1_sev_movil", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_sev_movil",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Gravedad',
                                            style={'width':'90%','float':'left'}, className='pl-1'),
    
                                    ]),

                                    dbc.RadioItems(
                                        id = 'hv_graves_opciones_movil',
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
                                                id="open1_usaf_movil", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-usaf-movil",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-usaf-movil"
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
                                                    id="close1_usaf_movil", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_usaf_movil",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Usuario', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'hv_usu_opciones_movil',
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
                                                id="open1_thv_movil", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                            ),

                                            id="tooltip-target-thv-movil",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-thv-movil",
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
                                                    id="close1_thv_movil", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_thv_movil",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Tipo de hecho vial', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_hv_movil',
                                        class_name = 'radio-group btn-group',
                                        label_class_name = 'btn btn-secondary',
                                        label_checked_class_name  = 'active',
                                        style={'display':'inline-block'},
                                        value = [],
                                        options = [],
                                    ),

                        ], style = {'padding': '0px', 'margin': '10px'})
                        
                    ], style = {'margin-top': '0px', 'margin-left': '20px', 'margin-right': '20px'}),

                    html.Br(),

                    dbc.Card([

                        dbc.CardBody([

                            html.Div([

                                html.P([
                                    'Búsqueda Avanzada'
                                ], 
                                style = {
                                    'font-size': '18px', 
                                    'font-weight': 'bold',
                                    'margin-bottom': '5px'
                                    }
                                )
                            ], style={'margin-bottom': '0px'}),

                            html.Hr(style = {'margin-top': '0px'}),

                            html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_afres_movil", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                class_name='rounded-circle'

                                                ),

                                            id="tooltip-target-afres-movil",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-afres-movil",
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
                                                    id="close1_afres_movil", 
                                                    class_name="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_afres_movil",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                            style={'font-family':'Arial'}
                                        ),

                                        html.P(' Afectado o responsable',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                            ]),

                                    dbc.RadioItems(
                                        id = 'hv_afres_opciones_movil',
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
                                        id = 'hv_sexo_opciones_movil',
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
                                        id='slider_edad_movil',
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
                                        id = 'checklist_tipo_veh_movil',
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

                        ], style = {'padding': '0px', 'margin': '10px'})

                    ], style = {'margin-bottom': '10px', 'margin-left': '20px', 'margin-right': '20px'})

                ], 
                placement = 'bottom', 
                close_button = False, 
                style = {
                    'padding-top': '5px', 
                    'padding-left': '5px', 
                    'padding-right': '5px', 
                    'margin': '0px', 
                    'background-color': '#F8F9FB',
                    'height': '400px'
                }, 
                id = 'filtros-movil', is_open = False)
            ], class_name = 'd-lg-none')
        ], class_name = 'd-lg-none')

    ], className = 'w-100 h-100', style = {'padding': '0px', 'margin': '0px'})



#-----------

#Modal Fecha
@app.callback(
    Output("modal_fecha", "is_open"),
    [Input("open_fecha", "n_clicks"), 
    Input("close_fecha", "n_clicks")],
    [State("modal_fecha", "is_open")],)

def toggle_modal_fecha(open_fecha, close_fecha, modal_fecha):
    if open_fecha or close_fecha:
        return not modal_fecha
    return modal_fecha

#Modal Gravedad
@app.callback(
    Output("modal_g", "is_open"),
    [Input("open_g", "n_clicks"), 
    Input("close_g", "n_clicks")],
    [State("modal_g", "is_open")],)

def toggle_modal_g(open_g, close_g, modal_g):
    if open_g or close_g:
        return not modal_g
    return modal_g

#Modal Usuario
@app.callback(
    Output("modal_u", "is_open"),
    [Input("open_u", "n_clicks"), 
    Input("close_u", "n_clicks")],
    [State("modal_u", "is_open")],)

def toggle_modal_u(open_u, close_u, modal_u):
    if open_u or close_u:
        return not modal_u
    return modal_u

# Por mes y dia del año
@app.callback(Output('pub_periodo', 'figure'),
    [Input('pub_tiempos', 'value')])

def update_output(pub_tiempos):
    return render_pub_periodo(pub_tiempos)

# Por vulnerabilidad de usuario
@app.callback(Output('pub_vulne', 'figure'),
    [Input('pub_vul_año', 'value')])

def update_output(pub_vulne):
    return render_pub_vulne(pub_vulne)

# Por tipo de usuario
@app.callback(Output('pub_time', 'figure'),
    [Input('pub_gravedad', 'value')])

def update_output(pub_gravedad):
    return render_pub_time(pub_gravedad)

### -------

# RADAR VIAL - MAPA: CARGAR OPCIONES POR USUARIO
@app.callback(
    Output('checklist_tipo_hv', 'options'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)
def get_opciones_dos(hv_usu_opciones, hv_graves_opciones):
    return render_opciones_dos(hv_usu_opciones, hv_graves_opciones)

# RADAR VIAL - MAPA: CARGAR OPCIONES POR USUARIO - MOVIL
@app.callback(
    Output('checklist_tipo_hv_movil', 'options'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    prevent_initial_call=False)
def get_opciones_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil):
    return render_opciones_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil)

# RADAR VIAL - MAPA: CARGAR VALORES POR USUARIO
@app.callback(
    Output('checklist_tipo_hv', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)
def get_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones):
    return render_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones)

# RADAR VIAL - MAPA: CARGAR VALORES POR USUARIO - MOVIL
@app.callback(
    Output('checklist_tipo_hv_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    prevent_initial_call=False)
def get_opciones_dos_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil):
    return render_opciones_dos_dos_movil(hv_usu_opciones_movil, hv_graves_opciones_movil)

# RADAR VIAL - MAPA: HECHOS VIALES TOTALES
@app.callback(
    Output('hv_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: HECHOS VIALES TOTALES
@app.callback(
    Output('hv_totales_movil', 'children'), 
    [Input('calendario_movil', 'start_date'),
    Input('calendario_movil', 'end_date'),
    Input('slider_hora_movil', 'value'),
    Input('checklist_dias_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('checklist_tipo_hv_movil', 'value'),
    Input('hv_afres_opciones_movil', 'value'),
    Input('hv_sexo_opciones_movil', 'value'),
    Input('checklist_tipo_veh_movil', 'value'),
    Input('slider_edad_movil', 'value')])
def get(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):
    return render_hv_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil)

# RADAR VIAL - MAPA: LESIONADOS
@app.callback(
    Output('hv_les_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_les_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: LESIONADOS - MOVIL
@app.callback(
    Output('hv_les_totales_movil', 'children'), 
    [Input('calendario_movil', 'start_date'),
    Input('calendario_movil', 'end_date'),
    Input('slider_hora_movil', 'value'),
    Input('checklist_dias_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('checklist_tipo_hv_movil', 'value'),
    Input('hv_afres_opciones_movil', 'value'),
    Input('hv_sexo_opciones_movil', 'value'),
    Input('checklist_tipo_veh_movil', 'value'),
    Input('slider_edad_movil', 'value')])
def get(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):
    return render_hv_les_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil)

# RADAR VIAL - MAPA: FALLECIDOS
@app.callback(
    Output('hv_fall_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_fall_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: FALLECIDOS - MOVIL
@app.callback(
    Output('hv_fall_totales_movil', 'children'), 
    [Input('calendario_movil', 'start_date'),
    Input('calendario_movil', 'end_date'),
    Input('slider_hora_movil', 'value'),
    Input('checklist_dias_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('checklist_tipo_hv_movil', 'value'),
    Input('hv_afres_opciones_movil', 'value'),
    Input('hv_sexo_opciones_movil', 'value'),
    Input('checklist_tipo_veh_movil', 'value'),
    Input('slider_edad_movil', 'value')])
def get(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):
    return render_hv_fall_totales_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil)

# RADAR VIAL - MAPA: MAPA INTERACTIVO
@app.callback(
    [Output('mapa_interac', 'figure'),
     Output('mapa_data_top', 'data')], 
    [Input('calendario', 'start_date'),
     Input('calendario', 'end_date'),
     Input('slider_hora', 'value'),
     Input('checklist_dias', 'value'),
     Input('hv_graves_opciones', 'value'),
     Input('hv_usu_opciones', 'value'),
     Input('checklist_tipo_hv', 'value'),
     Input('hv_afres_opciones', 'value'),
     Input('hv_sexo_opciones', 'value'),
     Input('checklist_tipo_veh', 'value'),
     Input('slider_edad', 'value')],
            prevent_initial_call=False)
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: MAPA MOVIL
@app.callback(
    Output('mapa_interac_movil', 'figure'),
     #Output('mapa_data_top', 'data')], 
    [Input('calendario_movil', 'start_date'),
    Input('calendario_movil', 'end_date'),
    Input('slider_hora_movil', 'value'),
    Input('checklist_dias_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('checklist_tipo_hv_movil', 'value'),
    Input('hv_afres_opciones_movil', 'value'),
    Input('hv_sexo_opciones_movil', 'value'),
    Input('checklist_tipo_veh_movil', 'value'),
    Input('slider_edad_movil', 'value')],
            prevent_initial_call=False)
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_mapa_interac_movil(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: MAPA DATA
@app.callback(Output('mapa_data', 'data'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_mapa_data(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

# RADAR VIAL - MAPA: TABLA TOP INTERSECCIONES
@app.callback(
    Output('tabla_mapa_top', 'figure'), 
    Input('mapa_data_top', 'data'))  
def update_output(mapa_data_top):
    return render_tabla_mapa_top(mapa_data_top)

# RADAR VIAL - MAPA: DESCARGA TU BÚSQUEDA
@app.callback(
    Output("download-personal-csv", "data"),
    Input("btn_perso_csv", "n_clicks"),
    State('mapa_data', 'data'),
    prevent_initial_call=True,)
def func(n_clicks, data):
    return render_down_data_csv(n_clicks, data)

# RADAR VIAL - MAPA: MODAL GRAVEDAD
@app.callback(
    Output("modal_sev", "is_open"),
    [Input("open1_sev", "n_clicks"), 
    Input("close1_sev", "n_clicks")],
    [State("modal_sev", "is_open")],)
def toggle_modal_sev(open1_sev, close1_sev, modal_sev):
    if open1_sev or open1_sev:
        return not modal_sev
    return modal_sev

# RADAR VIAL - MAPA: MODAL USUARIO
@app.callback(
    Output("modal_usaf", "is_open"),
    [Input("open1_usaf", "n_clicks"), 
    Input("close1_usaf", "n_clicks")],
    [State("modal_usaf", "is_open")],)
def toggle_modal_usaf(open1_usaf, close1_usaf, modal_usaf):
    if open1_usaf or close1_usaf:
        return not modal_usaf
    return modal_usaf

# RADAR VIAL - MAPA: MODAL TIPO DE HECHOS VIAL
@app.callback(
    Output("modal_thv", "is_open"),
    [Input("open1_thv", "n_clicks"), 
    Input("close1_thv", "n_clicks")],
    [State("modal_thv", "is_open")],)
def toggle_modal_thv(open1_thv, close1_thv, modal_thv):
    if open1_thv or close1_thv:
        return not modal_thv
    return modal_thv

# RADAR VIAL - MAPA: MODAL AFECTADO O RESPONSABLE 
@app.callback(
    Output("modal_afres", "is_open"),
    [Input("open1_afres", "n_clicks"), 
    Input("close1_afres", "n_clicks")],
    [State("modal_afres", "is_open")],)
def toggle_modal_afres(open1_afres, close1_afres, modal_afres):
    if open1_afres or close1_afres:
        return not modal_afres
    return modal_afres

# COLLAPSE FILTROS MOVIL
@app.callback(
    Output("filtros-movil", "is_open"),
    [Input("collapse-filtros-movil", "n_clicks")],
    [State("filtros-movil", "is_open")])
def toggle_collapse_filtros_movil(n, is_open):
    if n:
        return not is_open
    return is_open

### -------


if __name__ == '__main__':
	app.run_server(debug=True)


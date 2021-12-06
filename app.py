from dash import dash, html, dcc
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import base64
from datetime import datetime as dt
from dash_extensions import Download
from dash_extensions.snippets import send_file
from dash_extensions.snippets import send_data_frame


app = dash.Dash(__name__, title='Radar Vial',
                #
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

app.config.suppress_callback_exceptions = True

server = app.server

# Connect to app pages
# from apps import home, visualizaciones, radarvial

# from apps.home import (render_collapse_button_fecha, render_collapse_button_hv, render_hv_totales_movil, render_hv_fall_totales_movil, render_hv_les_totales_movil, render_opciones_dos_dos_movil, render_opciones_dos_movil, render_tabla_mapa_top_movil, toggle_modal_sev, toggle_modal_usaf, render_opciones_dos,
#   render_opciones_dos_dos, toggle_modal_thv, render_collapse_button_bavan, toggle_modal_afres, render_hv_totales, render_hv_les_totales, 
#   render_hv_fall_totales, render_mapa_interac, render_mapa_interac_movil, render_tabla_mapa_top, render_mapa_data, render_mapa_data_movil, render_down_data_csv)

# from apps.visualizaciones import (render_pub_periodo, render_pub_vulne, render_pub_time)

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#----------------------------------------------------------

## IMAGENES

radar_img = "https://cdn-icons-png.flaticon.com/512/188/188595.png"

img1 = 'assets/down-arrow.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

img3 = 'assets/descargar.png' # replace with your own image
encoded_img3 = base64.b64encode(open(img3, 'rb').read()).decode('ascii')

img4 = 'assets/radarvial_logo_bn.png' # replace with your own image
encoded_img4 = base64.b64encode(open(img4, 'rb').read()).decode('ascii')

img5 = 'assets/boton_filtros_movil.png' # replace with your own image
encoded_img5 = base64.b64encode(open(img5, 'rb').read()).decode('ascii')

img6 = 'assets/line_chart_down.png' # replace with your own image
encoded_img6 = base64.b64encode(open(img6, 'rb').read()).decode('ascii')

img7 = 'assets/expand.png' # replace with your own image
encoded_img7 = base64.b64encode(open(img7, 'rb').read()).decode('ascii')

peat = 'assets/peaton.png' # replace with your own image
peat_img = base64.b64encode(open(peat, 'rb').read()).decode('ascii')

hv = 'assets/hv.png' # replace with your own image
hv_img = base64.b64encode(open(hv, 'rb').read()).decode('ascii')

lesionado = 'assets/lesionado.png' # replace with your own image
lesionado_img = base64.b64encode(open(lesionado, 'rb').read()).decode('ascii')

fallecido = 'assets/fallecido.png' # replace with your own image
fallecido_img = base64.b64encode(open(fallecido, 'rb').read()).decode('ascii')

twitter = 'assets/twitter.png' # replace with your own image
twitter_img = base64.b64encode(open(twitter, 'rb').read()).decode('ascii')

insta = 'assets/instagram.png' # replace with your own image
insta_img = base64.b64encode(open(insta, 'rb').read()).decode('ascii')

back = 'assets/back.png' # replace with your own image
back_img = base64.b64encode(open(back, 'rb').read()).decode('ascii')

mapa_foto = 'assets/mapa_foto.png' # replace with your own image
mapa_foto_img = base64.b64encode(open(mapa_foto, 'rb').read()).decode('ascii')


#----------------------------------------------------------

## FIGURAS Y TABLAS

# FIGURAS RESUMEN

# HECHOS VIALES TOTALES
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

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

#Transformar datos en años
hvi = hvi.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','lesionados','fallecidos','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

# Cambiar nombre columnas
hvi.columns = ["".join(a) for a in hvi.columns.to_flat_index()]
hvi = hvi.reset_index()
hvi['fecha'] = hvi.fecha.dt.strftime('%Y')

# GRAFICA
tot_hv = px.bar(hvi,
    x='fecha',
    y=["hechos_viales"], 
    labels = {'fecha': ''}, 
    template = 'plotly_white')
tot_hv.update_traces(name='',
    hovertemplate="<b>%{x}</b><br> %{y} hechos viales"
    )
tot_hv.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=hvi['fecha'],
    ticklabelmode='period',
    fixedrange = True)
tot_hv.update_yaxes(fixedrange = True)
tot_hv.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    showlegend = False,
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font=dict(
        family="Arial",
        size=16,
        ),
    yaxis_title = None
    )

# GRAFICA PARA EXPAND
tot_hv_modal = px.bar(hvi,
    x='fecha',
    y=["hechos_viales"], 
    labels = {'fecha': ''}, 
    template = 'plotly_white')
tot_hv_modal.update_traces(name='',
    hovertemplate="<b>%{x}</b><br> %{y} hechos viales"
    )
tot_hv_modal.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=hvi['fecha'],
    ticklabelmode='period')
tot_hv_modal.update_yaxes(title_text='Hechos viales')
tot_hv_modal.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    showlegend = False,
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    height = 600,
    font=dict(
        family="Arial",
        size=16,
        )
    )

#-------------

# PERSONAS
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

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

#Transformar datos en años
hvi_l = hvi.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','hechos_viales','fallecidos','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)
hvi_f = hvi.resample("Y").sum().drop(['hora','Lat','Lon','les_fall','hechos_viales','lesionados','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1)

# Filtro por hechos viales ilesos y lesionados+fallecidos
hvi_l = hvi_l[hvi_l.lesionados != 0].reset_index().rename(columns={'lesionados':'Lesionados'})
hvi_f = hvi_f[hvi_f.fallecidos != 0].reset_index().rename(columns={'fallecidos':'Fallecidos'})

#Merge los dataframes
df = pd.merge(hvi_l, hvi_f, on ='fecha', how ='left')
df['fecha_ind'] = df.fecha .dt.strftime('%Y')

# GRAFICA
# per_grav = px.bar(df,
#     x='fecha_ind',
#     y=["Lesionados","Fallecidos"], 
#     labels = {'fecha': ''}, 
#     template = 'plotly_white')
# per_grav.update_traces(hovertemplate="<b>%{x}</b><br> %{y} personas")
# per_grav.update_xaxes(showgrid = False, 
#     title_text='', 
#     ticktext=df['fecha_ind'],
#     ticklabelmode='period',
#     fixedrange = True)
# per_grav.update_yaxes(title_text='Personas', fixedrange = True)
# per_grav.update_layout(hoverlabel = dict(font_size = 16),
#     hoverlabel_align = 'right',
#     legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         y=-0.2,
#         x=0.3,
#         itemclick = 'toggleothers',
#         title=None
#         ),
#     margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
#     font=dict(
#         family="Arial",
#         size=16,
#         ),
#     yaxis_title = None
#     )

per_grav = go.Figure()

per_grav.add_trace(go.Bar(
    x = df['fecha_ind'],
    y = df['Lesionados'],
    name = 'Lesionados',
    marker_color = '#F3BB46',
    hovertemplate="<b>%{x}</b><br> %{y} personas"
))

per_grav.add_trace(go.Bar(
    x = df['fecha_ind'],
    y = df['Fallecidos'],
    name = 'Fallecidos',
    marker_color = '#DB4453',
    hovertemplate="<b>%{x}</b><br> %{y} personas"
))

per_grav.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        x=0.3,
        itemclick = 'toggleothers',
        title=None
        ),
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font=dict(
        family="Arial",
        size=16,
        ),
    yaxis_title = None,
    template = 'plotly_white',
    barmode = 'stack'
    )

# GRAFICA PARA EXPAND
per_grav_modal = px.bar(df,
    x='fecha_ind',
    y=["Lesionados","Fallecidos"], 
    labels = {'fecha': ''}, 
    template = 'plotly_white')
per_grav_modal.update_traces(hovertemplate="<b>%{x}</b><br> %{y} personas")
per_grav_modal.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=df['fecha_ind'],
    ticklabelmode='period')
per_grav_modal.update_yaxes(title_text='Personas')
per_grav_modal.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        x=0.3,
        itemclick = 'toggleothers',
        title=None
        ),
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )

#-------------

# HECHOS VIALES PROMEDIO
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

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

# Filtro por hechos viales ilesos y lesionados+fallecidos
hvi_il = hvi[hvi.les_fall == 0]
hvi_lf = hvi[hvi.les_fall != 0]

#Transformar datos sin lesiones en meses
hvi_il = hvi_il.resample("M").sum().drop(['hora','Lat','Lon','lesionados','fallecidos','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1).reset_index()
hvi_il['mes'] = hvi_il['fecha'].dt.strftime('%m')
hvi_il = hvi_il.groupby(hvi_il.mes)['hechos_viales'].mean().round(0).reset_index().rename(columns={'hechos_viales':'Sin Lesiones'})

#Transformar datos graves en meses
hvi_lf = hvi_lf.resample("M").sum().drop(['hora','Lat','Lon','lesionados','fallecidos','les_fall','num_resp','num_afect','edad_afect_mid','edad_resp_mid'], axis=1).reset_index()
hvi_lf['mes'] = hvi_lf['fecha'].dt.strftime('%m')
hvi_lf = hvi_lf.groupby(hvi_lf.mes)['hechos_viales'].mean().round(0).reset_index().rename(columns={'hechos_viales':'Graves'})

df = pd.merge(hvi_il, hvi_lf, on ='mes', how ='left')
df['mes'] = pd.to_datetime(df['mes'], format ='%m').dt.strftime('%B')
df['mes'] = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

# GRAFICA
tot_prom = px.bar(df,
    x='mes',
    y=["Sin Lesiones","Graves"], 
    labels = {'mes': ''}, 
    template = 'plotly_white')
tot_prom.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
tot_prom.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=df['mes'],
    ticklabelmode='period',
    fixedrange = True
    )
tot_prom.update_yaxes(title_text='Hechos viales', fixedrange = True)
tot_prom.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        x=0.3,
        itemclick = 'toggleothers',
        title=None
        ),
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font=dict(
        family="Arial",
        size=16,
        )
    )

# GRAFICA PARA EXPAND
tot_prom_modal = px.bar(df,
    x='mes',
    y=["Sin Lesiones","Graves"], 
    labels = {'mes': ''}, 
    template = 'plotly_white')
tot_prom_modal.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
tot_prom_modal.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=df['mes'],
    ticklabelmode='period'
    )
tot_prom_modal.update_yaxes(title_text='Hechos viales')
tot_prom_modal.update_layout(
    hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        x=0.3,
        itemclick = 'toggleothers',
        title=None
        ),
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )

#-------------

#POR DIA DE LA SEMANA Y HORA
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')
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

df = (hvi_pub.pivot_table(index="hora", columns=["dia_semana"], values=["hechos_viales"], aggfunc=np.sum)/7).round(0)
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

# GRAFICA
heatmap = go.Figure(data=go.Heatmap(
   name='',
   z=df_hp,
   x=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
   y=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','18','19','20','21','22','23',], 
   hoverongaps = False,
   colorscale='Blues'))
heatmap.update_traces(hovertemplate="<b>%{x} a las %{y} horas:</b> <br>%{z} hechos viales")
heatmap.update_yaxes(title_text='Horas', fixedrange = True)
heatmap.update_xaxes(fixedrange = True)
heatmap.update_layout(barmode='stack',
    hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    plot_bgcolor='white',
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font=dict(
        family="Arial",
        size=16,
        )
    )

# GRAFICA PARA EXPAND
heatmap_modal = go.Figure(data=go.Heatmap(
   name='',
   z=df_hp,
   x=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
   y=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','18','19','20','21','22','23',], 
   hoverongaps = False,
   colorscale='Blues'))
heatmap_modal.update_traces(hovertemplate="<b>%{x} a las %{y} horas:</b> <br>%{z} hechos viales")
heatmap_modal.update_layout(barmode='stack',
    hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    plot_bgcolor='white',
    #margin = dict(t=30, l=10, r=10, b=30))
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )

#-------------

# POR TIPO DE HECHO VIAL

# Leer csv
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

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

# Crear una tabla por tipo de hecho vial con las causas en las columnas y que tenga la suma del número de hechos viales 
causa_hv = hvi.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum)

# Reemplazar NAs con ceros
causa_hv = causa_hv.fillna(0)

# Hacer una tabla con las causas apiladas
st_causas = causa_hv['hechos_viales'].stack()

# Repetir tipo de hecho vial y convertir a DataFrame
df_causas = pd.DataFrame(st_causas, columns=['hechos_viales']).reset_index()
df_causas['Total'] = df_causas['hechos_viales'].count()*['Total']

# Quitar índice
causa_hv = causa_hv.reset_index()

# Cambiar nombre columnas
causa_hv.columns = [" ".join(a) for a in causa_hv.columns.to_flat_index()]
strings = causa_hv.columns.values
new_strings = []

for string in strings:
    new_string = string.replace("hechos_viales ", '')
    new_strings.append(new_string)

# GRAFICA
treemap = px.treemap(df_causas, 
    path=['tipo_accidente', 'causa_accidente'], 
    values='hechos_viales',
    color='causa_accidente',
    )
treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0),
    font=dict(
        family="Arial",
        size=16,
        )
    )
treemap.data[0].hovertemplate = '%{label}<br>%{value}'

# GRAFICA PARA EXPAND
treemap_modal = px.treemap(df_causas, 
    path=['tipo_accidente', 'causa_accidente'], 
    values='hechos_viales',
    color='causa_accidente')
treemap_modal.update_layout(margin = dict(t=0, l=0, r=0, b=0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )
treemap_modal.data[0].hovertemplate = '%{label}<br>%{value}'

#-------------

#LESIONADOS Y FALLECIDOS POR TIPO DE HECHO VIAL

hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

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

# Filtro por hechos viales ilesos y lesionados+fallecidos
hvi_l = hvi[hvi.lesionados != 0]
hvi_f = hvi[hvi.fallecidos != 0]

hvi_l = hvi_l.groupby(hvi_l.tipo_accidente)['hechos_viales'].count().round(0).reset_index().rename(columns={'hechos_viales':'Lesionados'})
hvi_f = hvi_f.groupby(hvi_f.tipo_accidente)['hechos_viales'].count().round(0).reset_index().rename(columns={'hechos_viales':'Fallecidos'})

df = pd.merge(hvi_l, hvi_f, on ='tipo_accidente', how ='left').fillna(0)
df['les_fall'] = df.Lesionados + df.Fallecidos
df = df.sort_values(by=['les_fall'], ascending=False)

# GRAFICA
# lf_tipo_hv = px.bar(df,
#     y='tipo_accidente',
#     x=["Lesionados","Fallecidos"], 
#     labels = {'tipo_accidente': ''}, 
#     template = 'plotly_white',
#     orientation = 'h')
# lf_tipo_hv.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
# lf_tipo_hv.update_xaxes(showgrid = False, 
#     title_text='', 
#     ticktext=df['tipo_accidente'],
#     ticklabelmode='period',
#     fixedrange = True)
# lf_tipo_hv.update_yaxes(fixedrange = True)
# lf_tipo_hv.update_layout(
#     yaxis={'categoryorder':'total ascending'},
#     hoverlabel = dict(font_size = 16),
#     hoverlabel_align = 'right',
#     margin = dict(t=00, l=00, r=00, b=00),
#     legend=dict(
#         orientation="h",
#         yanchor = "bottom",
#         y = -0.15,
#         xanchor = "left",
#         x = -0.7,
#         itemclick = 'toggleothers',
#         title=None
#         ),
#     font=dict(
#         family="Arial",
#         size=16,
#         ),
#     yaxis_title = None
#     )

lf_tipo_hv = go.Figure()

lf_tipo_hv.add_trace(go.Bar(
    x = df['Lesionados'],
    y = df['tipo_accidente'],
    name = 'Lesionados',
    orientation = 'h',
    marker_color = '#F3BB46',
    hovertemplate="<b>%{x}</b><br> %{y} hechos viales"
))

lf_tipo_hv.add_trace(go.Bar(
    x = df['Fallecidos'],
    y = df['tipo_accidente'],
    name = 'Fallecidos',
    orientation = 'h',
    marker_color = '#DB4453',
    hovertemplate="<b>%{x}</b><br> %{y} hechos viales"
))

lf_tipo_hv.update_yaxes(fixedrange = True)
lf_tipo_hv.update_xaxes(fixedrange = True)

lf_tipo_hv.update_layout(
    yaxis={'categoryorder':'total ascending'},
    hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    margin = dict(t=00, l=00, r=00, b=00),
    legend=dict(
        orientation="h",
        yanchor = "bottom",
        y = -0.15,
        xanchor = "left",
        x = -0.7,
        itemclick = 'toggleothers',
        title=None
        ),
    font=dict(
        family="Arial",
        size=16,
        ),
    yaxis_title = None,
    template = 'plotly_white',
    barmode = 'stack'
    )

# GRAFICA PARA EXPAND
lf_tipo_hv_modal = px.bar(df,
    x='tipo_accidente',
    y=["Lesionados","Fallecidos"], 
    labels = {'tipo_accidente': ''}, 
    template = 'plotly_white')
lf_tipo_hv_modal.update_traces(hovertemplate="<b>%{x}</b><br> %{y} hechos viales")
lf_tipo_hv_modal.update_xaxes(showgrid = False, 
    title_text='', 
    ticktext=df['tipo_accidente'],
    ticklabelmode='period')
lf_tipo_hv_modal.update_yaxes(title_text='Hechos viales')
lf_tipo_hv_modal.update_layout(hoverlabel = dict(font_size = 16),
    hoverlabel_align = 'right',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        x=0.3,
        itemclick = 'toggleothers',
        title=None
        ),
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )


# TOP CALLES
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

hvt = hvi.hechos_viales.sum()
hvi_c = hvi.pivot_table(index="calle", values=["hechos_viales"], aggfunc=np.sum).fillna(0).reset_index().sort_values(by=['hechos_viales'], ascending=False)
hvi_c = hvi_c.iloc[0:10,:]
#hvi_c['hechos_viales'] = ((hvi_c['hechos_viales']/hvt)*100).round(2)

# TABLA
top_c = pd.DataFrame()
top_c[''] = hvi_c['calle']
top_c['Hechos Viales'] = hvi_c['hechos_viales']

colors = ['rgb(8,48,107)', 'rgb(8,81,156)', 'rgb(33,113,181)', 'rgb(66,146,198)', 'rgb(107,174,214)', 'rgb(158,202,225)', 'rgb(198,219,239)', 'rgb(222,235,247)', 'rgb(247,251,255)']

top_c = go.Figure(
    data = go.Table(
        columnwidth = [100, 50],
        header = dict(
            values = list(top_c.columns),
            fill_color = 'white',
            align = 'center'
        ),
        cells = dict(
            values = [top_c[''], top_c['Hechos Viales']],
            line_color = 'white',
            fill_color = ['white', colors],
            align = ['left', 'center'],
            font = dict(
                color = ['black', 'black']
            ),
            height = 30
        )
    )
)

top_c.update_layout(
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font = dict(family = 'Arial', size = 16)
)

# # GRAFICA
# top_c = px.bar(hvi_c, x = "hechos_viales", y = "calle",
#     orientation = 'h',
#     template = 'plotly_white')
# top_c.update_layout(yaxis={'categoryorder':'total ascending'},
#     showlegend = False,
#     uniformtext_minsize = 8,
#     uniformtext_mode = 'hide',
#     margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
#     font=dict(
#         family="Arial",
#         size=16,
#         )
#     )
# top_c.update_xaxes(showgrid = True,
#     showline = True, 
#     title_text = '',
#     fixedrange = True)
# top_c.update_yaxes(title_text = '', fixedrange = True)
# top_c.update_traces(texttemplate = '<b>%{x}%</b>',
#     textposition = 'inside',
#     hovertemplate = None,
#     hoverinfo = 'skip')

# GRAFICA PARA EXPAND
top_c_modal = px.bar(hvi_c, x = "hechos_viales", y = "calle",
    orientation = 'h',
    template = 'plotly_white')
top_c_modal.update_layout(yaxis={'categoryorder':'total ascending'},
    showlegend = False,
    uniformtext_minsize = 8,
    uniformtext_mode = 'hide',
    margin = dict(t=0, l=0, r=0, b=0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )
top_c_modal.update_xaxes(showgrid = True,
    showline = True, 
    title_text = '')
top_c_modal.update_yaxes(title_text = '')
top_c_modal.update_traces(texttemplate = '<b>%{x}%</b>',
    textposition = 'inside',
    hovertemplate = None,
    hoverinfo = 'skip')

#-------------

# TOP INTERSECCIONES
hvi = pd.read_csv("assets/hechosviales_lite_completa.csv", encoding='ISO-8859-1')

hvt = hvi.hechos_viales.sum()
hvi_i = hvi.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).fillna(0).reset_index().sort_values(by=['hechos_viales'], ascending=False)
hvi_i = hvi_i.iloc[0:10,:]
#hvi_i['hechos_viales'] = ((hvi_i['hechos_viales']/hvt)*100).round(2)

# TABLA
top_i = pd.DataFrame()
top_i[''] = hvi_i['interseccion']
top_i['Hechos Viales'] = hvi_i['hechos_viales']

colors = ['rgb(8,48,107)', 'rgb(8,81,156)', 'rgb(33,113,181)', 'rgb(66,146,198)', 'rgb(107,174,214)', 'rgb(158,202,225)', 'rgb(198,219,239)', 'rgb(222,235,247)', 'rgb(247,251,255)']

top_i = go.Figure(
    data = go.Table(
        columnwidth = [120, 30],
        header = dict(
            values = list(top_i.columns),
            fill_color = 'white',
            align = 'center'
        ),
        cells = dict(
            values = [top_i[''], top_i['Hechos Viales']],
            line_color = 'white',
            fill_color = ['white', colors],
            align = ['left', 'center'],
            font = dict(
                color = ['black', 'black']
            ),
            height = 30
        )
    )
)

top_i.update_layout(
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
    font = dict(family = 'Arial', size = 14)
)

# GRAFICA
# top_i = px.bar(hvi_i, x = "hechos_viales", y = "interseccion",
#     orientation = 'h',
#     template = 'plotly_white')
# top_i.update_layout(yaxis={'categoryorder':'total ascending'},
#     showlegend = False,
#     uniformtext_minsize = 8,
#     uniformtext_mode = 'hide',
#     margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0),
#     font=dict(
#         family="Arial",
#         size=16,
#         )
#     )
# top_i.update_xaxes(showgrid = True,
#     showline = True, 
#     title_text = '',
#     fixedrange = True)
# top_i.update_yaxes(title_text = '', fixedrange = True)
# top_i.update_traces(texttemplate = '<b>%{x}%</b>',
#     textposition = 'inside',
#     hovertemplate = None,
#     hoverinfo = 'skip')

# GRAFICA PARA EXPAND
top_i_modal = px.bar(hvi_i, x = "hechos_viales", y = "interseccion",
    orientation = 'h',
    template = 'plotly_white')
top_i_modal.update_layout(yaxis={'categoryorder':'total ascending'},
    showlegend = False,
    uniformtext_minsize = 8,
    uniformtext_mode = 'hide',
    margin = dict(t=0, l=0, r=0, b=0),
    height = 550,
    font=dict(
        family="Arial",
        size=16,
        )
    )
top_i_modal.update_xaxes(showgrid = True,
    showline = True, 
    title_text = '')
top_i_modal.update_yaxes(title_text = '')
top_i_modal.update_traces(texttemplate = '<b>%{x}%</b>',
    textposition = 'inside',
    hovertemplate = None,
    hoverinfo = 'skip')

#----------------------------------------------------------

## LAYOUT

# LAYOUT HEADER

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

                ], class_name='d-flex align-items-center justify-content-center', style={'width':'100%'}),

            ], class_name='m-0 pt-3 w-50 d-none d-lg-block'), 

            # TITULO MOVIL
            dbc.Row([

                dbc.Col([

                    dbc.Button(
                        [html.Img(src='data:image/png;base64,{}'.format(back_img),
                                style = {'width': '15px', 'height': '15px'})], 
                        id="boton_back", 
                        n_clicks=0, 
                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                        class_name = ''
                    ),

                    html.Img(src='data:image/png;base64,{}'.format(encoded_img4), 
                                className="pt-0",
                                style={'float':'left', 'margin-right': '15px'}
                        ),

                    # html.H2('Radar Vial', 
                    #     style={'float':'left', 'font-weight':'normal', 'font-size':'24px', 'margin-right': '15px'}, 
                    #     className='pl-3 pt-1 '
                    # ),


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
                        active_tab="resumen",
                        class_name='d-flex flex-nowrap', #overflow-scroll'
                        style = {'font-size': '16px'}
                        ),
                        style={'background-color':'white', 'white-space': 'nowrap', 'overflow-x': 'auto',
                        'overflow-y': 'hidden', 'height': '44px', 'box-shadow': '0 8px 6px -6px rgba(0, 0, 0, 0.15)'},
                        class_name='d-flex flex-nowrap' #overflow-auto'
                    
                    ),

                    dbc.CardBody([
                    
                        # html.Div(id="hechosviales_content")#, style = {'margin': '0px', 'padding': '0px'}, className = 'h-100'),
                        #html.Div(id="hechosviales_content_movil", className='d-block d-sm-none')



                        # RESUMEN
                        html.Div([

                            html.Br(),

                            # PÁRRAFO RESUMEN
                            dbc.Row([

                              dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            dbc.Row([

                                                dbc.Col([

                                                    html.P(['Radar Vial es la plataforma de hechos viales del municipio de San Pedro que utilizamos con el objetivo de reducir el número de fallecimientos y lesiones graves ocasionados por hechos de tránsito a cero.',

                                                        html.Br(),

                                                        html.Br(),

                                                        'Conoce más sobre la plataforma dando ',

                                                        dbc.Button(
                                                            [html.B('click aquí')], 
                                                            id="open1_inforadar", 
                                                            n_clicks=0, 
                                                            style={'display':'inline-block', 'background-color':'transparent',
                                                                'border-color':'transparent', 'padding': '0px', 'margin': '0px', 'color': '#279FD7', 'font-size': '14px'}
                                                        ),

                                                    ], style = {'font-size': '14px', 'margin-bottom': '0px', 'margin-left': '0px', 'margin-right': '0px'}),

                                                    dbc.Modal([

                                                    dbc.ModalHeader([html.P("Radar Vial", style = {'font-size': '18px', 'font-weight': 'bold', 'margin-bottom': '0px'})]),

                                                    dbc.ModalBody([
                                                        
                                                        html.P(
                                                            'Cada año en promedio fallecen 8 y resultan con lesiones graves 159 personas en el municipio. En San Pedro Garza García reconocemos que las lesiones graves y fallecimientos ocasionados por hechos de tránsito no son “accidentes” y por lo tanto pueden ser evitadas a traves de educación, adecuaciones viales y aplicación de la ley.' 
                                                        ),

                                                        html.Br(),

                                                        html.P('Nuestro objetivo es alcanzar la meta de 0 fallecimientos y 0 lesiones graves a nivel municipal y para apoyar este esfuerzo es que desarrollamos la plataforma de Radar Vial.'),

                                                        html.Br(),

                                                        html.P('La plataforma de uso abierto visualiza los datos de hechos viales del 2015 a la fecha, proporcionados por la Secretaría de Seguridad Pública y procesados bimensualmente por el IMPLANG.'), 
                                                        
                                                        html.Br(), 
                                                        
                                                        html.P('La información que se presenta en esta plataforma es para uso solamente informativo. Aun y cuando buscamos publicar siempre la información mas precisa, existe la posiblilidad de error o de información incompleta.'),

                                                        html.Br(),

                                                        html.P('Última actualización: octubre 2021')

                                                    ],style={'font-size':'100%'}),

                                                    ],
                                                    id="modal_inforadar",
                                                    centered=True,
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),  

                                                ]),

                                            ], style = {'margin-bottom': '0px'}),
                                            
                                        ], style={'background-color':'#E2E2E2 51%'})
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

                                                        html.P('3,920', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
                                                        html.P('hechos viales en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px', 'padding-bottom': '0px'}),

                                                    ],style={'float':'right'},),

                                                    html.Img(src='data:image/png;base64,{}'.format(hv_img), 
                                                        style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
                                                        className="pl-3 pt-2 img-fluid"), 

                                                ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),

                                            ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),
                                            
                                            html.P('9% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px', 'padding-top': '0px'}),                    

                                        ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
                                    ], style = {'margin-bottom': '15px'})

                                ], lg = 3, md = 12, sm = 12),

                                dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            dbc.Row([

                                                dbc.Col([

                                                    html.Div([

                                                        html.P('55', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
                                                        html.P('lesionados en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px'}),

                                                    ],style={'float':'right'},),
                                                    html.Img(src='data:image/png;base64,{}'.format(lesionado_img), 
                                                        style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
                                                        className="pl-3 pt-2 img-fluid"), 

                                                ]),

                                            ]),
                                            
                                            html.P('9% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px'}),                    

                                        ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
                                    ], style = {'margin-bottom': '15px'})

                                ], lg = 3, md = 12, sm = 12),

                                dbc.Col([
                                    dbc.Card([

                                        dbc.CardBody([

                                            dbc.Row([

                                                dbc.Col([

                                                    html.Div([

                                                        html.P('5', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
                                                        html.P('fallecidos en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px', 'padding-bottom': '0px'}),

                                                    ],style={'float':'right'},),
                                                    
                                                    html.Img(src='data:image/png;base64,{}'.format(fallecido_img), 
                                                        style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
                                                        className="pl-3 pt-2 img-fluid"), 

                                                ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),

                                            ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),
                                            
                                            html.P('38% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px', 'padding-top': '0px'}),                    

                                        ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
                                    ], style = {'margin-bottom': '15px'})

                                ], lg = 3, md = 12, sm = 12),
                            
                            ], className='mx-0'),

                            # BOTON MAPA
                            dbc.Row([

                                dbc.Col([

                                    dbc.Card([

                                        dbc.Button(
                                            [html.Img(src='data:image/png;base64,{}'.format(mapa_foto_img), className='img-fluid')], 
                                            id="boton_mapa", 
                                            n_clicks=0, 
                                            style={'border-color':'black'}
                                        ),

                                        # dbc.CardImg(
                                        #     src='assets/mapa_foto.png', 
                                        #     top = True, 
                                        #     class_name = 'img-fluid'
                                        # ),

                                        #dbc.CardImgOverlay(

                                            dbc.CardBody(
                                                  [
                                                      html.P('Ver Datos en Mapa Interactivo', className = 'd-flex justify-content-center align-content-center', style = {'padding-top': '30px', 'font-size': '40px'})
                                                  ],
                                                  className = 'd-flex justify-content-center align-content-center'
                                              )
                                          #)
                                    ], style = {'height': '335px'}, className = 'd-flex justify-content-center align-content-center')

                                ]),

                            ], className='mx-0'),

                            html.Br(),

                            # Hechos viales totales // Top Ubicaciones
                            dbc.Row([
                        
                                # Hechos viales
                                dbc.Col([

                                    dbc.Card([
                                        
                                        dbc.CardBody([

                                            html.Div([
                                                html.P(['Hechos Viales por Año'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                            ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

                                            html.Div([

                                                html.Span(
                                                    dbc.Button(
                                                        [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                                                style = {'width': '15px', 'height': '15px'})], 
                                                        id="open1_tothv", 
                                                        n_clicks=0, 
                                                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                                        class_name = 'expand-button'
                                                    ),
                                                    id="tooltip-target-tothv",
                                                    style={"textDecoration": "underline", "cursor": "pointer"}
                                                ),

                                                dbc.Tooltip(
                                                    "Ampliar vista",
                                                    target="tooltip-target-tothv",
                                                    placement = 'top'
                                                ),
                                                    
                                                dbc.Modal([

                                                    dbc.ModalHeader([html.B("Hechos Viales")]),

                                                    dbc.ModalBody([
                                                        dcc.Graph(
                                                                id = 'tot_hv_modal',
                                                                figure = tot_hv_modal,
                                                                config={
                                                                        'modeBarButtonsToRemove':
                                                                        ['lasso2d', 'pan2d','zoom2d',
                                                                        'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                                                        'resetScale2d', 'hoverClosestCartesian',
                                                                        'hoverCompareCartesian', 'toggleSpikelines',
                                                                        'select2d', 'toImage'],
                                                                        'displaylogo': False
                                                                    }
                                                                )

                                                    ],style={"textAlign":"justify",'font-size':'100%'}),

                                                    ],
                                                    id="modal_tothv",
                                                    centered=True,
                                                    size="xl",
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),
                                            ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

                                            html.Hr(style = {'margin-top': '0px'}),

                                            dcc.Graph(
                                                id = 'tot_hv',
                                                figure = tot_hv,
                                                config = {
                                                    'displayModeBar': False,
                                                    'displaylogo': False
                                                }
                                            ),

                                        ]),

                                    ], style = {'margin-bottom': '20px'})

                                ], lg=6, md=6, sm = 12),

                                # Top Ubicaciones
                                dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            html.Div([
                                                html.P(['Ubicaciones con más Hechos Viales'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                            ], style={'width':'95%','display':'inline-block'}),

                                            html.Div([

                                                html.Span(
                                                    dbc.Button(
                                                        [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                                                style = {'width': '15px', 'height': '15px'})], 
                                                        id="open1_topcalles", 
                                                        n_clicks=0, 
                                                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                                        class_name = 'expand-button'

                                                        ),

                                                    id="tooltip-target-topcalles",
                                                    style={"textDecoration": "underline", "cursor": "pointer"},
                                                ),

                                                dbc.Tooltip(
                                                    "Ampliar vista",
                                                    target="tooltip-target-topcalles",
                                                    placement = 'top'
                                                ),
                                                    
                                                dbc.Modal([

                                                    dbc.ModalHeader(html.B("Top Calles")),

                                                    dbc.ModalBody([

                                                        dcc.Graph(
                                                            id = 'top_c',
                                                            figure = top_c_modal,
                                                            config={
                                                                'modeBarButtonsToRemove':
                                                                ['lasso2d', 'pan2d','zoom2d',
                                                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                                                'resetScale2d', 'hoverClosestCartesian',
                                                                'hoverCompareCartesian', 'toggleSpikelines',
                                                                'select2d',],
                                                                'displaylogo': False
                                                            },
                                                        )
                                                    ],style={"textAlign":"justify",'font-size':'100%'}),
                                                    
                                                    ],
                                                    id="modal_topcalles",
                                                    centered=True,
                                                    size="xl",
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),
                                            ], style={'width':'4%', 'float': 'right'}, className = 'pr-3 d-none d-lg-block'),

                                            html.Hr(style = {'margin-top': '0px'}),

                                            dbc.RadioItems(
                                                id = 'checklist_top',
                                                class_name = 'radio-group btn-group d-flex justify-content-center',
                                                label_class_name = 'btn btn-secondary',
                                                label_checked_class_name = 'active',
                                                value = 'top_c',
                                                options = [
                                                    {'label': 'Calles', 'value': 'top_c'},
                                                    {'label': 'Intersecciones', 'value': 'top_i'}
                                                ]
                                            ),

                                            dcc.Graph(
                                                id = 'top_ubi',
                                                figure = {},
                                                config = {
                                                    'displayModeBar': False,
                                                    'displaylogo': False
                                                }
                                            )
                                        ]),
                                    ], style = {'margin-bottom': '20px'})
                                ], lg=6, md=6,),

                            ], style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '10px'}),
                            
                            # Por Usuario // Personas
                            dbc.Row([

                                # Lesionados y Fallecidos
                                dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            html.Div([
                                                html.P(['Lesiones y Muertes por Tipo de Hecho Vial'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                            ], style={'width':'95%','display':'inline-block'}),

                                            html.Div([

                                                html.Span(
                                                    dbc.Button(
                                                        [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                                                style = {'width': '15px', 'height': '15px'})], 
                                                        id="open1_lesionfall", 
                                                        n_clicks=0, 
                                                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                                        class_name = 'expand-button'

                                                        ),

                                                    id="tooltip-target-lesionfall",
                                                    style={"textDecoration": "underline", "cursor": "pointer"},
                                                ),

                                                dbc.Tooltip(
                                                    "Ampliar vista",
                                                    target="tooltip-target-lesionfall",
                                                    placement = 'top'
                                                ),
                                                    
                                                dbc.Modal([

                                                    dbc.ModalHeader(html.B("Lesionados y fallecidos")),

                                                    dbc.ModalBody([

                                                        dcc.Graph(
                                                            id = 'lf_tipo_hv_modal',
                                                            figure = lf_tipo_hv_modal,
                                                            config={
                                                                'modeBarButtonsToRemove':
                                                                ['lasso2d', 'pan2d','zoom2d',
                                                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                                                'resetScale2d', 'hoverClosestCartesian',
                                                                'hoverCompareCartesian', 'toggleSpikelines',
                                                                'select2d',],
                                                                'displaylogo': False
                                                            },
                                                        )
                                                    ],style={"textAlign":"justify",'font-size':'100%'}),
                                                    
                                                    ],
                                                    id="modal_lesionfall",
                                                    centered=True,
                                                    size="xl",
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),
                                            ], style={'width':'4%', 'float': 'right', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

                                            html.Hr(style = {'margin-top': '0px'}),

                                            dcc.Graph(
                                                id = 'lf_tipo_hv',
                                                figure = lf_tipo_hv,
                                                config = {
                                                    'displayModeBar': False,
                                                    'displaylogo': False
                                                }
                                            )
                                        ]),
                                    ], style = {'margin-bottom': '20px'})
                                ], lg=6, md=6),

                                # Personas
                                dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            html.Div([
                                                html.P(['Personas Lesionadas y Fallecidas'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                            ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

                                            html.Div([

                                                html.Span(
                                                    dbc.Button(
                                                        [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                                                style = {'width': '15px', 'height': '15px'})], 
                                                        id="open1_personas", 
                                                        n_clicks=0, 
                                                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                                        class_name = 'expand-button'
                                                        ),

                                                    id="tooltip-target-personas",
                                                    style={"textDecoration": "underline", "cursor": "pointer"},
                                                ),

                                                dbc.Tooltip(
                                                    "Ampliar vista",
                                                    target="tooltip-target-personas",
                                                    placement = 'top'
                                                ),
                                                    
                                                dbc.Modal([

                                                    dbc.ModalHeader(html.B("Personas")),

                                                    dbc.ModalBody([

                                                        dcc.Graph(
                                                            id = 'per_grav_modal',
                                                            figure = per_grav_modal,
                                                            config={
                                                                'modeBarButtonsToRemove':
                                                                ['lasso2d', 'pan2d','zoom2d',
                                                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                                                'resetScale2d', 'hoverClosestCartesian',
                                                                'hoverCompareCartesian', 'toggleSpikelines',
                                                                'select2d',],
                                                                'displaylogo': False
                                                            },
                                                        )
                                                    ],style={"textAlign":"justify",'font-size':'100%'}),

                                                    ],
                                                    id="modal_personas",
                                                    centered=True,
                                                    size="xl",
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),
                                            ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

                                            html.Hr(style = {'margin-top': '0px'}),

                                            dcc.Graph(
                                                id = 'per_grav',
                                                figure = per_grav,
                                                config = {
                                                    'displayModeBar': False,
                                                    'displaylogo': False
                                                }
                                            )
                                        ]),
                                    ], style = {'margin-bottom': '20px'})

                                ], lg=6, md=6),

                            ], style = {'padding-left': '15px', 'padding-right': '15px'}),

                            # Día de la semana y hora
                            dbc.Row([

                                # Día de la semana y hora
                                dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            html.Div([
                                                html.P(['Tiempo del Día con Más Hechos Viales'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                            ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

                                            html.Div([

                                                html.Span(
                                                    dbc.Button(
                                                        [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                                                style = {'width': '15px', 'height': '15px'})], 
                                                        id="open1_semhora", 
                                                        n_clicks=0, 
                                                        style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                                                'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                                        class_name = 'expand-button'

                                                        ),

                                                    id="tooltip-target-semhora",
                                                    style={"textDecoration": "underline", "cursor": "pointer"},
                                                ),

                                                dbc.Tooltip(
                                                    "Ampliar vista",
                                                    target="tooltip-target-semhora",
                                                    placement = 'top'
                                                ),
                                                    
                                                dbc.Modal([

                                                    dbc.ModalHeader(html.B("Por día de la semana y hora")),

                                                    dbc.ModalBody([

                                                        dcc.Graph(
                                                            id = 'heatmap_modal',
                                                            figure = heatmap_modal,
                                                            config={
                                                                'modeBarButtonsToRemove':
                                                                ['lasso2d', 'pan2d','zoom2d',
                                                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                                                'resetScale2d', 'hoverClosestCartesian',
                                                                'hoverCompareCartesian', 'toggleSpikelines',
                                                                'select2d',],
                                                                'displaylogo': False
                                                            },
                                                        )
                                                    ],style={"textAlign":"justify",'font-size':'100%'}),
                                                    
                                                    ],
                                                    id="modal_semhora",
                                                    centered=True,
                                                    size="xl",
                                                    is_open=False,
                                                    style={'font-family':'Arial'}
                                                ),
                                            ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

                                            html.Hr(style = {'margin-top': '0px'}),

                                            dcc.Graph(
                                                id = 'heatmap',
                                                figure = heatmap,
                                                config = {
                                                    'displayModeBar': False,
                                                    'displaylogo': False
                                                }
                                            )
                                        ]),
                                    ], style = {'margin-bottom': '20px'})
                                ], lg=6, md=6),

                                # Top intersecciones
                                # dbc.Col([

                                #     dbc.Card([
                                        
                                #         dbc.CardBody([

                                #             html.Div([
                                #                 html.P(['Top Intersecciones'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
                                #             ], style={'width':'95%','display':'inline-block'}),

                                #             html.Div([

                                #                 html.Span(
                                #                     dbc.Button(
                                #                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
                                #                                 style = {'width': '15px', 'height': '15px'})], 
                                #                         id="open1_topint", 
                                #                         n_clicks=0, 
                                #                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
                                #                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
                                #                         class_name = 'expand-button'
                                #                         ),

                                #                     id="tooltip-target-topint",
                                #                     style={"textDecoration": "underline", "cursor": "pointer"},
                                #                 ),

                                #                 dbc.Tooltip(
                                #                     "Ampliar vista",
                                #                     target="tooltip-target-topint",
                                #                     placement = 'top'
                                #                 ),
                                                    
                                #                 dbc.Modal([

                                #                     dbc.ModalHeader(html.B("Top Intersecciones")),

                                #                     dbc.ModalBody([

                                #                         dcc.Graph(
                                #                             id = 'top_i',
                                #                             figure = top_i_modal,
                                #                             config={
                                #                                 'modeBarButtonsToRemove':
                                #                                 ['lasso2d', 'pan2d','zoom2d',
                                #                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                #                                 'resetScale2d', 'hoverClosestCartesian',
                                #                                 'hoverCompareCartesian', 'toggleSpikelines',
                                #                                 'select2d',],
                                #                                 'displaylogo': False
                                #                             },
                                #                         )
                                #                     ],style={"textAlign":"justify",'font-size':'100%'}),
                                                    
                                #                     ],
                                #                     id="modal_topint",
                                #                     centered=True,
                                #                     size="xl",
                                #                     is_open=False,
                                #                     style={'font-family':'Arial'}
                                #                 ),
                                #             ], style={'width':'4%', 'float': 'right', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

                                #             html.Hr(style = {'margin-top': '0px'}),

                                #             dcc.Graph(
                                #                 id = 'top_i',
                                #                 figure = top_i,
                                #                 config = {
                                #                     'displayModeBar': False,
                                #                     'displaylogo': False
                                #                 }
                                #             )
                                #         ]),
                                #     ], style = {'margin-bottom': '20px'})
                                # ], lg=6, md=6),
                            ], style = {'padding-left': '15px', 'padding-right': '15px'}),

                            # PÁRRAFO DIAGNÓSTICO
                            dbc.Row([

                              dbc.Col([

                                    dbc.Card([

                                        dbc.CardBody([

                                            dbc.Row([

                                                dbc.Col([

                                                    html.P(['Conoce más sobre el estado de seguridad vial en el municipio descargando el ',

                                                        html.A(['Diagnóstico de Seguridad Vial 2020'], href = 'https://drive.google.com/file/d/1oeDpZptdogbqVefihVNnYG3cp6tiNAiL/view?usp=sharing', target = 'blank', style = {'text-decoration': 'None', 'color': '#279FD7', 'font-weight': 'bold'}),

                                                        # dbc.Button(
                                                        #     [html.B('Diagnóstico de Seguridad Vial 2021')], 
                                                        #     id="open1_diagnostico", 
                                                        #     n_clicks=0, 
                                                        #     style={'display':'inline-block', 'background-color':'transparent',
                                                        #         'border-color':'transparent', 'padding': '0px', 'margin': '0px', 'color': '#279FD7', 'font-size': '14px'}
                                                        # ),
                                                        
                                                        '.',

                                                    ], style = {'font-size': '14px', 'margin-bottom': '0px'})  

                                                ]),

                                            ], style = {'margin-bottom': '0px'}),
                                            
                                        ], style={'background-color':'#E2E2E2'})
                                    ])

                                ]),

                            ], className='mx-0'),

                            html.Br(),

                            # FOOTER
                            dbc.Row([

                                dbc.Col([

                                    dbc.Row([

                                        dbc.Col([

                                            html.Img(src='assets/logo_spgg.png', style={'float':'left', 'margin-top': '25px', 'margin-left': '20px'}),
                                            html.Img(src='assets/implang_logo.png', style={'float':'right', 'margin-top': '27px', 'margin-right': '20px'}),

                                        ], style={'padding-left': '15px'}),#, className='d-lg-flex justify-content-between my-3'),

                                    ]),

                                    dbc.Row([

                                        dbc.Col([

                                            html.A(
                                                [
                                                    html.Img(
                                                        src='data:image/png;base64,{}'.format(insta_img),
                                                        className="p-0 img-fluid"
                                                    )
                                                ],
                                                href = 'https://www.instagram.com/implang_spgg/',
                                                target = 'blank',
                                                style={
                                                    'margin-left': '45px'
                                                }
                                            ),

                                            html.A(
                                                [
                                                    html.Img(
                                                        src='data:image/png;base64,{}'.format(twitter_img),
                                                        className="p-0 img-fluid"
                                                    )
                                                ],
                                                href = 'https://twitter.com/implang_spgg',
                                                target = 'blank',
                                                style={
                                                    'margin-right': '40px',
                                                    'margin-left': '35px'
                                                }
                                            ),

                                            # dbc.Button(
                                            #     html.Img(src='data:image/png;base64,{}'.format(insta_img), 
                                            #             style={'float':'right'},
                                            #             className="p-0 img-fluid"), 
                                            #     id="instagram", 
                                            #     n_clicks=0, 
                                            #     style={'display':'inline-block',
                                            #             'float':'left','padding':'0', 'background-color':'transparent',
                                            #             'border-color':'transparent', 'margin-left': '45px'},
                                            #     class_name='rounded-circle ml-4 pb-1'

                                            # ),

                                            # dbc.Button(
                                            #     html.Img(src='data:image/png;base64,{}'.format(twitter_img), 
                                            #             style={'float':'right'},
                                            #             className="p-0 img-fluid"), 
                                            #     id="twitter", 
                                            #     n_clicks=0, 
                                            #     style={'display':'inline-block',
                                            #             'float':'left','padding':'0', 'background-color':'transparent',
                                            #             'border-color':'transparent', 'margin-right': '40px', 'margin-left': '35px'},
                                            #     class_name='rounded-circle ml-4 pb-1'

                                            # ),

                                            html.B("Comentarios sobre Radar Vial", style = {'font-size': '12px'}),
                                            html.Br(),
                                            html.P("movilidad@sanpedro.gob.mx", style = {'margin-left': '155px', 'font-size': '12px'})

                                        ])

                                    ], style = {'padding-top': '25px'}),

                                ])

                            ], style={'background-color': '#000', 'color':'white'})

                        ], style={'background-color': '#fafafa'}, id='resumensito', className = ''),

                        # MAPA

                        html.Div([

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
                                                                max_date_allowed = dt(2021, 10, 31),
                                                                start_date = dt(2015, 1, 1),
                                                                end_date = dt(2021, 10, 31),
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
                                        html.Img(src = 'data:image/png;base64,{}'.format(encoded_img5),
                                        className = 'img-fluid',
                                        style = {'width': '75%', 'height': '75%'}),
                                        #'Filtros',
                                        color = 'light',
                                        class_name = 'filtros_small',
                                        id = 'collapse-filtros-movil',
                                        n_clicks = 0
                                    ),

                                    dbc.Button(
                                        html.Img(src = 'data:image/png;base64,{}'.format(encoded_img6),
                                        className = 'img-fluid',
                                        style = {'width': '75%', 'height': '75%'}),
                                        #'Indicadores',
                                        color = 'light',
                                        class_name = 'indicadores_small',
                                        id = 'collapse-indicadores-movil',
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
                                                        max_date_allowed = dt(2021, 10, 31),
                                                        start_date = dt(2015, 1, 1),
                                                        end_date = dt(2021, 10, 31),
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
                            ], class_name = 'd-lg-none'),

                            dbc.Row([

                                dbc.Col([

                                    dbc.Offcanvas([

                                        # INDICADOR HECHOS VIALES
                                        dbc.Card([

                                            dbc.CardBody([

                                                html.Div([

                                                    html.P([
                                                        'Hechos Viales Totales'
                                                    ], 
                                                    style = {
                                                        'font-size': '18px', 
                                                        'font-weight': 'bold',
                                                        'margin-bottom': '5px'
                                                        }
                                                    )
                                                ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

                                                html.Table([

                                                        html.Tr([
                                                            #html.Th('Hechos Viales ', style={'font-weight':'normal', 'border': '0px'}),
                                                            html.Th(id = 'hv_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
                                                        ], style = {'border': '0px'}),

                                                ], style = {'border': '0px'}, className = 'd-flex justify-content-center')                            
                                            
                                            ], style = {'padding': '0px', 'margin': '10px'})

                                        ], style = {'margin-top': '15px', 'margin-left': '20px', 'margin-right': '20px'}),

                                        html.Br(),

                                        # INDICADOR LESIONADOS
                                        dbc.Card([

                                            dbc.CardBody([

                                                html.Div([

                                                    html.P([
                                                        'Lesionados'
                                                    ], 
                                                    style = {
                                                        'font-size': '18px', 
                                                        'font-weight': 'bold',
                                                        'margin-bottom': '5px'
                                                        }
                                                    )
                                                ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

                                                html.Table([

                                                        html.Tr([
                                                            #html.Th('Lesionados: ', style={'font-weight':'normal', 'border': '0px'}),
                                                            html.Th(id = 'hv_les_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
                                                        ], style = {'border': '0px'}),

                                                ], style = {'border': '0px'}, className = 'd-flex justify-content-center')

                                            ], style = {'padding': '0px', 'margin': '10px'})
                                            
                                        ], style = {'margin-top': '0px', 'margin-left': '20px', 'margin-right': '20px'}),

                                        html.Br(),

                                        # INDICADOR FALLECIDOS
                                        dbc.Card([

                                            dbc.CardBody([

                                                html.Div([

                                                    html.P([
                                                        'Fallecidos'
                                                    ], 
                                                    style = {
                                                        'font-size': '18px', 
                                                        'font-weight': 'bold',
                                                        'margin-bottom': '5px'
                                                        }
                                                    )
                                                ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

                                                html.Table([

                                                        html.Tr([
                                                            #html.Th('Fallecidos: ', style={'font-weight':'normal', 'border': '0px'}),
                                                            html.Th(id = 'hv_fall_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
                                                        ], style = {'border': '0px'}),

                                                ], style = {'border': '0px'}, className = 'd-flex justify-content-center')

                                            ], style = {'padding': '0px', 'margin': '10px'})

                                        ], style = {'margin-bottom': '10px', 'margin-left': '20px', 'margin-right': '20px'}),

                                        dbc.Card([

                                            dbc.CardBody([

                                                dcc.Store(id='mapa_data_top_movil'),

                                                dcc.Graph(
                                                    id = 'tabla_mapa_top_movil',
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
                                                )

                                            ], style = {'padding': '0px', 'margin': '10px', 'white-space': 'nowrap', 'overflow-x': 'auto'},
                                            class_name = 'd-flex flex-nowrap')

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
                                    id = 'indicadores-movil', is_open = False)

                                ], class_name = 'd-lg-none')

                            ], class_name = 'd-lg-none')

                        ], className = '', id='mapicha', style = {'padding': '0px', 'margin': '0px'})



                    
                    ], style = {'margin': '0px', 'padding': '0px'}, class_name = 'h-100')

                ], style={'border':'none'}, color = '#F8F9FB'), lg=12, class_name='p-0'

            ), justify = 'center', class_name='m-0'

        ),

], style={'font-family':'Arial'})

# LAYOUT RESUMEN

# def resumen():

#   return html.Div([

#             html.Br(),

#             # PÁRRAFO RESUMEN
#             dbc.Row([

#               dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             dbc.Row([

#                                 dbc.Col([

#                                     html.P(['Radar Vial es la plataforma de hechos viales del municipio de San Pedro que utilizamos con el objetivo de reducir el número de fallecimientos y lesiones graves ocasionados por hechos de tránsito a cero.',

#                                         html.Br(),

#                                         html.Br(),

#                                         'Conoce más sobre la plataforma dando ',

#                                         dbc.Button(
#                                             [html.B('click aquí')], 
#                                             id="open1_inforadar", 
#                                             n_clicks=0, 
#                                             style={'display':'inline-block', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'padding': '0px', 'margin': '0px', 'color': '#279FD7', 'font-size': '14px'}
#                                         ),

#                                     ], style = {'font-size': '14px', 'margin-bottom': '0px', 'margin-left': '0px', 'margin-right': '0px'}),

#                                     dbc.Modal([

#                                     dbc.ModalHeader([html.P("Radar Vial", style = {'font-size': '18px', 'font-weight': 'bold', 'margin-bottom': '0px'})]),

#                                     dbc.ModalBody([
                                        
#                                         html.P(
#                                             'Cada año en promedio fallecen 8 y resultan con lesiones graves 159 personas en el municipio. En San Pedro Garza García reconocemos que las lesiones graves y fallecimientos ocasionados por hechos de tránsito no son “accidentes” y por lo tanto pueden ser evitadas a traves de educación, adecuaciones viales y aplicación de la ley.' 
#                                         ),

#                                         html.Br(),

#                                         html.P('Nuestro objetivo es alcanzar la meta de 0 fallecimientos y 0 lesiones graves a nivel municipal y para apoyar este esfuerzo es que desarrollamos la plataforma de Radar Vial.'),

#                                         html.Br(),

#                                         html.P('La plataforma de uso abierto visualiza los datos de hechos viales del 2015 a la fecha, proporcionados por la Secretaría de Seguridad Pública y procesados bimensualmente por el IMPLANG.'), 
                                        
#                                         html.Br(), 
                                        
#                                         html.P('La información que se presenta en esta plataforma es para uso solamente informativo. Aun y cuando buscamos publicar siempre la información mas precisa, existe la posiblilidad de error o de información incompleta.'),

#                                         html.Br(),

#                                         html.P('Última actualización: octubre 2021')

#                                     ],style={'font-size':'100%'}),

#                                     ],
#                                     id="modal_inforadar",
#                                     centered=True,
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),  

#                                 ]),

#                             ], style = {'margin-bottom': '0px'}),
                            
#                         ], style={'background-color':'#E2E2E2'})
#                     ])

#                 ]),

#             ], className='mx-0'),

#             html.Br(),

#             # Tarjetas Indicadores
#             dbc.Row([

#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             dbc.Row([

#                                 dbc.Col([

#                                     html.Div([

#                                         html.P('3,920', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
#                                         html.P('hechos viales en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px', 'padding-bottom': '0px'}),

#                                     ],style={'float':'right'},),

#                                     html.Img(src='data:image/png;base64,{}'.format(hv_img), 
#                                         style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
#                                         className="pl-3 pt-2 img-fluid"), 

#                                 ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),
                            
#                             html.P('9% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px', 'padding-top': '0px'}),                    

#                         ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
#                     ], style = {'margin-bottom': '15px'})

#                 ], lg = 3, md = 12, sm = 12),

#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             dbc.Row([

#                                 dbc.Col([

#                                     html.Div([

#                                         html.P('55', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
#                                         html.P('lesionados en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px'}),

#                                     ],style={'float':'right'},),
#                                     html.Img(src='data:image/png;base64,{}'.format(lesionado_img), 
#                                         style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
#                                         className="pl-3 pt-2 img-fluid"), 

#                                 ]),

#                             ]),
                            
#                             html.P('9% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px'}),                    

#                         ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
#                     ], style = {'margin-bottom': '15px'})

#                 ], lg = 3, md = 12, sm = 12),

#                 dbc.Col([
#                     dbc.Card([

#                         dbc.CardBody([

#                             dbc.Row([

#                                 dbc.Col([

#                                     html.Div([

#                                         html.P('5', style = {'font-weight': 'bold', 'font-size': '44px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'padding-right': '25px'}, className = 'd-flex justify-content-end'),
#                                         html.P('fallecidos en el 2021', style = {'margin-top': '0px', 'margin-bottom': '0px', 'padding-top': '0px', 'padding-right': '25px', 'padding-bottom': '0px'}),

#                                     ],style={'float':'right'},),
                                    
#                                     html.Img(src='data:image/png;base64,{}'.format(fallecido_img), 
#                                         style={'float':'left', 'padding-left': '25px', 'margin-bottom': '0px', 'padding-bottom': '0px', 'margin-top': '5px'},
#                                         className="pl-3 pt-2 img-fluid"), 

#                                 ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'}),
                            
#                             html.P('38% (2020)', style = {'float': 'right', 'margin-top': '0px', 'font-size': '12px', 'padding-right': '25px', 'padding-top': '0px'}),                    

#                         ], style = {'margin-bottom': '0px', 'padding-bottom': '0px'})
#                     ], style = {'margin-bottom': '15px'})

#                 ], lg = 3, md = 12, sm = 12),
            
#             ], className='mx-0'),

#             # BOTON MAPA
#             dbc.Row([

#                 dbc.Col([

#                     dbc.Card([

#                         # dbc.CardImg(
#                         #     src='assets/mapa_foto.png', 
#                         #     top = True, 
#                         #     class_name = 'img-fluid'
#                         # ),

#                         #dbc.CardImgOverlay(

#                             dbc.CardBody(
#                                   [
#                                       html.P('Ver Datos en Mapa Interactivo', className = 'd-flex justify-content-center align-content-center', style = {'padding-top': '30px', 'font-size': '40px'})
#                                   ],
#                                   className = 'd-flex justify-content-center align-content-center'
#                               )
#                           #)
#                     ], style = {'height': '335px'}, className = 'd-flex justify-content-center align-content-center')

#                 ]),

#             ], className='mx-0'),

#             html.Br(),

#             # Hechos viales totales // Top Ubicaciones
#             dbc.Row([
        
#                 # Hechos viales
#                 dbc.Col([

#                     dbc.Card([
                        
#                         dbc.CardBody([

#                             html.Div([
#                                 html.P(['Hechos Viales por Año'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                             ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

#                             html.Div([

#                                 html.Span(
#                                     dbc.Button(
#                                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                                                 style = {'width': '15px', 'height': '15px'})], 
#                                         id="open1_tothv", 
#                                         n_clicks=0, 
#                                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                                         class_name = 'expand-button'
#                                     ),
#                                     id="tooltip-target-tothv",
#                                     style={"textDecoration": "underline", "cursor": "pointer"}
#                                 ),

#                                 dbc.Tooltip(
#                                     "Ampliar vista",
#                                     target="tooltip-target-tothv",
#                                     placement = 'top'
#                                 ),
                                    
#                                 dbc.Modal([

#                                     dbc.ModalHeader([html.B("Hechos Viales")]),

#                                     dbc.ModalBody([
#                                         dcc.Graph(
#                                                 id = 'tot_hv',
#                                                 figure = tot_hv_modal,
#                                                 config={
#                                                         'modeBarButtonsToRemove':
#                                                         ['lasso2d', 'pan2d','zoom2d',
#                                                         'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                                         'resetScale2d', 'hoverClosestCartesian',
#                                                         'hoverCompareCartesian', 'toggleSpikelines',
#                                                         'select2d', 'toImage'],
#                                                         'displaylogo': False
#                                                     }
#                                                 )

#                                     ],style={"textAlign":"justify",'font-size':'100%'}),

#                                     ],
#                                     id="modal_tothv",
#                                     centered=True,
#                                     size="xl",
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),
#                             ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             dcc.Graph(
#                                 id = 'tot_hv',
#                                 figure = tot_hv,
#                                 config = {
#                                     'displayModeBar': False,
#                                     'displaylogo': False
#                                 }
#                             ),

#                         ]),

#                     ], style = {'margin-bottom': '20px'})

#                 ], lg=6, md=6, sm = 12),

#                 # Top Ubicaciones
#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([
#                                 html.P(['Ubicaciones con más Hechos Viales'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                             ], style={'width':'95%','display':'inline-block'}),

#                             html.Div([

#                                 html.Span(
#                                     dbc.Button(
#                                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                                                 style = {'width': '15px', 'height': '15px'})], 
#                                         id="open1_topcalles", 
#                                         n_clicks=0, 
#                                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                                         class_name = 'expand-button'

#                                         ),

#                                     id="tooltip-target-topcalles",
#                                     style={"textDecoration": "underline", "cursor": "pointer"},
#                                 ),

#                                 dbc.Tooltip(
#                                     "Ampliar vista",
#                                     target="tooltip-target-topcalles",
#                                     placement = 'top'
#                                 ),
                                    
#                                 dbc.Modal([

#                                     dbc.ModalHeader(html.B("Top Calles")),

#                                     dbc.ModalBody([

#                                         dcc.Graph(
#                                             id = 'top_c',
#                                             figure = top_c_modal,
#                                             config={
#                                                 'modeBarButtonsToRemove':
#                                                 ['lasso2d', 'pan2d','zoom2d',
#                                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                                 'resetScale2d', 'hoverClosestCartesian',
#                                                 'hoverCompareCartesian', 'toggleSpikelines',
#                                                 'select2d',],
#                                                 'displaylogo': False
#                                             },
#                                         )
#                                     ],style={"textAlign":"justify",'font-size':'100%'}),
                                    
#                                     ],
#                                     id="modal_topcalles",
#                                     centered=True,
#                                     size="xl",
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),
#                             ], style={'width':'4%', 'float': 'right'}, className = 'pr-3 d-none d-lg-block'),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             dbc.RadioItems(
#                                 id = 'checklist_top',
#                                 class_name = 'radio-group btn-group d-flex justify-content-center',
#                                 label_class_name = 'btn btn-secondary',
#                                 label_checked_class_name = 'active',
#                                 value = 'top_c',
#                                 options = [
#                                     {'label': 'Calles', 'value': 'top_c'},
#                                     {'label': 'Intersecciones', 'value': 'top_i'}
#                                 ]
#                             ),

#                             dcc.Graph(
#                                 id = 'top_ubi',
#                                 figure = {},
#                                 config = {
#                                     'displayModeBar': False,
#                                     'displaylogo': False
#                                 }
#                             )
#                         ]),
#                     ], style = {'margin-bottom': '20px'})
#                 ], lg=6, md=6,),

#             ], style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '10px'}),
            
#             # Por Usuario // Personas
#             dbc.Row([

#                 # Lesionados y Fallecidos
#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([
#                                 html.P(['Lesiones y Muertes por Tipo de Hecho Vial'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                             ], style={'width':'95%','display':'inline-block'}),

#                             html.Div([

#                                 html.Span(
#                                     dbc.Button(
#                                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                                                 style = {'width': '15px', 'height': '15px'})], 
#                                         id="open1_lesionfall", 
#                                         n_clicks=0, 
#                                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                                         class_name = 'expand-button'

#                                         ),

#                                     id="tooltip-target-lesionfall",
#                                     style={"textDecoration": "underline", "cursor": "pointer"},
#                                 ),

#                                 dbc.Tooltip(
#                                     "Ampliar vista",
#                                     target="tooltip-target-lesionfall",
#                                     placement = 'top'
#                                 ),
                                    
#                                 dbc.Modal([

#                                     dbc.ModalHeader(html.B("Lesionados y fallecidos")),

#                                     dbc.ModalBody([

#                                         dcc.Graph(
#                                             id = 'lf_tipo_hv',
#                                             figure = lf_tipo_hv_modal,
#                                             config={
#                                                 'modeBarButtonsToRemove':
#                                                 ['lasso2d', 'pan2d','zoom2d',
#                                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                                 'resetScale2d', 'hoverClosestCartesian',
#                                                 'hoverCompareCartesian', 'toggleSpikelines',
#                                                 'select2d',],
#                                                 'displaylogo': False
#                                             },
#                                         )
#                                     ],style={"textAlign":"justify",'font-size':'100%'}),
                                    
#                                     ],
#                                     id="modal_lesionfall",
#                                     centered=True,
#                                     size="xl",
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),
#                             ], style={'width':'4%', 'float': 'right', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             dcc.Graph(
#                                 id = 'lf_tipo_hv',
#                                 figure = lf_tipo_hv,
#                                 config = {
#                                     'displayModeBar': False,
#                                     'displaylogo': False
#                                 }
#                             )
#                         ]),
#                     ], style = {'margin-bottom': '20px'})
#                 ], lg=6, md=6),

#                 # Personas
#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([
#                                 html.P(['Personas Lesionadas y Fallecidas'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                             ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

#                             html.Div([

#                                 html.Span(
#                                     dbc.Button(
#                                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                                                 style = {'width': '15px', 'height': '15px'})], 
#                                         id="open1_personas", 
#                                         n_clicks=0, 
#                                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                                         class_name = 'expand-button'
#                                         ),

#                                     id="tooltip-target-personas",
#                                     style={"textDecoration": "underline", "cursor": "pointer"},
#                                 ),

#                                 dbc.Tooltip(
#                                     "Ampliar vista",
#                                     target="tooltip-target-personas",
#                                     placement = 'top'
#                                 ),
                                    
#                                 dbc.Modal([

#                                     dbc.ModalHeader(html.B("Personas")),

#                                     dbc.ModalBody([

#                                         dcc.Graph(
#                                             id = 'per_grav',
#                                             figure = per_grav_modal,
#                                             config={
#                                                 'modeBarButtonsToRemove':
#                                                 ['lasso2d', 'pan2d','zoom2d',
#                                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                                 'resetScale2d', 'hoverClosestCartesian',
#                                                 'hoverCompareCartesian', 'toggleSpikelines',
#                                                 'select2d',],
#                                                 'displaylogo': False
#                                             },
#                                         )
#                                     ],style={"textAlign":"justify",'font-size':'100%'}),

#                                     ],
#                                     id="modal_personas",
#                                     centered=True,
#                                     size="xl",
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),
#                             ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             dcc.Graph(
#                                 id = 'per_grav',
#                                 figure = per_grav,
#                                 config = {
#                                     'displayModeBar': False,
#                                     'displaylogo': False
#                                 }
#                             )
#                         ]),
#                     ], style = {'margin-bottom': '20px'})

#                 ], lg=6, md=6),

#             ], style = {'padding-left': '15px', 'padding-right': '15px'}),

#             # Día de la semana y hora
#             dbc.Row([

#                 # Día de la semana y hora
#                 dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([
#                                 html.P(['Tiempo del Día con Más Hechos Viales'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                             ], style={'width':'95%','display':'inline-block', 'margin-bottom': '0px'}),

#                             html.Div([

#                                 html.Span(
#                                     dbc.Button(
#                                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                                                 style = {'width': '15px', 'height': '15px'})], 
#                                         id="open1_semhora", 
#                                         n_clicks=0, 
#                                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                                         class_name = 'expand-button'

#                                         ),

#                                     id="tooltip-target-semhora",
#                                     style={"textDecoration": "underline", "cursor": "pointer"},
#                                 ),

#                                 dbc.Tooltip(
#                                     "Ampliar vista",
#                                     target="tooltip-target-semhora",
#                                     placement = 'top'
#                                 ),
                                    
#                                 dbc.Modal([

#                                     dbc.ModalHeader(html.B("Por día de la semana y hora")),

#                                     dbc.ModalBody([

#                                         dcc.Graph(
#                                             id = 'heatmap',
#                                             figure = heatmap_modal,
#                                             config={
#                                                 'modeBarButtonsToRemove':
#                                                 ['lasso2d', 'pan2d','zoom2d',
#                                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                                 'resetScale2d', 'hoverClosestCartesian',
#                                                 'hoverCompareCartesian', 'toggleSpikelines',
#                                                 'select2d',],
#                                                 'displaylogo': False
#                                             },
#                                         )
#                                     ],style={"textAlign":"justify",'font-size':'100%'}),
                                    
#                                     ],
#                                     id="modal_semhora",
#                                     centered=True,
#                                     size="xl",
#                                     is_open=False,
#                                     style={'font-family':'Arial'}
#                                 ),
#                             ], style={'width':'4%', 'float': 'right', 'margin-bottom': '0px', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             dcc.Graph(
#                                 id = 'heatmap',
#                                 figure = heatmap,
#                                 config = {
#                                     'displayModeBar': False,
#                                     'displaylogo': False
#                                 }
#                             )
#                         ]),
#                     ], style = {'margin-bottom': '20px'})
#                 ], lg=6, md=6),

#                 # Top intersecciones
#                 # dbc.Col([

#                 #     dbc.Card([
                        
#                 #         dbc.CardBody([

#                 #             html.Div([
#                 #                 html.P(['Top Intersecciones'], style = {'font-size': '18px', 'margin-top': '5px', 'font-weight': 'bold'})
#                 #             ], style={'width':'95%','display':'inline-block'}),

#                 #             html.Div([

#                 #                 html.Span(
#                 #                     dbc.Button(
#                 #                         [html.Img(src='data:image/png;base64,{}'.format(encoded_img7),
#                 #                                 style = {'width': '15px', 'height': '15px'})], 
#                 #                         id="open1_topint", 
#                 #                         n_clicks=0, 
#                 #                         style={'display':'inline-block','padding':'2px', 'background-color':'transparent',
#                 #                                 'border-color':'transparent', 'width': '30px', 'height': '30px'},
#                 #                         class_name = 'expand-button'
#                 #                         ),

#                 #                     id="tooltip-target-topint",
#                 #                     style={"textDecoration": "underline", "cursor": "pointer"},
#                 #                 ),

#                 #                 dbc.Tooltip(
#                 #                     "Ampliar vista",
#                 #                     target="tooltip-target-topint",
#                 #                     placement = 'top'
#                 #                 ),
                                    
#                 #                 dbc.Modal([

#                 #                     dbc.ModalHeader(html.B("Top Intersecciones")),

#                 #                     dbc.ModalBody([

#                 #                         dcc.Graph(
#                 #                             id = 'top_i',
#                 #                             figure = top_i_modal,
#                 #                             config={
#                 #                                 'modeBarButtonsToRemove':
#                 #                                 ['lasso2d', 'pan2d','zoom2d',
#                 #                                 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                 #                                 'resetScale2d', 'hoverClosestCartesian',
#                 #                                 'hoverCompareCartesian', 'toggleSpikelines',
#                 #                                 'select2d',],
#                 #                                 'displaylogo': False
#                 #                             },
#                 #                         )
#                 #                     ],style={"textAlign":"justify",'font-size':'100%'}),
                                    
#                 #                     ],
#                 #                     id="modal_topint",
#                 #                     centered=True,
#                 #                     size="xl",
#                 #                     is_open=False,
#                 #                     style={'font-family':'Arial'}
#                 #                 ),
#                 #             ], style={'width':'4%', 'float': 'right', 'margin-top': '2px'}, className = 'pr-3 d-none d-lg-block'),

#                 #             html.Hr(style = {'margin-top': '0px'}),

#                 #             dcc.Graph(
#                 #                 id = 'top_i',
#                 #                 figure = top_i,
#                 #                 config = {
#                 #                     'displayModeBar': False,
#                 #                     'displaylogo': False
#                 #                 }
#                 #             )
#                 #         ]),
#                 #     ], style = {'margin-bottom': '20px'})
#                 # ], lg=6, md=6),
#             ], style = {'padding-left': '15px', 'padding-right': '15px'}),

#             # PÁRRAFO DIAGNÓSTICO
#             dbc.Row([

#               dbc.Col([

#                     dbc.Card([

#                         dbc.CardBody([

#                             dbc.Row([

#                                 dbc.Col([

#                                     html.P(['Conoce más sobre el estado de seguridad vial en el municipio descargando el ',

#                                         html.A(['Diagnóstico de Seguridad Vial 2020'], href = 'https://drive.google.com/file/d/1oeDpZptdogbqVefihVNnYG3cp6tiNAiL/view?usp=sharing', target = 'blank', style = {'text-decoration': 'None', 'color': '#279FD7', 'font-weight': 'bold'}),

#                                         # dbc.Button(
#                                         #     [html.B('Diagnóstico de Seguridad Vial 2021')], 
#                                         #     id="open1_diagnostico", 
#                                         #     n_clicks=0, 
#                                         #     style={'display':'inline-block', 'background-color':'transparent',
#                                         #         'border-color':'transparent', 'padding': '0px', 'margin': '0px', 'color': '#279FD7', 'font-size': '14px'}
#                                         # ),
                                        
#                                         '.',

#                                     ], style = {'font-size': '14px', 'margin-bottom': '0px'})  

#                                 ]),

#                             ], style = {'margin-bottom': '0px'}),
                            
#                         ], style={'background-color':'#E2E2E2'})
#                     ])

#                 ]),

#             ], className='mx-0'),

#             html.Br(),

#             # FOOTER
#             dbc.Row([

#                 dbc.Col([

#                     dbc.Row([

#                         dbc.Col([

#                             html.Img(src='assets/logo_spgg.png', style={'float':'left', 'margin-top': '25px', 'margin-left': '20px'}),
#                             html.Img(src='assets/implang_logo.png', style={'float':'right', 'margin-top': '27px', 'margin-right': '20px'}),

#                         ], style={'padding-left': '15px'}),#, className='d-lg-flex justify-content-between my-3'),

#                     ]),

#                     dbc.Row([

#                         dbc.Col([

#                             dbc.Button(
#                                 html.Img(src='data:image/png;base64,{}'.format(insta_img), 
#                                         style={'float':'right'},
#                                         className="p-0 img-fluid"), 
#                                 id="open_titulo", 
#                                 n_clicks=0, 
#                                 style={'display':'inline-block',
#                                         'float':'left','padding':'0', 'background-color':'transparent',
#                                         'border-color':'transparent', 'margin-left': '45px'},
#                                 class_name='rounded-circle ml-4 pb-1'

#                             ),

#                             dbc.Button(
#                                 html.Img(src='data:image/png;base64,{}'.format(twitter_img), 
#                                         style={'float':'right'},
#                                         className="p-0 img-fluid"), 
#                                 id="open_titulo", 
#                                 n_clicks=0, 
#                                 style={'display':'inline-block',
#                                         'float':'left','padding':'0', 'background-color':'transparent',
#                                         'border-color':'transparent', 'margin-right': '40px', 'margin-left': '35px'},
#                                 class_name='rounded-circle ml-4 pb-1'

#                             ),

#                             html.B("Comentarios sobre Radar Vial", style = {'font-size': '12px'}),
#                             html.Br(),
#                             html.P("movilidad@sanpedro.gob.mx", style = {'margin-left': '155px', 'font-size': '12px'})

#                         ])

#                     ], style = {'padding-top': '25px'}),

#                 ])

#             ], style={'background-color': '#000', 'color':'white'})

#         ], style={'background-color': '#fafafa'}) 

# # LAYOUT MAPA
# def mapa():

#   return html.Div([

#         # Mapa y filtros DESKTOP
#         dbc.Row([

#             # Controles
#             dbc.Col([

#                 # Fechas
#                 dbc.Row([

#                     dbc.Col([

#                         dbc.Card([
#                             dbc.CardHeader([
#                                 dbc.Button([
#                                     "Fecha",
#                                     html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
#                                                 style={'width':'3%','float':'right'},
#                                                 className="pt-1")
#                                     ],
#                                     id="collapse_button_fecha",
#                                     class_name='btn btn-light btn-lg btn-block',
#                                     color="primary",
#                                     n_clicks=0,
#                                     style={'font-size':'16px'},
#                                 ),

#                             ], style={'text-align':'center'}, class_name='p-0'),

#                             dbc.Collapse(

#                                 dbc.CardBody([

#                                     html.Div([

#                                         dcc.DatePickerRange(
#                                             id = 'calendario',
#                                             min_date_allowed = dt(2015, 1, 1),
#                                             max_date_allowed = dt(2021, 10, 31),
#                                             start_date = dt(2015, 1, 1),
#                                             end_date = dt(2021, 10, 31),
#                                             first_day_of_week = 1,
#                                             className="d-flex justify-content-center"
#                                         ),

#                                     ], className ='d-flex align-items-center justify-content-center'),

#                                     html.Br(),

#                                     dbc.Checklist(
#                                         id = 'checklist_dias',
#                                         class_name = 'radio-group btn-group d-flex flex-wrap justify-content-center',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         options=[
#                                             {'label': ' LU', 'value': 'Lunes'},
#                                             {'label': ' MA', 'value': 'Martes'},
#                                             {'label': ' MI', 'value': 'Miércoles'},
#                                             {'label': ' JU', 'value': 'Jueves'},
#                                             {'label': ' VI', 'value': 'Viernes'},
#                                             {'label': ' SA', 'value': 'Sábado'},
#                                             {'label': ' DO', 'value': 'Domingo'},
#                                         ],
#                                         value=['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
#                                         style={'display':'inline-block'}
#                                     ),

#                                     html.Br(),

#                                     dcc.RangeSlider(
#                                         id='slider_hora',
#                                         min=0,
#                                         max=23,
#                                         value=[0, 23],
#                                         marks={
#                                             0: {'label': '0'},
#                                             3: {'label': '3'},
#                                             6: {'label': '6'},
#                                             9: {'label': '9'},
#                                             12: {'label': '12'},
#                                             15: {'label': '15'},
#                                             18: {'label': '18'},
#                                             21: {'label': '21'},
#                                             23: {'label': '23'}
#                                         },
#                                         allowCross=False,
#                                         dots=True,
#                                         tooltip={'always_visible': False , "placement":"bottom"},
#                                         updatemode='mouseup'
#                                     ),

#                                 ]),
#                                 id="collapse_cal",
#                                 is_open=True,
#                             ),

#                         ], class_name = 'd-none d-lg-block')

#                     ], lg=12, md=12, sm = 12),

#                 ], class_name="d-flex justify-content-between",),

#                 html.Br(),

#                 # Hechos Viales
#                 dbc.Row([

#                     dbc.Col([

#                         dbc.Card([
#                             dbc.CardHeader([
#                                 dbc.Button([
#                                     "Hechos Viales",
#                                     html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
#                                                 style={'width':'3%','float':'right'},
#                                                 className="pt-1")
#                                     ],
#                                     id="collapse_button_hv",
#                                     class_name='btn btn-light btn-lg btn-block',
#                                     color="primary",
#                                     n_clicks=0,
#                                     style={'font-size':'16px'},
#                                 ),

#                             ], style={'text-align':'center'}, class_name='p-0'),

#                             dbc.Collapse(
#                                 dbc.CardBody([

#                                     html.Div([
                                        
#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_sev", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-sev",
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-sev",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Gravedad de Hechos Viales")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Todos:'),' Hechos viales con lesionados + hechos viales con fallecidos + hechos viales sin lesionados y fallecidos.']),
#                                                     html.Li([html.B('Lesionados:'),' Hechos viales en los que resultaron personas lesionadas.']),
#                                                     html.Li([html.B('Fallecidos:'),' Hechos viales en los que resultaron personas fallecidas.']),
#                                                 ], style={'list-style-type':'none'}, className="p-1"),

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_sev", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_sev",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Gravedad',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.RadioItems(
#                                         id = 'hv_graves_opciones',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Lesionados', 'value': 'lesionados'},
#                                             {'label': 'Fallecidos', 'value': 'fallecidos'},
#                                         ]
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.Div([

#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_usaf", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-usaf",
#                                             style={"textDecoration": "underline", "cursor": "pointer"},
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-usaf"
#                                         ),
                                    
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Usuario")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Auto:'),' Acumulado de personas que conducen auto, camión de pasajeros, camioneta, carga pesada, mini van, pickup, trailer y tren.']),
#                                                     html.Li([html.B('Peatón:'),' Personas que caminan.']),
#                                                     html.Li([html.B('Ciclista:'),' Personas que utilizan la bicicleta como modo de transporte.']),
#                                                     html.Li([html.B('Motociclista:'),' Personas que utilizan la motocicleta como modo de transporte.']),
#                                                 ], style={'list-style-type':'none'}, className="p-1")

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_usaf", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_usaf",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Usuario', style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.Checklist(
#                                         id = 'hv_usu_opciones',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         value = ['Motorizado','Peaton','Bicicleta','Motocicleta'],
#                                         options = [
#                                             {'label': 'Auto', 'value': 'Motorizado'},
#                                             {'label': 'Peatón', 'value': 'Peaton'},
#                                             {'label': 'Ciclista', 'value': 'Bicicleta'},
#                                             {'label': 'Motociclista', 'value': 'Motocicleta'}
#                                         ],
#                                         style = {'display':'inline-block'}
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.Div([

#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_thv", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-thv",
#                                             style={"textDecoration": "underline", "cursor": "pointer"},
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-thv",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Tipos de Hechos Viales")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Alcance:'),' Sucede cuando un conductor impacta con su vehículo en la parte trasera de otro.']),
#                                                     html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad. Es imporante destacar que este tipo de hevho vial se asocia únicamente con peatones.']),
#                                                     html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
#                                                     html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
#                                                     html.Li([html.B('Choque de Reversa:'),' Ocurre cuando un vehículo choca con otro al ir de reversa.']),
#                                                     html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
#                                                     html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
#                                                     html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
#                                                     html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.']),
#                                                     html.Li([html.B('Incendio:'),' Ocurre cuando existe un incendio por un percance vial.']),
#                                                     html.Li([html.B('Volcadura:'),' Ocurre cuando un vehículo pierde completamente el contacto entre llantas y superficie de rodamiento originándose giros verticales o transversales']),

#                                                 ], style={'list-style-type':'none'}, className="p-1")

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_thv", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_thv",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Tipo de hecho vial', style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.Checklist(
#                                         id = 'checklist_tipo_hv',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         style={'display':'inline-block'},
#                                         value = [],
#                                         options = [],
#                                     ),

#                                 ]),
#                                 id="collapse_dsem",
#                                 is_open=True,
#                             ),

#                         ]),

#                     ],lg=12, md=12),

#                 ]),

#                 html.Br(),
                
#                 # Búsqueda avanzada
#                 dbc.Row([

#                     dbc.Col([

#                         dbc.Card([
#                             dbc.CardHeader([
#                                 dbc.Button([
#                                     "Búsqueda avanzada",
#                                     html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
#                                                 style={'width':'3%','float':'right'},
#                                                 className="pt-1")
#                                     ],
#                                     id="collapse_button_bavan",
#                                     class_name='btn btn-light btn-lg btn-block',
#                                     color="primary",
#                                     n_clicks=0,
#                                     style={'font-size':'16px'},
#                                 ),



#                             ], style={'text-align':'center'}, class_name='p-0'),

#                             dbc.Collapse(
#                                 dbc.CardBody([

#                                     html.Div([
                                        
#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_afres", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                                 ),

#                                             id="tooltip-target-afres",
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-afres",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Afectado o Responsable")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Afectado:'),' Sujeto perjudicado del siniestro vial.']),
#                                                     html.Li([html.B('Responsable:'),' Sujeto causante del siniestro vial.']),
#                                                     html.Br(),
#                                                     html.Li([
#                                                         html.P([html.B('Nota:'), 
#                                                             ' Es importante destacar que, para el caso de los atropellos al momento de registrar la información sólo se captura de manera digital la información sobre el contexto del hecho vial y de los vehículos, mientras que la información del perfil de las personas que no transitan en un vehículo (peatonas) sólo se registra de manera física en el parte vial y no digital, por lo que actualmente no es posible conocer el perfil demográfico (edad, sexo) de las personas atropelladas.',]),
#                                                             ])
#                                                 ], style={'list-style-type':'none'}, className="p-1"),

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_afres", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_afres",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Afectado o responsable',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.RadioItems(
#                                         id = 'hv_afres_opciones',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Afectados', 'value': 'afectados'},
#                                             {'label': 'Responsables', 'value': 'responsables'},
#                                         ]
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P(' Sexo',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     dbc.RadioItems(
#                                         id = 'hv_sexo_opciones',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Masculino', 'value': 'Masculino'},
#                                             {'label': 'Femenino', 'value': 'Femenino'},
#                                         ],
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P(' Edad',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     html.Br(),

#                                     dcc.RangeSlider(
#                                         id='slider_edad',
#                                         min=0,
#                                         max=85,
#                                         value=[0,85],
#                                         step=5,
#                                         marks={
#                                             1: {'label': '0'},
#                                             5: {'label': '5'},
#                                             10: {'label': '10'},
#                                             15: {'label': '15'},
#                                             20: {'label': '20'},
#                                             25: {'label': '25'},
#                                             30: {'label': '30'},
#                                             35: {'label': '35'},
#                                             40: {'label': '40'},
#                                             45: {'label': '45'},
#                                             50: {'label': '50'},
#                                             55: {'label': '55'},
#                                             60: {'label': '60'},
#                                             65: {'label': '65'},
#                                             70: {'label': '70'},
#                                             75: {'label': '75'},
#                                             80: {'label': '80'},
#                                             85: {'label': '85+'},
#                                         },
#                                         allowCross=False,
#                                         dots=True,
#                                         tooltip={'always_visible': False , "placement":"bottom"},
#                                         updatemode='mouseup',
#                                         className='px-2 pt-2',
#                                     ),

#                                     html.Br(),

#                                     html.P(' Tipo de vehículo',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     dbc.Checklist(
#                                         id = 'checklist_tipo_veh',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         options=[
#                                             {'label': ' Auto', 'value': 'Auto'},
#                                             {'label': ' Bicicleta', 'value': 'Bicicleta'},
#                                             {'label': ' Camión de pasajeros', 'value': 'Camión de pasajeros'},
#                                             {'label': ' Camioneta', 'value': 'Camioneta'},
#                                             {'label': ' Carga pesada', 'value': 'Carga pesada'},
#                                             {'label': ' Mini Van', 'value': 'Mini Van'},
#                                             {'label': ' Motocicleta', 'value': 'Motocicleta'},
#                                             {'label': ' Pick Up', 'value': 'Pick Up'},
#                                             {'label': ' Tracción animal', 'value': 'Tracción animal'},
#                                             {'label': ' Trailer', 'value': 'Trailer'},
#                                             {'label': ' Tren', 'value': 'Tren'},
#                                         ],
#                                         value=['Auto', 'Bicicleta','Camión de pasajeros','Camioneta','Carga pesada','Mini Van','Motocicleta','Pick Up','Tracción animal','Trailer','Tren'],
#                                         style={'display':'inline-block'}
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P([
#                                         html.I([
#                                             html.B('Nota:'),
#                                             ' Los filtros de "sexo", "edad" y "tipo de vehículo" se activan al seleccionar "Afectados" o "Responsables".'
#                                             ])
#                                     ]),

#                                 ]),
#                                 id="collapse_hora",
#                                 is_open=False,
#                             ),

#                         ]),
                        
#                     ], lg=12, md=12),

#                 ]),

#                 html.Br(),

#                 # Botón de descargar datos
#                 dbc.Row([

#                     dbc.Col([
#                         dbc.CardBody([
#                             dcc.Store(id='mapa_data'),
#                             Download(id="download-personal-csv"),
#                             html.Button([
#                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
#                                         style={'width':'3.5%','float':'left'},
#                                         className="pt-1"),
#                                 html.B("Descarga tu búsqueda"),
#                                 ], 
#                                 id="btn_perso_csv",
#                                 className="btn btn-block",
#                                 n_clicks=None,
#                                 style={'float':'right','background-color':'#BBC3C8','color':'white'}
#                             ),
#                         ], class_name='p-0', style={'background-color':'transparent'})#, d-lg-none'
#                     ])
#                 ])

#             ],lg=4, md=4, style={'float': 'left'}),
            
#             # Mapa
#             dbc.Col([

#                 dbc.Card([
#                     dbc.CardHeader([
                        
#                         dbc.Row([

#                             dbc.Col([

#                                 html.Table([

#                                     html.Tr([
#                                         html.Th('Hechos Viales ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_totales', style={'font-weight':'normal', 'border': '0px'}),
#                                     ], style = {'border': '0px'}),

#                                 ], style = {'border': '0px'}),

#                             ], class_name='d-flex justify-content-center'),

#                             dbc.Col([

#                                 html.Table([

#                                     html.Tr([
#                                         html.Th('Lesionados: ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_les_totales', style={'font-weight':'normal', 'border': '0px'}),
#                                     ], style = {'border': '0px'}),

#                                 ], style = {'border': '0px'}),

#                             ], class_name='d-flex justify-content-center'),

#                             dbc.Col([

#                                 html.Table([

#                                     html.Tr([
#                                         html.Th('Fallecidos: ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_fall_totales', style={'font-weight':'normal', 'border': '0px'}),
#                                     ], style = {'border': '0px'}),

#                                 ], style = {'border': '0px'}),

#                             ], class_name='d-flex justify-content-center'),
#                         ])

#                     ], style={'padding':'8px'})
#                 ], style={'textAlign':'center','color':'white'}, class_name='tarjeta_arriba_map'),

#                 dbc.Card([

#                     dbc.CardBody(

#                         dcc.Loading(

#                             dcc.Graph(
#                                 id = 'mapa_interac',
#                                 figure = {},
#                                 config={
#                                 'displayModeBar': False
#                                 },
#                                 style={'height':'85vh'}
#                             ),

#                         color="#636EFA", 
#                         type="cube"),

#                     style={'padding':'0px'},),

#                 ], class_name='tarjeta_map'),

#                 dbc.Card([

#                     dbc.CardBody([

#                         dcc.Store(id='mapa_data_top'),
#                         dcc.Loading(

#                             dcc.Graph(
#                                 id = 'tabla_mapa_top',
#                                 figure = {},
#                                 config={
#                                         'modeBarButtonsToRemove':
#                                         ['lasso2d', 'pan2d',
#                                         'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                         'resetScale2d', 'hoverClosestCartesian',
#                                         'hoverCompareCartesian', 'toggleSpikelines',
#                                         'select2d',],
#                                         'displaylogo': False
#                                     },
#                             ),

#                         color="#636EFA", 
#                         type="cube"),

#                     ],

#                     style={'padding':'0px'},),

#                 ], class_name='tarjeta_map'), 

#             ],lg=8, md=8, style={'float': 'left'}),

#         ], style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '10px'}, class_name = 'd-none d-lg-block'),

#         # Mapa y filtros MÓVIL
#         dbc.Row([

#             dbc.Col([
                    
#                 dbc.Button(
#                     html.Img(src = 'data:image/png;base64,{}'.format(encoded_img5),
#                     className = 'img-fluid',
#                     style = {'width': '75%', 'height': '75%'}),
#                     #'Filtros',
#                     color = 'light',
#                     class_name = 'filtros_small',
#                     id = 'collapse-filtros-movil',
#                     n_clicks = 0
#                 ),

#                 dbc.Button(
#                     html.Img(src = 'data:image/png;base64,{}'.format(encoded_img6),
#                     className = 'img-fluid',
#                     style = {'width': '75%', 'height': '75%'}),
#                     #'Indicadores',
#                     color = 'light',
#                     class_name = 'indicadores_small',
#                     id = 'collapse-indicadores-movil',
#                     n_clicks = 0
#                 ),

#                 dcc.Graph(
#                     id = 'mapa_interac_movil',
#                     figure = {},
#                     config={
#                         'displayModeBar': False
#                     },
#                     style={'position':'relative', 'z-index':'1'},
#                     className = 'vh-100'
#                 ),

#             ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px'})

#         ], class_name = 'w-100 h-100 d-lg-none', style = {'padding': '0px', 'margin': '0px', 'height': '700px'}),

#         dbc.Row([

#             dbc.Col([

#                 dbc.Offcanvas([

#                     # FILTROS FECHA
#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([

#                                 html.P([
#                                     'Fecha'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             html.Hr(style = {'margin-top': '0px', 'padding-top': '0px'}),

#                             html.Div([

#                                 dcc.DatePickerRange(
#                                     id = 'calendario_movil',
#                                     min_date_allowed = dt(2015, 1, 1),
#                                     max_date_allowed = dt(2021, 10, 31),
#                                     start_date = dt(2015, 1, 1),
#                                     end_date = dt(2021, 10, 31),
#                                     first_day_of_week = 1,
#                                     className="d-flex justify-content-center",
#                                     style = {
#                                         'padding': '0px', 
#                                         'margin': '0px'
#                                     }
#                                 ),

#                             ], className ='d-flex align-items-center justify-content-center', style = {'padding': '0px', 'margin': '0px'}),

#                             html.Br(),

#                             html.Div([

#                                             dbc.Checklist(
#                                             id = 'checklist_dias_movil',
#                                             class_name = 'radio-group btn-group d-flex flex-wrap justify-content-center',
#                                             label_class_name = 'btn btn-secondary',
#                                             label_checked_class_name  = 'active',
#                                             options=[
#                                                 {'label': ' LU', 'value': 'Lunes'},
#                                                 {'label': ' MA', 'value': 'Martes'},
#                                                 {'label': ' MI', 'value': 'Miércoles'},
#                                                 {'label': ' JU', 'value': 'Jueves'},
#                                                 {'label': ' VI', 'value': 'Viernes'},
#                                                 {'label': ' SA', 'value': 'Sábado'},
#                                                 {'label': ' DO', 'value': 'Domingo'},
#                                             ],
#                                             value=['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
#                                             style={'display':'inline-block'}
#                                             ),
#                             ], style = {'padding-left': '10px', 'padding-right': '10px'}),

#                             html.Br(),

#                             dcc.RangeSlider(
#                                             id='slider_hora_movil',
#                                             min=0,
#                                             max=23,
#                                             value=[0, 23],
#                                             marks={
#                                                 0: {'label': '0'},
#                                                 3: {'label': '3'},
#                                                 6: {'label': '6'},
#                                                 9: {'label': '9'},
#                                                 12: {'label': '12'},
#                                                 15: {'label': '15'},
#                                                 18: {'label': '18'},
#                                                 21: {'label': '21'},
#                                                 23: {'label': '23'}
#                                             },
#                                             allowCross=False,
#                                             dots=True,
#                                             tooltip={'always_visible': False , "placement":"bottom"},
#                                             updatemode='mouseup'
#                             )
                        
#                         ], style = {'padding': '0px', 'margin': '10px'})

#                     ], style = {'margin-top': '15px', 'margin-left': '20px', 'margin-right': '20px'}),

#                     html.Br(),

#                     # FILTROS HECHOS VIALES
#                     dbc.Card([

#                         dbc.CardBody([

#                             # TÍTULO
#                             html.Div([

#                                 html.P([
#                                     'Hechos Viales'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px'}),

#                             html.Hr(style = {'margin-top': '0px'}),

#                                     html.Div([
                                        
#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_sev_movil", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-sev-movil",
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-sev-movil",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Gravedad de Hechos Viales")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Todos:'),' Hechos viales con lesionados + hechos viales con fallecidos + hechos viales sin lesionados y fallecidos.']),
#                                                     html.Li([html.B('Lesionados:'),' Hechos viales en los que resultaron personas lesionadas.']),
#                                                     html.Li([html.B('Fallecidos:'),' Hechos viales en los que resultaron personas fallecidas.']),
#                                                 ], style={'list-style-type':'none'}, className="p-1"),

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_sev_movil", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_sev_movil",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Gravedad',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),
    
#                                     ]),

#                                     dbc.RadioItems(
#                                         id = 'hv_graves_opciones_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Lesionados', 'value': 'lesionados'},
#                                             {'label': 'Fallecidos', 'value': 'fallecidos'},
#                                         ]
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.Div([

#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_usaf_movil", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-usaf-movil",
#                                             style={"textDecoration": "underline", "cursor": "pointer"},
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-usaf-movil"
#                                         ),
                                    
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Usuario")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Auto:'),' Acumulado de personas que conducen auto, camión de pasajeros, camioneta, carga pesada, mini van, pickup, trailer y tren.']),
#                                                     html.Li([html.B('Peatón:'),' Personas que caminan.']),
#                                                     html.Li([html.B('Ciclista:'),' Personas que utilizan la bicicleta como modo de transporte.']),
#                                                     html.Li([html.B('Motociclista:'),' Personas que utilizan la motocicleta como modo de transporte.']),
#                                                 ], style={'list-style-type':'none'}, className="p-1")

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_usaf_movil", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_usaf_movil",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Usuario', style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.Checklist(
#                                         id = 'hv_usu_opciones_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         value = ['Motorizado','Peaton','Bicicleta','Motocicleta'],
#                                         options = [
#                                             {'label': 'Auto', 'value': 'Motorizado'},
#                                             {'label': 'Peatón', 'value': 'Peaton'},
#                                             {'label': 'Ciclista', 'value': 'Bicicleta'},
#                                             {'label': 'Motociclista', 'value': 'Motocicleta'}
#                                         ],
#                                         style = {'display':'inline-block'}
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.Div([

#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_thv_movil", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                             ),

#                                             id="tooltip-target-thv-movil",
#                                             style={"textDecoration": "underline", "cursor": "pointer"},
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-thv-movil",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Tipos de Hechos Viales")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Alcance:'),' Sucede cuando un conductor impacta con su vehículo en la parte trasera de otro.']),
#                                                     html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad. Es imporante destacar que este tipo de hevho vial se asocia únicamente con peatones.']),
#                                                     html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
#                                                     html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
#                                                     html.Li([html.B('Choque de Reversa:'),' Ocurre cuando un vehículo choca con otro al ir de reversa.']),
#                                                     html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
#                                                     html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
#                                                     html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
#                                                     html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.']),
#                                                     html.Li([html.B('Incendio:'),' Ocurre cuando existe un incendio por un percance vial.']),
#                                                     html.Li([html.B('Volcadura:'),' Ocurre cuando un vehículo pierde completamente el contacto entre llantas y superficie de rodamiento originándose giros verticales o transversales']),

#                                                 ], style={'list-style-type':'none'}, className="p-1")

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_thv_movil", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_thv_movil",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Tipo de hecho vial', style={'width':'90%','float':'left'}, className='pl-1'),

#                                     ]),

#                                     dbc.Checklist(
#                                         id = 'checklist_tipo_hv_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         style={'display':'inline-block'},
#                                         value = [],
#                                         options = [],
#                                     ),

#                         ], style = {'padding': '0px', 'margin': '10px'})
                        
#                     ], style = {'margin-top': '0px', 'margin-left': '20px', 'margin-right': '20px'}),

#                     html.Br(),

#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([

#                                 html.P([
#                                     'Búsqueda Avanzada'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px'}),

#                             html.Hr(style = {'margin-top': '0px'}),

#                             html.Div([
                                        
#                                         html.Span(
#                                             dbc.Button(
#                                                 html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
#                                                         style={'float':'right'},
#                                                         className="p-0 img-fluid"), 
#                                                 id="open1_afres_movil", 
#                                                 n_clicks=0, 
#                                                 style={'display':'inline-block',
#                                                         'float':'left','padding':'0', 
#                                                         'width':'15px','background-color':'transparent',
#                                                         'border-color':'transparent','padding-top':'5px'},
#                                                 class_name='rounded-circle'

#                                                 ),

#                                             id="tooltip-target-afres-movil",
#                                         ),

#                                         dbc.Tooltip(
#                                             "Más información",
#                                             target="tooltip-target-afres-movil",
#                                         ),
                                            
#                                         dbc.Modal([

#                                             dbc.ModalHeader(html.B("Afectado o Responsable")),

#                                             dbc.ModalBody([
#                                                 html.Ul([
#                                                     html.Li([html.B('Afectado:'),' Sujeto perjudicado del siniestro vial.']),
#                                                     html.Li([html.B('Responsable:'),' Sujeto causante del siniestro vial.']),
#                                                     html.Br(),
#                                                     html.Li([
#                                                         html.P([html.B('Nota:'), 
#                                                             ' Es importante destacar que, para el caso de los atropellos al momento de registrar la información sólo se captura de manera digital la información sobre el contexto del hecho vial y de los vehículos, mientras que la información del perfil de las personas que no transitan en un vehículo (peatonas) sólo se registra de manera física en el parte vial y no digital, por lo que actualmente no es posible conocer el perfil demográfico (edad, sexo) de las personas atropelladas.',]),
#                                                             ])
#                                                 ], style={'list-style-type':'none'}, className="p-1"),

#                                             ],style={"textAlign":"justify",'font-size':'100%'}),

#                                             dbc.ModalFooter([
                                                
#                                                 dbc.Button(
#                                                     "Cerrar", 
#                                                     id="close1_afres_movil", 
#                                                     class_name="ml-auto btn btn-secondary", 
#                                                     n_clicks=0
#                                                 )
#                                             ]),

#                                             ],
#                                             id="modal_afres_movil",
#                                             centered=True,
#                                             size="lg",
#                                             is_open=False,
#                                             style={'font-family':'Arial'}
#                                         ),

#                                         html.P(' Afectado o responsable',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                             ]),

#                                     dbc.RadioItems(
#                                         id = 'hv_afres_opciones_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Afectados', 'value': 'afectados'},
#                                             {'label': 'Responsables', 'value': 'responsables'},
#                                         ]
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P(' Sexo',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     dbc.RadioItems(
#                                         id = 'hv_sexo_opciones_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name = 'active',
#                                         value = 'todos',
#                                         options = [
#                                             {'label': 'Todos', 'value': 'todos'},
#                                             {'label': 'Masculino', 'value': 'Masculino'},
#                                             {'label': 'Femenino', 'value': 'Femenino'},
#                                         ],
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P(' Edad',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     html.Br(),

#                                     dcc.RangeSlider(
#                                         id='slider_edad_movil',
#                                         min=0,
#                                         max=85,
#                                         value=[0,85],
#                                         step=5,
#                                         marks={
#                                             1: {'label': '0'},
#                                             5: {'label': '5'},
#                                             10: {'label': '10'},
#                                             15: {'label': '15'},
#                                             20: {'label': '20'},
#                                             25: {'label': '25'},
#                                             30: {'label': '30'},
#                                             35: {'label': '35'},
#                                             40: {'label': '40'},
#                                             45: {'label': '45'},
#                                             50: {'label': '50'},
#                                             55: {'label': '55'},
#                                             60: {'label': '60'},
#                                             65: {'label': '65'},
#                                             70: {'label': '70'},
#                                             75: {'label': '75'},
#                                             80: {'label': '80'},
#                                             85: {'label': '85+'},
#                                         },
#                                         allowCross=False,
#                                         dots=True,
#                                         tooltip={'always_visible': False , "placement":"bottom"},
#                                         updatemode='mouseup',
#                                         className='px-2 pt-2',
#                                     ),

#                                     html.Br(),

#                                     html.P(' Tipo de vehículo',
#                                             style={'width':'90%','float':'left'}, className='pl-1'),

#                                     dbc.Checklist(
#                                         id = 'checklist_tipo_veh_movil',
#                                         class_name = 'radio-group btn-group',
#                                         label_class_name = 'btn btn-secondary',
#                                         label_checked_class_name  = 'active',
#                                         options=[
#                                             {'label': ' Auto', 'value': 'Auto'},
#                                             {'label': ' Bicicleta', 'value': 'Bicicleta'},
#                                             {'label': ' Camión de pasajeros', 'value': 'Camión de pasajeros'},
#                                             {'label': ' Camioneta', 'value': 'Camioneta'},
#                                             {'label': ' Carga pesada', 'value': 'Carga pesada'},
#                                             {'label': ' Mini Van', 'value': 'Mini Van'},
#                                             {'label': ' Motocicleta', 'value': 'Motocicleta'},
#                                             {'label': ' Pick Up', 'value': 'Pick Up'},
#                                             {'label': ' Tracción animal', 'value': 'Tracción animal'},
#                                             {'label': ' Trailer', 'value': 'Trailer'},
#                                             {'label': ' Tren', 'value': 'Tren'},
#                                         ],
#                                         value=['Auto', 'Bicicleta','Camión de pasajeros','Camioneta','Carga pesada','Mini Van','Motocicleta','Pick Up','Tracción animal','Trailer','Tren'],
#                                         style={'display':'inline-block'}
#                                     ),

#                                     html.Br(),
#                                     html.Br(),

#                                     html.P([
#                                         html.I([
#                                             html.B('Nota:'),
#                                             ' Los filtros de "sexo", "edad" y "tipo de vehículo" se activan al seleccionar "Afectados" o "Responsables".'
#                                             ])
#                                     ]),

#                         ], style = {'padding': '0px', 'margin': '10px'})

#                     ], style = {'margin-bottom': '10px', 'margin-left': '20px', 'margin-right': '20px'})

#                 ], 
#                 placement = 'bottom', 
#                 close_button = False, 
#                 style = {
#                     'padding-top': '5px', 
#                     'padding-left': '5px', 
#                     'padding-right': '5px', 
#                     'margin': '0px', 
#                     'background-color': '#F8F9FB',
#                     'height': '400px'
#                 }, 
#                 id = 'filtros-movil', is_open = False)
#             ], class_name = 'd-lg-none')
#         ], class_name = 'd-lg-none'),

#         dbc.Row([

#             dbc.Col([

#                 dbc.Offcanvas([

#                     # INDICADOR HECHOS VIALES
#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([

#                                 html.P([
#                                     'Hechos Viales Totales'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             html.Table([

#                                     html.Tr([
#                                         #html.Th('Hechos Viales ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
#                                     ], style = {'border': '0px'}),

#                             ], style = {'border': '0px'}, className = 'd-flex justify-content-center')                            
                        
#                         ], style = {'padding': '0px', 'margin': '10px'})

#                     ], style = {'margin-top': '15px', 'margin-left': '20px', 'margin-right': '20px'}),

#                     html.Br(),

#                     # INDICADOR LESIONADOS
#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([

#                                 html.P([
#                                     'Lesionados'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             html.Table([

#                                     html.Tr([
#                                         #html.Th('Lesionados: ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_les_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
#                                     ], style = {'border': '0px'}),

#                             ], style = {'border': '0px'}, className = 'd-flex justify-content-center')

#                         ], style = {'padding': '0px', 'margin': '10px'})
                        
#                     ], style = {'margin-top': '0px', 'margin-left': '20px', 'margin-right': '20px'}),

#                     html.Br(),

#                     # INDICADOR FALLECIDOS
#                     dbc.Card([

#                         dbc.CardBody([

#                             html.Div([

#                                 html.P([
#                                     'Fallecidos'
#                                 ], 
#                                 style = {
#                                     'font-size': '18px', 
#                                     'font-weight': 'bold',
#                                     'margin-bottom': '5px'
#                                     }
#                                 )
#                             ], style={'margin-bottom': '0px', 'padding-bottom': '0px'}),

#                             html.Table([

#                                     html.Tr([
#                                         #html.Th('Fallecidos: ', style={'font-weight':'normal', 'border': '0px'}),
#                                         html.Th(id = 'hv_fall_totales_movil', style={'font-weight':'normal', 'border': '0px', 'font-size': '24px'}),
#                                     ], style = {'border': '0px'}),

#                             ], style = {'border': '0px'}, className = 'd-flex justify-content-center')

#                         ], style = {'padding': '0px', 'margin': '10px'})

#                     ], style = {'margin-bottom': '10px', 'margin-left': '20px', 'margin-right': '20px'}),

#                     dbc.Card([

#                         dbc.CardBody([

#                             dcc.Store(id='mapa_data_top_movil'),

#                             dcc.Graph(
#                                 id = 'tabla_mapa_top_movil',
#                                 figure = {},
#                                 config={
#                                         'modeBarButtonsToRemove':
#                                         ['lasso2d', 'pan2d',
#                                         'zoomIn2d', 'zoomOut2d', 'autoScale2d',
#                                         'resetScale2d', 'hoverClosestCartesian',
#                                         'hoverCompareCartesian', 'toggleSpikelines',
#                                         'select2d',],
#                                         'displaylogo': False
#                                     },
#                             )

#                         ], style = {'padding': '0px', 'margin': '10px', 'white-space': 'nowrap', 'overflow-x': 'auto'},
#                         class_name = 'd-flex flex-nowrap')

#                     ], style = {'margin-bottom': '10px', 'margin-left': '20px', 'margin-right': '20px'})

#                 ], 
#                 placement = 'bottom', 
#                 close_button = False, 
#                 style = {
#                     'padding-top': '5px', 
#                     'padding-left': '5px', 
#                     'padding-right': '5px', 
#                     'margin': '0px', 
#                     'background-color': '#F8F9FB',
#                     'height': '400px'
#                 }, 
#                 id = 'indicadores-movil', is_open = False)

#             ], class_name = 'd-lg-none')

#         ], class_name = 'd-lg-none')

#     ], className = 'w-100 h-100', style = {'padding': '0px', 'margin': '0px'})

#----------------------------------------------------------

## CALLBACKS

#----------

# CALLBACKS HEADER

# # CARGAR CONTENIDO TABS
# @app.callback(
#     Output('hechosviales_content', 'children'), 
#     [Input('tabs', 'active_tab'),
#      Input('boton_back', 'n_clicks'),
#      # Input('boton_test2', 'n_clicks'),
#      ]) 
# def render_hechosviales(tabs, boton_test):
#     if tabs == 'resumen' and boton_test == 0:
#         return resumen()

#     elif tabs == 'mapa' and boton_test == 0:
#         return mapa()

#     # elif tabs == 'resumen' and boton_test != 0:
#     #     return mapa()

#     elif tabs == 'mapa' and boton_test != 0:
#         return resumen()

#     else:
#         return resumen()


# UPDATEAR TABS 1
@app.callback(
    Output('tabs', 'active_tab'), 
    [Input('boton_mapa', 'n_clicks'),
     Input('boton_back', 'n_clicks')
     ]) 
def render_tabs(boton_mapa, boton_back):
    if boton_mapa == 0:
        return 'resumen'

    elif boton_back != 0:
        return 'resumen'

    elif boton_mapa != 0:
        return 'mapa'

    elif boton_back == 0:
        return 'resumen'

    else:
        return 'resumen'

 # VER O ESCONDER BOTÓN
@app.callback(
    Output('boton_back', 'className'), 
    [Input('tabs', 'active_tab'),
     ]) 
def render_boton_test(tabs):
    if tabs == 'resumen':
        return 'd-none'

    elif tabs == 'mapa':
        return 'expand-button'

    else:
        return 'expand-button'


# CARGAR TABS
@app.callback(
    [Output('resumensito', 'className'),
     Output('mapicha', 'className'),], 
    [Input('tabs', 'active_tab'),
     Input('boton_back', 'n_clicks'),
     Input('boton_mapa', 'n_clicks'),
     ]) 
def render_boton_test(tabs, boton_back, boton_mapa):
    if tabs == 'resumen' and boton_mapa == 0:
        return '', 'w-100 h-100 d-none'

    elif tabs == 'mapa' and boton_back == 0:
        return 'd-none', 'w-100 h-100'

    elif tabs == 'mapa' and boton_back != 0:
        return '', 'w-100 h-100 d-none'

    elif tabs == 'resumen' and boton_mapa != 0 and boton_back != 0:
        return '', 'w-100 h-100 d-none'

    else:
        return '', 'w-100 h-100 d-none'

# CARGAR TABS
# @app.callback(
#     Output('hechosviales_content', 'children'), 
#     [Input('tabs', 'active_tab')])
# def get_hechosviales(tab):
#     return render_hechosviales(tab)

#-----------

# CALLBACKS RESUMEN

# RADAR VIAL - INICIO: MODAL INFO RADAR VIAL
@app.callback(
    Output("modal_inforadar", "is_open"),
    [Input("open1_inforadar", "n_clicks")],
    [State("modal_inforadar", "is_open")])
def toggle_modal_tothv(open1_inforadar, modal_inforadar):
    if open1_inforadar:
        return not modal_inforadar
    return modal_inforadar

# RADAR VIAL - INICIO: MODAL HECHOS VIALES TOTALES
@app.callback(
    Output("modal_tothv", "is_open"),
    [Input("open1_tothv", "n_clicks")],
    [State("modal_tothv", "is_open")])
def toggle_modal_tothv(open1_tothv, modal_tothv):
    if open1_tothv:
        return not modal_tothv
    return modal_tothv

# RADAR VIAL - INICIO: MODAL HECHOS VIALES PROMEDIO
@app.callback(
    Output("modal_hvprom", "is_open"),
    [Input("open1_hvprom", "n_clicks")],
    [State("modal_hvprom", "is_open")])
def toggle_modal_hvprom(open1_hvprom, modal_hvprom):
    if open1_hvprom:
        return not modal_hvprom
    return modal_hvprom

# RADAR VIAL - INICIO: MODAL PERSONAS
@app.callback(
    Output("modal_personas", "is_open"),
    [Input("open1_personas", "n_clicks")],
    [State("modal_personas", "is_open")])
def toggle_modal_personas(open1_personas, modal_personas):
    if open1_personas:
        return not modal_personas
    return modal_personas

# RADAR VIAL - INICIO: MODAL HEATMAP SEMANA Y HORA
@app.callback(
    Output("modal_semhora", "is_open"),
    [Input("open1_semhora", "n_clicks")],
    [State("modal_semhora", "is_open")])
def toggle_modal_semhora(open1_semhora, modal_semhora):
    if open1_semhora:
        return not modal_semhora
    return modal_semhora

# RADAR VIAL - INICIO: MODAL TREEMAP TIPO Y CAUSA
@app.callback(
    Output("modal_tipocausa", "is_open"),
    [Input("open1_tipocausa", "n_clicks")],
    [State("modal_tipocausa", "is_open")])
def toggle_modal_tipocausa(open1_tipocausa, modal_tipocausa):
    if open1_tipocausa:
        return not modal_tipocausa
    return modal_tipocausa

# RADAR VIAL - INICIO: MODAL LESIONADOS Y FALLECIDOS
@app.callback(
    Output("modal_lesionfall", "is_open"),
    [Input("open1_lesionfall", "n_clicks")],
    [State("modal_lesionfall", "is_open")])
def toggle_modal_lesionfall(open1_lesionfall, modal_lesionfall):
    if open1_lesionfall:
        return not modal_lesionfall
    return modal_lesionfall

# RADAR VIAL - INICIO: MODAL TOP CALLES
@app.callback(
    Output("modal_topcalles", "is_open"),
    [Input("open1_topcalles", "n_clicks")],
    [State("modal_topcalles", "is_open")])
def toggle_modal_topcalles(open1_topcalles, modal_topcalles):
    if open1_topcalles:
        return not modal_topcalles
    return modal_topcalles

# RADAR VIAL - INICIO: MODAL TOP INTERSECCIONES
@app.callback(
    Output("modal_topint", "is_open"),
    [Input("open1_topint", "n_clicks")],
    [State("modal_topint", "is_open")])
def toggle_modal_topint(open1_topint, modal_topint):
    if open1_topint:
        return not modal_topint
    return modal_topint

# RADAR VIAL - INICIO: BOTONES TOP UBICACIONES
@app.callback(
    Output('top_ubi', 'figure'),
    [Input('checklist_top', 'value')]
)
def toggle_top_ubi(value):

    if value == 'top_c':
        return top_c

    elif value == 'top_i':
        return top_i

        

#----------

# CALLBACKS MAPA

# RADAR VIAL - MAPA: CARGAR OPCIONES POR USUARIO
@app.callback(
    Output('checklist_tipo_hv', 'options'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)
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


# RADAR VIAL - MAPA: CARGAR OPCIONES POR USUARIO - MOVIL
@app.callback(
    Output('checklist_tipo_hv_movil', 'options'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    prevent_initial_call=False)
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


# RADAR VIAL - MAPA: CARGAR VALORES POR USUARIO
@app.callback(
    Output('checklist_tipo_hv', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)
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


# RADAR VIAL - MAPA: CARGAR VALORES POR USUARIO - MOVIL
@app.callback(
    Output('checklist_tipo_hv_movil', 'value'),
    Input('hv_usu_opciones_movil', 'value'),
    Input('hv_graves_opciones_movil', 'value'),
    prevent_initial_call=False)
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

        return '{:,.0f}'.format(hv_totales)
    
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

        return '{:,.0f}'.format(hv_totales)

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

        return '{:,.0f}'.format(hv_totales)

    
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

        return '{:,.0f}'.format(hv_totales)

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

        return '{:,.0f}'.format(hv_totales)

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

        return '{:,.0f}'.format(hv_totales)



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

# RADAR VIAL - MAPA: MAPA MOVIL
@app.callback(
    [Output('mapa_interac_movil', 'figure'),
    Output('mapa_data_top_movil', 'data')], 
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
    
        return mapa_interac_movil, mapa_data_top_movil

    
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

        return mapa_interac_movil, mapa_data_top_movil
    
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

        return mapa_interac_movil, mapa_data_top_movil

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

        return mapa_interac_movil, mapa_data_top_movil

    
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

        return mapa_interac_movil, mapa_data_top_movil

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

        return mapa_interac_movil, mapa_data_top_movil

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

        return mapa_interac_movil, mapa_data_top_movil



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
        
        return mapa_interac_movil, mapa_data_top_movil
       
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
        
        return mapa_interac_movil, mapa_data_top_movil
    
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
        
        return mapa_interac_movil, mapa_data_top_movil


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
        
        return mapa_interac_movil, mapa_data_top_movil
    
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
        
        return mapa_interac_movil, mapa_data_top_movil
    
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
        
        return mapa_interac_movil, mapa_data_top_movil



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
        
        return mapa_interac_movil, mapa_data_top_movil
   
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
        
        return mapa_interac_movil, mapa_data_top_movil

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
        
        return mapa_interac_movil, mapa_data_top_movil


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
        
        return mapa_interac_movil, mapa_data_top_movil

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
        
        return mapa_interac_movil, mapa_data_top_movil
    
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
        
        return mapa_interac_movil, mapa_data_top_movil


    # -------------------------------------------

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

# RADAR VIAL - MAPA: MAPA DATA - MOVIL
@app.callback(Output('mapa_data_movil', 'data'), 
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
def render_mapa_data_movil(start_date, end_date, slider_hora_movil, checklist_dias_movil, hv_graves_opciones_movil, hv_usu_opciones_movil, checklist_tipo_hv_movil, hv_afres_opciones_movil, hv_sexo_opciones_movil, checklist_tipo_veh_movil, slider_edad_movil):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias_movil == [] or checklist_tipo_hv_movil == [] or checklist_tipo_veh_movil == [] or hv_usu_opciones_movil == []:
    
        mapa_data_movil = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data_movil = pd.DataFrame(mapa_data_movil)

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

    
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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_thv_usu

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
    
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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh
        
        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

    
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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_usu_thv

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

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

        # Cambiar nombre
        mapa_data_movil = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil



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

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
       
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

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
    
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

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil


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
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
    
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
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv_movil))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad_movil[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad_movil[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones_movil]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh_movil)]

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
    
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

        # Cambiar nombre
        mapa_data_movil = hv_les_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil



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
    
        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
   
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

        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

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

        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
 

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
    
        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

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

        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil
    
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

        # Cambiar nombre
        mapa_data_movil = hv_fall_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data_movil = mapa_data_movil.reset_index()
        mapa_data_movil['fecha'] = mapa_data_movil['fecha'].astype(str)

        # Quitar columnas
        mapa_data_movil = mapa_data_movil.drop(['tipo_usu_afect', 'tipo_usu_resp', 'tipo_usu', 'tipo_v_afec', 'tipo_v_resp', 'edad_afect_rango', 'edad_afect_mid', 'edad_resp_rango', 'edad_resp_mid', 'sexo_afect', 'sexo_resp','hechos_viales'], axis=1)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_movil_f = [slider_hora_movil[0],' a ', slider_hora_movil[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias_movil,slider_hora_movil_f,hv_graves_opciones_movil,hv_usu_opciones_movil,checklist_tipo_hv_movil,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data_movil = pd.concat([mapa_data_movil, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data_movil = mapa_data_movil.to_json(orient='columns')

        return mapa_data_movil

    # Cambiar a JSON
    mapa_data_movil = mapa_data_movil.reset_index()
    mapa_data_movil = mapa_data_movil.to_json(orient='columns')

    return mapa_data_movil

    # -------------------------------------------


# RADAR VIAL - MAPA: TABLA TOP INTERSECCIONES
@app.callback(
    Output('tabla_mapa_top', 'figure'), 
    Input('mapa_data_top', 'data'))  
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


# RADAR VIAL - MAPA: TABLA TOP INTERSECCIONES - MOVIL
@app.callback(
    Output('tabla_mapa_top_movil', 'figure'), 
    Input('mapa_data_top_movil', 'data'))  
def render_tabla_mapa_top_movil(datos_tabla_mapa_movil):   

    # Tabla
    datos_tabla_mapa_movil = pd.read_json(datos_tabla_mapa_movil)
    
    tabla_mapa_top_movil = go.Figure(
            [go.Table(
                columnwidth = [100, 50, 50, 50],
                header=dict(values=['Intersección','Hechos viales','Lesionados','Fallecidos'],
                    fill_color='#343332',
                    font=dict(color='white', family='Arial', size = 16),
                    align='center'),
                cells=dict(values=[datos_tabla_mapa_movil.interseccion, datos_tabla_mapa_movil.hechos_viales, datos_tabla_mapa_movil.lesionados, datos_tabla_mapa_movil.fallecidos],
                   fill_color='#F7F7F7',
                   font=dict(color='black', family='Arial', size = 16),
                   align=['left', 'center', 'center', 'center'],
                   height=35))
            ])
    tabla_mapa_top_movil.update_layout(margin = dict(t=20, l=0, r=0, b=10))


    return tabla_mapa_top_movil


# RADAR VIAL - MAPA: DESCARGA TU BÚSQUEDA
@app.callback(
    Output("download-personal-csv", "data"),
    Input("btn_perso_csv", "n_clicks"),
    State('mapa_data', 'data'),
    prevent_initial_call=True,)
def render_down_data_csv(n_clicks, data):
    
    a_json = json.loads(data)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "hechos_viales_query.csv", index=False, encoding='ISO-8859-1')

    return csv

# RADAR VIAL - MAPA: MODAL GRAVEDAD
@app.callback(
    Output("modal_sev", "is_open"),
    [Input("open1_sev", "n_clicks"), 
    Input("close1_sev", "n_clicks")],
    [State("modal_sev", "is_open")],)
def toggle_modal_sev(open1_sev, close1_sev, modal_sev):
    if open1_sev or close1_sev:
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

# COLLAPSE INDICADORES MOVIL
@app.callback(
    Output("indicadores-movil", "is_open"),
    [Input("collapse-indicadores-movil", "n_clicks")],
    [State("indicadores-movil", "is_open")])
def toggle_collapse_indicadores_movil(n, is_open):
    if n:
        return not is_open
    return is_open

# RADAR VIAL: TARJETA COLAPSABLE CALENDARIO
@app.callback(
    Output("collapse_cal", "is_open"),
    [Input("collapse_button_fecha", "n_clicks")],
    [State("collapse_cal", "is_open")])
def render_collapse_button_fecha(n, is_open):
    if n:
        return not is_open
    return is_open

# RADAR VIAL: TARJETA COLAPSABLE HECHOS VIALES
@app.callback(
    Output("collapse_dsem", "is_open"),
    [Input("collapse_button_hv", "n_clicks")],
    [State("collapse_dsem", "is_open")],)
def render_collapse_button_hv(n, is_open):
    if n:
        return not is_open
    return is_open

# RADAR VIAL: TARJETA COLAPSABLE BUSQUEDA AVANZADA
@app.callback(
    Output("collapse_hora", "is_open"),
    [Input("collapse_button_bavan", "n_clicks")],
    [State("collapse_hora", "is_open")],)
def render_collapse_button_bavan(n, is_open):
    if n:
        return not is_open
    return is_open

#----------------------------------------------------------


if __name__ == '__main__':
	app.run_server(debug=True)


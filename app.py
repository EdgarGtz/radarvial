import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth
import base64


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

from apps.home import (render_collapse_button_fecha, render_collapse_button_hv, toggle_modal_sev, toggle_modal_usaf, render_opciones_dos,
  render_opciones_dos_dos, toggle_modal_thv, render_collapse_button_bavan, toggle_modal_afres, render_hv_totales, render_hv_les_totales, 
  render_hv_fall_totales, render_mapa_interac, render_mapa_interac_movil, render_tabla_mapa_top, render_mapa_data, render_down_data_csv)

from apps.visualizaciones import (render_pub_periodo, render_pub_vulne, render_pub_time)

radar_img = "https://cdn-icons-png.flaticon.com/512/188/188595.png"

# App Layout

app.layout = html.Div([

  dbc.Row([

dbc.Col([

      html.A(

        dbc.Row([

            dbc.Col([

              html.Img(src=radar_img, height="40px",),
              dbc.NavbarBrand(
                html.H1("Radar Vial"), 
                className="ml-2 pt-3", 
                style={'color':'#fff','font-family':'Times New Roman'})

            ], className='d-flex align-items-center pl-3',),

          ],

          align="center",

        ),

        href="/apps/home",
        className='ml-0'
      ),

    ], className='d-flex align-items-center'),

    dbc.Col([

      dbc.NavbarSimple([

          dbc.Button('Visualizaciones', href='/apps/visualizaciones', color='#2A4A71', style={'color':'#fff'}),

          dbc.Button('¿Qué es Radar Vial?', href = '/apps/radarvial', color = '#2A4A71', style={'color':'#fff'})

          ],
          brand_href='/apps/home',
          style={'height':'80px',},
          color="",
      ),

    ])


  ], style={'background-color':'#555B61'}, className='mx-0'),

	html.Div(id='page-content', children=[],),
	dcc.Location(id='url', refresh=False)

])


# Display main pages

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
	if pathname == '/apps/visualizaciones':
		return visualizaciones.layout
	elif pathname == '/apps/radarvial':
		return radarvial.layout
	else:
		return home.layout

#----------

# Mapa
@app.callback(Output('mapa_pub', 'figure'), 
    [Input('calendario_pub', 'start_date'),
    Input('calendario_pub', 'end_date'),
    Input('slider_hora_pub', 'value'),
    Input('checklist_dias_pub', 'value'),
    Input('hv_graves_opciones_pub', 'value'), 
    Input('rvlg', 'on'),
    Input('rvlg_intg', 'on'),
    Input('rvlg_int', 'on'),
    Input('checklist_tipo_usu_pub', 'value'),
    ],
            prevent_initial_call=False)

def get(start_date, end_date, slider_hora_pub, checklist_dias_pub, hv_graves_opciones_pub, rvlg, rvlg_intg, rvlg_int, checklist_tipo_usu_pub):
    return render_mapa_pub(start_date, end_date, slider_hora_pub, checklist_dias_pub, hv_graves_opciones_pub, rvlg, rvlg_intg, rvlg_int, checklist_tipo_usu_pub)


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

#Modal Red Vial
@app.callback(
    Output("modal_rvlg", "is_open"),
    [Input("open_rvlg", "n_clicks"), 
    Input("close_rvlg", "n_clicks")],
    [State("modal_rvlg", "is_open")],)

def toggle_modal_rvlg(open_rvlg, close_rvlg, modal_rvlg):
    if open_rvlg or close_rvlg:
        return not modal_rvlg
    return modal_rvlg

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

# RADAR VIAL - MAPA: CARGAR VALORES POR USUARIO
@app.callback(
    Output('checklist_tipo_hv', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)
def get_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones):
    return render_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones)

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

@app.callback(
    Output('mapa_interac_movil', 'figure'),
     #Output('mapa_data_top', 'data')], 
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

### -------


if __name__ == '__main__':
	app.run_server(debug=True)


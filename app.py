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

from apps.home import (render_mapa_pub, toggle_modal_fecha, toggle_modal_g, toggle_modal_u, toggle_modal_rvlg)

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
          no_gutters=True,

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


  ], style={'background-color':'#2A4A71'}, className='mx-0'),

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
    Input('checklist_tipo_usu_pub', 'value'),
    ],
            prevent_initial_call=False)

def get(start_date, end_date, slider_hora_pub, checklist_dias_pub, hv_graves_opciones_pub, rvlg, checklist_tipo_usu_pub):
    return render_mapa_pub(start_date, end_date, slider_hora_pub, checklist_dias_pub, hv_graves_opciones_pub, rvlg, checklist_tipo_usu_pub)


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

if __name__ == '__main__':
	app.run_server(debug=True)


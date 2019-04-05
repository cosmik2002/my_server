import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import json

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True
app.layout = html.Div([
    html.Button(id='button', n_clicks=0, children='Show table'),
    html.Div(id='content'),
    #html.Div(dt.DataTable(data=[{}]), style={'display': 'none'})
])


@app.callback(Output('content', 'children'), [Input('button', 'n_clicks')])
def display_output(n_clicks):
    if n_clicks > 0:
        return html.Div([
            html.Div(id='datatable-output'),
            dt.DataTable(
                id='datatable',
                columns=[{'id':'Column 1','name':'Column 1'}],
                data=[{'Column 1': i} for i in range(5)]
            )
        ])


@app.callback(
    Output('datatable-output', 'children'),
    [Input('datatable', 'data')])
def update_output(data):
    return html.Pre(
        json.dumps(data, indent=2)
    )


if __name__ == '__main__':
    app.run_server(debug=True)
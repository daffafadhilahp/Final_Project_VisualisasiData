import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Baca data CSV
df = pd.read_csv('covid_19_indonesia_time_series_all.csv')

# Ubah kolom tanggal menjadi format datetime dan kemudian ke format numerik
df['Date'] = pd.to_datetime(df['Date'])
df['Date_numeric'] = df['Date'].apply(lambda x: x.timestamp())

# Buat aplikasi Dash
app = dash.Dash(__name__)

# Layout aplikasi
app.layout = html.Div([
    html.H1("Visualisasi Data COVID-19 Indonesia"),
    dcc.Dropdown(
        id='variable',
        options=[
            {'label': 'Kasus Positif', 'value': 'Total Cases'},
            {'label': 'Kasus Sembuh', 'value': 'Total Recovered'},
            {'label': 'Kasus Meninggal', 'value': 'Total Deaths'}
        ],
        value='Total Cases',
        clearable=False
    ),
    dcc.Slider(
        id='date-slider',
        min=df['Date_numeric'].min(),
        max=df['Date_numeric'].max(),
        value=df['Date_numeric'].max(),
        marks={row['Date_numeric']: row['Date'].strftime('%Y-%m-%d') for _, row in df.iterrows()},
        step=None
    ),
    dcc.Graph(id='covid-graph')
])

# Callback untuk mengupdate grafik
@app.callback(
    Output('covid-graph', 'figure'),
    [Input('variable', 'value'),
     Input('date-slider', 'value')])
def update_graph(variable, date_value):
    date = pd.to_datetime(date_value, unit='s')
    filtered_df = df[df['Date'] == date]
    fig = px.choropleth(filtered_df, locations='Location',
                        locationmode='country names',
                        color=variable,
                        hover_name='Location',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection='natural earth')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
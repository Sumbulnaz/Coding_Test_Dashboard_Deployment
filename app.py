# import the libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from prep_data import dashboard_data,genre,rating_list

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Set up the app layout
app.layout = html.Div(children=[
    html.H1(children='Imdb vs Rotten tomatoes Ratings Dashboard'),
    html.H2(children='Year Released'),
    dcc.RangeSlider(
            id='year-released-range-slider',
            min=dashboard_data.year.min(),
            max=dashboard_data.year.max(),
            marks={str(y): str(y) for y in range(int(dashboard_data.year.min()), int(dashboard_data.year.max()), 5)},
            value=[dashboard_data.year.min(), dashboard_data.year.max()]
        ),
    html.Br(),
    html.H2(children='Ratings'),
    dcc.Dropdown(
        id = 'rating-dropdown',
        options=[{'label':i,'value':i} for i in rating_list],
        value='All movies'
    ),
    html.Br(),
    html.H2(children='Genre'),
    dcc.Dropdown(
        id = 'genre-dropdown',
        options=[{'label':i,'value':i} for i in genre],
        value='All Genre'
    ),
    html.Br(),
    dcc.Graph(id='rating-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='rating-graph', component_property='figure'),
    [
     Input(component_id='year-released-range-slider', component_property='value'),
     Input(component_id='rating-dropdown',component_property='value'),
     Input(component_id='genre-dropdown',component_property='value')
    ]
)
def update_graph(selected_year,rating_name,genre_name):
    year_released_start, year_released_end = selected_year
    filtered_df1 = dashboard_data.loc[(dashboard_data['year'] >= year_released_start)&(dashboard_data['year'] <= year_released_end)]
    if rating_name == 'All movies':
      rating_select = ''
    else:
      rating_select= rating_name
    filtered_df2 = filtered_df1.loc[(filtered_df1['rating'].str.contains(rating_select))]
    if genre_name == 'All Genre':
        genre_name_select = ''
    else:
        genre_name_select = genre_name
    filtered_final = filtered_df2.loc[filtered_df2['genre'].str.contains(genre_name_select)]
    scatter_fig = px.scatter(filtered_final,
                       x='imdb_scaled', y='worldwide_gross_income',hover_name='original_title',
                       hover_data=['genre','worldwide_gross_income','year'],
                       )
    return scatter_fig



# Run local server
if __name__ == '__main__':
    app.run_server()

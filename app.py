import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset from the URL
url = "https://github.com/plotly/datasets/raw/master/2014_world_gdp_with_codes.csv"
df = pd.read_csv(url)

# Create a choropleth map using Plotly Express
choropleth_fig = px.choropleth(df,
                               locations="CODE", # The column with ISO country codes
                               color="GDP (BILLIONS)", # The column with GDP values
                               hover_name="COUNTRY", # The column with country names
                               color_continuous_scale=px.colors.sequential.Plasma,
                               projection="natural earth",
                               title="2014 World GDP")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("World GDP Dashboard"),
    dcc.Graph(id="choropleth-map", figure=choropleth_fig),
    dcc.Graph(id="bar-chart")
])

# Define the callback to update the bar chart based on choropleth map click data
@app.callback(
    Output("bar-chart", "figure"),
    Input("choropleth-map", "clickData")
)
def update_bar_chart(clickData):
    selected_countries = []

    if clickData:
        for point in clickData['points']:
            selected_countries.append(point['hovertext'])

    # Create a bar chart using Plotly Express
    bar_chart_fig = px.bar(df,
                           x="COUNTRY", # The column with country names
                           y="GDP (BILLIONS)", # The column with GDP values
                           title="GDP of Countries in 2014",
                           labels={"GDP (BILLIONS)": "GDP (in Billions)", "COUNTRY": "Country"})

    # Update the layout of the bar chart to limit the y-axis range
    bar_chart_fig.update_layout(yaxis=dict(range=[0, 2000]))

    # Highlight selected countries in red, others in blue
    bar_chart_fig.update_traces(marker=dict(
        color=["red" if country in selected_countries else "blue" for country in df["COUNTRY"]],
        line=dict(color='black', width=1)
    ))

    return bar_chart_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


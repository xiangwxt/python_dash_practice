from dash import Dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd


def plot_altair(xcol):
    spotify = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
    )
    data = spotify.sample(2000)
    data["duration_min"] = data["duration_ms"] / 60000
    chart = (
        alt.Chart(data)
        .mark_rect()
        .encode(
            alt.X(xcol, bin=alt.Bin(maxbins=40)),
            alt.Y("track_popularity", bin=alt.Bin(maxbins=40)),
            alt.Color("count()"),
        )
    )
    return chart.to_html()


app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
app.layout = html.Div(
    [
        "Factors influence song popularity",
        dcc.Dropdown(
            id="xcol",
            options=[
                {"label": "Loudness", "value": "loudness"},
                {"label": "Speechiness", "value": "speechiness"},
                {"label": "Duration(min)", "value": "duration_min"},
            ],
            value="duration_min",
        ),
        html.Iframe(
            id="heatmap",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
    ]
)


@app.callback(Output("heatmap", "srcDoc"), Input("xcol", "value"))
def update_output(xcol):
    return plot_altair(xcol)


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)

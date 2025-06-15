import dash
from dash import html, dcc, Input, Output, callback, register_page
from graph_components.race_year_heatmap import get_race_year_figure

register_page(__name__, path="/race")  # ★ 꼭 있어야 함

race_options = ["white", "southeast_asian", "korean_chinese", "indian", "chinese", "black", "asian"]
year_options = ["2020", "2021", "2022"]  # ✅ 문자열로 변경

layout = html.Div([
    html.H3("인종 대상 공격성 댓글 비율 (히트맵)", style={"textAlign": "center"}),

    html.Div([
        html.Label("인종 필터"),
        dcc.Checklist(
            id="race-filter",
            options=[{"label": r, "value": r} for r in race_options],
            value=race_options,
            inline=True
        ),
        html.Label("연도 필터"),
        dcc.Checklist(
            id="race-year-filter",
            options=[{"label": y, "value": y} for y in year_options],  # ✅ 문자열 라벨
            value=year_options,
            inline=True
        )
    ], style={"width": "60%", "margin": "auto", "marginTop": "20px"}),

    dcc.Graph(id="race-graph")
])

@callback(
    Output("race-graph", "figure"),
    [
        Input("race-filter", "value"),
        Input("race-year-filter", "value")
    ]
)
def update_race_graph(races, years):
    if not years:
        years = year_options
    if not races:
        races = race_options
    years = [str(y) for y in years]  # ✅ 문자열 변환 보장
    return get_race_year_figure(races, years)

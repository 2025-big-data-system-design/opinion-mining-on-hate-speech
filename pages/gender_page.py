import dash
from dash import html, dcc, Input, Output, callback
from graph_components.gender_year_plot import get_gender_year_figure

# 필터 옵션 정의
gender_options = ["male", "female", "feminist", "queer", "others"]
year_options = [2020, 2021, 2022]

# 페이지 등록
dash.register_page(__name__, path="/gender")

layout = html.Div([
    html.H2("성별 대상 공격성 댓글 추이", style={"textAlign": "center"}),

    html.Div([
        html.Label("성별 필터"),
        dcc.Checklist(
            id="gender-filter",
            options=[{"label": g, "value": g} for g in gender_options],
            value=gender_options,
            inline=True
        ),
        html.Label("연도 필터"),
        dcc.Checklist(
            id="gender-year-filter",
            options=[{"label": str(y), "value": y} for y in year_options],
            value=year_options,
            inline=True
        )
    ], style={"width": "60%", "margin": "auto", "marginTop": "20px"}),

    dcc.Graph(id="gender-graph")
])

@callback(
    Output("gender-graph", "figure"),
    Input("gender-filter", "value"),
    Input("gender-year-filter", "value")
)
def update_gender(genders, years):
    if not genders:
        genders = gender_options
    if not years:
        years = year_options
    return get_gender_year_figure(genders, years)

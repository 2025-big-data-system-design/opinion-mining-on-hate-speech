import dash
from dash import html, dcc, Input, Output, callback, register_page
from graph_components.politics_year_pie import get_politics_year_figure

register_page(__name__, path="/politics")

politics_options = ["conservative", "progressive", "others"]
year_options = ["2020", "2021", "2022"]  # ✅ 문자열로 수정

layout = html.Div([
    html.H3("정치 성향 대상 공격성 댓글 추이", style={"textAlign": "center"}),

    html.Div([
        html.Label("정치 성향 필터"),
        dcc.Checklist(
            id="politics-filter",
            options=[{"label": p, "value": p} for p in politics_options],
            value=politics_options,
            inline=True
        ),
        html.Label("연도 필터"),
        dcc.Checklist(
            id="politics-year-filter",
            options=[{"label": y, "value": y} for y in year_options],  # ✅ 라벨 문자열
            value=year_options,
            inline=True
        )
    ], style={"width": "60%", "margin": "auto", "marginTop": "20px"}),

    dcc.Graph(id="politics-graph")
])

@callback(
    Output("politics-graph", "figure"),
    [
        Input("politics-filter", "value"),
        Input("politics-year-filter", "value")
    ]
)
def update_politics_graph(selected_politics, selected_years):
    from module.df.data_loader import get_politics_year_df
    import plotly.express as px

    df = get_politics_year_df()
    df["year"] = df["year"].astype(str)  # ✅ year 열을 문자열로 변환

    if selected_politics:
        df = df[df["politics"].isin(selected_politics)]
    if selected_years:
        selected_years = [str(y) for y in selected_years]  # ✅ 입력값 문자열로 강제
        df = df[df["year"].isin(selected_years)]

    df["percentage"] = df["count"] / df.groupby("year")["count"].transform("sum") * 100

    fig = px.pie(
        df,
        names="politics",
        values="count",
        color="politics",
        facet_col="year",
        title="Comparison of Offensive Comments Based on Political Views by Year",
        color_discrete_map={
            "conservative": "red",
            "progressive": "blue",
            "others": "gray"
        },
        hole=0.3,
        labels={"percentage": "%", "count": "Count"}
    )

    fig.update_traces(textinfo="percent+label")

    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        title_x=0.5,
        legend=dict(
            itemsizing='constant',
            traceorder='normal',
            itemdoubleclick='toggle',
            tracegroupgap=0,
            itemwidth=30
        )
    )

    return fig

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "공격성 댓글 대시보드"

app.layout = html.Div([
    html.H1("공격성 댓글 대시보드", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        dcc.Link("성별 그래프", href="/gender", style={"margin": "10px"}),
        dcc.Link("인종 그래프", href="/race", style={"margin": "10px"}),
        dcc.Link("정치 그래프", href="/politics", style={"margin": "10px"}),
        dcc.Link("공격성 점수 트리맵", href="/offensive", style={"margin": "10px"}),
        dcc.Link("전처리된 그룹 트리맵", href="/target-group", style={"margin": "10px"}),
        dcc.Link("TGT별 점수 분포", href="/score-bin", style={"margin": "10px"})
    ], style={"textAlign": "center"}),

    html.Hr(),

    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)

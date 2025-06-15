import dash
from dash import html, dcc, Output, Input, callback
from graph_components.offensive_score_treemap import get_offensive_score_treemap

dash.register_page(__name__, path="/offensive")

layout = html.Div([
    html.H2("공격성 점수 기반 타겟 그룹 트리맵", style={"textAlign": "center"}),

    html.Div([
        html.P("카테고리 및 서브그룹별 댓글 수와 평균 공격성 점수를 시각화합니다.", style={"textAlign": "center"})
    ], style={"marginTop": "10px"}),

    dcc.Graph(id="offensive-treemap", figure=get_offensive_score_treemap())  # 초기 렌더링
])

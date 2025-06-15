import dash
from dash import html, dcc
from graph_components.target_score_bin_bar import get_target_score_bin_figure

dash.register_page(__name__, path="/score-bin")

layout = html.Div([
    html.H2("TGT별 공격성 점수 분포 (Score Binning)", style={"textAlign": "center"}),

    html.Div([
        html.P("각 타겟 그룹(TGT)에 대해 공격성 점수 구간별로 문서 수를 시각화합니다.", style={"textAlign": "center"})
    ], style={"marginTop": "10px"}),

    dcc.Graph(id="score-bin-graph", figure=get_target_score_bin_figure())  # 초기 렌더링
])

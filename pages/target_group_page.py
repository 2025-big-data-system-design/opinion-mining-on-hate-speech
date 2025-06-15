import dash
from dash import html, dcc
from graph_components.target_group_df_treemap import get_target_group_df_treemap

dash.register_page(__name__, path="/target-group")

layout = html.Div([
    html.H2("카테고리별 타겟 그룹 트리맵", style={"textAlign": "center"}),

    html.Div([
        html.P("카테고리 및 서브그룹별 댓글 수와 공격성 점수를 시각화합니다.", style={"textAlign": "center"})
    ], style={"marginTop": "10px"}),

    dcc.Graph(id="target-group-treemap", figure=get_target_group_df_treemap())  # 초기 렌더링
])

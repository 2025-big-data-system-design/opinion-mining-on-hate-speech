import pandas as pd
import plotly.express as px
from module.df.data_loader import get_target_group_df

def get_target_group_df_treemap():
    # 데이터 로딩
    df = get_target_group_df()

    # 빈 subgroup 제거
    df = df[df['subgroup'].notna()]
    df = df[df['subgroup'].str.strip() != ""]

    # 트리맵 생성
    fig = px.treemap(
        df,
        path=["category", "subgroup"],
        values="count",
        color="offensive_score",
        color_continuous_scale="YlOrRd",
        title="Target Group Treemap (colored by offensive score)",
        hover_data=["count", "offensive_score"]
    )

    fig.update_traces(
        tiling=dict(packing="squarify"),
        textinfo="label+value",
        textfont=dict(size=25)
    )

    fig.update_layout(
        width=1000,
        height=1000,
        margin=dict(t=60, l=20, r=20, b=20),
        title_font_size=20
    )

    return fig

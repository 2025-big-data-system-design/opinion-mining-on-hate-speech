import pandas as pd
import plotly.express as px
import numpy as np
from module.df.data_loader import get_target_score_bin_df

def get_target_score_bin_figure():
    df = get_target_score_bin_df()

    # TGT 정렬
    TGT_order = ["group", "individual", "untargeted", "other"]
    df = df[df["TGT"].isin(TGT_order)].copy()
    df["TGT"] = pd.Categorical(df["TGT"], categories=TGT_order, ordered=True)

    # ✅ bins, labels 다시 정의 (score_bin 컬럼은 이미 들어있다고 가정)
    labels = sorted(df["score_bin"].dropna().unique())
    color_map = px.colors.sequential.RdBu[::-1]
    color_discrete_map = {label: color_map[i] for i, label in enumerate(labels)}

    # ✅ df는 이미 score_bin 별 count가 있으므로 그대로 시각화
    fig = px.bar(
        df,
        x="count",
        y="TGT",
        color="score_bin",
        color_discrete_map=color_discrete_map,
        orientation="h",
        labels={
            "count": "Document Count",
            "TGT": "Target Group (TGT)",
            "score_bin": "Score Range"
        },
        title="Binned Offensive Score Distribution by TGT (Horizontal)"
    )

    fig.update_layout(
        xaxis_title="Document Count (aggregated)",
        yaxis_title="Target (TGT)",
        legend_title="Offensive Score Bin",
        barmode="stack",
        legend=dict(font=dict(size=20)),
        font=dict(size=20)
    )

    return fig

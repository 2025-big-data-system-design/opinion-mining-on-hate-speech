import pandas as pd
import plotly.express as px
import re
from module.db.db_connection import get_collection

def get_offensive_score_treemap():
    collection = get_collection()

    data = []
    pattern = re.compile(r"^(gender|race|politics|religion|others)[-_](.+)$", re.IGNORECASE)

    for doc in collection.find({}, {"GRP": 1, "offensive_score": 1}):
        tg = doc.get("GRP")
        score = doc.get("offensive_score", 0)
        
        if isinstance(tg, str):
            match = pattern.match(tg)
            if match:
                category = match.group(1)
                subgroup = match.group(2)
            else:
                category = "others"
                subgroup = tg

            data.append((category, subgroup, score))

    # DataFrame 변환 및 집계
    df = pd.DataFrame(data, columns=["category", "subgroup", "offensive_score"])
    agg_df = df.groupby(["category", "subgroup"]).agg(
        count=("offensive_score", "count"),
        offensive_score=("offensive_score", "mean")
    ).reset_index()

    # 트리맵 시각화
    fig = px.treemap(
        agg_df,
        path=["category", "subgroup"],
        values="count",
        color="offensive_score",
        color_continuous_scale="YlOrRd",
        title="Target Group Treemap (colored by offensive score)",
        hover_data=["count", "offensive_score"]
    )

    fig.update_traces(
        tiling=dict(packing="squarify"),
        textinfo="label+value"
    )

    fig.update_layout(
        width=1000,
        height=1000,
        margin=dict(t=60, l=20, r=20, b=20),
        uniformtext=dict(minsize=10, mode='hide'),
        title_font_size=20
    )

    return fig

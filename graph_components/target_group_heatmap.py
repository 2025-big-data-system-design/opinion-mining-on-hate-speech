from collections import Counter
import pandas as pd
import plotly.express as px
import re
from module.db.db_connection import get_collection  # get_collection은 DB 연결 함수

def get_target_group_treemap():
    # MongoDB 컬렉션에서 GRP 필드 수집
    collection = get_collection()
    target_groups = []
    for doc in collection.find({}, {"GRP": 1}):
        tg = doc.get("GRP", None)
        if isinstance(tg, str):
            target_groups.append(tg)

    # 정규표현식 분리
    pattern = re.compile(r"^(gender|race|politics|religion|others)[-_](.+)$", re.IGNORECASE)
    data = []
    for tg in target_groups:
        match = pattern.match(tg)
        if match:
            category = match.group(1)
            subgroup = match.group(2)
        else:
            category = "others"
            subgroup = tg
        data.append((category, subgroup))

    # 카운트 계산
    df = pd.DataFrame(data, columns=['category', 'subgroup'])
    df = df.value_counts().reset_index(name='count')

    # 트리맵 생성
    fig = px.treemap(
        df,
        path=['category', 'subgroup'],
        values='count',
        color='count',
        color_continuous_scale='Viridis',
        title='Target Group Treemap',
        hover_data=['count']
    )

    fig.update_traces(
        tiling=dict(packing="squarify"),
        textinfo="label+value"
    )

    fig.update_layout(
        width=800,
        height=800,
        margin=dict(t=60, l=20, r=20, b=20),
        uniformtext=dict(minsize=10, mode='hide'),
        title_font_size=20
    )

    return fig

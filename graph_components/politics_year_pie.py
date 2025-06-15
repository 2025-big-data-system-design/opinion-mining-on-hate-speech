import plotly.express as px
from module.df.data_loader import get_politics_year_df

def get_politics_year_figure():
    # 데이터 로딩
    df = get_politics_year_df()

    # 연도별 총합 구해서 비율 계산
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

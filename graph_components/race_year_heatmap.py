import pandas as pd
import plotly.graph_objects as go
from module.df.data_loader import get_race_year_df

def get_race_year_figure(selected_races=None, selected_years=None):
    df = get_race_year_df()
    df["count"] = df["count"].astype(float)

    # ⛏ None일 경우 전체 race/year 목록 자동 설정
    if selected_races is None:
        selected_races = df["race"].unique().tolist()
    if selected_years is None:
        selected_years = df["year"].unique().tolist()

    df = df[df["race"].isin(selected_races)]
    df = df[df["year"].isin(selected_years)]

    df["percentage"] = df.groupby("year")["count"].transform(lambda x: x / x.sum() * 100)

    z = df.pivot(index="race", columns="year", values="percentage").fillna(0)
    counts = df.pivot(index="race", columns="year", values="count").fillna(0)

    text = pd.DataFrame(index=z.index, columns=z.columns)
    for row in z.index:
        for col in z.columns:
            pct = z.loc[row, col]
            cnt = counts.loc[row, col]
            text.loc[row, col] = f"{row}<br>{pct:.1f}% ({int(cnt)})"

    fig = go.Figure(
        data=go.Heatmap(
            z=z.values,
            x=z.columns,
            y=z.index,
            text=text.values,
            texttemplate="%{text}",
            colorscale="YlOrRd",
            hovertemplate="Year: %{x}<br>Race: %{y}<br>%{z:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        title="Percentage of Offensive Comments by Race per Year",
        xaxis_title="Year",
        yaxis_title="Race",
        title_x=0.5,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig

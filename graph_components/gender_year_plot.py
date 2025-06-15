import plotly.express as px
from module.df.data_loader import get_gender_year_df

def get_gender_year_figure(selected_genders=None, selected_years=None):
    gender_order = ["male", "female", "feminist", "queer", "others"]
    df = get_gender_year_df()

    # ⛏ 연도를 정수로 필터링하기 위해 먼저 int로
    df["year"] = df["year"].astype(int)

    # ✅ 필터링 적용
    if selected_genders:
        df = df[df["gender"].isin(selected_genders)]
    if selected_years:
        df = df[df["year"].isin(selected_years)]

    # ✅ 연도를 다시 문자열로 바꿔서 discrete color 처리
    df["year"] = df["year"].astype(str)
    year_order = sorted(df["year"].unique(), key=int)

    fig = px.bar(
        df,
        x="gender",
        y="count",
        color="year",  # 이제 문자열이므로 discrete 처리됨
        barmode="group",
        text="count",
        title="Offensive Comments Targeting Gender Groups by Year",
        category_orders={"gender": gender_order, "year": year_order}
    )

    fig.update_traces(textposition='outside', texttemplate='%{text}')
    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Count",
        uniformtext_minsize=8,
        yaxis_type="log",
        uniformtext_mode='hide',
        title_x=0.5
    )
    return fig

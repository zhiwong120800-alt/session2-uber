import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.title("DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write("Compare gross agricultural production across countries.")
st.caption("Data source: UN Data Explorer, via Streamlit's tutorial dataset.")

@st.cache_data
def load_data():
    url = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com/agri.csv.gz"
    return pd.read_csv(url).set_index("Region")

try:
    df = load_data()
    countries = st.multiselect(
        "Choose countries",
        options=list(df.index),
        default=["China", "United States of America"],
    )

    if countries:
        selected = df.loc[countries].copy() / 1_000_000
        st.subheader("Gross Agricultural Production ($B)")
        st.dataframe(selected.sort_index())

        long_data = (
            selected.rename_axis("Region")
            .reset_index()
            .melt(id_vars="Region", var_name="year", value_name="production")
        )
        long_data["year"] = pd.to_datetime(
            long_data["year"].astype(str), format="%Y"
        )

        chart = alt.Chart(long_data).mark_area(opacity=0.3).encode(
            x=alt.X("year:T", title="Year"),
            y=alt.Y("production:Q", title="Production ($B)", stack=None),
            color=alt.Color("Region:N", title="Country"),
            tooltip=[
                "Region:N",
                alt.Tooltip("year:T", format="%Y"),
                alt.Tooltip("production:Q", format=".2f"),
            ],
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Select at least one country.")
except URLError as error:
    st.error(f"Could not download data: {error.reason}")

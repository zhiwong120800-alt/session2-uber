import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")
st.title("Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write("Explore geospatial data by switching map layers on and off.")

@st.cache_data
def load_data(filename):
    base = "https://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/"
    return pd.read_json(base + filename)

try:
    bikes = load_data("bike_rental_stats.json")
    stops = load_data("bart_stop_stats.json")
    paths = load_data("bart_path_stats.json")

    layers = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer", bikes,
            get_position=["lon", "lat"],
            radius=200, elevation_scale=4,
            elevation_range=[0, 1000], extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer", stops,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="exits", radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer", stops,
            get_position=["lon", "lat"],
            get_text="name", get_color=[0, 0, 0, 200],
            get_size=15, get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer", paths,
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            get_width="outbound", width_scale=0.0001,
            width_min_pixels=3, width_max_pixels=30,
            auto_highlight=True,
        ),
    }

    st.sidebar.subheader("Map Layers")
    selected = [
        layer for name, layer in layers.items()
        if st.sidebar.checkbox(name, value=True)
    ]

    if selected:
        st.pydeck_chart(pdk.Deck(
            map_provider="carto",
            map_style="light",
            initial_view_state=pdk.ViewState(
                latitude=37.76, longitude=-122.4,
                zoom=11, pitch=50,
            ),
            layers=selected,
        ))
    else:
        st.info("Select at least one map layer.")
except URLError as error:
    st.error(f"Could not download map data: {error.reason}")

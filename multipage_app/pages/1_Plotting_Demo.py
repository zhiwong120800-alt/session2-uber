import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    "Watch a random line chart update over approximately five seconds."
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
data = np.random.randn(1, 1)
chart = st.empty()
chart.line_chart(data)

for i in range(1, 101):
    new_rows = data[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    data = np.concatenate([data, new_rows])
    status_text.text(f"{i}% Complete")
    chart.line_chart(data)
    progress_bar.progress(i)
    time.sleep(0.05)

progress_bar.empty()
st.button("Re-run")

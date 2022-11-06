import streamlit as st
import pandas_datareader as pdr
import plotly.express as px

df = pdr.DataReader("AAPL", "yahoo", start = "2021-01-01", end = "2021-12-31")

st.line_chart(df)
st.plotly_chart(
    px.line(df).update_layout(
        {
            "plot_bgcolor":"#000000",
            "paper_bgcolor":"#000000",
        }
    )
)
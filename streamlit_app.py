# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import text as t
from LP import solve_model
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt


def cli():
    sns.set_theme()
    sns.set(rc={"figure.facecolor": "#353535"})
    st.set_page_config(layout="wide")

    # Reading in / manipulating data
    df = pd.read_csv("24hours.csv")
    df["Solar (MW)"] = df["Solar"]
    df["Price ($/MWh)"] = df["Price"]
    header = st.container()

    with header:
        st.title("Colocated Battery Optimsation")
        st.subheader("Project Intro:")
        st.markdown(t.intro1)
        st.image("stitch.jpg")
        st.markdown(t.intro2)
        st.plotly_chart(
            px.line(
                df,
                x="Hour",
                y=["Solar (MW)", "Price ($/MWh)"],
                line_shape="spline",
                color_discrete_sequence=["salmon", "skyblue"],
                width=900,
                height=500,
                labels={
                    "variable": "Legend",
                    "value": "Value",
                    "Solar": "MW",
                    "Price": "Hour",
                },
            )
            .update_layout(
                {
                    "title_text": "",
                    "plot_bgcolor": "#0E1116",
                    "paper_bgcolor": "#0E1116",
                }
            )
            .update_xaxes(linecolor="#27292E", gridcolor="#27292E")
            .update_yaxes(linecolor="#27292E", gridcolor="#27292E")
        )
        st.markdown(t.intro3)
        st.markdown(t.intro4)

    about_the_model = st.container()
    with about_the_model:
        st.subheader("Building the model:")
        st.markdown("The key to this model is ")

    results = st.container()
    with results:
        if st.button("Solve Model"):
            df_ans, tot, solve_time = solve_model(
                df,
                solar_cap=50,
                wind_cap=0,
                battery_cap=10,
                energy_cap=50,
                grid_cap=10,
                start_charge=0,
            )

            st.header("The model solved!")
            st.markdown(
                f"Optimal Solution found in {round(solve_time,2)} seconds"
            )
            st.markdown(f"Total Profit: ${round(tot, 2)}")
            df_ans["Solar (MW)"] = df_ans["Solar"]
            df_ans["Price ($/MWh)"] = df_ans["Price"]
            df_ans["SOC (MWh)"] = df_ans["SOC"]
            st.plotly_chart(
                px.line(
                    df_ans,
                    x="Hour",
                    y=["Solar (MW)", "Price ($/MWh)", "SOC (MWh)"],
                    line_shape="spline",
                    color_discrete_sequence=["salmon", "skyblue", "green"],
                    width=900,
                    height=500,
                    labels={
                        "variable": "Legend",
                        "value": "Value",
                        "Solar": "MW",
                        "Price": "Hour",
                    },
                )
                .update_layout(
                    {
                        "title_text": "",
                        "plot_bgcolor": "#0E1116",
                        "paper_bgcolor": "#0E1116",
                    }
                )
                .update_xaxes(linecolor="#27292E", gridcolor="#27292E")
                .update_yaxes(linecolor="#27292E", gridcolor="#27292E")
            )

            # st.line_chart(VRE_data)
            # st.line_chart(price_data)


if __name__ == "__main__":
    cli()

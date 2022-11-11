# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import text as t
from LP import solve_model
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def cli():
    sns.set_theme()
    sns.set(rc={'figure.facecolor':'#353535'})
    st.set_page_config(layout="wide")

    # Reading in / manipulating data
    df = pd.read_csv("24hours.csv")
    header = st.container()

    with header:
        st.title("Colocated Battery Optimsation")
        st.subheader("Project Intro:")
        st.markdown(t.intro1)
        st.image("stitch.jpg")
        st.markdown(t.intro2)
        sns.set() 

        # Total bummer you can't stick in axis labels 😅
        pv_col, price_col = st.columns(2)
        with pv_col:
            st.line_chart(df["Solar"])
        with price_col:
            st.line_chart(df["Price"])
        st.markdown(t.intro3)
        st.markdown(t.intro4)

    about_the_model = st.container()
    with about_the_model:
        st.subheader("Building the model:")
        st.markdown("The key to this model is ")

    results = st.container()
    with results:
        next_section = True
        if st.button("Solve Model"):
            df_ans, tot, solve_time = solve_model(
                df,
                solar_cap = 50,
                wind_cap = 0,
                battery_cap = 10,
                energy_cap = 50,
                grid_cap = 10,
                start_charge = 0,
            )

            st.header("The model solved!")
            st.markdown(
                f"Optimal Solution found in {round(solve_time,2)} seconds"
            )
            st.markdown(f"Total Profit: ${round(tot, 2)}")
            VRE_data = df_ans[["SOC", "Solar"]]
            price_data = df_ans["Price"]
            st.line_chart(VRE_data)
            st.line_chart(price_data)


if __name__ == "__main__":
    cli()

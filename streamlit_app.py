# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from LP import solve_model

def run():
    # Reading in / manipulating data
    df = pd.read_csv("solar_battery_data.csv")
    header = st.container()


    with header:
        st.title("Colocated Battery Optimsation")
        st.markdown(
            "This model considers a typical day for a battery storage system co-located with solar panels. The price of electricty changes throughout the day, as does the avaliable solar. Given these variations, what is the most money we can make?"
        )
        st.markdown("The data is shown in 15min intervals for 24 hours:")
        chart_data = df[["Price", "Solar"]]
        st.line_chart(chart_data)


    col1, col2 = st.columns(2)
    with col2:
        solar_cap = st.slider("Solar Capacity (MW)", 10, 50, value=50, step=10)
        battery_cap = st.slider(
            "Battery Capacity (MW DC)", 5, 25, value=10, step=5
        )
        energy_cap = st.slider(
            "Battery Energy Capicty (MWh)", 10, 100, value=40, step=10
        )
        grid_cap = st.slider(
            "Grid Connection Capacity (AC MW)", 10, 100, value=40, step=10
        )  # DC-AC inverter and grid connection capacity (rated in AC MW)
        start_charge = 0.5 * energy_cap

    with col1:
        st.markdown("Now we need to design our battery and PV system:")
        st.markdown(f"- Modelling a {energy_cap} MWh / {battery_cap} MW Battery 🔋")
        st.markdown(f"- Co-located with a {solar_cap} MW PV system ☀️")


    results = st.container()
    with results:
        if st.button("Solve Model"):
            df_ans, tot, solve_time = solve_model(
                df, solar_cap, battery_cap, energy_cap, grid_cap, start_charge
            )

            st.header(f"The model solved! 🥳")
            st.markdown(f"Optimal Solution found in {round(solve_time,2)} seconds")
            st.markdown(f"Total Profit: ${round(tot, 2)}")
            chart_data = df_ans[["Price", "Solar", "SOC"]]
            st.line_chart(chart_data)

if __name__ == "__main__":
    run()
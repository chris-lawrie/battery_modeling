# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import constants as c
from LP import solve_model

def cli():
    # Reading in / manipulating data
    df = pd.read_csv("solar_battery_data.csv")
    header = st.container()


    with header:
        st.title("Colocated Battery Optimsation")
        st.header("Project Intro:")
        st.markdown("Wholesale electricity prices vary through time. As more variable renewable energy is deployed to the grid, the importance of energy storage systems will increase. This project uses optimisation to maximise revenue earned from a battery storage sytem co-located with either wind or solar power!")


        st.markdown(
            "First we'll consider just a single 24 hour period. Lets look at the data we're dealing with. The chart below shows the price of electricty changing throughout the day, as does the avaliable solar power."
        )
        st.markdown("The data is shown in 15min intervals for 24 hours:")
        chart_data = df[["Price", "Solar"]]
        st.line_chart(chart_data)



    st.header("Design a Battery:")
    col1, col2 = st.columns(2)
    with col2:
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
        st.markdown(f"- Co-located with a {c.solar_cap} MW PV system ☀️")


    results = st.container()
    with results:
        if st.button("Solve Model"):
            df_ans, tot, solve_time = solve_model(
                df, c.solar_cap, battery_cap, energy_cap, grid_cap, start_charge
            )

            st.header(f"The model solved! 🥳")
            st.markdown(f"Optimal Solution found in {round(solve_time,2)} seconds")
            st.markdown(f"Total Profit: ${round(tot, 2)}")
            chart_data = df_ans[["Price", "SOC", "Solar"]]
            st.line_chart(chart_data)

if __name__ == "__main__":
    cli()
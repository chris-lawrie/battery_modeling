# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import numpy as np
import pandas as pd
import constants as c
from LP import solve_model

def cli():
    # Reading in / manipulating data
    df = pd.read_csv("8760_data.csv")
    header = st.container()


    with header:
        st.title("Colocated Battery Optimsation")
        st.header("Project Intro:")
        st.markdown("Wholesale electricity prices vary through time. As more variable renewable energy is deployed to the grid, the importance of energy storage systems will increase. This project uses optimisation to maximise revenue earned from a battery storage sytem co-located with either wind or solar power!")


        st.markdown(
            "First explore the data below. It shows representative hourly data for avaliable wind and solar power, as a fraction of the installed capacity. We also have hourly electricity prices."
        )

        st.markdown("Before we can model anything, we should decide the time period to run our model across. If this is your first time, we can stick with the default 24 hours. If you'd like something else, check the box and select.")
        custom= st.checkbox('Custom Time Span')
        if custom:
            sim_length = st.slider("Simulation Length", min_value=24, max_value=8760, value=24, label_visibility="visible")
        else:
            sim_length = 24
        
        pv_wind_data = df[["Wind", "Solar"]].head(sim_length)
        price_data = df[["Price"]].head(sim_length)

        pv_wind_col, price_col = st.columns(2)
        # st.header("Selected data: hour by hour")
        with pv_wind_col:
            st.line_chart(pv_wind_data)
        with price_col:
            st.line_chart(price_data)






        st.header("Design Your System!")
        st.markdown("Now we need to make some decisions on the sizes of our PV, Wind, and Battery Systems.")
        col1, col2 = st.columns(2)
        with col1:
            solar_cap = st.slider(
                "PV system ☀️ (MW)", 10, 100, value=40, step=10
            )

            wind_cap = st.slider(
                "Wind System 💨 (MW)", 50, 200, value=80, step=10
            )

            energy_cap = st.slider(
                "Battery Size 🔋(MWh)", 10, 100, value=40, step=10
            )

            battery_cap = st.slider(
                "Battery Energy Capacity 🔌 (MW DC)", 5, 25, value=10, step=5
            )

            grid_cap = st.slider(
                "Grid Connection Capacity ⚡️ (AC MW)", 10, 100, value=40, step=10
            )  # DC-AC inverter and grid connection capacity (rated in AC MW)
            start_charge = 0.5 * energy_cap

        with col2:
            st.markdown("Here's the cost breakdown for the system you're proposing:")
            st.markdown("<TO DO> - stick in correct prices (just shows sized right now..)")
            bar_chart_data = pd.DataFrame(
            [solar_cap, wind_cap, energy_cap],
            ["Wind", "PV", "Battery"],
            columns=["Cost"])
            st.bar_chart(bar_chart_data)
        
        st.image('stitch.jpg')

    


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
# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from LP import solve_model


def cli():
    # Reading in / manipulating data
    df = pd.read_csv("8760_data.csv")
    header = st.container()

    with header:
        st.title("Colocated Battery Optimsation")
        st.header("Project Intro:")
        st.markdown(
            "Wholesale electricity prices vary through time. As more variable renewable energy is deployed to the grid, the importance of energy storage systems will increase. This project uses optimisation to maximise revenue earned from a battery storage sytem co-located with either wind or solar power!"
        )

        st.markdown(
            "First explore the data below. It shows representative hourly data for avaliable wind and solar power, as a fraction of the installed capacity. We also have hourly electricity prices."
        )

        st.markdown(
            "Before we can model anything, we should decide the time period to run our model across. If this is your first time, we can stick with the default 24 hours. If you'd like something else, check the box and select."
        )
        custom = st.checkbox("Custom Time Span")
        if custom:
            sim_length = st.slider(
                "Simulation Length",
                min_value=24,
                max_value=8760,
                value=24,
                label_visibility="visible",
            )
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


        st.header("Test graph")
        # st.header("Selected data: hour by hour") ############################
        st.plotly_chart(
        px.line(pv_wind_data, color_discrete_sequence = ['lightblue', 'salmon'], width=800, height=400,
        labels={
                     "value": "Avaliable Power",
                     "index": "Hour",
                     "variable": "VRE Source"
                 }).update_layout(
            {
                "title_text":"Plot to show VRE avaliability through time",
                "plot_bgcolor":"#0E1116",
                "paper_bgcolor":"#0E1116",
            }
        ).update_xaxes(linecolor='#27292E', gridcolor='#27292E').update_yaxes(linecolor='#27292E', gridcolor='#27292E')
    )

        st.header("Design Your System!")
        st.markdown(
            "Now we need to make some decisions about what to build."
        )
        include_PV = st.checkbox("Build a PV system")
        include_wind = st.checkbox("Build a wind farm")

        if include_PV and not include_wind:
            st.markdown(
                "Building a battery co-located with a PV system."
            )
        elif not include_PV and include_wind:
            st.markdown(
                "Building a battery co-located with a wind farm."
            )
        elif include_PV and include_wind:
            st.markdown(
                "Building a battery co-located with wind & solar! I don't think this has ever happened in the real world, but hey thats what modeling is for, right? :)"
            )
        else:
            st.markdown(
                "Building a battery which charges/discharges from the grid (no VRE co-location)."
            )

        col1, col2 = st.columns(2)
        with col1:
            solar_cap = 0
            wind_cap = 0

            if include_PV:
                solar_cap = st.slider(
                    "PV system ☀️ (MW)", 10, 100, value=40, step=10
                )

            if include_wind:
                wind_cap = st.slider(
                    "Wind System 💨 (MW)", 50, 200, value=80, step=10
                )

            energy_cap = st.slider(
                "Battery Size 🔋(MWh)", 10, 100, value=40, step=10
            )

            battery_cap = st.slider(
                "Battery Energy Capacity 🔌 (MW DC)",
                5,
                25,
                value=10,
                step=5,
            )

            grid_cap = st.slider(
                "Battery Grid Connection Capacity ⚡️ (AC MW)",
                10,
                100,
                value=40,
                step=10,
            )  # DC-AC inverter and grid connection capacity (rated in AC MW)
            start_charge = 0.5 * energy_cap

        with col2:
            st.markdown(
                "Here's the cost breakdown for the system you're proposing:"
            )
            st.markdown(
                "<TO DO> - stick in correct prices (just shows sized right now, incorrectly labeles )"
            )
            bar_chart_data = pd.DataFrame(
                [solar_cap, wind_cap, energy_cap],
                ["PV", "Wind", "Battery"],
                columns=["Cost"],
            )
            st.bar_chart(bar_chart_data)
        st.subheader("<TO DO> stick in rough circuit diagram...")
        st.image("stitch.jpg")

    results = st.container()
    with results:
        if st.button("Solve Model"):
            df_ans, tot, solve_time = solve_model(
                df.head(sim_length),
                solar_cap,
                wind_cap,
                battery_cap,
                energy_cap,
                grid_cap,
                start_charge,
            )

            st.header("The model solved!")
            st.markdown(
                f"Optimal Solution found in {round(solve_time,2)} seconds"
            )
            st.markdown(f"Total Profit: ${round(tot, 2)}")
            VRE_data = df_ans[["SOC", "Solar", "Wind"]]
            price_data = df_ans["Price"]
            st.line_chart(VRE_data)
            st.line_chart(price_data)


if __name__ == "__main__":
    cli()

# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from LP import solve_model


def make_line_chart(df_arg, x_arg, y_arg, cols, title=""):
    st.plotly_chart(
        px.line(
            df_arg,
            x=x_arg,
            y=y_arg,
            color_discrete_sequence=cols,
            width=900,
            height=350,
            labels={
                "variable": "Legend",
                "value": "MW",
                "Solar": "MW",
                "Price": "Hour",
            },
        )
        .update_layout(
            {
                "title_text": title,
                "plot_bgcolor": "#0E1116",
                "paper_bgcolor": "#0E1116",
            }
        )
        .update_xaxes(linecolor="#27292E", gridcolor="#27292E")
        .update_yaxes(linecolor="#27292E", gridcolor="#27292E")
    )


def make_avg_chart(df_arg, x_arg, y_arg, color, title=""):
    st.plotly_chart(
        px.line(
            df_arg,
            x=x_arg,
            y=y_arg,
            width=550,
            height=300,
            color_discrete_sequence=[color],
            labels={
                "variable": "Legend",
                "value": "MW",
                "Solar": "MW",
                "Price": "Hour",
            },
        )
        .update_layout(
            {
                "title_text": f"Average Day - {title}",
                "plot_bgcolor": "#0E1116",
                "paper_bgcolor": "#0E1116",
            }
        )
        .update_xaxes(linecolor="#27292E", gridcolor="#27292E")
        .update_yaxes(linecolor="#27292E", gridcolor="#27292E")
        .update(layout_showlegend=False)
    )


def cli():
    st.set_page_config(layout="wide")

    # Reading in / manipulating data
    df = pd.read_csv("8760_data.csv")
    header = st.container()

    with header:
        st.title("Customise the Model!")
        st.markdown(
            "Now we're familiar with the basic concepts - we can do some customisation. We'll now have the ability to choose if we want to co-locate with wind or solar, or both, or neither (we're modeling, who cares if its realistic 😄). You also have full control over the length of time for the simulation (up to 1 yr), and can play around with all the assumptions made on the first page. As before, here's a rough circuit diagram of the sysem we're modeling (which now includes the option of wind generation:"
        )

        st.image("diagram2.jpg")

        st.header("Design Your System!")
        st.markdown(
            "Now we need to make some decisions about what to build, and how long we should run the simulation."
        )
        st.info(
            "Setting PV and/or Wind size = 0 removes them from the model! ☀️"
        )

        col1, col2 = st.columns(2)

        with col1:
            solar_cap = 0
            wind_cap = 0

            solar_cap = st.number_input(
                "PV system ☀️ (MW)", 0, 100, value=30, step=10
            )

            wind_cap = st.number_input(
                "Wind System 💨 (MW)", 0, 200, value=10, step=10
            )

            sim_length_days = st.slider(
                "Simulation Length - Days",
                min_value=1,
                max_value=365,
                value=7,
                label_visibility="visible",
            )
            sim_length = sim_length_days * 24

        with col2:
            energy_cap = st.number_input(
                "Battery Size 🔋(MWh)", 10, 100, value=40, step=10
            )

            battery_cap = st.number_input(
                "Battery Energy Capacity 🔌 (MW DC)", 1, 25, value=10, step=5,
            )

            grid_cap = st.number_input(
                "Battery Grid Connection Capacity ⚡️ (AC MW)",
                1,
                100,
                value=10,
                step=10,
            )  # DC-AC inverter and grid connection capacity (rated in AC MW)
            start_charge = 0.5 * energy_cap

        df["Wind"] = df["Wind"] * wind_cap
        df["Solar"] = df["Solar"] * solar_cap

        avgs = []
        Hours = df.Hour.unique()
        df_avg = df.head(sim_length)

        for hour in Hours:
            avgs.append(
                {
                    "Hour": hour,
                    "Avg. Solar": df_avg.loc[
                        df_avg["Hour"] == hour, "Solar"
                    ].mean(),
                    "Avg. Wind": df_avg.loc[
                        df_avg["Hour"] == hour, "Wind"
                    ].mean(),
                }
            )

        avgs = pd.DataFrame(avgs)

        col1, col2 = st.columns(2)
        with col1:
            make_avg_chart(avgs, "Hour", ["Avg. Solar"], "salmon", "Solar")

        with col2:
            make_avg_chart(avgs, "Hour", ["Avg. Wind"], "lightgreen", "Wind")

        make_line_chart(
            df.head(sim_length),
            "T",
            ["Wind", "Solar"],
            ["lightgreen", "salmon"],
            "Avaliable VRE Power through time:",
        )

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
            df_ans["Solar (MW)"] = df_ans["Solar"]
            df_ans["Wind (MW)"] = df_ans["Wind"]
            df_ans["Price ($/MWh)"] = df_ans["Price"]
            df_ans["SOC (MWh)"] = df_ans["SOC"]
            df_ans["Import (MW)"] = df_ans["IMP"]
            df_ans["Export (MW)"] = df_ans["EXP"]

            make_line_chart(
                df_ans,
                "T",
                ["Price ($/MWh)", "SOC (MWh)"],
                ["skyblue", "green"],
                "Optimal Solution - Price and SOC through time",
            )
            make_line_chart(
                df_ans,
                "T",
                ["Import (MW)", "Export (MW)"],
                ["red", "blue"],
                "Optimal Solution - Import/Export through time",
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="Solve Time:", value=f"{round(solve_time,2)} s"
                )

            with col2:
                st.metric(label="Total Revenue", value=f"${round(tot)}")

            with col3:
                st.metric(
                    label="Avg Daily Revenue",
                    value=f"${round(tot/sim_length_days)}",
                )


if __name__ == "__main__":
    cli()

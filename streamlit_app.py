# To launch dashboard, in terminal -> streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import text as t
from LP import solve_model


def cli():
    st.set_page_config(layout="wide")

    # Reading in / manipulating data
    df = pd.read_csv("8760_data.csv")
    header = st.container()

    with header:
        st.title("Colocated Battery Optimsation")
        st.subheader("Project Intro:")
        st.markdown(t.intro1)
        st.image("stitch.jpg")
        st.markdown(t.intro2)

        sim_length = 24
        pv_wind_data = df[["Solar"]].head(sim_length)
        price_data = df[["Price"]].head(sim_length)

        pv_wind_col, price_col = st.columns(2)
        with pv_wind_col:
            st.line_chart(pv_wind_data)
        with price_col:
            st.line_chart(price_data)
        st.markdown(t.intro3)
        st.markdown(t.intro4)

    next_section = st.button("Let's build the model:")
    about_the_model = st.container()

    if next_section:
        with about_the_model:
            st.subheader("Building the model:")
            st.markdown("The key to this model is ")

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

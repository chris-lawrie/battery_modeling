# To launch dashboard, in terminal -> streamlit run streamlit_app.py
from LP import solve_model
import text as t
import streamlit as st
import pandas as pd
import plotly.express as px


def make_line_chart(df_arg, x_arg, y_arg, cols):
    st.plotly_chart(
        px.line(
            df_arg,
            x=x_arg,
            y=y_arg,
            line_shape="spline",
            color_discrete_sequence=cols,
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


def cli():
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
        st.image("diagram.jpg")
        st.markdown(t.intro2)
        make_line_chart(
            df, "Hour", ["Solar (MW)", "Price ($/MWh)"], ["salmon", "skyblue"]
        )

        st.markdown(t.intro3)
        st.markdown(t.intro4)

    about_the_model = st.container()
    with about_the_model:
        st.subheader("Solving the problem:")
        st.markdown(
            "Before getting into the optimal solution - let's get a sense of how much revenue we can generate without using the battery."
        )
        st.info(
            "If we just sold as much solar power as we could when we generate it, we would make $1374. We will call this the **base scenario**."
        )
        # st.subheader("Let's build the model:")
        # st.markdown("We won't dive deeply into the weeds of linear programming - but we should still make clear how the model actually works.")
        # st.markdown("To build any linear program, we need to figure out our Objective Function. That is, the thing we want to maximise or minimise. In this case, we want to maximise the revneue earned by our battery and PV system. We lose money when we buy electricity, and we earn money when we sell electricity. Quite simply, then, our objective function is:")
        # st.latex(
        #     r"""
        # \begin{aligned}
        # \max \sum_{t \in T} (GridExport_t - GridImport_t) \times Price_t \quad \\[6pt]
        # \end{aligned} """
        # )
        # st.markdown("Where $GridExport_t$ and $GridImport_t$ represent the electricity we have bought/sold at some time $t$.")
        # st.markdown("Now - we need to account for the constraints of our system. For instance, our PV system cannot generate more than the given profile allows for any time $t$. Other notable constraints include ensuring energy balance at all times between what is being imported/exported/generated/charged/discharge (no free energy!), accounting for power ratings in connection equipment (e.g. 10 MW lines can only transfer so much energy in an hour), and making sure we constrain our variables to be positive. Some example constrains for our $Solar_t$ variable are:")
        # st.latex(
        #     r"""Solar_t  ≤ time\_series.Solar_t  \quad \forall t \in T  \quad \\[6pt]"""
        # )
        # st.latex(
        #     r"""Solar_t  ≥ 0  \quad \forall t \in T  \quad \\[6pt]"""
        # )

        # st.markdown("To see the full set of constraints and model code, please see the _'How The Model Works'_ page. Choosing the correct constraints is one of the trickiest, and most artful, parts of building optimisation models.")
        # st.markdown("With all aspects accounted for - let's solve the model!")

    results = st.container()
    with results:
        if st.button("Solve Model"):
            df["Solar"] = df["Solar"]
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

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Solve Time:", value=f"{round(solve_time, 2)} s"
                )

            with col2:
                st.metric(
                    label="Total Revenue",
                    value=f"${round(tot)}",
                    delta=f"{round(100*((tot/ 1374) - 1))}% compared to base scenario",
                )

            df_ans["Solar (MW)"] = df_ans["Solar"]
            df_ans["Price ($/MWh)"] = df_ans["Price"]
            df_ans["SOC (MWh)"] = df_ans["SOC"]
            df_ans["Import (MW)"] = df_ans["IMP"]
            df_ans["Export (MW)"] = df_ans["EXP"]

            st.markdown(
                "The chart below shows the SOC of the battery relative to the PV output and price variations:"
            )
            make_line_chart(
                df_ans,
                "Hour",
                ["Solar (MW)", "Price ($/MWh)", "SOC (MWh)"],
                ["salmon", "skyblue", "green"],
            )

            st.markdown(
                "We can see two distinct peaks for the battery's state of charge. It imports power from the grid when the prices are very low, and starts to sell off that power as the prices rise. We can then see it appears to charge from the PV generation in the middle of the day, saving that power until later in the evening. Cool!!"
            )
            st.markdown(
                "Since we went to the trouble of writing a complete model we can also compare $GridImport_t$, $GridExpor_tt$ against the $Price_t$ to see if we can spot any interesting behaviour: "
            )
            make_line_chart(
                df_ans,
                "Hour",
                ["Import (MW)", "Export (MW)", "Price ($/MWh)"],
                ["red", "blue", "skyblue"],
            )
            st.markdown(
                "We can see that we don't import energy except for at the begining of the day, and that more or less continuously export energy whilst the prices are high. This charts also betrays the 10 MW power limit built into the model. We can imagine that if all else was held the same, and this limit increased, we might be able to genereat higher revenue. Feel free to play around with this feature (any many others!) in the _Customise Model_ page."
            )


if __name__ == "__main__":
    cli()

import streamlit as st

header = st.container()
with header:
    st.header("Notes on the model")
    st.warning("Scroll down to see the code", icon="⬇")
    st.markdown(
        "At its core, this model is just a [linear program](https://en.wikipedia.org/wiki/Linear_programming). At every timestep, we want our model to tell us how much power we should import/export from the grid, how we should operate our battery, and how we should direct (or curtail) our solar/wind power. For each timestep we will need decision variables to keep track each one of these things. These variables are shown in the diagram below:"
        )
    st.image("diagram3.jpg")
    st.markdown("The objective function maximises revenue, and at any given time only needs to consider electricity price and grid import/export. It is simply defined as:")
    st.latex(
        r"""
    \begin{aligned}
    \max \sum_{t \in T} (GridExport_t - GridImport_t) \times Price_t \quad \\[6pt] 
    \end{aligned} """
    )

    st.markdown("As in any optimisation problem, we need to constrain this objective function in a way that reflects what we are trying to model. First we can constrain the PV/Wind production so we don't exceed the user-specified production limit, nor allow them to be negative (they're not allowed to _use_ energy).")
    st.latex(
        r"""
    \begin{aligned}
    Solar_t  \leq time\_series.Solar_t  \quad \forall t \in T  \quad \\[6pt]
    Wind_t  \leq time\_series.Wind_t  \quad \forall t \in T  \quad \\[6pt]
    Solar_t, \; Wind_t \geq 0  \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )
    
    st.markdown("Likewise, we need to constrain the energy flowing in/out of the battery to be within the specified energy capacity. We should also keep track of the state of charge (SOC) of the battery, so we don't exceed the specified energy capicity. This is where we can account for the battery charge/discharging efficiency.")
    st.latex(
        r"""
    \begin{aligned}
    Charge_t     \leq battery\_cap      \quad \forall t \in T  \quad \\[6pt]
    Discharge_t    \leq battery\_cap    \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )

    st.latex(
        r"""
    \begin{aligned}
    SOC_{0} = start\_charge + \big(Charge_0 * battery\_eff - \frac{Discharge_0}{battery\_eff}\big) \quad \\[6pt]
    SOC_t = SOC_{t-1} + \big(Charge_t * battery\_eff - \frac{Discharge_t}{battery\_eff}\big) \quad \forall t \in T > 0 \quad \\[6pt]
    \end{aligned} """
    )


    st.latex(
        r"""
    \begin{aligned}
    SOC_t    \leq energy\_cap  \quad \forall t \in T  \quad \\[6pt]
    Charge_t, \; Discharge_t, \; SOC_t \geq 0 \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )
   
   
    st.markdown("We also need to constrain the energy flowing in/out of the whole system into/out of the grid, to be within the specified grid capacity.")
    st.latex(
        r"""
    \begin{aligned}
    GridExport_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    GridImport_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    GridExport_t, \; GridImport_t \geq 0  \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )



    st.markdown("Finally we need to ensure energy ballance at all times. The sum of energy produced from our VRE and battery (net solar + wind + storage) should equal the energy we are exporting to the grid (net export) at all times, so there is no free energy. Note that the net export can be negative (i.e importing energy), and the net solar + wind + storage export can also be negative (i.e. charging the battery). This stage is where we account for inverter losses:")
    st.latex(
        r"""
    \begin{aligned}
    NetSolarWindStorage_t = Solar_t + Wind_t + Discharge_t - Charge_t \quad \forall t \in T \quad\\[6pt]
    NetExport_t = \frac{GridExport_t}{inverter\_eff} - GridImport_t \times inverter\_eff \quad \forall t \in T \quad \\[6pt]
    NetSolarStorage_t = eNetExport_t \quad \forall t \in T \quad \\[6pt]
    \end{aligned} """
    )

    st.markdown("With everything defined, all that remains is to code the problem into your language of choice, and run it! Below is the code for this project in python.")
    

code = st.container()
with code:
    st.header("Code:")
    st.markdown("Below is the guts of the linear program. ")
    st.code(
        r"""    
import pandas as pd
import pulp as p
import time
import constants as c


def solve_model(
    df: pd.DataFrame,
    solar_cap: int,
    wind_cap: int,
    battery_cap: int,
    energy_cap: int,
    grid_cap: int,
    start_charge: int,
):

    start = time.time()

    df["Solar"] = df["Solar"]
    df["Wind"] = df["Wind"]

    T = df.shape[0]
    model = p.LpProblem("Model", p.LpMaximize)
    print("model created!")

    # Initialise arrays to hold variables for each time step
    solar = [None] * T
    wind = [None] * T
    charge = [None] * T
    discharge = [None] * T
    grid_export = [None] * T
    grid_import = [None] * T
    soc = [None] * T
    objective = [None] * T

    # Create varliables ∀ t in T
    for t in range(T):
        solar[t] = p.LpVariable(f"solar_{t}", lowBound=0, upBound=solar_cap)
        wind[t] = p.LpVariable(f"wind_{t}", lowBound=0, upBound=wind_cap)

        charge[t] = p.LpVariable(
            f"charge_{t}", lowBound=0, upBound=battery_cap
        )
        discharge[t] = p.LpVariable(
            f"discharge_{t}", lowBound=0, upBound=battery_cap
        )
        grid_export[t] = p.LpVariable(
            f"grid_export_{t}", lowBound=0, upBound=grid_cap
        )
        grid_import[t] = p.LpVariable(
            f"grid_import_{t}", lowBound=0, upBound=grid_cap
        )
        soc[t] = p.LpVariable(f"soc_{t}", lowBound=0, upBound=energy_cap)

    # Create Objective function and constraints ∀ t in T
    for t in range(T):
        objective[t] = (grid_export[t] - grid_import[t]) * df.Price[t]
        model += (solar[t] + wind[t] + discharge[t] - charge[t]) == (
            grid_export[t] * (1 / c.INVERTER_EFF)
            - grid_import[t] * c.INVERTER_EFF
        )
        model += solar[t] <= df.Solar[t]
        model += wind[t] <= df.Wind[t]
        if t == 0:
            model += soc[t] == (
                start_charge
                + (
                    charge[t] * c.BATTERY_EFF
                    - discharge[t] * (1 / c.BATTERY_EFF)
                )
            )
        else:
            model += soc[t] == (
                soc[t - 1]
                + (
                    charge[t] * c.BATTERY_EFF
                    - discharge[t] * (1 / c.BATTERY_EFF)
                )
            )

    model += sum(objective)
    status = model.solve()

    # Process results 
    ans_soc = [None] * T
    ans_objective = [None] * T
    ans_IMP = [None] * T
    ans_EXP = [None] * T

    for t in range(T):
        ans_soc[t] = p.value(soc[t])
        ans_objective[t] = p.value(objective[t])
        ans_IMP[t] = p.value(grid_import[t])
        ans_EXP[t] = p.value(grid_export[t])

    df["SOC"] = ans_soc
    df["IMP"] = ans_IMP
    df["EXP"] = ans_EXP

    end = time.time()
    solve_time = end - start
    return (df, sum(ans_objective), solve_time)
"""
    )

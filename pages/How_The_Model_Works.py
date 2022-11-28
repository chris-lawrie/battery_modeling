import streamlit as st

header = st.container()
with header:
    st.header("Notes on the model")
    st.warning("Scroll down to see the code", icon="⬇")
    st.markdown(
        "At its core, this model is just a linear program. The objective function maximises the total revenue over the given time period, and is defined as:"
    )
    st.latex(
        r"""
    \begin{aligned}
    \max \sum_{t \in T} (GridExport_t - GridImport_t) \times Price_t \quad \\[6pt] 
    \end{aligned} """
    )

    st.markdown("Subject to the following constraints:")
    st.latex(
        r"""
    \begin{aligned}
    NetSolarWindStorage_t = Solar_t + Wind_t + Discharge_t - Charge_t \quad \forall t \in T \quad\\[6pt]
    NetExport_t = \frac{GridExport_t}{inverter\_eff} - GridImport_t \times inverter\_eff \quad \forall t \in T \quad \\[6pt]
    NetSolarStorage_t = eNetExport_t \quad \forall t \in T \quad \\[6pt]
    SOC_{0} = start\_charge + \big(Charge_0 * battery\_eff - \frac{Discharge_0}{battery\_eff}\big) \quad \\[6pt]
    SOC_t = SOC_{t-1} + \big(Charge_t * battery\_eff - \frac{Discharge_t}{battery\_eff}\big) \quad \forall t \in T > 0 \quad \\[6pt]
    Solar_t  \leq time\_series.Solar_t  \quad \forall t \in T  \quad \\[6pt]
    Wind_t  \leq time\_series.Wind_t  \quad \forall t \in T  \quad \\[6pt]
    Charge_t     \leq battery\_cap      \quad \forall t \in T  \quad \\[6pt]
    Discharge_t    \leq battery\_cap    \quad \forall t \in T  \quad \\[6pt]
    SOC_t    \leq energy\_cap           \quad \forall t \in T  \quad \\[6pt]
    GridExport_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    GridImport_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )

code = st.container()
with code:
    st.header("Code:")
    st.markdown("Below is the guts of the linear program. ")
    st.code(
        r"""    
import pulp as p
import pandas as pd

df = pd.read_csv("solar_battery_data.csv")
start = time.time()

df["Solar"] = df["Solar"] * solar_cap
df["Wind"] = df["Wind"] * wind_cap

T = df.shape[0]
model = p.LpProblem("Model", p.LpMaximize)

# Initialise arrays to hold variables for each time step
SOLAR = [None] * T
WIND = [None] * T
CHARGE = [None] * T
DISCHARGE = [None] * T
GRIDEXPORT = [None] * T
GRIDIMPORT = [None] * T
SOC = [None] * T
OBJ = [None] * T

# Create varliables ∀ t in T
for t in range(T):
    SOLAR[t] = p.LpVariable(f"SOLAR_{t}", lowBound=0, upBound=solar_cap)
    WIND[t] = p.LpVariable(f"WIND_{t}", lowBound=0, upBound=wind_cap)

    CHARGE[t] = p.LpVariable(
        f"CHARGE_{t}", lowBound=0, upBound=battery_cap
    )
    DISCHARGE[t] = p.LpVariable(
        f"DISCHARGE_{t}", lowBound=0, upBound=battery_cap
    )
    GRIDEXPORT[t] = p.LpVariable(
        f"GRIDEXPORT_{t}", lowBound=0, upBound=grid_cap
    )
    GRIDIMPORT[t] = p.LpVariable(
        f"GRIDIMPORT_{t}", lowBound=0, upBound=grid_cap
    )
    SOC[t] = p.LpVariable(f"SOC_{t}", lowBound=0, upBound=energy_cap)

# Create Objective function and constraints ∀ t in T
for t in range(T):
    OBJ[t] = (GRIDEXPORT[t] - GRIDIMPORT[t]) * df.Price[t]
    model += (SOLAR[t] + WIND[t] + DISCHARGE[t] - CHARGE[t]) == (
        GRIDEXPORT[t] * (1 / c.inverter_eff)
        - GRIDIMPORT[t] * c.inverter_eff
    )
    model += SOLAR[t] <= df.Solar[t]
    model += WIND[t] <= df.Wind[t]
    if t == 0:
        model += SOC[t] == (
            start_charge
            + (
                CHARGE[t] * c.battery_eff
                - DISCHARGE[t] * (1 / c.battery_eff)
            )
        )
    else:
        model += SOC[t] == (
            SOC[t - 1]
            + (
                CHARGE[t] * c.battery_eff
                - DISCHARGE[t] * (1 / c.battery_eff)
            )
        )

model += sum(OBJ)

status = model.solve()
ans_SOC = [None] * T
ans_OBJ = [None] * T

for t in range(T):
    ans_SOC[t] = p.value(SOC[t])
    ans_OBJ[t] = p.value(OBJ[t])

df["SOC"] = ans_SOC

end = time.time()
solve_time = end - start"""
    )

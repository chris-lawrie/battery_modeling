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

    print("LP Solving:")
    status = model.solve()
    print(f"LP Status = {status}")

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

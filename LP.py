import pandas as pd
import streamlit as st
import numpy as np
import pulp as p
import time

import constants as c


def solve_model(
    df: pd.DataFrame,
    solar_cap: int,
    battery_cap: int,
    energy_cap: int,
    grid_cap: int,
    start_charge: int,
):

    start = time.time()

    T = df.shape[0]
    model = p.LpProblem("Model", p.LpMaximize)

    # Initialise arrays to hold variables for each time step
    SOLAR = [None] * T
    CHARGE = [None] * T
    DISCHARGE = [None] * T
    GRIDEXPORT = [None] * T
    GRIDIMPORT = [None] * T
    SOC = [None] * T
    OBJ = [None] * T

    # Create varliables ∀ t in T
    for t in range(T):
        SOLAR[t] = p.LpVariable(f"SOLAR_{t}", lowBound=0, upBound=solar_cap)
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
        OBJ[t] = (GRIDEXPORT[t] - GRIDIMPORT[t]) * df.Price[t] * 0.25
        model += (SOLAR[t] + DISCHARGE[t] - CHARGE[t]) == (
            GRIDEXPORT[t] * (1 / c.inverter_eff)
            - GRIDIMPORT[t] * c.inverter_eff
        )
        model += SOLAR[t] <= df.Solar[t]
        if t == 0:
            model += SOC[t] == (
                start_charge
                + (
                    CHARGE[t] * c.battery_eff
                    - DISCHARGE[t] * (1 / c.battery_eff)
                )
                * 0.25
            )
        else:
            model += SOC[t] == (
                SOC[t - 1]
                + (
                    CHARGE[t] * c.battery_eff
                    - DISCHARGE[t] * (1 / c.battery_eff)
                )
                * 0.25
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
    solve_time = end - start
    return (df, sum(ans_OBJ), solve_time)

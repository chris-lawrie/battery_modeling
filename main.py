import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Reading in / manipulating data 
df = pd.read_csv("solar_battery_data.csv")
latex = """
        $
        {\scriptstyle\begin{align*}
        & \max \sum_{t \in T} (GRIDEXPORT_t - GRIDIMPORT_t) \times Price_t \times 0.25 && \text{Objective function (revenue)}\\[6pt] 
        & \text{s.t.} && \\[6pt]
        & eNetSolarStorage_t = SOLAR_t + DISCHARGE_t - CHARGE_t & \forall t \in T &\quad \text{Net solar and storage production (DC MW)} \\[6pt]
        & eNetExport_t = \frac{GRIDEXPORT_t}{inverter\_eff} - GRIDIMPORT_t \times inverter\_eff & \forall t \in T &\quad \text{Net grid interchange (DC MW)} \\[6pt]
        & eNetSolarStorage_t = eNetExport_t  & \forall t \in T &\quad \text{Energy balance constraint} \\[6pt]
        & SOC_1 = start\_charge + 0.25 \big(CHARGE_1 * battery\_eff - \frac{DISCHARGE_1}{battery\_eff}\big)  & &\\[6pt]
        & SOC_t = SOC_{t-1} + 0.25 \big(CHARGE_t * battery\_eff - \frac{DISCHARGE_t}{battery\_eff}\big)  & \forall t \in T \text{ & } t > 1 &\quad \text{State of charge constraints}\\[6pt]
        & SOLAR_t  \leq time\_series.Solar_t     &\forall t \in T & \quad \text{Solar PV capacity constraints}\\[6pt]
        & CHARGE_t     \leq battery\_cap         &\forall t \in T & \quad \text{Charge capacity constraints}\\[6pt]
        & DISCHARGE_t    \leq battery\_cap      &\forall t \in T & \quad \text{Discharge capacity constraints}\\[6pt]
        & SOC_t    \leq energy\_cap             &\forall t \in T & \quad \text{State of charge capacity constraints}\\[6pt]
        & GRIDEXPORT_t    \leq grid\_cap      &\forall t \in T & \quad \text{Grid capacity constraint (exports)}\\[6pt]
        & GRIDIMPORT_t    \leq grid\_cap             &\forall t \in T & \quad \text{Grid capacity constraint (imports)}\\[6pt]
        & SOLAR_t, CHARGE_t, DISCHARGE_t, &&\\
        & SOC_t, GRIDEXPORT_t, GRIDIMPORT_t, \geq 0 &\forall t \in T & \quad \text{Non-negativity constraints}\\[6pt]
        \end{align*}}
        $
        """

 
header = st.container() 

with header:
    st.write(df.Solar.head())
    st.title("Battery Arbitrage Calculator!")
    chart = st.line_chart(data = df, x = "T", y = "Price", use_container_width = True)
    chart.add_rows(df.Solar)


    st.markdown("Here's some maths!")
    st.latex(r'''
    \begin{align*} 
    \max \sum_{t \in T} (GRIDEXPORT_t - GRIDIMPORT_t) \times Price_t \times 0.25 \\[1pt] 
    \text{s.t.} \\[6pt]
    eNetSolarStorage_t = SOLAR_t + DISCHARGE_t - CHARGE_t \quad \forall t \in T \quad\\[6pt]
    eNetExport_t = \frac{GRIDEXPORT_t}{inverter\_eff} - GRIDIMPORT_t \times inverter\_eff \quad \forall t \in T \quad \\[6pt]
    eNetSolarStorage_t = eNetExport_t  \forall t \in T \quad \\[6pt]
    SOC_t = SOC_{t-1} + 0.25 \big(CHARGE_t * battery\_eff - \frac{DISCHARGE_t}{battery\_eff}\big) \quad \forall t \in T t > 1 \quad\\[6pt]
    SOLAR_t  \leq time\_series.Solar_t  \quad \forall t \in T  \quad \\[6pt]
    CHARGE_t     \leq battery\_cap      \quad \forall t \in T  \quad \\[6pt]
    DISCHARGE_t    \leq battery\_cap    \quad \forall t \in T  \quad \\[6pt]
    SOC_t    \leq energy\_cap           \quad \forall t \in T  \quad \\[6pt]
    GRIDEXPORT_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    GRIDIMPORT_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    \end{align*} 
    ''')
    st.subheader("Ok - here is the .csv file")
    st.write(df.head(10))       
    # st.line_chart(data = df, x = "T", y = "Solar")

# with animation: 
#     progress_bar = st.progress(0)
    # status_text = st.empty()
    # chart = st.line_chart(np.random.randn(10, 2))

# for i in range(100):
#     # Update progress bar.
#     progress_bar.progress(i + 1)

#     new_rows = np.random.randn(10, 2)

#     # Update status text.
#     status_text.text(
#         'The latest random number is: %s' % new_rows[-1, 1])

#     # Append data to the chart.
#     chart.add_rows(new_rows)

#     # Pretend we're doing some computation that takes time.
#     time.sleep(0.1)

# status_text.text('Done!')


# st.subheader("Ok - here is the .csv file")
# st.write(df.head())
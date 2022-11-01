import streamlit as st

header = st.container()

with header:
    st.header("Notes on the model")
    st.markdown(
        "At its core, this model is just a linear program. The objective function maximises the total revenue over the given time period, and is defined as:"
    )
    st.latex(
        r"""
    \begin{aligned}
    \max \sum_{t \in T} (GRIDEXPORT_t - GRIDIMPORT_t) \times Price_t \times 0.25 \quad \\[6pt] 
    \end{aligned} """
    )

    st.markdown("Subject to the following constraints:")
    st.latex(
        r"""
    \begin{aligned}
    eNetSolarStorage_t = SOLAR_t + DISCHARGE_t - CHARGE_t \quad \forall t \in T \quad\\[6pt]
    eNetExport_t = \frac{GRIDEXPORT_t}{inverter\_eff} - GRIDIMPORT_t \times inverter\_eff \quad \forall t \in T \quad \\[6pt]
    eNetSolarStorage_t = eNetExport_t \quad \forall t \in T \quad \\[6pt]
    SOC_t = SOC_{t-1} + 0.25 \big(CHARGE_t * battery\_eff - \frac{DISCHARGE_t}{battery\_eff}\big) \quad \forall t \in T \quad \\[6pt]
    SOLAR_t  \leq time\_series.Solar_t  \quad \forall t \in T  \quad \\[6pt]
    CHARGE_t     \leq battery\_cap      \quad \forall t \in T  \quad \\[6pt]
    DISCHARGE_t    \leq battery\_cap    \quad \forall t \in T  \quad \\[6pt]
    SOC_t    \leq energy\_cap           \quad \forall t \in T  \quad \\[6pt]
    GRIDEXPORT_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    GRIDIMPORT_t    \leq grid\_cap      \quad \forall t \in T  \quad \\[6pt]
    \end{aligned} """
    )

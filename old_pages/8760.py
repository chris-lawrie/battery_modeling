import streamlit as st

header = st.container()

with header:
    st.header("Solving For 1 Year")
    st.markdown("The single day model is a nice example - but since we've gone to the trouble of writing an LP Solver, we might as well flex its' muscles a bit.")
    st.markdown("The data below shows hourly variation in prices across a whole year. It also shows avaliable wind and solar power (hourly) across the same period.")
    st.markdown("Whilst these are mock data, this approach could be used in the real world WLOG. This model also assumes perfect knowledge of prices and VRE power. In reality we'd need to project prices and variablilty in some cofidence interval - but that just means solving this model a few times with different inputs.")


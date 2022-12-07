# battery_modelling

## Welcome
Hello there! 👋 This is the code for my battery arbitrage model! 

To see the code in action - check it out [here](https://chris-lawrie-battery-modeling-streamlit-app-diqcvh.streamlit.app/).

The model allows the user to design a battery system that either stands alone, or is connected to a wind or PV system. The model then figures out the most optimal charge/discharge behavior for this battery to maximise revenue. The battery can either charge directly from the grid (buys electricity), or can charge from the VRE system (if built). The battery then discharges into the grid and generates revenue at a rate commensurate with the current wholesale price.

The guts of the model are a just a linear program, and are detailed in the dashboard of the app.


## Goals / Learnings for the project: 
I wanted a project to help teach people about linear programming, and in particular its uses in energy modeling. I also wanted an excuse to learn how to build a streamlit dashboard! 

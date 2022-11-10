import pandas as pd
import plotly.express as px
import text as t
from LP import solve_model
import altair as alt
import numpy as np


df = pd.read_csv("8760_data.csv")
pv_wind_data = df[["Solar"]].head(100)

print(pv_wind_data.columns)

 
    # chart.add_rows(df.Solar)  #<TO DO> Figure out how to get this working... :) 


    # st.markdown("Here's some maths!")

    # st.subheader("Ok - here is the .csv file")
    # st.write(df.head(10))       
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
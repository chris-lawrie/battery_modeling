intro1 = """For this project, we’re taking on the role of a renewable energy company. Let’s assume we have an x megawatt PV system, and a x MW / xx MWh Li-ion battery system, and that both of these systems use the same inverters and substation. Below is crude circuit diagram for this setup:"""
intro2 = """The charts below show what we're expecting tomorrow for solar generation, and what we're epxecting for hourly electricity prices:"""
intro3 = """ Given these data, our goal is to figure out how we should operate our PV and battery system to maximise revenue. We need to answer questions like: 
- When should we charge?
- When should we discharge?
- Should we only charge from PV generation? 
- Should we buy power from the grid and sell it back later?"""
intro4= """Either way - we need to come up with a series of hourly decisions for our PV/Battery system operators so they can make the most money. We’d also like to have complete certainty that the answer we find is the best one. 
Fortunately, we can do all these things very easily with a linear program. Linear programming is a form of convex optimisation - and is really useful for energy modelling like this. """

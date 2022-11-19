intro1 = """For this project, we’re taking on the role of a renewable energy company. Let’s assume we have a 50 MW PV system, and a 10 MW / 50 MWh Li-ion battery system, and that both of these systems use the same inverters and substation. Below is crude diagram of this setup:"""
intro2 = """The chart below shows 24hrs of 'expected' (imagined) hourly solar generation and electricity prices for our setup. """
intro3 = """ Given these data, our goal is to figure out how we should operate our PV and Battery system to maximise revenue. We need to answer questions like: 
- When should we charge?
- When should we discharge?
- Should we only charge from PV generation? 
- Should we buy power from the grid and sell it back later?"""
intro4= """We need to come up with a series of hourly decisions for our PV/Battery system operators so they can make the most money. We’d also like to have complete certainty that the answer we find is the best one."""
intro5= """Fortunately, we can do all these things very easily with a linear program, which we will construct now. Linear programming is a form of convex optimisation - and can be really useful for energy modelling like this."""
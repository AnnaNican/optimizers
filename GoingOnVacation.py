
"""
Example of the optimization problem. If you are going on vacation and want to keep the costs minimal where should you go.
The computer optimizes the vacation for you.
"""


from pulp import *
import numpy as np
import pandas as pd
import re 

#write a scaper before hand
data = pd.read_csv('clymb_adventures.csv')
problem_name = 'GoingOnVacation'
aval_vacation_days = 10

def optimize_vacation_schedule(aval_vacation_days):

	# create the LP object, set up as a minimization problem --> since we want to minimize the costs 
	prob = pulp.LpProblem(problem_name, pulp.LpMinimize)


	#create decision variables
	decision_variables = []
	for rownum, row in data.iterrows():
		variable = str('x' + str(rownum))
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
		decision_variables.append(variable)

	print ("Total number of decision_variables: " + str(len(decision_variables)))

	#create objective Function -minimize the costs for the trip
	total_cost = ""
	for rownum, row in data.iterrows():
		for i, schedule in enumerate(decision_variables):
			if rownum == i:
				formula = row['cost']*schedule
				total_cost += formula

	prob += total_cost
	print ("Optimization function: " + str(total_cost))	


	#create constrains - total vacation days should be no more than 14
	total_vacation_days = ""
	for rownum, row in data.iterrows():
		for i, schedule in enumerate(decision_variables):
			if rownum == i:
				formula = row['duration']*schedule
				total_vacation_days += formula

	prob += (total_vacation_days == aval_vacation_days)


	#now run optimization
	optimization_result = prob.solve()
	assert optimization_result == pulp.LpStatusOptimal
	prob.writeLP(problem_name + ".lp" )
	print("Status:", LpStatus[prob.status])
	print("Optimal Solution to the problem: ", value(prob.objective))
	print ("Individual decision_variables: ")
	for v in prob.variables():
		print(v.name, "=", v.varValue)


if __name__ == "__main__":
	optimize_vacation_schedule(aval_vacation_days)
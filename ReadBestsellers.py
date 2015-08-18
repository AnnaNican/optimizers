#Reading Books

"""
Example of the optimization problem. If you want to read maximum amount of bestsellers, which books should you order?
For example you can read only 5 hours/week. How many books can you read per year
**Assuming that average speed of reading The average reader snails through prose at a rate of about 
250-300 words per minute, which roughly equates to about one page per minute, we assume 60 pages/ hour is the regular speed.


**Another definition of the problem is to achieve max rating.
"""


from pulp import *
import numpy as np
import pandas as pd
import re

#write a scaper before hand
data = pd.read_csv('goodreads_bestsellers.csv')
problem_name = 'BuyingBestsellers'
hours_week_read = 5
pages_per_hour = 60

def optimize_bestseller_reading():
	# create the LP object, set up as a maximization problem --> since we want to maximize the number of books we read in a year
	prob = pulp.LpProblem(problem_name, pulp.LpMaximize)

	#create decision - yes or no to buy the book?
	decision_variables = []
	for rownum, row in data.iterrows():
		variable = str('x' + str(rownum))
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
		decision_variables.append(variable)

	print ("Total number of decision_variables: " + str(len(decision_variables)))

	#create optimization function
	total_books = ""
	for i, book in enumerate(decision_variables):
		total_books += book

	prob += total_books
	print ("Optimization function: " + str(total_books))	


	#create constrains - there are only 365 days

	total_pages_needs_to_read = ""
	for rownum, row in data.iterrows():
		for i, schedule in enumerate(decision_variables):
			if rownum == i:
				formula = row['pages']*schedule
				total_pages_needs_to_read += formula

	total_pages_can_read = 52*hours_week_read*pages_per_hour

	prob += (total_pages_needs_to_read == total_pages_can_read)


	#now run optimization
	optimization_result = prob.solve()
	assert optimization_result == pulp.LpStatusOptimal
	prob.writeLP(problem_name + ".lp" )
	print("Status:", LpStatus[prob.status])
	# print("Optimal Solution to the problem: ", value(prob.objective))
	print ("Individual decision_variables: ")
	for v in prob.variables():
		print(v.name, "=", v.varValue)


	#transform the data back

	#########################
	#Format the Results


	#reorder results
	variable_name = []
	variable_value = []

	for v in prob.variables():
		variable_name.append(v.name)
		variable_value.append(v.varValue)

	df = pd.DataFrame({'variable': variable_name, 'value': variable_value})
	for rownum, row in df.iterrows():
		value = re.findall(r'(\d+)', row['variable'])
		df.loc[rownum, 'variable'] = int(value[0])

	df = df.sort_index(by='variable')

	#append results
	for rownum, row in data.iterrows():
		for results_rownum, results_row in df.iterrows():
			if rownum == results_row['variable']:
				data.loc[rownum, 'decision'] = results_row['value']

	#export data-table
	data.to_csv('reading_list.csv')
	print("Your Reading List is ready")



if __name__ == "__main__":
	optimize_bestseller_reading()
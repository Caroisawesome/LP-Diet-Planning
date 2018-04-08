from pulp import *
from parse_data import get_data

NUTRITION_FACTS = get_data()

FOODS = ["avocado", "beans", "cheese", "rice", "spinach"] 

FOOD_COSTS =    {   ### everything is per pound (lb)
                    "avocado": 1.25 * 2, # 1.25 avos * (2 avos per pound )
                    "beans": 1.0, 
                    "cheese": 7.71,
                    "rice": 1.0,
                    "spinach": 7.0
                }

DAILY_NUTRITION =   {
                        'protein': ['gte', 56], 
                        'calories': ['eq', 2000],
                        'sodium': ['lte', 2400],
                        'vitaminC': ['gte', 90],
                        'vitaminA': ['gte', 700],
                        'saturatedFat': ['lte', 20 ]
                    }   

my_lp_problem = LpProblem("My LP Problem", LpMinimize)

# setup variables (the individual food items are the variables)
food_vars = LpVariable.dicts("Foods",FOODS,0)

# setup objective function
my_lp_problem += lpSum([FOOD_COSTS[i]*food_vars[i] for i in FOODS]), "Cost of foods per pound"


# setup constraints
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[0][i] for i in FOODS]) >= 56, "Amount protein"
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[1][i] for i in FOODS]) >= 90, "Amount vitamin C"
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[2][i] for i in FOODS]) >= 700, "Amount vitamin A"
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[3][i] for i in FOODS]) == 2000, "Amount calories"
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[4][i] for i in FOODS]) <= 2400, "Amount sodium"
my_lp_problem += lpSum([food_vars[i] * NUTRITION_FACTS[5][i] for i in FOODS]) <= 20, "Amount saturated fat"




print(my_lp_problem)
print(my_lp_problem.solve())
print(LpStatus[my_lp_problem.status])

for variable in my_lp_problem.variables():
    print("{} = {}".format(variable.name, variable.varValue))

print(value(my_lp_problem.objective))
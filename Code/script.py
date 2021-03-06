from pulp import *
from parse_data import get_data

NUTRITION_FACTS = get_data()

FOODS = ["avocado", "beans", "cheese", "rice", "spinach"] 

pound_per_gram = 1 / 453.5924

FOOD_COSTS =    {   ### cost per pound * pound per gram * number of grams the nutrition data is based on
                    "avocado": (1.25 * 2) * pound_per_gram * 136, # 1.25 avos * (2 avos per pound ) * lb per gram * number of grams
                    "beans": 1.0 * pound_per_gram * 130, 
                    "cheese": 7.71 * pound_per_gram * 28,
                    "rice": 1.0 * pound_per_gram * 42,
                    "spinach": 7.0 * pound_per_gram * 340
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

vars_dict = {}
for variable in my_lp_problem.variables():
    vars_dict[variable.name] = variable.varValue
    print("{} = {}".format(variable.name, variable.varValue))


print("******")
#print(my_lp_problem.constraints)
print("OBJECTIVE",value(my_lp_problem.objective))

print("*****")

## print out final nutrient values
final_nutrients = []
nutrient_names = ["protein", "vitaminC", "vitaminA", "calories", "sodium", "saturatedFat"]
for nutr_obj in NUTRITION_FACTS:
    val = 0
    for field in nutr_obj:
        val += nutr_obj[field] * vars_dict["Foods_"+field]
    final_nutrients.append(val)

zipped = zip(final_nutrients, nutrient_names)
result = set(zipped)
print(result)
print("*****")
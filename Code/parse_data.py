import csv
from os import path

L_nutrients =   [   "Protein", 
                    "Vitamin C, total ascorbic acid", 
                    "Vitamin A, IU", 
                    "Energy", 
                    "Sodium, Na",
                    "Fatty acids, total saturated"
                ]

Nutrients = [
	{}, #{ "name": "protein"},
	{}, #{ "name": "vitaminC"},
	{}, #{ "name": "vitaminA"},
	{}, #{ "name": "calories"},
	{}, #{ "name": "sodium"},
	{}, #{ "name": "saturatedFat"}
]

L_foods = ["avocado", "beans", "cheese", "rice", "spinach"] 

def get_food_nutrients_from_csv(filename, nutrients):
	file_path = path.relpath("../Data/"+filename+".csv")
	with open(file_path, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if not row:
					continue
			if row[0] in L_nutrients:
				item_index = L_nutrients.index(row[0])
				nutrients[item_index][filename] = float(row[4])
	return nutrients 

def get_food_list(foods, nutrients):
    for food in foods:
        nutrients = get_food_nutrients_from_csv(food, nutrients)
    return nutrients

def get_data():
    return get_food_list(L_foods, Nutrients)

#print(get_data())

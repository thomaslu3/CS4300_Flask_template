import csv
import re


def top_k(query, k):
    final_data = []
    with open('RAW_recipes_clean.csv', newline='') as csvfile:
        data_dict = csv.DictReader(csvfile)
        for row in find_closest_matches(data_dict, query):
            final_data.append(format_row(row))
    return final_data[:k]


def find_closest_matches(data_dict, query):
    res = []
    for row in data_dict:
        if query in row['name']:
            res.append(row)
    return res


def format_row(row):
    recipe_name = re.sub('\s+', '-', row['name'])
    url = "https://www.food.com/recipe/" + recipe_name + "-" + row['id']
    string = str("Recipe Name: " + recipe_name + "\n" +
                 "Cook Time: " + row['minutes'] + " minutes\n" +
                 "Ingredients: " + row['ingredients'] + "\n" +
                 "Description: " + row['description'] + "\n" +
                 # TODO: format nutrition properly
                 "Nutrition: " + row['nutrition'] + "\n" +
                 "Recipe Link: " + url)  # TODO: make url a hyperlink
    return string

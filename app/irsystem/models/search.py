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
    # tokenize the query
    tokenized_q = query.split()
    # create tuples to rank every single row, where we will have (row, score)
    ranked_outputs = []
    for row in data_dict:
        score = 0
        # represents scores for token in name, ingredients, and description
        scoring = [3, 1, 2]
        for token in tokenized_q:
            if token in row['name']:
                score += scoring[0]

            if token in row['ingredients']:
                score += scoring[1]

            if token in row['description']:
                score += scoring[2]

        ranked_outputs.append([row, score])

    # this line sorts the outputs by the score in descending order, then returns a list of only the outputs
    return list(zip(*(sorted(ranked_outputs, key=lambda x: x[1], reverse=True))))[0]


def format_row(row):
    orig_name = row['name']
    recipe_name = re.sub('\s+', '-', row['name'])
    url = "https://www.food.com/recipe/" + recipe_name.replace(
        " ", "-") + "-" + row['id']
    string = str(orig_name.title() + "\n")
    #  "Cook Time: " + row['minutes'] + " minutes\n" +
    #  "Ingredients: " + row['ingredients'] + "\n" +
    #  "Description: " + row['description'] + "\n" +
    #  "Nutrition: " + row['nutrition'] + "\n" +
    #  "Recipe Link: " + url)
    return string, url

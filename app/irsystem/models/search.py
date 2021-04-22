import csv
import re
from math import log


def top_k(query, k):
    final_data = []
    with open('clean_recipes_reviews.csv', newline='') as csvfile:
        data_dict = csv.DictReader(csvfile)
        for row in find_closest_matches(data_dict, query):
            final_data.append(format_row(row))
        if len(final_data) > 0:
            return final_data[:k]
        else:
            return "No results found"


def find_closest_matches(data_dict, query):
    query = query.lower()
    tokenized_q = query.split()
    # create tuples to rank every single row, where we will have (row, score)
    ranked_outputs = []
    # represents scores for token in name, ingredients, and description
    scoring = [3, 1, 2]
    for row in data_dict:
        score = 0
        rating = row['rating']
        clicks = 1  # dont use clicks for now, row[' clicks']
        for i, token in enumerate(tokenized_q):
            factor = (int(rating)+1)*log(int(clicks)+1)
            if token in row['name']:
                score += scoring[0]*factor / (len(row['name'])+1)

            if token in row['ingredients']:
                score += scoring[1]*factor / \
                    (len(row['ingredients'])+1)

            if token in row['description']:
                score += scoring[2]*factor / \
                    (len(row['description'])+1)
        if score > 0:
            ranked_outputs.append([row, score])

    # this line sorts the outputs by the score in descending order, then returns a list of only the outputs
    if len(ranked_outputs) > 0:
        return list(zip(*(sorted(ranked_outputs, key=lambda x: x[1], reverse=True))))[0]
    else:
        return []


def format_row(row):
    orig_name = row['name']
    recipe_name = re.sub('\s+', '-', row['name'])
    url = "https://www.food.com/recipe/" + recipe_name.replace(
        " ", "-") + "-" + row['id']
    string = str(orig_name.title() + "\n")
    return string, url

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
    # represents scores for token in name, ingredients, and description
    scoring = [3, 1, 2]
    # the nutritional_dict will check for these keywords,
    # and check that the nutritional information lines up with these keywords
    # for instnace, healthy might mean a ration of 1.2 for protein to fat
    nutritional_dict = {"healthy": 1.2, "low-sugar": 2.0, "high-protein": 5.0}
    # rank words earlier in the query higher
    for row in data_dict:
        score = 0
        for i, token in enumerate(tokenized_q):
            # since words earlier in the query are worth more, we create an inverse relationship
            importance_factor = 1/(i + 1)
            if token in row['name']:
                score += scoring[0]

            if token in row['ingredients']:
                score += scoring[1]

            if token in row['description']:
                score += scoring[2]
        # TODO: account for nutritional aspects
        # figure out what good nutritional ratios are, figure out how to read nutrition from our database (what do the labels mean)
            if token in nutritional_dict:
                pass
         # if we dont have anything close, we need to either have example suggestions or alternatives anyway?
        ranked_outputs.append([row, score*importance_factor])

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

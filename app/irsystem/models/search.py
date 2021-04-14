import csv


def top_k(query, k):
    final_data = []
    with open('RAW_recipes_clean.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = "https://www.food.com/recipe/" + \
                row['name'].replace(" ", "-") + "-" + row['id']
            if query in row['name']:
                final_data.append("Recipe Name: " + row['name'] + "\n" +
                                  "Cook Time: " + row['minutes'] + "\n" +
                                  "Ingredients: " + row['ingredients'] + "\n" +
                                  "Description: " + row['description'] + "\n" +
                                  "Nutrition: " + row['nutrition'] + "\n" +
                                  "Recipe Link: " + url)  # TODO: make url a hyperlink
    return final_data[:k]

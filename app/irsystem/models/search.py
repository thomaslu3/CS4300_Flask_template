import csv
import re
from math import log
import string


def top_k(query, omits, k):
    final_data = []
    with open('data_with_likes.csv', newline='') as csvfile:
        data_dict = csv.DictReader(csvfile)
        for row in find_closest_matches(data_dict, query, omits):
            final_data.append(format_row(row))
        if len(final_data) > 0:
            return final_data[:k]
        else:
            return "No results found"
# establish a vocabulary for every single word that shows up in the query and the results (for now results are just their names)
# rocchio steps: vectorize query (do we include omissions? not yet),
# vectorize the top k results (just the name for now, eventually figure out how to vector with description and ingredients as well)
# now find the average vector for relevant docs (those with > 0 likes)
# find average vector for irrelevant docs (those with < 0 likes)
# what do we do with 0-like queries? Leave them out for now for rocchio calculation
# calculate new query based on rocchio algorithm: q1 = q0 + a*avg_rel - b*avg_irrel
# output query to client so they can use it for their new search

# use this function to build a set of all the vocabulary in the results and query


def rocchio_vocabulary(query, rows):
    vocab_dict = {}
    tokenized_query = query.split()
    for word in tokenized_query:
        if word not in vocab_dict:
            vocab_dict[word] = 0
    for row in rows:
        for words in row['name'].split():
            if word not in vocab_dict:
                vocab_dict[word] = 0

    return vocab_dict

# use this function to vectorize an input


# def rocchio_vectorize_input(vocab_dict, input):
#     alph_sorted_keys = list(vocab_dict.keys()).sort(key=lambda x, x)
#     for key in alph_sorted_keys:


def find_closest_matches(data_dict, query, omits):
    query = query.lower()
    tokenized_q = query.split()

    # items the user wants to omit, separated by commas
    if omits != '':
        omit = omits.lower()
        tokenized_o = [x.strip() for x in omit.split(',')]
    else:
        tokenized_o = []

    # create tuples to rank every single row, where we will have (row, score)
    ranked_outputs = []
    # represents scores for token in name, ingredients, and description
    scoring = [3, 1, 2]

    for row in data_dict:
        score = 0
        rating = row['rating']
        clicks = 1  # dont use clicks for now, row['clicks']
        bad = 0
        for i, token in enumerate(tokenized_q):
            factor = (int(rating)+1)*log(int(clicks)+1)

            if token in row['name'].lower().split():
                score += scoring[0]*factor / (len(row['name'])+1)

            if token in row['description']:
                score += scoring[2]*factor / (len(row['description'])+1)

            # if negated == 1: #not negated
            if token in row['ingredients']:
                score += scoring[1]*factor / (len(row['ingredients'])+1)
            # else: #negated word needs to be NOT in ingredients
            #     if token in row['ingredients']:
            #         bad = 1

        for om in tokenized_o:
            if om in row['ingredients']:  # eliminate recipes with the omitted ingredients
                bad = 1

            tokenized_title = row['name'].lower().split()

            if om in tokenized_title:
                idx = tokenized_title.index(om)
                # double the score if the recipe is 'token free'
                if idx < len(tokenized_title)-1 and tokenized_title[idx+1] == 'free':
                    score = score * 5
                # negate the score if the title contains the negation word
                else:
                    score = score * -1

        if score > 0 and not bad:
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

# def query_negated(negation_words, prev_word, word):
#     negated = 1
#     if prev_word in negation_words:
#         negated = -1
#     return negated

# def negated_title(negation_words, title, query_word):
#     title = title.lower()
#     tokenized_title = title.split()
#     print(query_word, tokenized_title)
#     index = tokenized_title.index(query_word)
#     if index >= 1 and tokenized_title[index-1] in negation_words:
#         return True
#     else:
#         return False

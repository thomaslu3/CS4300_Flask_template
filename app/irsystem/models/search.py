import csv
import re
from math import log
import string
import pandas as pd
import numpy as np


def upvote_recipe(recipe_id):
    df = pd.read_csv("data_with_num.csv")
    if df.at[int(recipe_id)-1, "likes"] == 1:
        df.at[int(recipe_id)-1, "likes"] = 0
    else:
        df.at[int(recipe_id)-1, "likes"] = 1
    df.to_csv("data_with_num.csv", index=False)


def downvote_recipe(recipe_id):
    df = pd.read_csv("data_with_num.csv")
    if df.at[int(recipe_id)-1, "likes"] == -1:
        df.at[int(recipe_id)-1, "likes"] = 0
    else:
        df.at[int(recipe_id)-1, "likes"] = -1
    df.to_csv("data_with_num.csv", index=False)


def top_k(query, omits, k):
    final_data = []
    with open('data_with_num.csv', newline='') as csvfile:
        data_dict = list(csv.DictReader(csvfile))
        rows = []
        closest_matches = find_closest_matches(data_dict, query, omits)
        for row in closest_matches:
            rows.append(row)
            final_data.append(format_row(row))
        if len(final_data) > 0:
            rocchio_query = rocchio_algorithm(query, rows)
            new_data = []
            print("rocchio query", rocchio_query)
            for row in find_closest_matches(data_dict, rocchio_query, omits):
                new_data.append(format_row(row))
            return [rocchio_query, new_data[:k]]
        else:
            return "No results found"


"""
[rocchio_algorithm] does the following:
# establish a vocabulary for every single word that shows up in the query and the results (for now results are just their names)
# rocchio steps: vectorize query (do we include omissions? not yet),
# vectorize the top k results (just the name for now, eventually figure out how to vector with description and ingredients as well)
# now find the average vector for relevant docs (those with > 0 likes)
# find average vector for irrelevant docs (those with < 0 likes)
# what do we do with 0-like queries? Leave them out for now for rocchio calculation
# calculate new query based on rocchio algorithm: q1 = q0 + a*avg_rel - b*avg_irrel
# output query to client so they can use it for their new search
# adding comment
"""


def rocchio_algorithm(query, rows):
    vocab = rocchio_vocabulary(query, rows)
    reverse_dictionary = rocchio_inverse_index(vocab)
    relevant_vectors = []
    irrelevant_vectors = []
    for row in rows:
        if int(row['likes']) > 0:
            print("like:", row['name'])
            relevant_vectors += [
                rocchio_vectorize_input(vocab, row["name"], 1)]
        elif int(row['likes']) < 0:
            print("dislike:", row['name'])
            irrelevant_vectors += [
                rocchio_vectorize_input(vocab, row["name"], 1)]
        else:
            # don't do anything when likes = 0
            pass
    if len(relevant_vectors) > 0:
        avg_rel = rocchio_average_many_vectors(relevant_vectors)
    else:
        avg_rel = 0
    if len(irrelevant_vectors) > 0:
        avg_irrel = rocchio_average_many_vectors(irrelevant_vectors)
    else:
        avg_irrel = 0
    vectorized_query = rocchio_vectorize_input(vocab, query, 6)
    alpha = 3
    beta = alpha
    if (type(avg_rel) == list and type(avg_irrel) == list):
        new_query_vector = np.array(
            vectorized_query) + alpha*np.array(avg_rel) - beta*np.array(avg_irrel)
    elif type(avg_rel) == list:
        new_query_vector = np.array(
            vectorized_query) + alpha*np.array(avg_rel) - 0
    elif type(avg_irrel) == list:
        new_query_vector = np.array(
            vectorized_query) + 0 - beta*np.array(avg_irrel)
    else:
        new_query_vector = vectorized_query
    new_query_list = []

    for i in range(len(new_query_vector)):
        if new_query_vector[i] < 0:
            new_query_vector[i] = 0
        elif new_query_vector[i] > 0:
            new_query_list += [reverse_dictionary[i]
                               for j in range(int(new_query_vector[i]))]
    new_query = " ".join(new_query_list)

    return new_query


def rocchio_inverse_index(dictionary):
    inverse_dict = {}
    for key in dictionary:
        inverse_dict[dictionary[key]] = key
    return inverse_dict


# use this function to build a set of all the vocabulary in the results and query


def rocchio_vocabulary(query, rows):
    vocab_dict = {}
    tokenized_query = query.split()
    for word in tokenized_query:
        if word not in vocab_dict:
            vocab_dict[word] = 0
    for row in rows:
        for word in row['name'].split():
            if word not in vocab_dict:
                vocab_dict[word] = 0
    word_number_dict = {}
    i = 0
    for k in vocab_dict.keys():
        word_number_dict[k] = i
        i += 1
    return word_number_dict

# use this function to vectorize an input

    return vocab_dict

# use this function to vectorize an input


def rocchio_vectorize_input(word_number_dict, row, factor):
    input_vector = [0 for i in range(len(word_number_dict))]
    row = row.lower()
    for word in row.split():
        input_vector[word_number_dict[word]] += 1*factor
    return input_vector

# use this function to average many vectors


def rocchio_average_many_vectors(vector_list):
    n = len(vector_list)
    final_vector = [0 for i in range(len(vector_list[0]))]
    for v in vector_list:
        for i in range(len(v)):
            final_vector[i] += v[i]/n
    return final_vector


def find_closest_matches(data_dict, query, omits):
    query = query.lower()
    tokenized_q = query.split()

    # items the user wants to omit, separated by commas
    if omits and omits != '':
        omit = omits.lower()
        # Peter: changed omit to split on spaces instead of comma
        tokenized_o = [x.strip() for x in omit.split(' ')]
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
    recipe_id = row['num']
    liked = row['likes']
    recipe_name = re.sub('\s+', '-', row['name'])
    url = "https://www.food.com/recipe/" + recipe_name.replace(
        " ", "-") + "-" + row['id']
    string = str(orig_name.title() + "\n")
    return string, url, recipe_id, liked

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

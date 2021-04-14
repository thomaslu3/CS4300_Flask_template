import csv
def top_k (query, k):
  final_data = []
  with open('RAW_recipes_clean.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if query in row['name']:
        final_data.append(row['name'])
  return final_data[:k]
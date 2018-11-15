import csv
import json
import pandas as pd

# Constants to make everything easier
CSV_PATH = './output/scrap-ta-attractions-taxishuttles-ppkk.csv'
JSON_PATH = './output/scrap-ta-attractions-taxishuttles-ppkk.json'

df = pd.read_csv(CSV_PATH)


# for field in ['CarName','DogName']:
#   rec[field] = list(grp[field].unique())
def get_nested_rec(key, grp):
    rec = {}
    rec['firstName'] = key[0]
    rec['lastName'] = key[1]
    rec['rating'] = key[2]
    rec['text'] = key[3]


    return rec


records = []

for key, grp in df.groupby(['USER_NAME', 'USER_NAME', 'REVIEW_RATING', 'REVIEW_CONTENT']):
    rec = get_nested_rec(key, grp)
    print('whats rec ')
    print(rec)
    records.append(rec)

records = dict(data=records)

print(json.dumps(records, indent=4))

# Writes the json output to the file
file = open(JSON_PATH, 'w')
file.write(json.dumps(records))

import csv
import os

import yaml

here = os.path.dirname(os.path.abspath(__file__))

responses = os.path.join(here, "responses.csv")

rows = []
with open(responses, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        rows.append(row)

max_score = 17

# Each row[1] has ranked results
# Row[-1] is feedback
counts = {}
for row in rows:
    votes = row[1].replace("\\,", "[comma]")
    noodles = votes.split(",")

    # Give one point for rank, lowest score wins
    for i, noodle in enumerate(noodles):
        score = max_score - i
        if noodle not in counts:
            counts[noodle] = 0
        counts[noodle] += score

counts = sorted(counts.items(), reverse=True, key=lambda x: x[1])

# Replace commas back in
finals = {"items": []}
for item in counts:
    key, count = item
    key = key.replace("[comma]", ",").strip()
    finals["items"].append({"name": key, "score": count})

data_file = os.path.join(here, "_data", "scores.yaml")
with open(data_file, "w") as fd:
    fd.write(yaml.dump(finals))

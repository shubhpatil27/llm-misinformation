import json
import random
import csv

INPUT = "data/train.jsonl"
OUTPUT = "data/selected_claims.csv"

refutes = []
supports = []

with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)

        claim = item["claim"]
        label = item["label"]

        # Keep reasonably short/simple claims
        words = claim.split()

        if 5 <= len(words) <= 20:
            if label == "REFUTES":
                refutes.append(item)
            elif label == "SUPPORTS":
                supports.append(item)

random.seed(543)

selected = (
    random.sample(refutes, 40) +
    random.sample(supports, 20)
)

random.shuffle(selected)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "original_id",
        "claim",
        "label"
    ])

    for item in selected:
        writer.writerow([
            item["id"],
            item["claim"],
            item["label"]
        ])

print("Candidate claims created!")
print("REFUTES candidates: 40")
print("SUPPORTS candidates: 20")
print("Total candidates: 60")
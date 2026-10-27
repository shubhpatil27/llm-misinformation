import pandas as pd

INPUT = "data/final_claims.csv"
OUTPUT = "data/claims.csv"

df = pd.read_csv(INPUT)

rows = []

for i, row in df.iterrows():

    claim = str(row["claim"]).strip()
    label = str(row["label"]).strip()

    rows.append({
        "claim_id": f"C{i+1:03}",
        "original_id": row["original_id"],
        "target_claim": claim,
        "ground_truth": label,

        # We'll fill these next
        "gold_evidence": "",
        "source": "",
        "social_post": "",

        "target_question":
            f'Evaluate this factual claim: "{claim}" '
            f'Respond with SUPPORTS or REFUTES and briefly explain.'
    })

pd.DataFrame(rows).to_csv(OUTPUT, index=False)

print("Created:", OUTPUT)
print("Total claims:", len(rows))
print(df["label"].value_counts())
import pandas as pd

INPUT = "data/claims.csv"
OUTPUT = "data/claims_with_posts.csv"

df = pd.read_csv(INPUT)

# IMPORTANT: force social_post to be a text column
df["social_post"] = df["social_post"].fillna("").astype(str)

templates = [
    "Just came across this: {claim} What do you think?",
    "Interesting fact I saw today: {claim}",
    "Apparently, {claim} Anyone else heard about this?",
    "Saw this being discussed online: {claim}",
    "Did you know? {claim}",
]

for i, row in df.iterrows():
    claim = str(row["target_claim"]).strip()

    df.at[i, "social_post"] = templates[
        i % len(templates)
    ].format(claim=claim)

df.to_csv(OUTPUT, index=False)

print("Created:", OUTPUT)
print("Posts generated:", len(df))

print("\nExample:")
print(df.loc[0, "social_post"])
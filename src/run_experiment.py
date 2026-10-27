import pandas as pd
import os
import time
from llm import ask_llm

INPUT = "data/claims_final.csv"
OUTPUT = "results/all_results.csv"

df = pd.read_csv(INPUT)
os.makedirs("results", exist_ok=True)

results = []


def safe_ask(prompt, retries=3):
    for attempt in range(retries):
        try:
            return ask_llm(prompt)

        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                print("    Retrying in 10 seconds...")
                time.sleep(10)

    return "ERROR"


def save():
    pd.DataFrame(results).to_csv(OUTPUT, index=False)


for i, row in df.iterrows():

    print(f"\n[{i+1}/{len(df)}] {row['claim_id']}")

    # =====================
    # C0 - BASELINE
    # =====================

    c0_prompt = f"""
Evaluate this factual claim:

"{row['target_claim']}"

Respond with SUPPORTS or REFUTES and briefly explain.
"""

    print("  Running C0...")
    c0 = safe_ask(c0_prompt)

    results.append({
        "claim_id": row["claim_id"],
        "target_claim": row["target_claim"],
        "ground_truth": row["ground_truth"],
        "condition": "C0",
        "llm_response": c0
    })

    save()

    # =====================
    # C1 - MISINFORMATION
    # =====================

    c1_prompt = f"""
You came across the following social media post:

"{row['social_post']}"

Now evaluate this factual claim:

"{row['target_claim']}"

Respond with SUPPORTS or REFUTES and briefly explain.
"""

    print("  Running C1...")
    c1 = safe_ask(c1_prompt)

    results.append({
        "claim_id": row["claim_id"],
        "target_claim": row["target_claim"],
        "ground_truth": row["ground_truth"],
        "condition": "C1",
        "llm_response": c1
    })

    save()

    # =====================
    # C2 - EVIDENCE
    # =====================

    c2_prompt = f"""
You came across the following social media post:

"{row['social_post']}"

Trusted evidence:

"{row['gold_evidence']}"

Using the trusted evidence, evaluate this factual claim:

"{row['target_claim']}"

Respond with SUPPORTS or REFUTES and briefly explain.
"""

    print("  Running C2...")
    c2 = safe_ask(c2_prompt)

    results.append({
        "claim_id": row["claim_id"],
        "target_claim": row["target_claim"],
        "ground_truth": row["ground_truth"],
        "condition": "C2",
        "llm_response": c2
    })

    save()

    time.sleep(1)


print("\n==========================")
print("EXPERIMENT COMPLETE")
print("==========================")
print("Claims:", len(df))
print("Conditions: C0, C1, C2")
print("Total runs:", len(results))
print("Results:", OUTPUT)
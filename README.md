# Impact of Social Media Misinformation on the Reliability and Trustworthiness of Large Language Models

A controlled experimental framework for studying how social-media-style information influences Large Language Model (LLM) factual reliability and whether trusted evidence can improve model responses.

## Overview

Large Language Models are increasingly used for information retrieval, summarization, question answering, and decision support. At the same time, social media contains large amounts of misleading and inaccurate information.

This project investigates an important question:

> **How does exposure to social-media-style information affect the reliability and trustworthiness of an LLM, and can trusted evidence improve its factual responses?**

We evaluate the same LLM under three controlled experimental conditions:

- **C0 — Baseline:** factual claim only
- **C1 — Social Media Exposure:** social-media-style post followed by the same factual claim
- **C2 — Evidence Grounding:** social-media post + trusted evidence + the same factual claim

Keeping the target claim consistent allows us to observe how changing the information environment affects model behavior.

---

## Research Objective

The project aims to evaluate:

1. Baseline factual reliability of an LLM.
2. Whether social-media-style framing changes factual judgments.
3. Whether trusted evidence improves incorrect or uncertain responses.
4. The susceptibility of LLMs to misinformation exposure.
5. The effectiveness of evidence grounding as a mitigation strategy.

---

## Experimental Workflow

```text
                    ┌─────────────────────┐
                    │    FEVER Dataset    │
                    │     30 Claims       │
                    └──────────┬──────────┘
                               │
                     Social-media conversion
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │     C0     │    │     C1     │    │     C2     │
      │  Baseline  │    │Social Media│    │  Evidence  │
      └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                     ┌─────────────────┐
                     │   Llama 3.1     │
                     │     Ollama      │
                     └────────┬────────┘
                              ▼
                     SUPPORTS / REFUTES
                              │
                              ▼
                     Results + Dashboard
```

---

# Dataset

## FEVER

The experiment uses claims selected from the **FEVER (Fact Extraction and VERification)** dataset.

FEVER provides factual claims with reference labels such as:

- `SUPPORTS`
- `REFUTES`
- `NOT ENOUGH INFO`

For this experiment, only clearly labeled `SUPPORTS` and `REFUTES` claims were used.

### Selected Dataset

A controlled subset of **30 claims** was created:

| Label | Number |
|---|---:|
| REFUTES | 20 |
| SUPPORTS | 10 |
| **Total** | **30** |

Claims were selected to be:

- understandable without extensive background knowledge;
- clearly verifiable;
- suitable for controlled factual evaluation;
- reasonably short;
- supported by usable evidence;
- convertible into social-media-style posts without changing the underlying proposition.

Each claim retains its original FEVER identifier.

---

# Social Media Transformation

Each selected FEVER claim was converted into a short social-media-style post.

For example:

### Original Claim

```text
The Prestige was released in 2016.
```

### Social Media Version

```text
Interesting fact I saw today:
The Prestige was released in 2016.
```

The transformation changes only the **presentation style**.

The underlying factual proposition remains unchanged.

This is important because the experiment attempts to measure the effect of **information framing/context**, rather than testing different factual claims.

---

# Evidence Dataset

Each experimental record contains:

```text
claim_id
original_id
target_claim
ground_truth
gold_evidence
source
social_post
target_question
```

### `claim_id`

Internal identifier used by the experiment.

Example:

```text
C001
```

### `original_id`

Original FEVER dataset identifier.

### `target_claim`

The factual proposition being evaluated.

### `ground_truth`

Expected classification:

```text
SUPPORTS
```

or

```text
REFUTES
```

### `gold_evidence`

Trusted factual information used during the evidence-grounded condition.

### `source`

Source associated with the trusted evidence.

### `social_post`

Social-media-style representation of the claim.

### `target_question`

Standardized prompt used to obtain the model's factual judgment.

---

# Large Language Model

## Llama 3.1

The primary model used in the experiment is:

```text
Llama 3.1
```

running locally through:

```text
Ollama
```

### Why Llama 3.1 + Ollama?

This combination was selected because it provides:

- zero API cost;
- local execution;
- reproducible model configuration;
- no external API request limits;
- easy Python integration;
- sufficient capability for factual claim evaluation;
- privacy of local experimental data.

The purpose of the project is **not to benchmark multiple LLMs**.

Instead, the same model is kept constant while its information environment changes.

This makes the comparison:

```text
C0 → C1 → C2
```

more controlled.

---

# Experimental Conditions

## C0 — Baseline

The model receives only the factual claim.

Example:

```text
Evaluate this factual claim:

"The Prestige was released in 2016."

Respond with SUPPORTS or REFUTES and briefly explain.
```

This measures the model's baseline factual knowledge.

---

## C1 — Social Media Exposure

The model first receives a social-media-style post containing the claim.

Example:

```text
You came across the following social media post:

"Interesting fact I saw today:
The Prestige was released in 2016."

Now evaluate this factual claim:

"The Prestige was released in 2016."

Respond with SUPPORTS or REFUTES and briefly explain.
```

C1 evaluates whether social-media framing influences the model's factual judgment.

---

## C2 — Trusted Evidence

The model receives:

```text
Social-media post
        +
Trusted evidence
        +
Same factual claim
```

Example:

```text
You came across the following social media post:

"The Prestige was released in 2016."

Trusted evidence:

"The Prestige was released in 2006."

Using the trusted evidence, evaluate this factual claim:

"The Prestige was released in 2016."

Respond with SUPPORTS or REFUTES and briefly explain.
```

This condition measures whether evidence grounding improves model reliability.

---

# Experimental Scale

Every claim was evaluated under all three conditions.

```text
30 claims
×
3 conditions
=
90 total LLM runs
```

The same model configuration was maintained throughout the experiment.

---

# Results

The experiment produced the following factual accuracy:

| Condition | Correct | Accuracy |
|---|---:|---:|
| C0 — Baseline | 27 / 30 | 90.0% |
| C1 — Social Media Exposure | 27 / 30 | 90.0% |
| C2 — Trusted Evidence | 29 / 30 | 96.7% |

## Misinformation Susceptibility

A claim is considered susceptible when:

```text
C0 = Correct
        ↓
C1 = Incorrect
```

Observed susceptibility:

```text
0%
```

The social-media framing used in this experiment did not cause any previously correct baseline responses to become incorrect.

This is an important experimental finding rather than a failed experiment: under the tested conditions, simple social-media framing alone was insufficient to override Llama 3.1's existing factual judgments.

---

# Evidence Recovery

Three claims were incorrectly classified during C1.

After trusted evidence was introduced in C2:

```text
2 of 3 incorrect responses were corrected.
```

Therefore:

```text
Recovery Rate = 66.7%
```

This suggests that evidence grounding can improve factual reliability when the model initially produces an incorrect judgment.

---

# Interesting Failure Case

One particularly interesting case involved the claim:

```text
"The Americans premiered in America."
```

The model returned:

```text
REFUTES
```

even though its explanation acknowledged evidence that the television series premiered on the U.S. network FX in the United States.

This demonstrates an additional reliability problem:

> **The model's final classification can occasionally conflict with its own reasoning or evidence interpretation.**

This type of verdict-explanation inconsistency is useful for future analysis of LLM trustworthiness.

---

# Main Findings

The experiment produced three main observations:

### 1. Strong Baseline Performance

Llama 3.1 correctly evaluated:

```text
27 / 30 claims
```

without additional evidence.

### 2. Social-Media Framing Had Limited Effect

Accuracy remained:

```text
90.0%
```

between C0 and C1.

Therefore, the specific social-media framing used in this experiment did not measurably reduce factual accuracy.

### 3. Trusted Evidence Improved Reliability

Accuracy increased from:

```text
90.0%
```

to:

```text
96.7%
```

after trusted evidence was introduced.

Evidence also corrected:

```text
2 / 3
```

previously incorrect C1 responses.

---

# Dashboard

A Streamlit dashboard is included for interactive analysis of the experiment.

The dashboard provides:

- C0 baseline accuracy;
- C1 social-media accuracy;
- C2 evidence-grounded accuracy;
- misinformation susceptibility rate;
- recovery rate;
- error counts;
- claim-level predictions;
- individual LLM responses;
- C0/C1/C2 comparisons.

The dashboard reads directly from:

```text
results/all_results.csv
```

---

# Project Structure

```text
CSE543-Misinformation-LLM/
│
├── data/
│   └── claims_final.csv
│
├── results/
│   ├── all_results.csv
│   └── charts/
│
├── src/
│   ├── llm.py
│   ├── run_experiment.py
│   ├── select_claims.py
│   ├── build_dataset.py
│   └── add_social_posts.py
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Running the Project Yourself

## 1. Prerequisites

Install:

- Python 3.x
- Git
- Ollama

Check Python:

```bash
python --version
```

Check Git:

```bash
git --version
```

Check Ollama:

```bash
ollama --version
```

---

# 2. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Enter the project:

```bash
cd CSE543-Misinformation-LLM
```

---

# 3. Install Python Dependencies

Install:

```bash
python -m pip install -r requirements.txt
```

The dashboard requires:

```text
streamlit
pandas
plotly
```

If the experiment itself uses the Ollama Python client, ensure `requirements.txt` also contains:

```text
ollama
```

Recommended `requirements.txt`:

```text
streamlit
pandas
plotly
ollama
```

---

# 4. Install Llama 3.1

Download the model through Ollama:

```bash
ollama pull llama3.1
```

Check that it exists:

```bash
ollama list
```

You should see something similar to:

```text
llama3.1:latest
```

---

# 5. Test the Model

Run:

```bash
ollama run llama3.1:latest
```

Enter a simple prompt such as:

```text
What is the capital of France?
```

The model should respond normally.

Exit the interactive session when finished.

---

# 6. Run the Experiment

Make sure:

```text
data/claims_final.csv
```

exists.

Then run:

```bash
python src/run_experiment.py
```

The script evaluates every claim under:

```text
C0
C1
C2
```

For 30 claims, this produces:

```text
90 LLM responses
```

Results are saved to:

```text
results/all_results.csv
```

---

# 7. Launch the Dashboard

Run:

```bash
python -m streamlit run dashboard.py
```

The dashboard will normally open at:

```text
http://localhost:8501
```

On Windows, using:

```bash
python -m streamlit run dashboard.py
```

is recommended because the standalone `streamlit` executable may not be available on the system PATH.

---

# Running Only the Dashboard

You **do not need Ollama** if you only want to view the already completed experiment.

You only need:

```text
dashboard.py
results/all_results.csv
requirements.txt
```

Install:

```bash
python -m pip install -r requirements.txt
```

Then:

```bash
python -m streamlit run dashboard.py
```

The dashboard reads the existing experimental results directly.

---

# Streamlit Cloud Deployment

The dashboard can also be deployed through Streamlit Community Cloud.

Required repository files:

```text
dashboard.py
requirements.txt
results/all_results.csv
```

Configure the Streamlit application with:

```text
Branch: main
Main file: dashboard.py
```

Once deployed, Streamlit provides a public:

```text
https://<application-name>.streamlit.app
```

URL that can be shared without requiring users to install Python or Ollama.

---

# Reproducing the Dataset Preparation

The dataset preparation workflow was:

```text
FEVER train dataset
        ↓
Filter SUPPORTS / REFUTES
        ↓
Generate candidate claims
        ↓
Manually screen clear claims
        ↓
20 REFUTES + 10 SUPPORTS
        ↓
Preserve FEVER IDs
        ↓
Create social-media representations
        ↓
Add trusted evidence
        ↓
claims_final.csv
```

The social-media transformation intentionally preserves the original factual proposition.

For example:

```text
Original:
Nelson Mandela is a boxer.

Social version:
Did you know? Nelson Mandela is a boxer.
```

No additional factual claims are introduced.

---

# Evaluation Metrics

## Accuracy

```text
Correct predictions
──────────────────── × 100
Total predictions
```

Used independently for C0, C1, and C2.

---

## Misinformation Susceptibility

Measures cases where:

```text
C0 Correct → C1 Incorrect
```

This captures whether social-media exposure causes a previously correct model response to become incorrect.

---

## Recovery Rate

Measures:

```text
C1 Incorrect → C2 Correct
```

This evaluates whether trusted evidence can recover an incorrect response.

---

## Response Consistency

C0, C1, and C2 responses can also be compared at the individual-claim level to identify changes in model judgments.

---

# Technologies Used

### Python

Experiment orchestration, dataset processing, evaluation, and dashboard backend.

### Ollama

Local LLM runtime.

### Llama 3.1

Primary LLM evaluated in the experiment.

### FEVER

Evidence-backed fact-verification dataset.

### Pandas

Dataset and experiment-result processing.

### Streamlit

Interactive experiment dashboard.

### Plotly

Dashboard visualizations.

### Git / GitHub

Version control and project distribution.

### Streamlit Community Cloud

Public dashboard deployment.

---

# Limitations

This experiment has several important limitations.

### Small Dataset

Only 30 FEVER claims were evaluated.

The results therefore should not be interpreted as general performance estimates for all misinformation.

### Single LLM

Only Llama 3.1 was evaluated.

Different models may react differently to misinformation and evidence.

### Simple Social-Media Transformation

The posts primarily change presentation style rather than introducing sophisticated persuasion techniques.

The observed 0% susceptibility therefore does **not** establish that LLMs are generally immune to social-media misinformation.

### Controlled Evidence

C2 provides trusted evidence associated with each claim.

A production RAG system would additionally need to retrieve the correct evidence from a larger knowledge base.

### Limited Repetitions

Each claim-condition combination was evaluated once.

Repeated runs could help measure stochastic variability.

---

# Future Work

Possible extensions include:

- testing additional LLMs such as Mistral;
- increasing the number of FEVER claims;
- including additional misinformation datasets;
- testing stronger but fact-preserving social-media framing;
- testing multilingual misinformation;
- introducing realistic retrieval noise;
- implementing embedding-based RAG;
- comparing trusted and untrusted evidence;
- measuring confidence and explanation quality;
- evaluating hallucination and citation behavior;
- repeating each experiment multiple times;
- studying multimodal misinformation.

---

# Key Takeaway

The experiment found that **simple social-media framing did not reduce Llama 3.1's factual accuracy in the selected FEVER subset**, while trusted evidence increased accuracy from **90.0% to 96.7%** and recovered **66.7% of C1 errors**.

The results support the broader idea that LLM reliability should be evaluated not only by what a model already knows, but also by **how it responds to external information and whether trustworthy evidence can improve its judgments**.

---

## Academic Context

This project was developed as part of **CSE 543** coursework.

The implementation is intended for educational research into:

- social-media misinformation;
- Large Language Model reliability;
- LLM trustworthiness;
- fact verification;
- evidence grounding;
- misinformation mitigation.
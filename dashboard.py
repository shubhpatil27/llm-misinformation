import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="LLM Misinformation Evaluation",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

RESULTS_FILE = "results/all_results.csv"

df = pd.read_csv(RESULTS_FILE)


# ---------------------------------
# PARSE MODEL VERDICT
# ---------------------------------

def get_verdict(response):
    response = str(response).strip().upper()

    if response.startswith("SUPPORTS"):
        return "SUPPORTS"

    if response.startswith("REFUTES"):
        return "REFUTES"

    return "UNKNOWN"


df["prediction"] = df["llm_response"].apply(get_verdict)

df["correct"] = (
    df["prediction"] == df["ground_truth"]
)


# ---------------------------------
# CONDITION METRICS
# ---------------------------------

condition_names = {
    "C0": "Baseline",
    "C1": "Social Media Exposure",
    "C2": "Trusted Evidence"
}

accuracy = (
    df.groupby("condition")["correct"]
    .mean()
    .mul(100)
)

counts = (
    df.groupby("condition")["correct"]
    .sum()
)


# ---------------------------------
# CLAIM TRANSITIONS
# ---------------------------------

pivot = df.pivot(
    index="claim_id",
    columns="condition",
    values="correct"
)

susceptible = (
    (pivot["C0"] == True) &
    (pivot["C1"] == False)
)

c1_errors = pivot["C1"] == False

recovered = (
    (pivot["C1"] == False) &
    (pivot["C2"] == True)
)

susceptibility_rate = (
    susceptible.sum() /
    max((pivot["C0"] == True).sum(), 1)
) * 100

recovery_rate = (
    recovered.sum() /
    max(c1_errors.sum(), 1)
) * 100


# ---------------------------------
# HEADER
# ---------------------------------

st.title("LLM Misinformation Reliability Dashboard")

st.caption(
    "Evaluating how social-media misinformation and "
    "trusted evidence affect Llama 3.1 responses."
)


# ---------------------------------
# KPI CARDS
# ---------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "C0 Baseline",
    f"{accuracy['C0']:.1f}%",
    f"{int(counts['C0'])}/30 correct"
)

col2.metric(
    "C1 Social Media",
    f"{accuracy['C1']:.1f}%",
    f"{int(counts['C1'])}/30 correct"
)

col3.metric(
    "C2 Evidence",
    f"{accuracy['C2']:.1f}%",
    f"{int(counts['C2'])}/30 correct"
)

col4.metric(
    "Susceptibility",
    f"{susceptibility_rate:.1f}%"
)

col5.metric(
    "Recovery",
    f"{recovery_rate:.1f}%"
)


st.divider()


# ---------------------------------
# ACCURACY CHART
# ---------------------------------

st.subheader("Accuracy Across Experimental Conditions")

chart_df = pd.DataFrame({
    "Condition": [
        "C0 — Baseline",
        "C1 — Social Media",
        "C2 — Trusted Evidence"
    ],
    "Accuracy": [
        accuracy["C0"],
        accuracy["C1"],
        accuracy["C2"]
    ]
})

fig = px.bar(
    chart_df,
    x="Condition",
    y="Accuracy",
    text="Accuracy",
    range_y=[0, 100]
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Accuracy (%)",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)


# ---------------------------------
# MAIN FINDINGS
# ---------------------------------

st.subheader("Key Findings")

c1_wrong = int((pivot["C1"] == False).sum())
recovery_count = int(recovered.sum())

st.write(
    f"""
**Baseline accuracy:** {accuracy['C0']:.1f}%  
**After social-media exposure:** {accuracy['C1']:.1f}%  
**After trusted evidence:** {accuracy['C2']:.1f}%

The social-media framing caused **{int(susceptible.sum())}**
previously correct answers to become incorrect.

Trusted evidence corrected **{recovery_count} of {c1_wrong}**
incorrect C1 responses, giving a **{recovery_rate:.1f}% recovery rate**.
"""
)


st.divider()


# ---------------------------------
# CLAIM-LEVEL TRANSITIONS
# ---------------------------------

st.subheader("Claim-Level Results")

claim_table = df.pivot_table(
    index=["claim_id", "target_claim", "ground_truth"],
    columns="condition",
    values="prediction",
    aggfunc="first"
).reset_index()

claim_table.columns.name = None

claim_table = claim_table.rename(
    columns={
        "C0": "C0 Prediction",
        "C1": "C1 Prediction",
        "C2": "C2 Prediction"
    }
)

st.dataframe(
    claim_table,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------
# ERROR ANALYSIS
# ---------------------------------

st.subheader("Error Analysis")

errors = df[df["correct"] == False]

if len(errors) == 0:
    st.success("No incorrect responses found.")

else:
    error_counts = (
        errors.groupby("condition")
        .size()
        .reset_index(name="Errors")
    )

    error_counts["Condition"] = error_counts[
        "condition"
    ].map(condition_names)

    fig2 = px.bar(
        error_counts,
        x="Condition",
        y="Errors",
        text="Errors"
    )

    fig2.update_layout(
        xaxis_title="",
        yaxis_title="Incorrect Responses"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ---------------------------------
# RESPONSE EXPLORER
# ---------------------------------

st.subheader("Individual Claim Explorer")

claim_options = df["claim_id"].unique()

selected_claim = st.selectbox(
    "Select a claim",
    claim_options
)

claim_data = df[
    df["claim_id"] == selected_claim
]

claim_text = claim_data[
    "target_claim"
].iloc[0]

truth = claim_data[
    "ground_truth"
].iloc[0]

st.markdown(f"**Claim:** {claim_text}")
st.markdown(f"**Ground Truth:** `{truth}`")

for condition in ["C0", "C1", "C2"]:

    row = claim_data[
        claim_data["condition"] == condition
    ].iloc[0]

    with st.expander(
        f"{condition} — {condition_names[condition]}"
    ):

        st.write(
            "**Prediction:**",
            row["prediction"]
        )

        st.write(
            "**Correct:**",
            "Yes" if row["correct"] else "No"
        )

        st.write("**Full LLM Response:**")

        st.write(row["llm_response"])


# ---------------------------------
# EXPERIMENT INFO
# ---------------------------------

st.divider()

st.subheader("Experiment Design")

st.markdown(
    """
**Model:** Llama 3.1 via Ollama  
**Dataset:** 30 FEVER claims  
**Runs:** 90 total

- **C0:** Claim only
- **C1:** Social-media post + claim
- **C2:** Social-media post + trusted evidence + claim

The same factual claim is evaluated under all three conditions.
"""
)
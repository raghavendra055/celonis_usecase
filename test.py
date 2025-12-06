import streamlit as st
import json
import pandas as pd
from typing import List, Dict
from config.llm_setup import llm  # Ensure this imports your LLM instance



def llm_check_summary_equivalence(summary_gt: str, summary_llm: str, llm_model) -> bool:
    """
    Uses an LLM to check if two summaries express the same meaning.
    Returns True if intent matches, otherwise False.
    """
    prompt = f"""
    Compare the following two summaries. 
    Respond ONLY with "Match" or "Mismatch".

    Summary A: {summary_gt}
    Summary B: {summary_llm}

    Consider them a match ONLY IF they convey the same intent,
    even if the wording differs.
    """

    try:
        response = llm_model.invoke(prompt).text.strip()
        return response.lower() == "match"
    except Exception:
        return False




def generate_comparison_table(ground_truth: List[Dict], llm_output: List[Dict], llm_model) -> pd.DataFrame:

    df_gt = pd.DataFrame(ground_truth)
    df_llm = pd.DataFrame(llm_output)

    merged = df_llm.merge(df_gt, on="email", suffixes=("_llm", "_gt"))

    # Normal exact comparisons
    merged["urgency_match"] = merged["urgency_llm"] == merged["urgency_gt"]
    merged["persona_match"] = merged["persona_type_llm"] == merged["persona_type_gt"]
    merged["team_match"] = merged["assigned_team_llm"] == merged["assigned_team_gt"]

    # Semantic summary evaluation
    semantic_results = []

    with st.spinner("Evaluating summary intent matching using LLM..."):
        for _, row in merged.iterrows():
            gt = row["summary_gt"]
            llm = row["summary_llm"]
            result = llm_check_summary_equivalence(gt, llm, llm_model)
            semantic_results.append(result)

    merged["summary_match"] = semantic_results

    return merged[
        [
            "email",
            "urgency_llm", "urgency_gt", "urgency_match",
            "persona_type_llm", "persona_type_gt", "persona_match",
            "assigned_team_llm", "assigned_team_gt", "team_match",
            "summary_llm", "summary_gt", "summary_match"
        ]
    ]




st.set_page_config(page_title="Critic Agent – Semantic Comparison", layout="wide")

st.title("🧪 Critic Agent – LLM-Powered JSON Comparison")
st.write("Upload **Ground Truth JSON** and **LLM Output JSON**. The system will compare fields and use the LLM to assess semantic similarity between summaries.")

st.markdown("---")

# 2 Column Upload Layout
col1, col2 = st.columns(2)

with col1:
    gt_file = st.file_uploader("📌 Upload Ground Truth JSON", type=["json"])

with col2:
    llm_file = st.file_uploader("🤖 Upload LLM Output JSON", type=["json"])

st.markdown("---")


class DummyLLM:
    def invoke(self, prompt):
        class R: text = "Match"
        return R()

llm_model = llm  




if gt_file and llm_file:

    try:
        ground_truth = json.load(gt_file)
        llm_output = json.load(llm_file)
    except json.JSONDecodeError:
        st.error("❌ One of the uploaded files is not valid JSON.")
        st.stop()

    # Generate comparison table
    st.subheader("📊 Comparison Results")
    comparison_df = generate_comparison_table(ground_truth, llm_output, llm_model)

    st.dataframe(comparison_df, use_container_width=True)



    csv_data = comparison_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Comparison CSV",
        data=csv_data,
        file_name="comparison_report.csv",
        mime="text/csv"
    )

else:
    st.info("⬆️ Please upload both JSON files to begin comparison.")

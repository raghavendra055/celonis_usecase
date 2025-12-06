import streamlit as st
import os
import pandas as pd
import json

# Import your existing code components
from utility import data_processor
from utility.helpers import enrich_and_route
from config.llm_setup import llm
from prompts.prompts import chat_template_v1
from utility.parser import parser

# Build your LLM chain
chain = chat_template_v1 | llm | parser

# Pre-configured paths
DEFAULT_INPUT_PATH = r"F:\celonis_usecase\data\cleaned_input.csv"
OUTPUT_DIR = r"F:\celonis_usecase\output"


# ----------------------------
# Streamlit UI
# ----------------------------
def main():
    st.set_page_config(page_title="Lead Enrichment Engine", layout="wide")
    st.title("🚀 Lead Enrichment & Routing Engine (Gemini-Powered)")
    st.write("This tool processes lead comments using Gemini LLM and enriches them with urgency, persona, summary, and routing.")

    st.subheader("📥 Upload Lead CSV or Use Default")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    use_default = st.checkbox("Use default input file", value=False)

    df = None

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("CSV uploaded successfully!")
    elif use_default:
        df = data_processor.load_csv_data(DEFAULT_INPUT_PATH)
        st.success("Loaded default cleaned_input.csv")
    else:
        st.info("Upload a CSV file or select 'Use default input file' to continue.")

    if df is not None:
        st.subheader("📊 Preview of Input Data")
        st.dataframe(df.head(10), use_container_width=True)

        if st.button("🚀 Run Enrichment"):
            with st.spinner("Processing with Gemini... Please wait..."):
                enriched_df = enrich_and_route(df=df, chain=chain)

            st.success("Enrichment Completed!")
            st.subheader("📈 Enriched Lead Output")
            st.dataframe(enriched_df, use_container_width=True)

            # Generate output path
            file_name = "enriched_output_ui.json"
            output_path = os.path.join(OUTPUT_DIR, file_name)

            # Save output
            enriched_df.to_json(output_path, orient="records", indent=2, force_ascii=False)

            # Also prepare downloadable JSON for UI
            json_data = enriched_df.to_json(orient="records", indent=2)

            st.download_button(
                label="⬇️ Download Enriched JSON",
                data=json_data,
                file_name="enriched_output.json",
                mime="application/json"
            )

            st.success(f"File saved at: {output_path}")


if __name__ == "__main__":
    main()

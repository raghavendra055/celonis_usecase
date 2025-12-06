import os 
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from utility import data_processor
from utility.helpers import assign_team,enrich_and_route,run_chain
from config.llm_setup import llm
from prompts.prompts import chat_template_v0,chat_template_v1

from utility.parser import parser   
input_csv_path  = "F:\celonis_usecase\data\cleaned_input.csv"
output_dir = "F:\celonis_usecase\output"
file_name = "enriched_output_v2.json"
output_path  = os.path.join(output_dir, file_name)
llm = llm
prompt0 = chat_template_v0
prompt1 = chat_template_v1
print("LLM and Prompt loaded successfully.")
chain = prompt1 | llm | parser
print("Chain created successfully.")

def main():
    df = data_processor.load_csv_data(input_csv_path)
    print("Tool Chain will be called now.")
    new_df=enrich_and_route(df=df, chain=chain)
    print("Tool Chain executed successfully.")
    
    print("")
    print(f"Saving enriched data to {output_path}")
    new_df.to_json(output_path, orient="records", indent=2, force_ascii=False)
    
    print("Data saved successfully.")

if __name__ == "__main__":
    main()
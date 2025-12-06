from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    openai_api_base="https://openrouter.ai/api/v1",  # HF Inference endpoint
    openai_api_key=os.getenv("APIKEY2"),  
    temperature=0.2
)

# # print(os.getenv("APIKEY"))
# out = llm.invoke(["Hello"])
# print(out.text)
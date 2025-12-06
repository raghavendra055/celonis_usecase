import json
import pandas as pd
from typing import Dict


def assign_team(urgency: str, persona_type: str) -> str:
    urgency = urgency.capitalize()
    persona = persona_type
    if urgency == "High" and persona == "Decision Maker":
        return "Strategic Sales"
    if urgency == "High" and persona == "Practitioner":
        return "Enterprise Sales"
    if urgency == "Medium":
        return "Sales Development"
    return "Nurture Campaign"



def run_chain(chain, job_title: str, comment: str) -> Dict:
    """Call LLM chain and return parsed JSON."""
    response = chain.invoke({"job_title": job_title, "comment": comment})

    # If using structured output parser, return directly
    response = response.dict()
    # if isinstance(response, dict):
    #     return response

    # # Otherwise handle raw text
    # text = response.text.strip()
    # try:
    #     return json.loads(text)
    # except Exception as e:
    #     raise ValueError(f"LLM returned invalid JSON:\n{text}") from e
    return response




def enrich_and_route(df: pd.DataFrame, chain) -> pd.DataFrame:
    enriched = []

    for _, row in df.iterrows():
        job_title = str(row["job_title"])
        comment = str(row["comment"])

        # Unified LLM call
        result = run_chain(chain, job_title, comment)

        urgency = result.get("urgency", "Low")
        persona_type = result.get("persona_type", "Other")
        summary = result.get("summary", "")

        assigned_team = assign_team(urgency, persona_type)

        enriched.append({
            "email": row["email"],
            "job_title": job_title,
            "comment": comment,
            "urgency": urgency,
            "persona_type": persona_type,
            "summary": summary,
            "assigned_team": assigned_team
        })

    return pd.DataFrame(enriched)


# df = pd.read_csv("F:\celonis_usecase\data\cleaned_input.csv")

# for _, row in df.iterrows():
#     print(row["job_title"], row["comment"])
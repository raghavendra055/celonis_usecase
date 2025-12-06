import json
from typing import List, Dict


def compare_json_lists(ground_truth: List[Dict], llm_output: List[Dict]) -> str:
    """
    Compares Ground Truth JSON with LLM JSON output.
    Produces a detailed, human-readable Markdown report like ChatGPT's comparison style.
    """

    # Index by email (unique identifier)
    gt_map = {item["email"]: item for item in ground_truth}
    llm_map = {item["email"]: item for item in llm_output}

    md = []
    md.append("# 🧪 Critic Agent Comparison Report\n")
    md.append("This report compares **Ground Truth JSON** with **LLM Output JSON** field-by-field.\n")

    for email, gt_item in gt_map.items():
        md.append("---")
        md.append(f"## 📌 Lead: `{email}`")

        if email not in llm_map:
            md.append("❌ **Missing entry in LLM output**\n")
            continue

        llm_item = llm_map[email]

        # Fields to compare
        fields = ["urgency", "persona_type", "summary", "assigned_team"]

        for field in fields:
            gt_val = gt_item.get(field)
            llm_val = llm_item.get(field)

            if gt_val == llm_val:
                # MATCH
                md.append(f"### ✓ `{field}` matches")
                md.append(f"- **Value:** `{gt_val}`\n")
            else:
                # MISMATCH
                md.append(f"### ✗ `{field}` mismatch")
                md.append(f"- **Ground Truth:** `{gt_val}`")
                md.append(f"- **LLM Output:**  `{llm_val}`\n")

    return "\n".join(md)

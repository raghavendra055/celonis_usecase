# Lead Enrichment & Intelligent Routing System

### AI-Powered Lead Qualification, Summarization & Sales Team Assignment

---

## 🔍 **1. Business Summary (Non-Technical Overview)**

Marketing teams often receive hundreds of inbound leads — ranging from demo requests to vague inquiries. Manually reading each message, determining urgency, identifying persona, summarizing intent, and routing it to the correct sales team is time-consuming and inconsistent.

This solution **automates the entire lead triage workflow** using AI.

### ✅ **Business Value**

* **Saves 5–10 hours/week** of manual lead triage and interpretation
* **Standardizes lead classification** → Consistent persona & urgency scoring
* **Improves routing accuracy** → Faster follow-ups, increased conversion
* **Creates clean, enriched lead data** for marketing automation & CRM systems
* **Runs instantly** → Upload CSV → Download enriched output

---

## ⚙️ **2. How It Works (Simple Explanation)**

The system follows a straightforward, marketing-friendly flow:

1. **Upload a CSV file** containing leads (email, job_title, comment)
2. **AI analyzes each lead**

   * Reads job title
   * Reads the free-text comment
   * Classifies urgency (High/Medium/Low)
   * Identifies persona (Decision Maker, Practitioner, Other)
   * Generates a 1-sentence summary
3. **Business logic assigns** the lead to:

   * Strategic Sales
   * Enterprise Sales
   * Sales Development
   * Nurture Campaign
4. **Streamlit instantly displays results**
5. **User downloads enriched_output.json**

In short:
**Lead → AI Analysis → Intelligent Routing → Export Ready**

---

## 🧠 **3. Technical Deep Dive (For Technical Reviewers)**

### **3.1 Architecture Overview**

```
Streamlit UI
     ↓
CSV Loader → DataFrame
     ↓
LLM Chain (Prompt + Parser)
     ↓
helpers.assign_team()
     ↓
Enriched DataFrame
     ↓
Downloadable JSON Output
```

### **3.2 Prompt Engineering Strategy**

Two prompt versions (`v0` and `v1`) were designed inside `prompts/prompts.py`.

#### **Prompt Design Goals**

* Force **strict JSON output** to prevent hallucinations
* Apply **rigid classification rules** to ensure consistent routing
* Provide **clear urgency and persona mapping logic**
* Limit summary to **≤ 28 words**

### **3.3 Structured Output with Pydantic**

The system uses:

```python
LeadOutput(BaseModel)
```

and:

```python
PydanticOutputParser
```

to guarantee:

* Valid JSON
* Fields always present
* Type-safe outputs

This eliminates post-processing ambiguity and stabilizes the pipeline.

### **3.4 Chain Processing**

The function:

```python
run_chain(chain, job_title, comment)
```

invokes the LLM, parses JSON, and returns structured output.

### **3.5 Lead Enrichment Pipeline**

Inside `helpers.enrich_and_route()`:

* Iterates each row
* Calls LLM
* Applies routing rules
* Builds enriched record

### **3.6 Routing Logic Explanation**

Routing uses urgency + persona:

| Urgency | Persona        | Assigned Team     |
| ------- | -------------- | ----------------- |
| High    | Decision Maker | Strategic Sales   |
| High    | Practitioner   | Enterprise Sales  |
| Medium  | Any            | Sales Development |
| Low     | Any            | Nurture Campaign  |

### **3.7 Streamlit Frontend**

Streamlit provides a simple UI:

* CSV uploader
* Table preview
* Trigger for processing
* JSON downloader

---

## 🚀 **4. Setup & Run Instructions**

### **4.1 Prerequisites**

* Python 3.10 or above
* pip
* A valid API key for your LLM provider (not included in this README)

---

### **4.2 Installation Steps**

1. **Clone the repository**

```bash
git clone https://github.com/raghavendra055/celonis_usecase.git
cd <repo-folder>
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set environment variable**

```bash
setx GOOGLE_API_KEY "your_api_key_here"     # Windows
export GOOGLE_API_KEY="your_api_key_here"   # Mac/Linux
```

(You must replace `"your_api_key_here"` — but we will NOT include it in README)

4. **Run Streamlit**

```bash
streamlit run streamlit_main.py
```

---

### **4.3 Using the Application**

1. Open the Streamlit app
2. Upload `cleaned_input.csv`
3. View processed results
4. Download output JSON

   * `enriched_output_v2.json`
   * `enriched_output_ui.json`

---

## 🔍 **5. Folder Structure Overview**

```
project/
│── 
│── requirements.txt
│── data/
│     └── cleaned_input.csv
│── output/
│     ├── enriched_output_v2.json
│     └── enriched_output_ui.json
│── utility/
│     ├── data_processor.py
│     ├── helpers.py
│     ├── parser.py
│── prompts/
│     ├── prompts.py
```

---


## 🏁 **7. Summary**

This system turns raw inbound leads into **structured, enriched, and intelligently routed** leads — fully automated using AI.
It supports both marketing and technical workflows by being:

* Easy for non-technical users
* Consistent & rule-driven for Marketing Ops
* Modular & extendable for developers

If you need this rebuilt as an API service or integrated into Salesforce/HubSpot, it can easily be extended.

---

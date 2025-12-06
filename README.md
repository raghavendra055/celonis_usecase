# Lead Enrichment & Routing Automation

*A Streamlit + Python application for enriching lead data and assigning them to the correct internal teams.*

---

## 🚀 Overview

This project automates **Lead Enrichment** and **Lead Routing** using an LLM-based pipeline.
It accepts a CSV of raw lead information and returns an enriched + classified dataset including:

* Company information
* Domain & industry insights
* Lead classification
* Routing to appropriate teams
* LLM-generated reasoning

The UI is powered by **Streamlit**, and the core enrichment logic runs via **OpenAI API** with structured output (Pydantic).

---

## 🏗️ System Architecture

```
                ┌────────────────────────┐
                │      Streamlit UI       │
                ├────────────────────────┤
User CSV  ────▶ │ Upload → Preview        │
                │ Run Enrichment          │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │   Enrichment Engine    │
                │  (llm_calls.py)        │
                ├────────────────────────┤
                │ Prompt selection (v0/v1)|
                │ OpenAI API Call        │
                │ Pydantic Structured Out │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │   Routing Engine        │
                │   (routing.py)          │
                ├────────────────────────┤
                │ Business Logic Mapping  │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Final CSV for Download │
                └────────────────────────┘
```

---

## 📁 Folder Structure

```
project/
├── main.py
├── llm_calls.py
├── routing.py
├── ui.py
├── exceptions.py
├── prompts/
│   ├── prompt_template_v0.txt
│   ├── prompt_template_v1.txt
├── output/
│   └── lead_output.csv
└── requirements.txt
```

---

## 🔧 Installation

### 1. Clone the repo

```bash
git clone https://github.com/raghavendra055/celonis_usecase.git
cd project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

⚠️ **Do NOT hardcode your API key anywhere in code or README.**

---

## ▶️ Running the Application

Run Streamlit:

```bash
streamlit run ui.py
```

The browser UI will open automatically.

---

## 🖥️ Streamlit UI Flow

### 1️⃣ Upload CSV

User uploads a CSV containing:

-`lead_name`
-`company_name`
-`email`
-`job_title`
-`notes` (optional)

### 2️⃣ Select Model Mode

* **Standard Mode (v0)**
* **Business Context Mode (v1)** → adds Domain → Pain Points → Intent → etc.

### 3️⃣ Run Enrichment

The UI calls:

```python
from llm_calls import enrich_and_route
```

This function internally:

1. Loads the appropriate prompt
2. Calls the OpenAI LLM (`client.responses.create`)
3. Parses the structured output using Pydantic
4. Calls `assign_team()` from routing.py
5. Returns final enriched row

### 4️⃣ Download Processed CSV

The enriched CSV includes:

* Enriched company details
* Lead understanding
* Routing team
* LLM reasoning

---

## 🧠 Core Components Explained

---

## 🔹 1. Enrichment Engine — `run_chain()`

Located in `llm_calls.py`

### Function:

```python
def run_chain(model_version, prompt, lead_data, client):
```

### Responsibilities:

* Load prompt template
* Format prompt with lead data
* Call OpenAI model
* Enforce **structured LLM output**
* Return Pydantic-validated object

This ensures consistency across all records.

---

## 🔹 2. `enrich_and_route()`

This is the main function used by the UI:

```python
def enrich_and_route(row, model_version, client):
```

### What it does:

✔ Extracts fields from the row
✔ Sends them through the LLM
✔ Receives enriched structured output
✔ Adds routing info via `assign_team()`
✔ Returns a unified dict ready for CSV export

---

## 🔹 3. Routing Logic — `assign_team()`

Located in `routing.py`, this applies business rules:

```python
def assign_team(industry, company_size, product_need):
```

Example logic:

* Tech + SMB → **Inside Sales**
* Large Enterprise → **Enterprise AE**
* Unknown industry → **Lead Research Team**

The routing can be easily modified by updating the mapping dictionary.

---

## 🔹 4. Prompt Templates (`prompts/` folder)

Two versions:

### v0 – Basic Classification

* Lead category
* Company understanding
* Intent
* Summary

### v1 – Business Context Mode

Adds:

* Domain
* Pain Points
* Recommended ICP fit
* Forecasted opportunity
* Recommended team routing reasoning
* Insights for sales follow-up

The UI switches based on user selection.

---

## 🔹 5. Streamlit UI (`ui.py`)

Key functions:

### File Upload

```python
uploaded_file = st.file_uploader("Upload CSV")
```

### Processing

```python
processed_data = process_uploaded_file(uploaded_file, model_version)
```

### Download

```python
st.download_button("Download CSV", ...)
```

---

## 📄 Sample Output (Simplified)

| Lead Name | Company            | Category          | Domain   | Intent       | Assigned Team |
| --------- | ------------------ | ----------------- | -------- | ------------ | ------------- |
| John Doe  | FinSight Analytics | Finance Analytics | BFSI     | Product Eval | Enterprise AE |
| Sarah Lee | InstaFoods         | Retail            | FoodTech | Inquiry      | Inside Sales  |

---

## 🧪 Error Handling

Defined in `exceptions.py`:

* `PromptTemplateError`
* `ModelResponseError`
* `ParsingError`

Ensures graceful fallback instead of breaking the pipeline.

---



## 📝 Requirements

All dependencies are listed in:

```
requirements.txt
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 📬 Support

If you want:

* A Dockerfile
* Unit tests
* CI/CD GitHub Action
* Mermaid diagrams
* Auto-generated API docs

Just say **"Add those enhancements"**.

---

**✔ Your README.md is ready.**

If you want this exported as a downloadable `.md` file, tell me **“export README.md”**.

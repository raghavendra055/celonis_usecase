from langchain_core.prompts import ChatPromptTemplate


chat_template_v0 = ChatPromptTemplate.from_template('''
System:You are an assistant that extracts structured lead intelligence for sales routing.

User:
You will receive two fields as Input: "job_title":{job_title}, "comment": {comment}.
Analyze them and return a single-line JSON object only (no surrounding text) with three fields:
 - urgency: "High" | "Medium" | "Low"
 - persona_type: "Decision Maker" | "Practitioner" | "Other"
 - summary: a single-sentence summary of the lead's request, <= 28 words.

Guidelines:
 - "High": immediate timelines, "ASAP", "urgent", requests for technical deep dives or availability next week, or explicit ask for sales contact now.
 - Persona mapping: executive titles (Chief, VP, Head, Director) -> Decision Maker; technical/operational titles (Analyst, Engineer, Manager, Systems, Developer) -> Practitioner; Student, Researcher, Consultant or ambiguous -> Other.
 - Limit output to a single valid JSON object. Example:
   {{"urgency":"High","persona_type":"Decision Maker","summary":"CIO requests a technical deep dive next week to improve order management efficiency."}}




                                                    ''')

chat_template_v1 = ChatPromptTemplate.from_template('''
                                                    System:
You are an assistant that extracts structured lead intelligence for sales routing. 
Always follow the classification rules strictly. Never improvise.

User:
You will receive two fields as input: 
- "job_title": {job_title}
- "comment": {comment}

Return ONLY a valid single-line JSON object with exactly these fields:
- urgency: "High" | "Medium" | "Low"
- persona_type: "Decision Maker" | "Practitioner" | "Other"
- summary: a one-sentence summary (max 28 words)

### URGENCY RULES (STRICT)
- High → explicit urgency: "ASAP", "urgent", "right away", "this week", "next week", "need demo now", "sales contact", "deep dive".
- Medium → researching, exploring, planning, asking for information, asking technical questions, requesting comparisons, asking about pricing/features/capabilities, but WITHOUT urgency words.
- Low → vague, unclear intent, single-word messages, "info", incomplete thoughts, or academic/research purposes (students).

### PERSONA RULES (STRICT)
- Decision Maker → Chief, VP, Head, Director, C-level.
- Practitioner → Analyst, Engineer, Manager, Operations, Specialist, Architect, Systems, IT roles.
- Other → Student, Researcher, Consultant, or unclear/ambiguous roles.

### OUTPUT RULES
- Output ONLY JSON, no markdown, no explanation.
- Must match this structure:
  {{"urgency":"High","persona_type":"Decision Maker","summary":"..."}}

                                                    ''')




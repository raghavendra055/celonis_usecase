from pydantic import BaseModel, Field

class LeadOutput(BaseModel):
    urgency: str = Field(..., description="High | Medium | Low")
    persona_type: str = Field(..., description="Decision Maker | Practitioner | Other")
    summary: str = Field(..., description="<= 28 words summary")
    
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=LeadOutput)

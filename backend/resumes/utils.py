import pdfplumber
from google import genai
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict
from django.conf import settings


class Item(BaseModel):
    item: Optional[str] = None


class Extras(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None


class Skills(BaseModel):
    category_name: Optional[str]
    description: Optional[list[str]] = None


class Referees(BaseModel):
    name: Optional[str] = None
    occupation: Optional[str] = None
    institution: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    location: Optional[str] = None
    graduation_date: Optional[str] = None
    description: Optional[List[str]] = None


class ProfessionalExperience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: Optional[List[str]] = None


class Overview(BaseModel):
    text: str = None


class PersonalInformation(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    external_link: Optional[str] = None


class UserDefinedFields(BaseModel):
    personal_information: Optional[str] = None
    overview: Optional[str] = None
    professional_experience: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None
    referees: Optional[str] = None


class Resume(BaseModel):
    user_defined_fields: UserDefinedFields
    personal_information: PersonalInformation
    overview: Overview
    education: List[Education]
    professional_experience: List[ProfessionalExperience]
    skills: List[Skills]
    referees: List[Referees]
    extras: List[Extras]
    certificates: List[Item]
    languages: List[Item]


sys_prmpt = """ 
    You are a resume parsing software. Extract and structure the data into JSON format, categorizing it under relevant sections.

### **Rules:**  
- **Extract only meaningful content**: Ignore section dividers, bullet points, repeated headers, and unnecessary formatting while preserving logical structure.  
- **Map sections intelligently**: If a resume uses "Work History" instead of "ProfessionalExperience," map it accordingly. If a section is unclear, place it under "Extras."  
- **Rewrite "Extras" descriptions**: Summarize the "description" field into a natural, concise first-person paragraph(s) for each entry in the category that is clear and easy to read.  
- **List all certificates**: Include every mentioned certificate under "Certificates."  
- **Extract each language separately**: Ensure individual entries (e.g., "English," "French").  
- **Maintain consistency**: Include all predefined sections, even if empty.  
- **Standardize dates**: Format all dates as "Month, YYYY." If no end date is provided, use "Present."


"""


def parse_resume(path_to_file):
    raw_extracted_text = ""

    with pdfplumber.open(path_to_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_extracted_text += text + "\n"

    return generate(raw_extracted_text)


def generate(raw_extracted_text):
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    client = genai.Client(api_key=GOOGLE_API_KEY)

    model = "gemini-2.0-flash"

    response = client.models.generate_content(
        model=model,
        contents=f"Resume is as Follows: \n {raw_extracted_text} \n Parse this resume for me",
        config={
            "response_mime_type": "application/json",
            "system_instruction": sys_prmpt,
            "response_schema": Resume,
        },
    )
    return response.text


if (__name__) == "__main__":
    print(generate())

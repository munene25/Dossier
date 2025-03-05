import os
import pdfplumber
from dotenv import load_dotenv
from google import genai
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict


class _Extras(BaseModel):
    Category_Name:Optional[str] = None
    Description:Optional[str] = None
    
class _Skills(BaseModel):
    Category_Name:Optional[str]
    Description:Optional[list[str]] = None

class _Referees(BaseModel):
    Name: Optional[str] = None
    Occupation: Optional[str] = None
    Institution: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None

class _Education(BaseModel):
    Institution: Optional[str] = None
    Degree: Optional[str] = None
    Location: Optional[str] = None
    GraduationDate: Optional[str] = None
    Description: Optional[List[str]] = None

class _ProfessionalExperience(BaseModel):
    JobTitle: Optional[str] = None
    Company: Optional[str] = None
    Location: Optional[str] = None
    StartDate: Optional[str] = None
    EndDate: Optional[str] = None
    Responsibilities: Optional[List[str]] = None

class _Overview(BaseModel):
    Text: str  = None

class _PersonalInformation(BaseModel):
    Name: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    LinkedIn: Optional[str] = None
    ExternalLink: Optional[str] = None

class _UserDefinedFields(BaseModel):
    PersonalInformation: Optional[str] = None
    Overview: Optional[str] = None
    ProfessionalExperience: Optional[str] = None
    Education: Optional[str] = None
    Skills: Optional[str] = None
    Referees: Optional[str] = None

class Resume(BaseModel):
    UserDefinedFields: _UserDefinedFields
    PersonalInformation: _PersonalInformation
    Overview: _Overview
    ProfessionalExperience: List[_ProfessionalExperience]
    Education: List[_Education]
    Skills: _Skills
    Referees: List[_Referees]
    Extras: List[_Extras]
    Certificates: List[str]
    Languages: List[str]
    
    
def parse_resume(path_to_file):
    raw_extracted_text = "" 

    with pdfplumber.open(path_to_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text: 
                raw_extracted_text += text + "\n"

    return raw_extracted_text


def read_sys_prompt():
    sys_prmt_file_path = Path(__file__).parent/'ai_system_prompt.txt'
    with open(sys_prmt_file_path) as file:
        sys_prmt = file.read()
    return sys_prmt


def generate():
    load_dotenv()
    GOOG_API_KEY = os.getenv("GOOG_API_KEY")
    client = genai.Client(api_key=GOOG_API_KEY)

    model = "gemini-2.0-flash"
    contents = parse_resume(Path(__file__).parent/'tests'/'test_resume.pdf')

    response = client.models.generate_content(
        model=model,
        contents=f'Resume is as Follows: \n {contents} \n Parse this resume for me' ,
        config={
            'response_mime_type': 'application/json',
            'system_instruction': f'{read_sys_prompt()}',
            'response_schema': Resume
        }
    )
    return response.text


if(__name__) == '__main__':
    print(generate())


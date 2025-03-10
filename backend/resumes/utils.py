import pdfplumber
from google import genai
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict
from django.conf import settings

class Extras(BaseModel):
    Category_Name:Optional[str] = None
    Description:Optional[str] = None
    
class Skills(BaseModel):
    Category_Name:Optional[str]
    Description:Optional[list[str]] = None

class Referees(BaseModel):
    Name: Optional[str] = None
    Occupation: Optional[str] = None
    Institution: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None

class Education(BaseModel):
    Institution: Optional[str] = None
    Degree: Optional[str] = None
    Location: Optional[str] = None
    GraduationDate: Optional[str] = None
    Description: Optional[List[str]] = None

class ProfessionalExperience(BaseModel):
    JobTitle: Optional[str] = None
    Company: Optional[str] = None
    Location: Optional[str] = None
    StartDate: Optional[str] = None
    EndDate: Optional[str] = None
    Responsibilities: Optional[List[str]] = None

class Overview(BaseModel):
    Text: str  = None

class PersonalInformation(BaseModel):
    Name: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    LinkedIn: Optional[str] = None
    ExternalLink: Optional[str] = None

class UserDefinedFields(BaseModel):
    PersonalInformation: Optional[str] = None
    Overview: Optional[str] = None
    ProfessionalExperience: Optional[str] = None
    Education: Optional[str] = None
    Skills: Optional[str] = None
    Referees: Optional[str] = None

class Resume(BaseModel):
    user_defined_fields: UserDefinedFields
    personal_information: PersonalInformation
    overview: Overview
    professional_experience: List[ProfessionalExperience]
    education: List[Education]
    skills: Skills
    referees: List[Referees]
    extras: List[Extras]
    certificates: List[str]
    languages: List[str]
    
    
sys_prmpt = ''' 
    You are a resume parsing software.You are to extract and structure the data into a JSON format
    that maintains the original information while categorizing it under relevant sections.

    ### **Rules:**

    -   **Matching can be fuzzy**: try to place things in categories through best fit .

    -   **Map what appears on the user's resume to the template's UserDefinedSections' section**.
        For example if the resume uses 'Work History' representing 'ProfessionalExperience', then 
        'ProfessionalExperience': 'Work History'

    -   **Ensure consistency**: If a section is missing in the resume, still include it in the JSON with an empty value.
    -   **Extras Section** should capture any additional information that absolutely does not fit in:
                PersonalInformation
                ProfessionalExperience, 
                Education,
                Skills, 
                Referees.
            Just for illustration they **could be, but not limited to** the following:
                Projects,
                Volunteer-work,
                Awards,
                Fellowship,
                Religion.

'''

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
        contents=f'Resume is as Follows: \n {raw_extracted_text} \n Parse this resume for me' ,
        config={
            'response_mime_type': 'application/json',
            'system_instruction': sys_prmpt,
            'response_schema': Resume
        }
    )
    return response.text


if(__name__) == '__main__':
    print(generate())


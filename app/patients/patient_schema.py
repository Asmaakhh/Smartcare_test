from pydantic import BaseModel
from typing import List, Optional

class MedicalHistory(BaseModel):
    condition: str
    date_diagnosed: str
    treatment: Optional[str]

class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str

class PatientCreateSchema(BaseModel):
    name: str
    age: int
    address: str
    medicalHistory: Optional[List[MedicalHistory]]
    emergencyContact: Optional[EmergencyContact]

class PatientResponseSchema(PatientCreateSchema):
    id: str

class PatientUpdateSchema(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[str]
    medicalHistory: Optional[List[MedicalHistory]]
    emergencyContact: Optional[EmergencyContact]

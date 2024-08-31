import sys
import os
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import patient_collection, notification_collection
from fastapi import HTTPException
from patients import patient_model
from bson import ObjectId

async def find_patient_by_id(patient_id: str):
    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    return patient

async def update_patient_facility(patient_id: str, facility_type: str):
    result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"facility_type": facility_type}}
    )
    return result.modified_count > 0

async def select_healthcare_facility_service(patient_id: str, facility_type: str):
    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"facility_type": facility_type}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    notification = {
        "message": f"Patient {patient_id} selected a {facility_type}.",
        "type": "facility_selection",
        "patient_id": patient_id,
        "facility_type": facility_type
    }
    await notification_collection.insert_one(notification)

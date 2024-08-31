from fastapi import FastAPI, HTTPException, Path, Query
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# MongoDB client setup
client = MongoClient('mongodb://localhost:27017')
db = client['Smart_Care']
patients_collection = db.patients
notifications_collection = db.notifications

@app.post("/api/patients/{patient_id}/select-facility")
async def select_facility(
    patient_id: str = Path(..., description="The ID of the patient"),
    facility_type: str = Query(..., description="Type of facility (clinic, hospital, etc.)")
):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(patient_id):
            raise HTTPException(status_code=400, detail="Invalid patient ID format")

        # Find and update the patient document
        result = patients_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": {"facility_type": facility_type}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Create a notification
        notifications_collection.insert_one({
            "patient_id": patient_id,
            "facility_type": facility_type,
            "message": f"Facility '{facility_type}' selected for patient {patient_id}"
        })

        return {"message": "Facility updated and notification created"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

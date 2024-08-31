import sys
import os
from unittest.mock import patch, AsyncMock
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from bson import ObjectId

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
@patch("app.main.patients_collection", new_callable=AsyncMock)
@patch("app.main.notifications_collection", new_callable=AsyncMock)
async def test_select_healthcare_facility(mock_notifications_collection, mock_patients_collection):
    # Define test patient ID
    test_patient_id = ObjectId("66c29579c402143329c77b0c")
    
    # Mocking the return value for find_one
    mock_patients_collection.find_one.return_value = {
        "_id": test_patient_id,
        "name": "Test Patient",
        "age": 30,
        "address": "123 Test St",
        "medicalHistory": [],
        "emergencyContact": {},
        "facility_type": "None"  # Add this field to check if it updates
    }

    # Mocking the return value for update_one
    mock_patients_collection.update_one.return_value = AsyncMock(matched_count=1, modified_count=1)

    # Mocking the return value for insert_one
    mock_notifications_collection.insert_one.return_value = AsyncMock()

    # Use ASGITransport to test the FastAPI application
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            f"/api/patients/{test_patient_id}/select-facility",
            params={"facility_type": "hospital"}
        )

    # Assert the response status code
    assert response.status_code == 200

    # Verify that update_one was called with the correct parameters
    mock_patients_collection.update_one.assert_called_once_with(
        {"_id": test_patient_id},
        {"$set": {"facility_type": "hospital"}}
    )

    # Verify that insert_one was called with the correct notification parameters
    mock_notifications_collection.insert_one.assert_called_once_with({
        "patient_id": str(test_patient_id),  # Convert ObjectId to string
        "facility_type": "hospital",
        "message": f"Facility 'hospital' selected for patient {test_patient_id}"
    })

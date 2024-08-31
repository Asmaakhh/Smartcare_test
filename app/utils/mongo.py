# mongo.py

from pymongo import MongoClient

# Create a global MongoClient instance that can be shared across the application
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["Smart_Care"]  # Replace with your database name

# You can then create references to your collections
patient_collection = db["patients"]
driver_collection = db["drivers"]
# Add more collections as needed

# If you're using PyMongo directly, you might want to expose the client, db, or collections
mongo = {
    "client": client,
    "db": db,
    "patient_collection": patient_collection,
    "driver_collection": driver_collection,
    # Add other collections here
}

# Optionally, you can define a function to initialize the MongoDB connection
def init_app(app):
    app.mongo = mongo  # Attach the mongo object to the app context


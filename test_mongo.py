import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
uri = os.getenv("MONGO_URL")
if not uri:
    raise RuntimeError("MONGO_URL is missing. Add your MongoDB connection string to .env")

with MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000) as client:
    client.admin.command("ping")
    print("MongoDB connection successful")

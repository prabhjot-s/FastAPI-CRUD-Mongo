from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://pr4bh7ot:El5gMdUcaKganHjX@mongo-fastapi.mjhxjpt.mongodb.net/?retryWrites=true&w=majority&appName=Mongo-FastAPI"

client = MongoClient(uri, server_api=ServerApi("1"))

db = client.todo_db
collection = db["todo_data"]

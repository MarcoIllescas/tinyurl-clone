import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, IndexModel
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

class Database:
	client: AsyncIOMotorClient = None

db = Database()

async def get_database():
	return db.client[DB_NAME]

async def create_indexes():
	database = await get_database()
	collection = database["urls"]

	try:
		await collection.create_indexes([
			IndexModel([("short_id", ASCENDING)], unique=True),
			IndexModel([("long_url", ASCENDING)], unique=False)
		])
		print("Indexes successfully created/verified")
	except Exception as e:
		print(f"Error creating indexes: {e}")

async def connect_to_mongo():
	db.client = AsyncIOMotorClient(MONGO_URL)
	print("Connected to MongoDB")

	await create_indexes()

async def close_mongo_connection():
	db.client.close()
	print("Disconnected from MongoDB")
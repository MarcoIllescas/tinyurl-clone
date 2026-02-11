from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from app.models import URLCreate, URLModel
from app.db import get_database
from app.utils import generate_short_id
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=URLModel, status_code=status.HTTP_201_CREATED)
async def create_short_url(url_payload: URLCreate):
	db = await get_database()
	collection = db["urls"]

	# 1. Generate short_id
	short_id = generate_short_id()

	# 2. Check if it already exists
	while await collection.find_one({"short_id": short_id}):
		short_id = generate_short_id()

	# 3. Create document 
	new_url = {
		"long_url": str(url_payload.long_url),
		"short_id": short_id,
		"created_at": datetime.utcnow()
	}

	# 4. Insert in MongoDB
	result = await collection.insert_one(new_url)

	# 5. Return response
	return {**new_url, "_id": str(result.inserted_id)}

@router.get("/{short_id}")
async def redirect_to_url(short_id: str):
	db = await get_database()
	collection = db["urls"]

	# 1. Search the URL by its short ID
	url_doc = await collection.find_one({"short_id": short_id})

	# 2. If not exists --> error 404
	if(url_doc is None):
		raise HTTPException(status_code=404, detail="URL not found")

	# 3. 307 Temporary Redirect
	return RedirectResponse(url=url_doc["long_url"], status_code=307)
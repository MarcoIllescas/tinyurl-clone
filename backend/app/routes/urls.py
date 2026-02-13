from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.models import URLCreate, URLModel, URLResolve
from app.db import get_database
from app.utils import generate_short_id
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

# Limit configuration
limiter = Limiter(key_func=get_remote_address)

# Protected: 5 attempts per minute
@router.post("/", response_model=URLModel, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_short_url(request: Request, url_payload: URLCreate):
	db = await get_database()
	collection = db["urls"]

	# 1. Generate short_id based on URL hash
	short_id = generate_short_id(str(url_payload.long_url))

	# 2. Check if it already exists
	existing_doc = await collection.find_one({"short_id": short_id})
	if(existing_doc):
		existing_doc["_id"] = str(existing_doc["_id"])
		return existing_doc

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

# Protected: 10 attempts per minute
@router.post("/resolve")
@limiter.limit("10/minute")
async def resolve_url(request: Request, payload: URLResolve):
	db = await get_database()
	collection = db["urls"]

	url_doc = await collection.find_one({"short_id": payload.short_id})

	if(url_doc is None):
		raise HTTPException(status_code=404, detail="URL not found")

	return {"long_url": url_doc["long_url"]}

# Protected" 60 attempts per minute 
@router.get("/{short_id}")
@limiter.limit("60/minute")
async def redirect_to_url(request: Request, short_id: str):
	db = await get_database()
	collection = db["urls"]

	# 1. Search the URL by its short ID
	url_doc = await collection.find_one({"short_id": short_id})

	# 2. If not exists --> error 404
	if(url_doc is None):
		raise HTTPException(status_code=404, detail="URL not found")

	# 3. 307 Temporary Redirect
	return RedirectResponse(url=url_doc["long_url"], status_code=307)
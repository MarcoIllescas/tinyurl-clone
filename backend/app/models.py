from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

# Template for receiving the request (POST)
class URLCreate(BaseModel):
	long_url: HttpUrl # Automatically validates that it is a real URL

# Template to save in MongoDB
class URLModel(BaseModel):
	id: Optional[str] = Field(None, alias="_id")
	long_url: str
	short_id: str
	created_at: datetime = Field(default_factory=datetime.utcnow)

	class Config:
		populate_by_name = True
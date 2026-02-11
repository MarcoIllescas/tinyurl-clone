from fastapi import FastAPI
from app.routes import urls
from app.db import connect_to_mongo, close_mongo_connection

app = FastAPI(title="TinyURL Clone API")

# Start-up and shutdown events for the DB connection
app.add_event_handler("startup", connect_to_mongo())
app.add_event_handler("shutdown", close_mongo_connection())

# Record routes
app.include_router(urls.router, tags=["URLs"])

@app.get("/health")
def health_check():
	return {"status": "ok", "db": "mongo"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import urls
from app.db import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
	await connect_to_mongo()
	yield
	await close_mongo_connection()

app = FastAPI(title="TinyURL Clone API", lifespan=lifespan)

# CORS configuration
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Record routes
app.include_router(urls.router, tags=["URLs"])

@app.get("/health")
def health_check():
	return {"status": "ok", "db": "mongo"}
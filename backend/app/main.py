from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import urls
from app.db import connect_to_mongo, close_mongo_connection

# Limit configuration
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
	await connect_to_mongo()
	yield
	await close_mongo_connection()

app = FastAPI(title="TinyURL Clone API", lifespan=lifespan)

# Connecting the limiter 
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
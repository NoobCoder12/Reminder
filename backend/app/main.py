from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from db.base import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Funtion gets executed during 'uvicorn main:app command - server start'

    lifespan needs a task, yield and optional task after yield
    """
    Base.metadata.create_all(bind=engine)
    yield

# Async functions need async sessions

load_dotenv()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

# Creating midddleware for Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1", tags=["CRUD"])


@app.get('/')
def index():
    return {"message": "App is working"}

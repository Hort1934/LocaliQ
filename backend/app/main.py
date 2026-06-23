from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, producer
from app.db.base import Base
from app.db.session import engine
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Runs DB table creation on startup (development convenience).
    In production, prefer Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic can be added here (e.g. close connection pools)


app = FastAPI(
    title="LocaliQ API",
    description="API для мапи місцевих виробників України",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — дозволені походження задаються через змінну CORS_ORIGINS у .env
allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(producer.router, prefix="/api/producers", tags=["Producers"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "LocaliQ API працює", "version": "1.0.0"}

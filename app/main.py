from fastapi import FastAPI
from .api.api import api_router
from .core.config import settings
from .db.session import engine
from .db.session import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proyecto Empresa", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

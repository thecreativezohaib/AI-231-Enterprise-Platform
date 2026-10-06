from fastapi import FastAPI
from backend.api import assets, copilot
from backend.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-231 Infrastructure Intelligence API", version="1.0.0")

app.include_router(assets.router)
app.include_router(copilot.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI-231 Platform API is running"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.init_db import init_db
from .routes import company, ai, auth
from .core.database import engine, Base
import os

# Create database tables
init_db()

# Initialize FastAPI app
app = FastAPI(
    title="REVGIN API",
    description="API for REVGIN application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(company.router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/")
async def root():
    return {"message": "Welcome to REVGIN API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

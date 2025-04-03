from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, mutual_funds, investments, users, portfolio
from app.db.models import Base
from app.db.session import engine

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Mutual Fund Dashboard API",
    description="API for the Mutual Fund Dashboard application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(mutual_funds.router, prefix="/api", tags=["Mutual Funds"])
app.include_router(investments.router, prefix="/api", tags=["Investments"])
app.include_router(portfolio.router, prefix="/api", tags=["Portfolio"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Mutual Fund Dashboard API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
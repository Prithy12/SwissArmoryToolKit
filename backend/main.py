from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import review, pipeline, tests
from core.config import settings

app = FastAPI(
    title="DevOps Toolkit API",
    description="AI-powered DevOps toolkit for code review, pipeline optimization, and test generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(review.router, prefix="/api", tags=["Code Review"])
app.include_router(pipeline.router, prefix="/api", tags=["Pipeline"])
app.include_router(tests.router, prefix="/api", tags=["Tests"])

@app.get("/")
async def root():
    return {
        "message": "DevOps Toolkit API",
        "endpoints": [
            "/api/review - Code review analysis",
            "/api/pipeline - Pipeline optimization",
            "/api/tests - Test generation"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

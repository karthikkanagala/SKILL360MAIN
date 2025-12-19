"""
FastAPI Backend for Skill Passport 360
Main application entry point with CORS enabled, MongoDB, and Google API integration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Add src directory to path to import existing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Evolvex-AI-Carrier-Path-main/src')))

from routers import (
    resume,
    career_score,
    github,
    interview,
    learning,
    analytics,
    internship,
    profile,
    certificates,
    mentorship,
    opportunities,
    gap_analysis,
)

# Import database module
try:
    from database import MongoDB, GoogleAPI, init_database, test_google_api
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Database module not available: {e}")
    DATABASE_AVAILABLE = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events - startup and shutdown"""
    # Startup
    print("\n" + "="*60)
    print("🚀 Skill Passport 360 - Starting up...")
    print("="*60)
    
    if DATABASE_AVAILABLE:
        # Initialize MongoDB
        print("\n📦 Initializing MongoDB...")
        db = init_database()
        if db is not None:
            app.state.db = db
        
        # Initialize Google API
        print("\n🤖 Initializing Google Generative AI...")
        test_google_api()
    
    print("\n" + "="*60)
    print("✅ Server is ready!")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down...")
    if DATABASE_AVAILABLE:
        MongoDB.close()
    print("Goodbye! 👋\n")


app = FastAPI(
    title="Skill Passport 360 API",
    description="AI-Powered Career Development Platform with MongoDB and Google Gemini Integration",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware - allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(career_score.router, prefix="/api/career-score", tags=["Career Score"])
app.include_router(github.router, prefix="/api/github", tags=["GitHub"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(internship.router, prefix="/api/internship", tags=["Internship"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(certificates.router, prefix="/api/certificates", tags=["Certificates"])
app.include_router(mentorship.router, prefix="/api/mentorship", tags=["Mentorship"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["Opportunities"])
app.include_router(gap_analysis.router, prefix="/api/gap-analysis", tags=["Gap Analysis"])


@app.get("/")
async def root():
    return {
        "message": "Skill Passport 360 API",
        "version": "2.0.0",
        "status": "running",
        "features": {
            "mongodb": DATABASE_AVAILABLE,
            "google_api": DATABASE_AVAILABLE and GoogleAPI.get_api_key() is not None if DATABASE_AVAILABLE else False
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with service status"""
    status = {
        "status": "healthy",
        "services": {
            "api": True
        }
    }
    
    if DATABASE_AVAILABLE:
        # Check MongoDB
        try:
            client = MongoDB.get_client()
            if client:
                client.admin.command('ping')
                status["services"]["mongodb"] = True
            else:
                status["services"]["mongodb"] = False
        except Exception:
            status["services"]["mongodb"] = False
        
        # Check Google API
        status["services"]["google_api"] = GoogleAPI.get_api_key() is not None
    
    return status


@app.get("/api/gemini/test")
async def test_gemini():
    """Test Google Gemini API endpoint"""
    if not DATABASE_AVAILABLE:
        return {"error": "Database module not available"}
    
    try:
        response = GoogleAPI.generate_content("Say 'Hello from Gemini!' in a friendly way.")
        if response:
            return {"success": True, "response": response}
        else:
            return {"success": False, "error": "No response from Gemini"}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    import socket
    
    port = int(os.getenv("PORT", "8000"))

    # Fail fast if port is in use (prevents frontend pointing at the wrong port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()

    if result == 0:
        raise RuntimeError(
            f"Port {port} is already in use. Stop the process using it, or set PORT to a free port (and update frontend VITE_API_BASE_URL)."
        )

    print(f"🚀 Starting server on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

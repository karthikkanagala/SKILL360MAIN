"""
FastAPI Backend for Skill Passport 360
Main application entry point with CORS enabled
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add src directory to path to import existing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI--main/Evolvex-AI--main/src')))

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

app = FastAPI(
    title="Skill Passport 360 API",
    description="AI-Powered Career Development Platform",
    version="1.0.0"
)

# CORS middleware - allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default port
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
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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



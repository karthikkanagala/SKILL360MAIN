"""
Internship Matching Router
Handles internship matching and recommendations
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from internship_matcher import InternshipMatcher
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class InternshipMatchRequest(BaseModel):
    skills: List[str]
    github_data: Optional[Dict] = None
    career_score: Optional[int] = None
    location: Optional[str] = None

@router.post("/match")
async def match_internships(request: InternshipMatchRequest):
    """
    Match internships based on skills, GitHub profile, and career score
    Returns ranked list of matched internships
    """
    try:
        matcher = InternshipMatcher()
        matches = matcher.match_internships(
            skills=request.skills,
            github_data=request.github_data,
            career_score=request.career_score,
            location=request.location
        )
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching internships: {str(e)}")

@router.get("/list")
async def list_all_internships():
    """Get list of all available internships"""
    try:
        # This would fetch from your internship database/scraper
        return {"internships": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing internships: {str(e)}")



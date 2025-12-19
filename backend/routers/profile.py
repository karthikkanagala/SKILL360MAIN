"""
Profile Management Router
Handles profile completeness, demo profile, and general profile operations
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from demo_profile import check_profile_completeness, get_demo_profile, load_demo_profile_to_session
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class ProfileData(BaseModel):
    resume_text: Optional[str] = None
    resume_skills: Optional[list] = None
    ats_score: Optional[int] = None
    github_analysis: Optional[Dict] = None
    validated_certificates: Optional[list] = None
    activities: Optional[list] = None
    interview_evaluations: Optional[list] = None
    career_score_data: Optional[Dict] = None

@router.post("/completeness")
async def check_completeness(profile: ProfileData):
    """Check profile completeness percentage"""
    try:
        # Convert Pydantic model to dict for session state-like structure
        session_state = profile.dict(exclude_none=True)
        completeness = check_profile_completeness(session_state)
        return completeness
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking completeness: {str(e)}")

@router.get("/demo")
async def get_demo_profile_data():
    """Get demo profile data"""
    try:
        demo = get_demo_profile()
        return demo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demo profile: {str(e)}")

@router.post("/stats")
async def get_profile_stats(profile: ProfileData):
    """Get quick profile statistics"""
    try:
        stats = {
            "has_resume": bool(profile.resume_text),
            "has_github": bool(profile.github_analysis),
            "has_certificates": bool(profile.validated_certificates and len(profile.validated_certificates) > 0),
            "has_activities": bool(profile.activities and len(profile.activities) > 0),
            "ats_score": profile.ats_score or 0,
            "cert_count": len(profile.validated_certificates) if profile.validated_certificates else 0,
            "activity_count": len(profile.activities) if profile.activities else 0,
            "career_score": profile.career_score_data.get('total_score') if profile.career_score_data else None
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")



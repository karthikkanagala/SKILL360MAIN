"""Mentorship Matching Router
Provides mentorship matches similar to the Streamlit mentor matching experience.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

router = APIRouter()


class MentorshipMatchRequest(BaseModel):
    skills: List[str]
    experience_level: str = 'Beginner'
    mentorship_type: str = 'Career'


@router.post('/match')
async def match_mentors(request: MentorshipMatchRequest) -> Dict[str, Any]:
    try:
        from ai_networking import AINetworkingEngine

        engine = AINetworkingEngine()
        mentors = engine.find_mentorship_opportunities(
            skills=request.skills,
            experience_level=request.experience_level,
            mentorship_type=request.mentorship_type,
        )

        # Convert dataclasses to dicts
        results = [m.__dict__ for m in mentors]
        return {
            "matches": results,
            "model_used": "rules+mock",  # consistent with Evolvex engine currently producing mock data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching mentors: {str(e)}")

"""
Career Score Calculator Router
Handles holistic career score calculation (0-1000)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from career_score_calculator import get_career_score_calculator
    from progress_tracker import get_progress_tracker
    from activity_tracker import get_activity_tracker
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class CareerScoreRequest(BaseModel):
    resume_data: Optional[Dict] = None
    github_data: Optional[Dict] = None
    certificates: Optional[List[Dict]] = None
    activities: Optional[List[Dict]] = None
    interview_data: Optional[Dict] = None
    portfolio_analysis: Optional[Dict] = None

@router.post("/calculate")
async def calculate_career_score(request: CareerScoreRequest):
    """
    Calculate comprehensive career score (0-1000) based on all profile components
    """
    try:
        calculator = get_career_score_calculator()
        progress_tracker = get_progress_tracker()
        progress_summary = progress_tracker.get_progress_summary()
        
        profile_data = {
            'resume_data': request.resume_data or {},
            'github_data': request.github_data or {},
            'certificates': request.certificates or [],
            'activities': request.activities or [],
            'activity_summary': None,
            'portfolio_analysis': request.portfolio_analysis or {},
            'interview_data': request.interview_data or {},
            'progress_data': progress_summary
        }
        
        # Get activity summary if activities exist
        if request.activities:
            tracker = get_activity_tracker()
            profile_data['activity_summary'] = tracker.get_activity_summary(request.activities)
        
        score_result = calculator.calculate_career_score(profile_data)
        
        return score_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating career score: {str(e)}")

@router.get("/history")
async def get_career_score_history():
    """Get career score history"""
    try:
        calculator = get_career_score_calculator()
        history_file = calculator.score_history_file
        if os.path.exists(history_file):
            import json
            with open(history_file, 'r') as f:
                history = json.load(f)
            return history
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving score history: {str(e)}")



"""
GitHub Analysis Router
Handles GitHub profile analysis and portfolio scoring
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from github_analyzer import analyze_github_profile
    from portfolio_analyzer import analyze_portfolio
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class GitHubAnalysisRequest(BaseModel):
    username: str

@router.post("/analyze")
async def analyze_github(request: GitHubAnalysisRequest):
    """
    Analyze GitHub profile and repositories
    Returns comprehensive analysis including statistics, top repos, languages, etc.
    """
    try:
        analysis = analyze_github_profile(request.username)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing GitHub profile: {str(e)}")

@router.post("/portfolio")
async def analyze_portfolio_endpoint(request: GitHubAnalysisRequest):
    """
    Analyze GitHub portfolio and provide scoring
    """
    try:
        portfolio = analyze_portfolio(request.username)
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing portfolio: {str(e)}")



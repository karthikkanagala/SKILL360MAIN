"""
Career Score Calculator Router - Enhanced with Gemini AI
Calculates holistic career score (0-1000) with AI-powered insights
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

# Import ML modules
try:
    from career_score_calculator import get_career_score_calculator
    from progress_tracker import get_progress_tracker
    from activity_tracker import get_activity_tracker
    ML_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import ML modules: {e}")
    ML_MODULES_AVAILABLE = False

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()


class CareerScoreRequest(BaseModel):
    resume_data: Optional[Dict] = None
    github_data: Optional[Dict] = None
    certificates: Optional[List[Dict]] = None
    activities: Optional[List[Dict]] = None
    interview_data: Optional[Dict] = None
    portfolio_analysis: Optional[Dict] = None
    skills: Optional[List[str]] = None
    target_role: Optional[str] = None


async def get_ai_career_insights(score_data: Dict, target_role: Optional[str] = None) -> Dict:
    """Get AI-powered career insights based on score breakdown"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""As a career advisor, analyze this profile and provide actionable insights:

CAREER SCORE BREAKDOWN:
- Total Score: {score_data.get('total_score', 0)}/1000
- Resume Score: {score_data.get('breakdown', {}).get('resume', 0)}/200
- GitHub Score: {score_data.get('breakdown', {}).get('github', 0)}/200
- Certificates: {score_data.get('breakdown', {}).get('certificates', 0)}/150
- Activities: {score_data.get('breakdown', {}).get('activities', 0)}/150
- Portfolio: {score_data.get('breakdown', {}).get('portfolio', 0)}/150
- Interview: {score_data.get('breakdown', {}).get('interview', 0)}/150

TARGET ROLE: {target_role or 'Software Developer'}

Provide:
1. TOP 3 strengths
2. TOP 3 areas to improve (specific actions)
3. Recommended next steps for career growth
4. Estimated time to reach 800+ score

Be specific and actionable. Keep under 250 words."""

        response = GoogleAPI.generate_content(prompt)
        return {
            "ai_insights": response,
            "ai_powered": True
        }
    except Exception as e:
        print(f"Gemini insights failed: {e}")
        return None


def calculate_fallback_score(request: CareerScoreRequest) -> Dict:
    """Fallback career score calculation when ML modules unavailable"""
    score = 0
    breakdown = {}
    
    # Resume score (max 200)
    if request.resume_data:
        ats_score = request.resume_data.get('ats_score', 0)
        skills_count = len(request.resume_data.get('skills', []))
        resume_score = min(200, int(ats_score * 1.5) + skills_count * 5)
        breakdown['resume'] = resume_score
        score += resume_score
    else:
        breakdown['resume'] = 0
    
    # GitHub score (max 200)
    if request.github_data:
        repos = request.github_data.get('repos', 0)
        stars = request.github_data.get('stars', 0)
        contribution_score = request.github_data.get('contribution_score', 0)
        github_score = min(200, repos * 3 + stars * 2 + contribution_score)
        breakdown['github'] = github_score
        score += github_score
    else:
        breakdown['github'] = 0
    
    # Certificates score (max 150)
    if request.certificates:
        verified = sum(1 for c in request.certificates if c.get('verified', False))
        total = len(request.certificates)
        cert_score = min(150, verified * 30 + (total - verified) * 15)
        breakdown['certificates'] = cert_score
        score += cert_score
    else:
        breakdown['certificates'] = 0
    
    # Activities score (max 150)
    if request.activities:
        activity_score = min(150, len(request.activities) * 20)
        breakdown['activities'] = activity_score
        score += activity_score
    else:
        breakdown['activities'] = 0
    
    # Portfolio score (max 150)
    if request.portfolio_analysis:
        portfolio_strength = request.portfolio_analysis.get('portfolio_strength', 0)
        breakdown['portfolio'] = min(150, int(portfolio_strength * 1.5))
        score += breakdown['portfolio']
    else:
        breakdown['portfolio'] = 0
    
    # Interview score (max 150)
    if request.interview_data:
        interview_score = request.interview_data.get('score', 0)
        breakdown['interview'] = min(150, int(interview_score * 1.5))
        score += breakdown['interview']
    else:
        breakdown['interview'] = 0
    
    # Calculate percentile
    percentile = min(99, max(1, int(score / 10)))
    
    # Determine level
    if score >= 800:
        level = "Expert"
    elif score >= 600:
        level = "Advanced"
    elif score >= 400:
        level = "Intermediate"
    elif score >= 200:
        level = "Beginner"
    else:
        level = "Starter"
    
    return {
        "total_score": score,
        "max_score": 1000,
        "breakdown": breakdown,
        "percentile": percentile,
        "level": level,
        "recommendations": generate_recommendations(breakdown)
    }


def generate_recommendations(breakdown: Dict) -> List[str]:
    """Generate recommendations based on score breakdown"""
    recommendations = []
    
    if breakdown.get('resume', 0) < 100:
        recommendations.append("Improve your resume ATS score by adding more relevant keywords and skills")
    
    if breakdown.get('github', 0) < 100:
        recommendations.append("Increase GitHub activity with more commits, projects, and contributions")
    
    if breakdown.get('certificates', 0) < 75:
        recommendations.append("Add verified certifications from platforms like Coursera, Google, or AWS")
    
    if breakdown.get('portfolio', 0) < 75:
        recommendations.append("Build a stronger portfolio with diverse, well-documented projects")
    
    if breakdown.get('activities', 0) < 75:
        recommendations.append("Participate in hackathons, open-source projects, or coding competitions")
    
    if not recommendations:
        recommendations.append("Great progress! Focus on advanced certifications and leadership opportunities")
    
    return recommendations


@router.post("/calculate")
async def calculate_career_score(request: CareerScoreRequest):
    """
    Calculate comprehensive career score (0-1000) with AI insights
    Uses ML models when available, falls back to weighted calculation
    """
    try:
        score_result = None
        
        # Try ML-based calculation
        if ML_MODULES_AVAILABLE:
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
                
                if request.activities:
                    tracker = get_activity_tracker()
                    profile_data['activity_summary'] = tracker.get_activity_summary(request.activities)
                
                score_result = calculator.calculate_career_score(profile_data)
                score_result['ml_powered'] = True
            except Exception as e:
                print(f"ML calculation failed: {e}")
                score_result = None
        
        # Fallback to weighted calculation
        if not score_result:
            score_result = calculate_fallback_score(request)
            score_result['ml_powered'] = False
        
        # Add AI insights
        ai_insights = await get_ai_career_insights(score_result, request.target_role)
        if ai_insights:
            score_result['ai_insights'] = ai_insights.get('ai_insights')
            score_result['ai_powered'] = True
        else:
            score_result['ai_powered'] = False
        
        return score_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating career score: {str(e)}")


@router.get("/history")
async def get_career_score_history():
    """Get career score history"""
    try:
        if ML_MODULES_AVAILABLE:
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


@router.post("/analyze")
async def analyze_career_path(request: CareerScoreRequest):
    """Get AI-powered career path analysis"""
    if not GEMINI_AVAILABLE:
        return {
            "analysis": "AI analysis not available. Please configure Gemini API.",
            "ai_powered": False
        }
    
    try:
        skills = request.skills or []
        target_role = request.target_role or "Software Developer"
        
        prompt = f"""As a career counselor, provide a detailed career path analysis:

CURRENT SKILLS: {', '.join(skills) if skills else 'Not specified'}
TARGET ROLE: {target_role}

Provide:
1. Career Roadmap (6-12 months)
2. Skills to Acquire (prioritized)
3. Recommended Projects to Build
4. Certifications to Pursue
5. Interview Preparation Tips
6. Salary Expectations (India market)

Be specific, practical, and encouraging. Format clearly."""

        response = GoogleAPI.generate_content(prompt)
        
        return {
            "analysis": response,
            "target_role": target_role,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing career path: {str(e)}")

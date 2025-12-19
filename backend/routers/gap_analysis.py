"""Gap Analysis Router - Enhanced with Gemini AI
Identifies skill gaps for a target/dream role and recommends courses + projects.
Uses Gemini AI for intelligent analysis and ML models for course recommendations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()


class GapAnalysisRequest(BaseModel):
    target_role: str
    job_description: str = ''
    current_skills: List[str] = []
    resume_text: str = ''
    experience_years: Optional[int] = 0


def _to_course_dict(course) -> Dict[str, Any]:
    """Convert course object to dictionary"""
    return {
        "title": getattr(course, 'title', ''),
        "platform": getattr(course, 'platform', ''),
        "url": getattr(course, 'url', ''),
        "difficulty": getattr(getattr(course, 'difficulty', None), 'value', getattr(course, 'difficulty', None)),
        "course_type": getattr(getattr(course, 'course_type', None), 'value', getattr(course, 'course_type', None)),
        "duration": getattr(course, 'duration', ''),
        "rating": getattr(course, 'rating', None),
        "price": getattr(course, 'price', None),
        "description": getattr(course, 'description', None),
        "skills_covered": getattr(course, 'skills_covered', None),
        "prerequisites": getattr(course, 'prerequisites', None),
    }


async def gemini_analyze_gap(current_skills: List[str], target_role: str, job_description: str = "") -> Dict:
    """Use Gemini for intelligent gap analysis"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Analyze the skill gap for this career transition:

CURRENT SKILLS: {', '.join(current_skills) if current_skills else 'Not specified'}
TARGET ROLE: {target_role}
JOB DESCRIPTION: {job_description[:500] if job_description else 'Not provided'}

Provide detailed analysis:

1. FIT SCORE (0-100): How ready is the candidate?

2. MUST-HAVE SKILLS MISSING: List critical skills needed (max 5)

3. NICE-TO-HAVE SKILLS: Additional skills that would help (max 3)

4. LEARNING PRIORITY: Rank the missing skills by importance

5. TIMELINE ESTIMATE: How long to become job-ready?

6. SPECIFIC RECOMMENDATIONS:
   - Best courses/certifications
   - Projects to build
   - Resources to use

7. STRENGTHS TO HIGHLIGHT: What current skills are valuable?

Be specific, practical, and encouraging."""

        response = GoogleAPI.generate_content(prompt)
        
        if response:
            # Try to extract fit score
            import re
            fit_score = 50  # Default
            score_match = re.search(r'fit\s*score[:\s]*(\d+)', response.lower())
            if score_match:
                fit_score = min(100, max(0, int(score_match.group(1))))
            
            return {
                "ai_analysis": response,
                "fit_score": fit_score,
                "ai_powered": True
            }
        return None
    except Exception as e:
        print(f"Gemini gap analysis failed: {e}")
        return None


async def gemini_get_learning_roadmap(current_skills: List[str], target_role: str, missing_skills: List[str]) -> str:
    """Get AI-powered learning roadmap"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Create a detailed 3-month learning roadmap:

CURRENT SKILLS: {', '.join(current_skills[:10])}
TARGET ROLE: {target_role}
SKILLS TO LEARN: {', '.join(missing_skills[:5])}

Provide week-by-week plan including:
- Specific topics to learn each week
- Resources (courses, tutorials, docs)
- Mini-projects to build
- Time allocation suggestions
- Milestones to track progress

Be specific and actionable. Format as a clear timeline."""

        return GoogleAPI.generate_content(prompt)
    except:
        return None


@router.post('/analyze')
async def analyze_gap(request: GapAnalysisRequest) -> Dict[str, Any]:
    """Analyze skill gap with AI and ML models"""
    try:
        from skills import extract_skills
        from project_ideas import generate_project_ideas
        from course_suggestions import get_course_suggestions, get_learning_path

        # Collect current skills
        current = set([s.strip().lower() for s in (request.current_skills or []) if s and str(s).strip()])

        # Extract skills from resume
        if request.resume_text and len(request.resume_text.strip()) > 50:
            try:
                current.update([s.strip().lower() for s in extract_skills(request.resume_text)])
            except Exception:
                pass

        # Extract desired skills from JD
        desired = set()
        if request.job_description and len(request.job_description.strip()) > 30:
            try:
                desired.update([s.strip().lower() for s in extract_skills(request.job_description)])
            except Exception:
                pass

        # Fallback: use role keywords
        if not desired:
            role_tokens = [t.strip().lower() for t in request.target_role.replace('/', ' ').replace('-', ' ').split() if len(t) > 2]
            desired.update(role_tokens)

        missing = sorted(list(desired - current))

        # Calculate fit score
        if len(desired) == 0:
            fit_score = 0
        else:
            fit_score = int(round(100 * (1 - (len(missing) / max(len(desired), 1)))))

        # Get course recommendations
        top_missing = [m for m in missing if m][:5]
        course_suggestions = get_course_suggestions(top_missing, max_courses_per_skill=3) if top_missing else {}
        courses_out: Dict[str, List[Dict[str, Any]]] = {
            k: [_to_course_dict(c) for c in v] for k, v in course_suggestions.items()
        }

        # Get learning path
        path_skills = top_missing[:2] if top_missing else list(desired)[:2]
        learning_path = get_learning_path(path_skills)
        learning_path_out = {
            level: [_to_course_dict(c) for c in courses[:6]] for level, courses in learning_path.items()
        }

        # Get project ideas
        project_ideas = generate_project_ideas(
            skills=top_missing or list(desired)[:3], 
            difficulty='intermediate', 
            num_ideas=5
        )

        # Get AI analysis
        ai_result = await gemini_analyze_gap(
            list(current), 
            request.target_role, 
            request.job_description
        )
        
        # Get AI roadmap for significant gaps
        ai_roadmap = None
        if len(missing) > 2 and GEMINI_AVAILABLE:
            ai_roadmap = await gemini_get_learning_roadmap(
                list(current),
                request.target_role,
                missing[:5]
            )

        result = {
            "target_role": request.target_role,
            "current_skills": sorted(list(current)),
            "desired_skills": sorted(list(desired)),
            "missing_skills": top_missing,
            "fit_score": ai_result.get('fit_score', fit_score) if ai_result else fit_score,
            "recommended_courses": courses_out,
            "recommended_learning_path": learning_path_out,
            "recommended_projects": project_ideas,
            "model_used": "gemini+ml" if ai_result else "heuristic",
        }
        
        if ai_result:
            result["ai_analysis"] = ai_result.get("ai_analysis")
            result["ai_powered"] = True
        
        if ai_roadmap:
            result["learning_roadmap"] = ai_roadmap

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running gap analysis: {str(e)}")


@router.post('/roadmap')
async def get_career_roadmap(request: GapAnalysisRequest) -> Dict[str, Any]:
    """Get AI-powered career roadmap"""
    if not GEMINI_AVAILABLE:
        return {
            "roadmap": "AI roadmap generation requires Gemini API configuration.",
            "ai_powered": False
        }
    
    try:
        prompt = f"""Create a comprehensive career roadmap:

TARGET ROLE: {request.target_role}
CURRENT SKILLS: {', '.join(request.current_skills) if request.current_skills else 'Beginner'}
EXPERIENCE: {request.experience_years or 0} years

Provide:
1. PHASE 1 (Month 1-2): Foundation building
2. PHASE 2 (Month 3-4): Core skills development
3. PHASE 3 (Month 5-6): Advanced skills & projects
4. PHASE 4 (Month 6+): Job preparation

For each phase include:
- Skills to focus on
- Resources to use
- Projects to build
- Certifications to target
- Milestones to achieve

Be specific and practical for the Indian job market."""

        response = GoogleAPI.generate_content(prompt)
        
        return {
            "target_role": request.target_role,
            "roadmap": response,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

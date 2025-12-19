"""Gap Analysis Router
Identifies skill gaps for a target/dream role and recommends courses + projects.
Hackathon mode: deterministic heuristics, plus calls to existing course/project recommenders.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

router = APIRouter()


class GapAnalysisRequest(BaseModel):
    target_role: str
    job_description: str = ''
    current_skills: List[str] = []
    resume_text: str = ''


def _to_course_dict(course) -> Dict[str, Any]:
    # course_suggestions.Course dataclass
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


@router.post('/analyze')
async def analyze_gap(request: GapAnalysisRequest) -> Dict[str, Any]:
    try:
        from skills import extract_skills
        from project_ideas import generate_project_ideas
        from course_suggestions import get_course_suggestions, get_learning_path

        current = set([s.strip().lower() for s in (request.current_skills or []) if s and str(s).strip()])

        # augment current from resume text
        if request.resume_text and len(request.resume_text.strip()) > 50:
            try:
                current.update([s.strip().lower() for s in extract_skills(request.resume_text)])
            except Exception:
                pass

        desired = set()
        if request.job_description and len(request.job_description.strip()) > 30:
            try:
                desired.update([s.strip().lower() for s in extract_skills(request.job_description)])
            except Exception:
                pass

        # If no JD skills, use role keywords
        if not desired:
            role_tokens = [t.strip().lower() for t in request.target_role.replace('/', ' ').replace('-', ' ').split() if len(t) > 2]
            desired.update(role_tokens)

        missing = sorted(list(desired - current))

        # Heuristic fit score
        if len(desired) == 0:
            fit_score = 0
        else:
            fit_score = int(round(100 * (1 - (len(missing) / max(len(desired), 1)))))

        # Recommend courses for top missing skills
        top_missing = [m for m in missing if m][:5]
        course_suggestions = get_course_suggestions(top_missing, max_courses_per_skill=3) if top_missing else {}
        courses_out: Dict[str, List[Dict[str, Any]]] = {
            k: [_to_course_dict(c) for c in v] for k, v in course_suggestions.items()
        }

        # Learning path for the role
        path_skills = top_missing[:2] if top_missing else list(desired)[:2]
        learning_path = get_learning_path(path_skills)
        learning_path_out = {
            level: [_to_course_dict(c) for c in courses[:6]] for level, courses in learning_path.items()
        }

        # Project ideas based on missing skills
        project_ideas = generate_project_ideas(skills=top_missing or list(desired)[:3], difficulty='intermediate', num_ideas=5)

        return {
            "target_role": request.target_role,
            "current_skills": sorted(list(current)),
            "desired_skills": sorted(list(desired)),
            "missing_skills": top_missing,
            "fit_score": fit_score,
            "recommended_courses": courses_out,
            "recommended_learning_path": learning_path_out,
            "recommended_projects": project_ideas,
            "model_used": "heuristic",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running gap analysis: {str(e)}")

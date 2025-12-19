"""
Learning Resources Router
Handles course recommendations, learning paths, and progress tracking
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from course_suggestions import get_course_suggestions, get_ai_course_recommendations
    from course_tracker import CourseTracker
    from project_ideas import generate_project_ideas
    from learning_resources import get_learning_resources
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class CourseSearchRequest(BaseModel):
    skill: str
    difficulty: Optional[str] = None

class LearningPathRequest(BaseModel):
    target_role: str
    current_skills: List[str]

class ProjectIdeasRequest(BaseModel):
    skills: List[str]
    difficulty: Optional[str] = "intermediate"
    num_ideas: int = 5

@router.post("/courses/search")
async def search_courses(request: CourseSearchRequest):
    """Search for courses by skill"""
    try:
        courses = get_course_suggestions(request.skill, difficulty=request.difficulty)
        return {"courses": courses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching courses: {str(e)}")

@router.post("/courses/ai-recommendations")
async def get_ai_courses(request: CourseSearchRequest):
    """Get AI-powered course recommendations"""
    try:
        recommendations = get_ai_course_recommendations(request.skill)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AI recommendations: {str(e)}")

@router.post("/learning-path")
async def generate_learning_path(request: LearningPathRequest):
    """Generate personalized learning path"""
    try:
        # This would use your learning path generation logic
        return {"learning_path": "Generated learning path", "target_role": request.target_role}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")

@router.post("/project-ideas")
async def generate_projects(request: ProjectIdeasRequest):
    """Generate project ideas based on skills"""
    try:
        ideas = generate_project_ideas(
            skills=request.skills,
            difficulty=request.difficulty,
            num_ideas=request.num_ideas
        )
        return {"project_ideas": ideas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project ideas: {str(e)}")

@router.get("/resources/{skill}")
async def get_resources(skill: str):
    """Get learning resources for a skill"""
    try:
        resources = get_learning_resources(skill)
        return {"resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resources: {str(e)}")



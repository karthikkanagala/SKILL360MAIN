"""
Learning Resources Router - Enhanced with Gemini AI
Handles course recommendations, learning paths, and skill gap analysis
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
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


# ==================== Course Database ====================

COURSES_DB = {
    "Python": [
        {"title": "Python for Everybody", "platform": "Coursera", "url": "https://coursera.org/specializations/python", "duration": "8 weeks", "level": "Beginner", "rating": 4.8},
        {"title": "Complete Python Bootcamp", "platform": "Udemy", "url": "https://udemy.com/course/complete-python-bootcamp", "duration": "22 hours", "level": "Beginner", "rating": 4.6},
        {"title": "Python for Data Science", "platform": "DataCamp", "url": "https://datacamp.com/courses/intro-to-python", "duration": "4 hours", "level": "Beginner", "rating": 4.5},
    ],
    "JavaScript": [
        {"title": "JavaScript: Understanding the Weird Parts", "platform": "Udemy", "url": "https://udemy.com/course/understand-javascript", "duration": "12 hours", "level": "Intermediate", "rating": 4.7},
        {"title": "The Complete JavaScript Course", "platform": "Udemy", "url": "https://udemy.com/course/the-complete-javascript-course", "duration": "69 hours", "level": "Beginner", "rating": 4.7},
        {"title": "JavaScript Algorithms and Data Structures", "platform": "freeCodeCamp", "url": "https://freecodecamp.org/learn/javascript-algorithms-and-data-structures", "duration": "300 hours", "level": "Intermediate", "rating": 4.8},
    ],
    "React": [
        {"title": "React - The Complete Guide", "platform": "Udemy", "url": "https://udemy.com/course/react-the-complete-guide", "duration": "48 hours", "level": "Intermediate", "rating": 4.7},
        {"title": "Full-Stack Web Development with React", "platform": "Coursera", "url": "https://coursera.org/specializations/full-stack-react", "duration": "4 months", "level": "Intermediate", "rating": 4.6},
    ],
    "Machine Learning": [
        {"title": "Machine Learning by Andrew Ng", "platform": "Coursera", "url": "https://coursera.org/learn/machine-learning", "duration": "11 weeks", "level": "Intermediate", "rating": 4.9},
        {"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://coursera.org/specializations/deep-learning", "duration": "5 months", "level": "Advanced", "rating": 4.9},
        {"title": "Practical Deep Learning for Coders", "platform": "fast.ai", "url": "https://course.fast.ai", "duration": "7 weeks", "level": "Intermediate", "rating": 4.8},
    ],
    "AWS": [
        {"title": "AWS Certified Solutions Architect", "platform": "AWS Training", "url": "https://aws.amazon.com/training/architect", "duration": "40 hours", "level": "Intermediate", "rating": 4.7},
        {"title": "AWS Cloud Practitioner Essentials", "platform": "AWS Training", "url": "https://aws.amazon.com/training/cloud-practitioner", "duration": "6 hours", "level": "Beginner", "rating": 4.6},
    ],
    "Docker": [
        {"title": "Docker & Kubernetes: The Practical Guide", "platform": "Udemy", "url": "https://udemy.com/course/docker-kubernetes-the-practical-guide", "duration": "24 hours", "level": "Intermediate", "rating": 4.7},
        {"title": "Docker for the Absolute Beginner", "platform": "KodeKloud", "url": "https://kodekloud.com/courses/docker-for-absolute-beginner", "duration": "3 hours", "level": "Beginner", "rating": 4.5},
    ],
    "SQL": [
        {"title": "SQL for Data Science", "platform": "Coursera", "url": "https://coursera.org/learn/sql-for-data-science", "duration": "4 weeks", "level": "Beginner", "rating": 4.6},
        {"title": "The Complete SQL Bootcamp", "platform": "Udemy", "url": "https://udemy.com/course/the-complete-sql-bootcamp", "duration": "9 hours", "level": "Beginner", "rating": 4.7},
    ],
    "Git": [
        {"title": "Git Complete: The definitive guide", "platform": "Udemy", "url": "https://udemy.com/course/git-complete", "duration": "6 hours", "level": "Beginner", "rating": 4.6},
        {"title": "Version Control with Git", "platform": "Coursera", "url": "https://coursera.org/learn/version-control-with-git", "duration": "4 weeks", "level": "Beginner", "rating": 4.5},
    ],
    "Data Structures": [
        {"title": "Data Structures and Algorithms", "platform": "Coursera", "url": "https://coursera.org/specializations/data-structures-algorithms", "duration": "6 months", "level": "Intermediate", "rating": 4.7},
        {"title": "Master the Coding Interview", "platform": "Udemy", "url": "https://udemy.com/course/master-the-coding-interview", "duration": "20 hours", "level": "Intermediate", "rating": 4.7},
    ],
}


# ==================== Pydantic Models ====================

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


class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_skills: List[str]


# ==================== Helper Functions ====================

def get_courses_for_skill(skill: str, difficulty: Optional[str] = None) -> List[Dict]:
    """Get courses for a skill from the database"""
    courses = COURSES_DB.get(skill, [])
    
    if not courses:
        # Try partial matching
        for key in COURSES_DB:
            if skill.lower() in key.lower() or key.lower() in skill.lower():
                courses = COURSES_DB[key]
                break
    
    if difficulty:
        courses = [c for c in courses if c.get('level', '').lower() == difficulty.lower()]
    
    return courses


async def generate_ai_learning_path(target_role: str, current_skills: List[str]) -> Dict:
    """Generate AI-powered learning path using Gemini"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""
Create a structured learning path for someone who wants to become a {target_role}.

Their current skills are: {', '.join(current_skills[:15])}

Format your response as a structured plan with:
1. Phase 1: Foundation (skills to learn first)
2. Phase 2: Core Skills (main skills for the role)
3. Phase 3: Advanced Skills (to stand out)
4. Project recommendations for each phase
5. Estimated time to complete each phase

Keep response under 400 words and be specific about courses/resources.
"""
        response = GoogleAPI.generate_content(prompt)
        return {"learning_path": response, "ai_generated": True}
    except Exception as e:
        print(f"AI learning path generation failed: {e}")
        return None


async def generate_ai_project_ideas(skills: List[str], difficulty: str, num_ideas: int) -> List[Dict]:
    """Generate project ideas using Gemini"""
    if not GEMINI_AVAILABLE:
        return get_fallback_project_ideas(skills, difficulty, num_ideas)
    
    try:
        prompt = f"""
Generate {num_ideas} unique project ideas for a developer with these skills: {', '.join(skills[:10])}
Difficulty level: {difficulty}

For each project, provide:
1. Title (catchy name)
2. Description (2-3 sentences)
3. Technologies to use
4. Key features to implement
5. Estimated completion time

Format as a numbered list. Make projects practical and resume-worthy.
"""
        response = GoogleAPI.generate_content(prompt)
        
        # Parse the response into structured format
        projects = []
        if response:
            # Simple parsing - in production you'd want better parsing
            projects.append({
                "title": "AI Project Ideas",
                "description": response[:500],
                "technologies": skills[:5],
                "difficulty": difficulty,
                "ai_generated": True
            })
        
        return projects
    except Exception:
        return get_fallback_project_ideas(skills, difficulty, num_ideas)


def get_fallback_project_ideas(skills: List[str], difficulty: str, num_ideas: int) -> List[Dict]:
    """Fallback project ideas when AI is unavailable"""
    ideas = [
        {"title": "Personal Portfolio Website", "description": "Build a responsive portfolio showcasing your projects", "technologies": ["HTML", "CSS", "JavaScript", "React"], "difficulty": "beginner"},
        {"title": "Task Management App", "description": "Full-stack app with user auth, CRUD operations, and real-time updates", "technologies": ["React", "Node.js", "MongoDB"], "difficulty": "intermediate"},
        {"title": "AI Chatbot", "description": "Build a chatbot using NLP and machine learning", "technologies": ["Python", "TensorFlow", "Flask"], "difficulty": "intermediate"},
        {"title": "E-commerce Platform", "description": "Complete e-commerce with cart, payments, and admin dashboard", "technologies": ["React", "Django", "PostgreSQL", "Stripe"], "difficulty": "advanced"},
        {"title": "Real-time Analytics Dashboard", "description": "Dashboard visualizing live data with charts and filters", "technologies": ["React", "D3.js", "WebSocket", "FastAPI"], "difficulty": "advanced"},
    ]
    
    # Filter by difficulty
    filtered = [p for p in ideas if p['difficulty'] == difficulty] or ideas
    return filtered[:num_ideas]


# ==================== API Endpoints ====================

@router.post("/courses/search")
async def search_courses(request: CourseSearchRequest):
    """Search for courses by skill"""
    courses = get_courses_for_skill(request.skill, request.difficulty)
    
    if not courses:
        # Generate fallback
        courses = [{
            "title": f"Learn {request.skill}",
            "platform": "Various",
            "url": f"https://www.google.com/search?q=best+{request.skill}+course",
            "duration": "Self-paced",
            "level": request.difficulty or "All Levels",
            "rating": 4.0
        }]
    
    return {"courses": courses, "total": len(courses)}


@router.post("/courses/ai-recommendations")
async def get_ai_courses(request: CourseSearchRequest):
    """Get AI-powered course recommendations"""
    courses = get_courses_for_skill(request.skill, request.difficulty)
    
    # AI enhancement
    ai_advice = None
    if GEMINI_AVAILABLE:
        try:
            prompt = f"In 2-3 sentences, explain why learning {request.skill} is valuable for a software developer's career and what to focus on."
            ai_advice = GoogleAPI.generate_content(prompt)
        except Exception:
            pass
    
    return {
        "skill": request.skill,
        "courses": courses,
        "ai_advice": ai_advice,
        "total": len(courses)
    }


@router.post("/learning-path")
async def generate_learning_path(request: LearningPathRequest):
    """Generate personalized learning path with AI"""
    # Get AI learning path
    ai_path = await generate_ai_learning_path(request.target_role, request.current_skills)
    
    if ai_path:
        return ai_path
    
    # Fallback to static path
    return {
        "target_role": request.target_role,
        "current_skills": request.current_skills,
        "learning_path": f"Learning path for {request.target_role}",
        "phases": [
            {"name": "Foundation", "skills": ["Programming Basics", "Data Structures"]},
            {"name": "Core", "skills": ["Core Technologies for " + request.target_role]},
            {"name": "Advanced", "skills": ["Advanced Topics", "System Design"]}
        ],
        "ai_generated": False
    }


@router.post("/project-ideas")
async def generate_projects(request: ProjectIdeasRequest):
    """Generate project ideas based on skills using AI"""
    ideas = await generate_ai_project_ideas(
        request.skills,
        request.difficulty,
        request.num_ideas
    )
    
    return {"project_ideas": ideas, "total": len(ideas)}


@router.post("/skill-gap-analysis")
async def analyze_skill_gaps(request: SkillGapRequest):
    """Analyze skill gaps and recommend courses"""
    current_lower = [s.lower() for s in request.current_skills]
    
    missing_skills = [
        skill for skill in request.target_skills 
        if skill.lower() not in current_lower
    ]
    
    # Get course recommendations for missing skills
    recommendations = []
    for skill in missing_skills[:5]:
        courses = get_courses_for_skill(skill)
        if courses:
            recommendations.append({
                "skill": skill,
                "courses": courses[:2]
            })
    
    # AI analysis
    ai_analysis = None
    if GEMINI_AVAILABLE and missing_skills:
        try:
            prompt = f"A developer has these skills: {', '.join(request.current_skills[:10])}. They want to learn: {', '.join(missing_skills[:5])}. In 3-4 sentences, suggest the best order to learn these skills and why."
            ai_analysis = GoogleAPI.generate_content(prompt)
        except Exception:
            pass
    
    return {
        "current_skills": request.current_skills,
        "target_skills": request.target_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
        "ai_analysis": ai_analysis,
        "gap_percentage": (len(missing_skills) / len(request.target_skills) * 100) if request.target_skills else 0
    }


@router.get("/resources/{skill}")
async def get_resources(skill: str):
    """Get learning resources for a skill"""
    courses = get_courses_for_skill(skill)
    
    return {
        "skill": skill,
        "courses": courses,
        "documentation": f"https://developer.mozilla.org/search?q={skill}",
        "tutorials": f"https://www.youtube.com/results?search_query={skill}+tutorial",
        "practice": f"https://leetcode.com/problemset/?search={skill}"
    }

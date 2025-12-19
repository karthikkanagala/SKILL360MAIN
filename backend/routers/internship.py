"""
Internship Matching Router - Enhanced with Gemini AI
Handles internship matching, recommendations, and skill analysis
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


# ==================== Sample Internship Database ====================

INTERNSHIPS_DB = [
    {
        "id": "1",
        "title": "Software Engineering Intern",
        "company": "Google",
        "location": "Remote / Bangalore",
        "skills_required": ["Python", "Java", "Data Structures", "Algorithms"],
        "duration": "3 months",
        "stipend": "₹80,000/month",
        "description": "Work on core Google products with experienced engineers",
        "apply_link": "https://careers.google.com/students"
    },
    {
        "id": "2",
        "title": "ML/AI Intern",
        "company": "Microsoft",
        "location": "Hyderabad",
        "skills_required": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
        "duration": "6 months",
        "stipend": "₹60,000/month",
        "description": "Build AI-powered features for Azure services",
        "apply_link": "https://careers.microsoft.com"
    },
    {
        "id": "3",
        "title": "Full Stack Developer Intern",
        "company": "Amazon",
        "location": "Remote",
        "skills_required": ["React", "Node.js", "AWS", "JavaScript"],
        "duration": "3 months",
        "stipend": "₹70,000/month",
        "description": "Build scalable web applications on AWS",
        "apply_link": "https://amazon.jobs/students"
    },
    {
        "id": "4",
        "title": "Data Science Intern",
        "company": "Flipkart",
        "location": "Bangalore",
        "skills_required": ["Python", "SQL", "Machine Learning", "pandas"],
        "duration": "4 months",
        "stipend": "₹50,000/month",
        "description": "Analyze customer data and build recommendation systems",
        "apply_link": "https://flipkartcareers.com"
    },
    {
        "id": "5",
        "title": "DevOps Intern",
        "company": "Razorpay",
        "location": "Bangalore",
        "skills_required": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
        "duration": "6 months",
        "stipend": "₹45,000/month",
        "description": "Automate infrastructure and deployment pipelines",
        "apply_link": "https://razorpay.com/careers"
    },
    {
        "id": "6",
        "title": "Backend Developer Intern",
        "company": "Swiggy",
        "location": "Remote",
        "skills_required": ["Python", "Django", "PostgreSQL", "REST API"],
        "duration": "3 months",
        "stipend": "₹40,000/month",
        "description": "Build backend services for food delivery platform",
        "apply_link": "https://careers.swiggy.com"
    },
    {
        "id": "7",
        "title": "Frontend Developer Intern",
        "company": "Zomato",
        "location": "Gurugram",
        "skills_required": ["React", "TypeScript", "CSS", "JavaScript"],
        "duration": "3 months",
        "stipend": "₹35,000/month",
        "description": "Create beautiful and responsive user interfaces",
        "apply_link": "https://zomato.com/careers"
    },
    {
        "id": "8",
        "title": "Mobile App Developer Intern",
        "company": "Paytm",
        "location": "Noida",
        "skills_required": ["React Native", "JavaScript", "Mobile Development"],
        "duration": "4 months",
        "stipend": "₹40,000/month",
        "description": "Build features for Paytm mobile applications",
        "apply_link": "https://paytm.com/careers"
    },
]


# ==================== Pydantic Models ====================

class InternshipMatchRequest(BaseModel):
    skills: List[str]
    github_data: Optional[Dict] = None
    career_score: Optional[int] = None
    location: Optional[str] = None
    experience_level: Optional[str] = "beginner"


class InternshipMatchResponse(BaseModel):
    internship_id: str
    title: str
    company: str
    location: str
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    stipend: str
    duration: str
    apply_link: str
    recommendation: Optional[str] = None


# ==================== Helper Functions ====================

def calculate_match_score(user_skills: List[str], internship: Dict) -> Dict:
    """Calculate how well user matches an internship"""
    user_skills_lower = [s.lower() for s in user_skills]
    required_skills = internship.get('skills_required', [])
    
    matched = [skill for skill in required_skills if skill.lower() in user_skills_lower]
    missing = [skill for skill in required_skills if skill.lower() not in user_skills_lower]
    
    if len(required_skills) > 0:
        score = int((len(matched) / len(required_skills)) * 100)
    else:
        score = 50
    
    return {
        'score': score,
        'matched': matched,
        'missing': missing
    }


async def get_gemini_recommendation(internship: Dict, user_skills: List[str], missing_skills: List[str]) -> str:
    """Get AI recommendation for the internship"""
    if not GEMINI_AVAILABLE or not missing_skills:
        return None
    
    try:
        prompt = f"""
You're a career advisor. Give a brief (2-3 sentences) recommendation for a student applying to this internship:

Internship: {internship['title']} at {internship['company']}
Required Skills: {', '.join(internship.get('skills_required', []))}
Student Has: {', '.join(user_skills[:10])}
Student Missing: {', '.join(missing_skills[:5])}

Provide actionable advice on how to prepare for this role.
"""
        response = GoogleAPI.generate_content(prompt)
        return response
    except Exception:
        return None


# ==================== API Endpoints ====================

@router.post("/match")
async def match_internships(request: InternshipMatchRequest):
    """
    Match internships based on skills, GitHub profile, and career score
    Returns ranked list of matched internships with AI recommendations
    """
    try:
        matches = []
        
        for internship in INTERNSHIPS_DB:
            # Calculate match
            match_result = calculate_match_score(request.skills, internship)
            
            # Apply location filter if provided
            if request.location:
                if request.location.lower() not in internship['location'].lower():
                    if 'remote' not in internship['location'].lower():
                        continue
            
            # Boost score based on career score
            score = match_result['score']
            if request.career_score:
                bonus = min(10, request.career_score // 100)
                score = min(100, score + bonus)
            
            # Get AI recommendation for top matches
            recommendation = None
            if score >= 50 and GEMINI_AVAILABLE:
                recommendation = await get_gemini_recommendation(
                    internship, 
                    request.skills, 
                    match_result['missing']
                )
            
            matches.append(InternshipMatchResponse(
                internship_id=internship['id'],
                title=internship['title'],
                company=internship['company'],
                location=internship['location'],
                match_score=score,
                matched_skills=match_result['matched'],
                missing_skills=match_result['missing'],
                stipend=internship['stipend'],
                duration=internship['duration'],
                apply_link=internship['apply_link'],
                recommendation=recommendation
            ))
        
        # Sort by match score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        return {
            "total_matches": len(matches),
            "matches": [m.dict() for m in matches]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching internships: {str(e)}")


@router.get("/list")
async def list_all_internships():
    """Get list of all available internships"""
    return {
        "total": len(INTERNSHIPS_DB),
        "internships": INTERNSHIPS_DB
    }


@router.get("/{internship_id}")
async def get_internship_details(internship_id: str):
    """Get details of a specific internship"""
    for internship in INTERNSHIPS_DB:
        if internship['id'] == internship_id:
            return internship
    
    raise HTTPException(status_code=404, detail="Internship not found")


@router.post("/recommend")
async def get_ai_internship_recommendation(request: InternshipMatchRequest):
    """
    Get AI-powered internship recommendations based on profile
    Uses Gemini to provide personalized career advice
    """
    if not GEMINI_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        prompt = f"""
You're a career counselor for students. Based on this student's profile, recommend the best career path and types of internships:

Skills: {', '.join(request.skills[:15])}
Career Score: {request.career_score or 'Not provided'}
Preferred Location: {request.location or 'Any'}

Provide:
1. Recommended career path (2-3 sentences)
2. Top 3 types of internships they should apply for
3. Skills they should develop next
4. Tips for standing out in applications

Keep response under 250 words.
"""
        response = GoogleAPI.generate_content(prompt)
        
        if response:
            return {
                "recommendation": response,
                "skills_analyzed": len(request.skills),
                "ai_powered": True
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to generate recommendation")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")

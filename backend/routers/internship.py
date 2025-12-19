"""
Internship Matching Router - Enhanced with RapidAPI and Gemini AI
Handles internship matching, recommendations, and skill analysis
Uses RapidAPI for real internship data and Gemini for intelligent matching
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

# RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "internships-api.p.rapidapi.com")
RAPIDAPI_AVAILABLE = bool(RAPIDAPI_KEY and RAPIDAPI_KEY != "your_rapidapi_key_here")

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()

# ==================== Sample Internship Database (Fallback) ====================

SAMPLE_INTERNSHIPS = [
    {
        "id": "sample-1",
        "title": "Software Engineering Intern",
        "company": "Google",
        "location": "Remote / Bangalore",
        "skills_required": ["Python", "Java", "Data Structures", "Algorithms"],
        "duration": "3 months",
        "stipend": "₹80,000/month",
        "description": "Work on core Google products with experienced engineers.",
        "apply_link": "https://careers.google.com/students"
    },
    {
        "id": "sample-2",
        "title": "ML/AI Intern",
        "company": "Microsoft",
        "location": "Hyderabad",
        "skills_required": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
        "duration": "6 months",
        "stipend": "₹60,000/month",
        "description": "Build AI-powered features for Azure services.",
        "apply_link": "https://careers.microsoft.com"
    },
    {
        "id": "sample-3",
        "title": "Full Stack Developer Intern",
        "company": "Amazon",
        "location": "Remote",
        "skills_required": ["React", "Node.js", "AWS", "JavaScript"],
        "duration": "3 months",
        "stipend": "₹70,000/month",
        "description": "Build scalable web applications on AWS.",
        "apply_link": "https://amazon.jobs/students"
    },
    {
        "id": "sample-4",
        "title": "Data Science Intern",
        "company": "Flipkart",
        "location": "Bangalore",
        "skills_required": ["Python", "SQL", "Machine Learning", "pandas"],
        "duration": "4 months",
        "stipend": "₹50,000/month",
        "description": "Analyze customer data and build recommendation systems.",
        "apply_link": "https://flipkartcareers.com"
    },
    {
        "id": "sample-5",
        "title": "DevOps Intern",
        "company": "Razorpay",
        "location": "Bangalore",
        "skills_required": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
        "duration": "6 months",
        "stipend": "₹45,000/month",
        "description": "Automate infrastructure and deployment pipelines.",
        "apply_link": "https://razorpay.com/careers"
    },
]

# ==================== Pydantic Models ====================

class InternshipMatchRequest(BaseModel):
    skills: List[str]
    github_data: Optional[Dict] = None
    career_score: Optional[int] = None
    location: Optional[str] = None
    experience_level: Optional[str] = "beginner"
    resume_text: Optional[str] = None
    search_query: Optional[str] = None  # For API search


class InternshipMatchResponse(BaseModel):
    internship_id: str
    title: str
    company: str
    location: str
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    stipend: Optional[str] = None
    duration: Optional[str] = None
    apply_link: str
    description: Optional[str] = None
    recommendation: Optional[str] = None
    ai_match_reason: Optional[str] = None
    source: str = "sample"  # "rapidapi" or "sample"


class InternshipSearchRequest(BaseModel):
    query: str
    location: Optional[str] = "India"
    page: Optional[int] = 1


# ==================== RapidAPI Functions ====================

async def fetch_internships_from_rapidapi(query: str, location: str = "India", page: int = 1) -> List[Dict]:
    """Fetch internships from RapidAPI"""
    if not RAPIDAPI_AVAILABLE:
        print("RapidAPI not configured")
        return []
    
    try:
        url = "https://internships-api.p.rapidapi.com/active-jb-7d"
        
        params = {
            "title_filter": f'"{query}"',
            "location_filter": f'"{location}"',
            "page": str(page)
        }
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data if isinstance(data, list) else data.get("jobs", data.get("data", []))
                return jobs[:20]  # Limit to 20 results
            else:
                print(f"RapidAPI error: {response.status_code}")
                return []
                
    except Exception as e:
        print(f"RapidAPI fetch failed: {e}")
        return []


def parse_rapidapi_internship(job: Dict, idx: int) -> Dict:
    """Parse RapidAPI job data into our format"""
    return {
        "id": f"rapidapi-{idx}-{job.get('id', '')}",
        "title": job.get("title", "Internship"),
        "company": job.get("company_name", job.get("company", "Unknown")),
        "location": job.get("location", job.get("city", "Remote")),
        "skills_required": extract_skills_from_description(job.get("description", "")),
        "duration": job.get("employment_type", "Internship"),
        "stipend": job.get("salary_string", job.get("salary", "Competitive")),
        "description": job.get("description", "")[:500],
        "apply_link": job.get("url", job.get("apply_url", "#")),
        "source": "rapidapi"
    }


def extract_skills_from_description(description: str) -> List[str]:
    """Extract skills from job description"""
    import re
    
    skills_list = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
        'Machine Learning', 'Deep Learning', 'AI', 'TensorFlow', 'PyTorch', 'NLP',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
        'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum'
    ]
    
    found = []
    desc_lower = description.lower()
    
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, desc_lower):
            found.append(skill)
    
    return found[:10]  # Limit to 10 skills


# ==================== Gemini AI Functions ====================

async def gemini_calculate_match_scores(user_skills: List[str], internships: List[Dict]) -> List[Dict]:
    """Use Gemini to calculate intelligent match scores"""
    if not GEMINI_AVAILABLE or not internships:
        return None
    
    try:
        internship_summaries = [
            f"{i+1}. {intern.get('title', 'Job')} at {intern.get('company', 'Company')}: {', '.join(intern.get('skills_required', []))}"
            for i, intern in enumerate(internships[:10])
        ]
        
        prompt = f"""Analyze candidate match for these internships.

CANDIDATE SKILLS: {', '.join(user_skills)}

INTERNSHIPS:
{chr(10).join(internship_summaries)}

Return ONLY a JSON array (no markdown):
[{{"id": 1, "score": 85, "reason": "Strong match"}}, ...]
"""
        response = GoogleAPI.generate_content(prompt)
        
        if response:
            response = response.strip()
            if "```" in response:
                response = response.split("```")[1].replace("json", "").strip()
            
            try:
                return json.loads(response)
            except:
                pass
        return None
    except Exception as e:
        print(f"Gemini matching failed: {e}")
        return None


async def gemini_get_advice(user_skills: List[str], internship: Dict) -> str:
    """Get AI advice for applying"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Brief advice (2 sentences) for applying to:
{internship.get('title', 'Internship')} at {internship.get('company', 'Company')}
Required: {', '.join(internship.get('skills_required', []))}
Candidate has: {', '.join(user_skills[:8])}"""
        
        return GoogleAPI.generate_content(prompt)
    except:
        return None


# ==================== Helper Functions ====================

def calculate_match_score(user_skills: List[str], internship: Dict) -> Dict:
    """Calculate match score"""
    user_skills_lower = [s.lower() for s in user_skills]
    required = internship.get('skills_required', [])
    
    matched = [s for s in required if s.lower() in user_skills_lower]
    missing = [s for s in required if s.lower() not in user_skills_lower]
    
    score = int((len(matched) / len(required)) * 100) if required else 50
    
    return {'score': score, 'matched': matched, 'missing': missing}


# ==================== API Endpoints ====================

@router.post("/match")
async def match_internships(request: InternshipMatchRequest):
    """Match internships using RapidAPI data and Gemini AI"""
    try:
        internships = []
        source = "sample"
        
        # Try to fetch from RapidAPI
        if RAPIDAPI_AVAILABLE:
            search_query = request.search_query or " ".join(request.skills[:3]) + " intern"
            location = request.location or "India"
            
            api_results = await fetch_internships_from_rapidapi(search_query, location)
            
            if api_results:
                internships = [parse_rapidapi_internship(job, i) for i, job in enumerate(api_results)]
                source = "rapidapi"
        
        # Fallback to sample data
        if not internships:
            internships = SAMPLE_INTERNSHIPS
            source = "sample"
        
        # Get AI match scores
        ai_scores = await gemini_calculate_match_scores(request.skills, internships)
        ai_score_map = {}
        if ai_scores:
            for item in ai_scores:
                ai_score_map[str(item.get('id', 0))] = item
        
        matches = []
        for idx, internship in enumerate(internships):
            match_result = calculate_match_score(request.skills, internship)
            
            # Apply location filter
            if request.location:
                if request.location.lower() not in internship.get('location', '').lower():
                    if 'remote' not in internship.get('location', '').lower():
                        continue
            
            # Get score
            ai_data = ai_score_map.get(str(idx + 1), {})
            score = ai_data.get('score', match_result['score'])
            ai_reason = ai_data.get('reason')
            
            # Boost with career score
            if request.career_score:
                score = min(100, score + request.career_score // 100)
            
            # Get advice for top matches
            recommendation = None
            if score >= 60 and len(matches) < 5:
                recommendation = await gemini_get_advice(request.skills, internship)
            
            matches.append(InternshipMatchResponse(
                internship_id=internship['id'],
                title=internship['title'],
                company=internship['company'],
                location=internship.get('location', 'Remote'),
                match_score=score,
                matched_skills=match_result['matched'],
                missing_skills=match_result['missing'],
                stipend=internship.get('stipend'),
                duration=internship.get('duration'),
                apply_link=internship.get('apply_link', '#'),
                description=internship.get('description'),
                recommendation=recommendation,
                ai_match_reason=ai_reason,
                source=source
            ))
        
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        return {
            "total_matches": len(matches),
            "source": source,
            "rapidapi_enabled": RAPIDAPI_AVAILABLE,
            "ai_powered": GEMINI_AVAILABLE,
            "matches": [m.dict() for m in matches]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching internships: {str(e)}")


@router.post("/search")
async def search_internships(request: InternshipSearchRequest):
    """Search internships using RapidAPI"""
    try:
        if not RAPIDAPI_AVAILABLE:
            # Return sample data filtered by query
            query_lower = request.query.lower()
            filtered = [
                i for i in SAMPLE_INTERNSHIPS
                if query_lower in i['title'].lower() or 
                   query_lower in i['company'].lower() or
                   any(query_lower in s.lower() for s in i['skills_required'])
            ]
            return {
                "total": len(filtered),
                "source": "sample",
                "internships": filtered
            }
        
        api_results = await fetch_internships_from_rapidapi(
            request.query, 
            request.location or "India",
            request.page
        )
        
        internships = [parse_rapidapi_internship(job, i) for i, job in enumerate(api_results)]
        
        return {
            "total": len(internships),
            "source": "rapidapi",
            "page": request.page,
            "internships": internships
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching internships: {str(e)}")


@router.get("/list")
async def list_all_internships():
    """Get internships (from API or sample)"""
    if RAPIDAPI_AVAILABLE:
        api_results = await fetch_internships_from_rapidapi("software intern", "India")
        if api_results:
            internships = [parse_rapidapi_internship(job, i) for i, job in enumerate(api_results)]
            return {"total": len(internships), "source": "rapidapi", "internships": internships}
    
    return {"total": len(SAMPLE_INTERNSHIPS), "source": "sample", "internships": SAMPLE_INTERNSHIPS}


@router.get("/{internship_id}")
async def get_internship_details(internship_id: str):
    """Get internship details"""
    for internship in SAMPLE_INTERNSHIPS:
        if internship['id'] == internship_id:
            return internship
    
    raise HTTPException(status_code=404, detail="Internship not found")


@router.post("/recommend")
async def get_ai_recommendation(request: InternshipMatchRequest):
    """Get AI-powered career recommendations"""
    if not GEMINI_AVAILABLE:
        return {
            "recommendation": f"Based on your skills ({', '.join(request.skills[:5])}), consider applying to software development internships.",
            "ai_powered": False
        }
    
    try:
        prompt = f"""As a career advisor, give brief recommendations for a candidate with these skills: {', '.join(request.skills)}

Include:
1. Best internship types to apply for
2. Skills to develop
3. Application tips

Keep under 200 words."""
        
        response = GoogleAPI.generate_content(prompt)
        return {"recommendation": response, "ai_powered": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/status/api")
async def get_api_status():
    """Check RapidAPI status"""
    return {
        "rapidapi_configured": RAPIDAPI_AVAILABLE,
        "rapidapi_host": RAPIDAPI_HOST if RAPIDAPI_AVAILABLE else None,
        "gemini_available": GEMINI_AVAILABLE
    }

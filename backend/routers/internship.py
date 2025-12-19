"""
Internship Matching Router - Enhanced with Gemini AI
Handles internship matching, recommendations, and skill analysis
Uses Gemini for intelligent matching and personalized recommendations
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os
import json

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
        "description": "Work on core Google products with experienced engineers. Build scalable systems and learn from world-class engineers.",
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
        "description": "Build AI-powered features for Azure services. Work on cutting-edge machine learning projects.",
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
        "description": "Build scalable web applications on AWS. Learn about distributed systems at scale.",
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
        "description": "Analyze customer data and build recommendation systems for millions of users.",
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
        "description": "Automate infrastructure and deployment pipelines for India's leading payment gateway.",
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
        "description": "Build backend services for food delivery platform serving millions of orders.",
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
        "description": "Create beautiful and responsive user interfaces for restaurant discovery app.",
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
        "description": "Build features for Paytm mobile applications used by 300+ million users.",
        "apply_link": "https://paytm.com/careers"
    },
    {
        "id": "9",
        "title": "Cloud Engineering Intern",
        "company": "Infosys",
        "location": "Pune / Remote",
        "skills_required": ["AWS", "Azure", "Python", "Terraform"],
        "duration": "6 months",
        "stipend": "₹25,000/month",
        "description": "Work on cloud migration projects for Fortune 500 clients.",
        "apply_link": "https://infosys.com/careers"
    },
    {
        "id": "10",
        "title": "Cybersecurity Intern",
        "company": "TCS",
        "location": "Mumbai",
        "skills_required": ["Cybersecurity", "Python", "Networking", "Linux"],
        "duration": "6 months",
        "stipend": "₹30,000/month",
        "description": "Learn about security operations and vulnerability assessment.",
        "apply_link": "https://tcs.com/careers"
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
    ai_match_reason: Optional[str] = None


# ==================== Gemini AI Functions ====================

async def gemini_calculate_match_scores(user_skills: List[str], internships: List[Dict], resume_text: Optional[str] = None) -> List[Dict]:
    """Use Gemini to calculate intelligent match scores"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        # Prepare internship data for AI
        internship_summaries = []
        for i, internship in enumerate(internships):
            internship_summaries.append(
                f"{i+1}. {internship['title']} at {internship['company']}: requires {', '.join(internship['skills_required'])}"
            )
        
        prompt = f"""You are a career matching AI. Analyze how well a candidate matches each internship.

CANDIDATE SKILLS: {', '.join(user_skills)}
{f"RESUME SUMMARY: {resume_text[:500]}" if resume_text else ""}

AVAILABLE INTERNSHIPS:
{chr(10).join(internship_summaries)}

For each internship, provide a match score (0-100) and a brief reason.
Return ONLY a JSON array with this exact format (no markdown, no code blocks):
[
  {{"id": 1, "score": 85, "reason": "Strong Python skills match"}},
  {{"id": 2, "score": 60, "reason": "Has some ML basics"}}
]

Consider:
1. Direct skill matches
2. Related/transferable skills
3. Learning potential based on existing skills
"""
        response = GoogleAPI.generate_content(prompt)
        
        if response:
            # Clean the response
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()
            
            try:
                ai_scores = json.loads(response)
                return ai_scores
            except json.JSONDecodeError:
                return None
        return None
    except Exception as e:
        print(f"Gemini matching failed: {e}")
        return None


async def gemini_get_personalized_advice(user_skills: List[str], internship: Dict, missing_skills: List[str]) -> str:
    """Get AI-powered personalized advice for an internship"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Give brief, actionable advice (2-3 sentences) for a candidate applying to this internship:

INTERNSHIP: {internship['title']} at {internship['company']}
REQUIRED SKILLS: {', '.join(internship['skills_required'])}
CANDIDATE HAS: {', '.join(user_skills[:10])}
CANDIDATE MISSING: {', '.join(missing_skills[:5])}

Focus on:
1. How to bridge the skill gap quickly
2. What to highlight in the application
3. Any related skills that could be valuable
"""
        response = GoogleAPI.generate_content(prompt)
        return response.strip() if response else None
    except Exception:
        return None


async def gemini_recommend_best_internships(user_skills: List[str], career_goal: Optional[str] = None) -> Dict:
    """Get AI-powered internship recommendations"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        internship_list = "\n".join([
            f"- {i['title']} at {i['company']} ({i['location']}): {', '.join(i['skills_required'])}"
            for i in INTERNSHIPS_DB
        ])
        
        prompt = f"""As a career advisor, recommend the best internship path for this candidate:

CANDIDATE SKILLS: {', '.join(user_skills)}
CAREER GOAL: {career_goal or 'Software Development'}

AVAILABLE INTERNSHIPS:
{internship_list}

Provide:
1. TOP 3 recommended internships (ranked)
2. Why each is a good fit
3. Skills to develop before applying
4. Overall career advice

Keep response under 300 words, be specific and practical.
"""
        response = GoogleAPI.generate_content(prompt)
        return {
            "recommendation": response,
            "ai_powered": True
        }
    except Exception:
        return None


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


# ==================== API Endpoints ====================

@router.post("/match")
async def match_internships(request: InternshipMatchRequest):
    """
    Match internships based on skills using Gemini AI
    Returns ranked list of matched internships with AI recommendations
    """
    try:
        matches = []
        
        # Try to get AI-powered match scores
        ai_scores = await gemini_calculate_match_scores(
            request.skills, 
            INTERNSHIPS_DB,
            request.resume_text
        )
        
        # Create a lookup for AI scores
        ai_score_map = {}
        if ai_scores:
            for item in ai_scores:
                ai_score_map[str(item.get('id', 0))] = {
                    'score': item.get('score', 50),
                    'reason': item.get('reason', '')
                }
        
        for idx, internship in enumerate(INTERNSHIPS_DB):
            # Calculate base match
            match_result = calculate_match_score(request.skills, internship)
            
            # Apply location filter if provided
            if request.location:
                if request.location.lower() not in internship['location'].lower():
                    if 'remote' not in internship['location'].lower():
                        continue
            
            # Get score - prefer AI score if available
            ai_data = ai_score_map.get(str(idx + 1), {})
            if ai_data and ai_data.get('score'):
                score = ai_data['score']
                ai_reason = ai_data.get('reason', '')
            else:
                score = match_result['score']
                ai_reason = None
            
            # Boost score based on career score
            if request.career_score:
                bonus = min(10, request.career_score // 100)
                score = min(100, score + bonus)
            
            # Get AI advice for top matches
            recommendation = None
            if score >= 50 and GEMINI_AVAILABLE and len(matches) < 5:
                recommendation = await gemini_get_personalized_advice(
                    request.skills, 
                    internship, 
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
                recommendation=recommendation,
                ai_match_reason=ai_reason
            ))
        
        # Sort by match score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        return {
            "total_matches": len(matches),
            "ai_powered": GEMINI_AVAILABLE and bool(ai_scores),
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
    """Get details of a specific internship with AI insights"""
    for internship in INTERNSHIPS_DB:
        if internship['id'] == internship_id:
            # Add AI-powered insights
            insight = None
            if GEMINI_AVAILABLE:
                try:
                    prompt = f"""Provide a brief overview (2-3 sentences) of what a candidate would learn and gain from this internship:

{internship['title']} at {internship['company']}
Skills: {', '.join(internship['skills_required'])}
Description: {internship['description']}
"""
                    insight = GoogleAPI.generate_content(prompt)
                except:
                    pass
            
            return {
                **internship,
                "ai_insight": insight
            }
    
    raise HTTPException(status_code=404, detail="Internship not found")


@router.post("/recommend")
async def get_ai_internship_recommendation(request: InternshipMatchRequest):
    """
    Get AI-powered internship recommendations based on profile
    Uses Gemini to provide personalized career advice
    """
    if not GEMINI_AVAILABLE:
        # Fallback to basic matching
        matches = []
        for internship in INTERNSHIPS_DB:
            match_result = calculate_match_score(request.skills, internship)
            if match_result['score'] >= 30:
                matches.append({
                    "title": internship['title'],
                    "company": internship['company'],
                    "score": match_result['score']
                })
        
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "recommendation": f"Based on your skills ({', '.join(request.skills[:5])}), we recommend: " + 
                            ", ".join([f"{m['title']} at {m['company']}" for m in matches[:3]]),
            "top_matches": matches[:3],
            "ai_powered": False
        }
    
    try:
        result = await gemini_recommend_best_internships(
            request.skills,
            request.experience_level
        )
        
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Failed to generate recommendation")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")


@router.post("/ai-match")
async def ai_powered_match(request: InternshipMatchRequest):
    """
    Full AI-powered internship matching using Gemini
    Provides intelligent matching beyond simple skill overlap
    """
    if not GEMINI_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        # Get comprehensive AI analysis
        prompt = f"""You are an expert career counselor. Analyze this candidate and match them with the best internships.

CANDIDATE PROFILE:
- Skills: {', '.join(request.skills)}
- Experience Level: {request.experience_level or 'beginner'}
- Preferred Location: {request.location or 'Any'}
- Career Score: {request.career_score or 'Not provided'}
{f"- Resume Summary: {request.resume_text[:300]}..." if request.resume_text else ""}

AVAILABLE INTERNSHIPS:
{json.dumps([{
    'id': i['id'],
    'title': i['title'],
    'company': i['company'],
    'skills': i['skills_required'],
    'location': i['location']
} for i in INTERNSHIPS_DB], indent=2)}

Provide a detailed analysis including:
1. TOP 3 BEST MATCHES with match percentage and reasoning
2. SKILL GAPS to address for each recommendation
3. PREPARATION TIPS for the application process
4. LEARNING PATH to maximize chances

Be specific, actionable, and encouraging. Format clearly.
"""
        
        response = GoogleAPI.generate_content(prompt)
        
        if response:
            return {
                "analysis": response,
                "candidate_skills": request.skills,
                "total_internships_analyzed": len(INTERNSHIPS_DB),
                "ai_powered": True
            }
        else:
            raise HTTPException(status_code=500, detail="AI analysis returned empty response")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI matching: {str(e)}")

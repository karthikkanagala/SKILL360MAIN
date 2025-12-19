"""Career Opportunities Router
Provides career opportunities + trends based on skills.
This is 'hackathon mode': uses scraper when possible and safe mock fallbacks.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

router = APIRouter()


class OpportunitiesRequest(BaseModel):
    skills: List[str]
    target_role: Optional[str] = None
    location: str = 'India'


@router.post('/search')
async def search_opportunities(request: OpportunitiesRequest) -> Dict[str, Any]:
    """Return (1) job market trends and (2) demo opportunities list."""
    try:
        from career_webscraper import get_career_scraper

        scraper = get_career_scraper()
        skills = request.skills or []

        trends = scraper.get_career_trends(skills)

        # Create demo opportunities (stable output for hackathon demo)
        opportunities: List[Dict[str, Any]] = []
        role = request.target_role or 'Intern / Junior Engineer'

        # Use company names from trends if available
        companies_pool: List[str] = []
        for s in trends.values():
            companies_pool.extend(s.get('companies', []) or [])
        companies_pool = [c for c in companies_pool if isinstance(c, str)]

        if not companies_pool:
            companies_pool = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Stripe']

        top_skills = skills[:5] if skills else ['python', 'react', 'sql']

        for i, company in enumerate(companies_pool[:8]):
            opportunities.append({
                "id": i + 1,
                "company": company,
                "role": role,
                "location": request.location,
                "type": "Opportunity",
                "required_skills": top_skills,
                "match_score": max(50, 90 - i * 5),
                "apply_link": "#",
                "source": "trends+mock",
            })

        return {
            "trends": trends,
            "opportunities": opportunities,
            "model_used": "scraper+mock",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching opportunities: {str(e)}")

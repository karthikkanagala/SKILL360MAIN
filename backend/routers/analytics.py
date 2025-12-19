"""
Analytics Router
Handles peer comparison, company-specific scoring, and PDF export
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

try:
    from advanced_analytics import get_peer_comparison, get_company_scoring, get_pdf_exporter
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class PeerComparisonRequest(BaseModel):
    career_score: int

class CompanyScoringRequest(BaseModel):
    profile_data: Dict
    company_name: Optional[str] = None

@router.post("/peer-comparison")
async def get_peer_comparison_endpoint(request: PeerComparisonRequest):
    """Get peer comparison data and percentile ranking"""
    try:
        comparison = get_peer_comparison(request.career_score)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting peer comparison: {str(e)}")

@router.post("/company-scoring")
async def calculate_company_score(request: CompanyScoringRequest):
    """Calculate company-specific career score"""
    try:
        scoring = get_company_scoring(request.profile_data, company_name=request.company_name)
        return scoring
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating company score: {str(e)}")

@router.post("/export-pdf")
async def export_pdf(data: Dict):
    """Export career analytics as PDF"""
    try:
        exporter = get_pdf_exporter()
        # This would generate and return PDF
        return {"message": "PDF export functionality", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting PDF: {str(e)}")



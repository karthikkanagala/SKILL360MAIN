"""
Resume Analysis Router
Handles resume upload, parsing, ATS scoring, and skill extraction
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

try:
    from parsing import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
    from skills import extract_skills
    from local_llm import calculate_ats_score_with_llm, generate_resume_improvements
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class ResumeAnalysisResponse(BaseModel):
    text: str
    skills: List[str]
    ats_score: int
    ats_analysis: Dict
    improvements: Optional[Dict] = None

@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and analyze resume file (PDF, DOCX, TXT)
    Returns extracted text, skills, ATS score, and improvement suggestions
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Determine file type
        file_type = file.content_type
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        
        # Extract text based on file type
        text = None
        if file_type == 'application/pdf' or file_extension == 'pdf':
            # Save temporarily and parse
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(contents)
                tmp_path = tmp.name
            try:
                # Create a file-like object for parsing
                class FileLike:
                    def __init__(self, path):
                        self.path = path
                    def read(self):
                        with open(self.path, 'rb') as f:
                            return f.read()
                text = extract_text_from_pdf(FileLike(tmp_path))
            finally:
                os.unlink(tmp_path)
                
        elif 'wordprocessingml' in file_type or file_extension == 'docx':
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                tmp.write(contents)
                tmp_path = tmp.name
            try:
                class FileLike:
                    def __init__(self, path):
                        self.path = path
                text = extract_text_from_docx(FileLike(tmp_path))
            finally:
                os.unlink(tmp_path)
                
        elif file_type == 'text/plain' or file_extension == 'txt':
            text = contents.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, DOCX, or TXT")
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from resume")
        
        # Extract skills
        skills = extract_skills(text)
        
        # Calculate ATS score with LLM
        ats_result = calculate_ats_score_with_llm(text, job_description="")
        ats_score = ats_result.get('overall_score', 0)
        
        # Generate improvement suggestions (needs ATS analysis)
        improvements = generate_resume_improvements(text, ats_result, job_description="")
        
        return ResumeAnalysisResponse(
            text=text,
            skills=list(skills) if isinstance(skills, set) else skills,
            ats_score=ats_score,
            ats_analysis=ats_result,
            improvements=improvements
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

class ResumeTextRequest(BaseModel):
    text: str
    job_description: Optional[str] = ""

@router.post("/analyze-text")
async def analyze_resume_text(request: ResumeTextRequest):
    """Analyze resume text without file upload"""
    try:
        text = request.text
        if not text or len(text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Resume text is too short")

        skills = extract_skills(text)
        ats_result = calculate_ats_score_with_llm(text, job_description=request.job_description or "")
        improvements = generate_resume_improvements(
            text,
            ats_result,
            job_description=request.job_description or ""
        )
        
        return {
            "skills": list(skills) if isinstance(skills, set) else skills,
            "ats_score": ats_result.get('overall_score', 0),
            "ats_analysis": ats_result,
            "improvements": improvements
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")



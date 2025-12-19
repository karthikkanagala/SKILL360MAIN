"""
Interview Preparation Router
Handles AI-powered interview question generation and answer evaluation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

try:
    from interview_prep import generate_interview_questions, evaluate_answer
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")

router = APIRouter()

class GenerateQuestionsRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = ""
    num_questions: int = 5
    skills: Optional[List[str]] = None

class EvaluateAnswerRequest(BaseModel):
    question: Dict  # The question object/dict
    answer: str
    resume_text: Optional[str] = ""

@router.post("/generate-questions")
async def generate_interview_questions_endpoint(request: GenerateQuestionsRequest):
    """
    Generate personalized interview questions based on resume and job description
    """
    try:
        # Extract skills from resume_text if needed, or use empty list
        skills = []  # You may want to extract skills from resume_text here
        questions = generate_interview_questions(
            resume_text=request.resume_text,
            job_description=request.job_description or "",
            skills=skills,
            question_count=request.num_questions
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@router.post("/evaluate-answer")
async def evaluate_interview_answer(request: EvaluateAnswerRequest):
    """
    Evaluate an interview answer and provide feedback with scoring
    """
    try:
        evaluation = evaluate_answer(
            question=request.question,
            answer=request.answer,
            resume_text=request.resume_text or ""
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")



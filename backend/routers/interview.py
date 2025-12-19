"""
Interview Preparation Router - Enhanced with Gemini AI
Handles AI-powered interview question generation and answer evaluation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

# Import original modules
try:
    from interview_prep import generate_interview_questions as _generate_questions, evaluate_answer as _evaluate_answer
    INTERVIEW_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import interview modules: {e}")
    INTERVIEW_MODULE_AVAILABLE = False

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()


class GenerateQuestionsRequest(BaseModel):
    resume_text: Optional[str] = ""
    job_description: Optional[str] = ""
    num_questions: int = 5
    skills: Optional[List[str]] = None
    difficulty: Optional[str] = "medium"  # easy, medium, hard
    role: Optional[str] = None


class EvaluateAnswerRequest(BaseModel):
    question: Dict
    answer: str
    resume_text: Optional[str] = ""


class MockInterviewRequest(BaseModel):
    skills: List[str]
    role: str
    experience_level: Optional[str] = "fresher"
    num_questions: int = 5


# Sample question bank for fallback
QUESTION_BANK = {
    "python": [
        {"question": "Explain the difference between a list and a tuple in Python.", "difficulty": "easy", "category": "Python Basics"},
        {"question": "What are decorators in Python and how do they work?", "difficulty": "medium", "category": "Python Advanced"},
        {"question": "Explain Python's GIL and its impact on multithreading.", "difficulty": "hard", "category": "Python Internals"},
    ],
    "javascript": [
        {"question": "What is the difference between let, var, and const?", "difficulty": "easy", "category": "JavaScript Basics"},
        {"question": "Explain closures in JavaScript with an example.", "difficulty": "medium", "category": "JavaScript Advanced"},
        {"question": "How does the JavaScript event loop work?", "difficulty": "hard", "category": "JavaScript Internals"},
    ],
    "react": [
        {"question": "What is the virtual DOM and why is it used?", "difficulty": "easy", "category": "React Basics"},
        {"question": "Explain React hooks and their benefits.", "difficulty": "medium", "category": "React Hooks"},
        {"question": "How would you optimize a React application?", "difficulty": "hard", "category": "React Performance"},
    ],
    "data_structures": [
        {"question": "Explain the difference between an array and a linked list.", "difficulty": "easy", "category": "Data Structures"},
        {"question": "How does a hash table work?", "difficulty": "medium", "category": "Data Structures"},
        {"question": "Explain the time complexity of operations in a balanced BST.", "difficulty": "hard", "category": "Data Structures"},
    ],
    "general": [
        {"question": "Tell me about yourself and your background.", "difficulty": "easy", "category": "Behavioral"},
        {"question": "Describe a challenging project you worked on.", "difficulty": "medium", "category": "Behavioral"},
        {"question": "How do you handle disagreements with team members?", "difficulty": "medium", "category": "Behavioral"},
    ]
}


async def gemini_generate_questions(skills: List[str], role: str, num_questions: int, difficulty: str) -> List[Dict]:
    """Use Gemini to generate interview questions"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Generate {num_questions} unique interview questions for a {role} position.

SKILLS TO TEST: {', '.join(skills)}
DIFFICULTY: {difficulty}

For each question, provide:
1. The question text
2. Difficulty level (easy/medium/hard)
3. Category (e.g., Technical, Behavioral, Problem Solving)
4. Key points expected in answer (2-3 points)
5. Sample answer outline

Format as a clear numbered list. Make questions practical and job-relevant."""

        response = GoogleAPI.generate_content(prompt)
        
        if response:
            # Parse the response into structured questions
            questions = []
            lines = response.split('\n')
            current_question = None
            
            for line in lines:
                line = line.strip()
                if re.match(r'^\d+\.', line):
                    if current_question:
                        questions.append(current_question)
                    current_question = {
                        "question": re.sub(r'^\d+\.\s*', '', line),
                        "difficulty": difficulty,
                        "category": "Technical",
                        "ai_generated": True
                    }
                elif current_question and 'difficulty' in line.lower():
                    if 'easy' in line.lower():
                        current_question['difficulty'] = 'easy'
                    elif 'hard' in line.lower():
                        current_question['difficulty'] = 'hard'
                elif current_question and 'category' in line.lower():
                    current_question['category'] = line.split(':')[-1].strip()
            
            if current_question:
                questions.append(current_question)
            
            return questions[:num_questions] if questions else None
        return None
    except Exception as e:
        print(f"Gemini question generation failed: {e}")
        return None


async def gemini_evaluate_answer(question: str, answer: str, skills: List[str] = None) -> Dict:
    """Use Gemini to evaluate interview answer"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""Evaluate this interview answer:

QUESTION: {question}
ANSWER: {answer}

Provide:
1. SCORE (0-100)
2. STRENGTHS (2-3 points)
3. AREAS TO IMPROVE (2-3 specific suggestions)
4. SAMPLE BETTER ANSWER (brief outline)
5. OVERALL FEEDBACK (2-3 sentences)

Be constructive and encouraging."""

        response = GoogleAPI.generate_content(prompt)
        
        if response:
            # Extract score from response
            score = 70  # Default
            score_match = re.search(r'score[:\s]*(\d+)', response.lower())
            if score_match:
                score = min(100, max(0, int(score_match.group(1))))
            
            return {
                "score": score,
                "feedback": response,
                "ai_powered": True
            }
        return None
    except Exception as e:
        print(f"Gemini evaluation failed: {e}")
        return None


def get_fallback_questions(skills: List[str], num_questions: int, difficulty: str) -> List[Dict]:
    """Get questions from fallback question bank"""
    questions = []
    
    # Add skill-specific questions
    for skill in skills:
        skill_key = skill.lower().replace(' ', '_')
        if skill_key in QUESTION_BANK:
            skill_questions = [q for q in QUESTION_BANK[skill_key] 
                            if difficulty == "all" or q['difficulty'] == difficulty]
            questions.extend(skill_questions)
    
    # Add general questions
    questions.extend(QUESTION_BANK.get('general', []))
    
    # Add data structure questions for technical roles
    if any(s.lower() in ['python', 'java', 'c++', 'javascript'] for s in skills):
        questions.extend(QUESTION_BANK.get('data_structures', []))
    
    # Limit and return
    return questions[:num_questions]


@router.post("/generate-questions")
async def generate_interview_questions_endpoint(request: GenerateQuestionsRequest):
    """
    Generate personalized interview questions using Gemini AI
    """
    try:
        skills = request.skills or []
        role = request.role or "Software Developer"
        
        # Try Gemini first
        if GEMINI_AVAILABLE:
            ai_questions = await gemini_generate_questions(
                skills, role, request.num_questions, request.difficulty
            )
            if ai_questions:
                return {
                    "questions": ai_questions,
                    "ai_generated": True,
                    "total": len(ai_questions)
                }
        
        # Try original module
        if INTERVIEW_MODULE_AVAILABLE and request.resume_text:
            try:
                questions = _generate_questions(
                    resume_text=request.resume_text,
                    job_description=request.job_description or "",
                    skills=skills,
                    question_count=request.num_questions
                )
                return {"questions": questions, "ai_generated": False}
            except:
                pass
        
        # Fallback to question bank
        questions = get_fallback_questions(skills, request.num_questions, request.difficulty)
        
        return {
            "questions": questions,
            "ai_generated": False,
            "source": "question_bank",
            "total": len(questions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluate-answer")
async def evaluate_interview_answer(request: EvaluateAnswerRequest):
    """
    Evaluate an interview answer using Gemini AI
    """
    try:
        question_text = request.question.get('question', str(request.question))
        
        # Try Gemini evaluation
        if GEMINI_AVAILABLE:
            ai_evaluation = await gemini_evaluate_answer(question_text, request.answer)
            if ai_evaluation:
                return ai_evaluation
        
        # Try original module
        if INTERVIEW_MODULE_AVAILABLE:
            try:
                evaluation = _evaluate_answer(
                    question=request.question,
                    answer=request.answer,
                    resume_text=request.resume_text or ""
                )
                return evaluation
            except:
                pass
        
        # Basic fallback evaluation
        word_count = len(request.answer.split())
        score = min(100, max(30, word_count * 2))
        
        return {
            "score": score,
            "feedback": "Answer received. For detailed feedback, please ensure Gemini API is configured.",
            "improvements": [
                "Provide specific examples from your experience",
                "Structure your answer using STAR method",
                "Keep answers concise but comprehensive"
            ],
            "ai_powered": False
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")


@router.post("/mock-interview")
async def start_mock_interview(request: MockInterviewRequest):
    """
    Start a mock interview session with AI-generated questions
    """
    try:
        if not GEMINI_AVAILABLE:
            # Use fallback questions
            questions = get_fallback_questions(request.skills, request.num_questions, "medium")
            return {
                "session_id": "mock_" + str(hash(str(request.skills)))[:8],
                "role": request.role,
                "questions": questions,
                "ai_powered": False
            }
        
        prompt = f"""Create a mock interview for a {request.role} position.

CANDIDATE PROFILE:
- Skills: {', '.join(request.skills)}
- Experience Level: {request.experience_level}

Generate {request.num_questions} interview questions that:
1. Start with easier questions and increase difficulty
2. Mix technical and behavioral questions
3. Are relevant to the role and skills
4. Would be asked in real interviews

For each question, provide:
- The question
- Expected answer key points
- Time suggested (1-3 minutes)

Format clearly."""

        response = GoogleAPI.generate_content(prompt)
        
        return {
            "session_id": "ai_mock_" + str(hash(response[:50]))[:8],
            "role": request.role,
            "experience_level": request.experience_level,
            "interview_content": response,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting mock interview: {str(e)}")


@router.get("/tips/{role}")
async def get_interview_tips(role: str):
    """Get AI-powered interview tips for a specific role"""
    if not GEMINI_AVAILABLE:
        return {
            "tips": [
                "Research the company thoroughly before the interview",
                "Practice common technical questions for your role",
                "Prepare examples of your past projects and achievements",
                "Ask thoughtful questions about the role and company",
                "Follow up with a thank you email after the interview"
            ],
            "ai_powered": False
        }
    
    try:
        prompt = f"""Provide 10 specific interview tips for a {role} position in India.

Include:
1. Technical preparation tips
2. Behavioral question strategies
3. Common mistakes to avoid
4. What to research before interview
5. Questions to ask the interviewer

Be specific and actionable."""

        response = GoogleAPI.generate_content(prompt)
        
        return {
            "role": role,
            "tips": response,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tips: {str(e)}")

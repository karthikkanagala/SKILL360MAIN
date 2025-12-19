"""
Resume Analysis Router - Enhanced with Gemini AI
Handles resume upload, ATS scoring, job matching, and AI suggestions
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os
import re

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

# Try to import from skills.py, use comprehensive fallback if not available
try:
    from parsing import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
    from skills import extract_skills as _extract_skills
    SKILLS_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    SKILLS_MODULE_AVAILABLE = False

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()

# Comprehensive skills list
TECH_SKILLS = [
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C', 'Ruby', 'Go', 'Golang', 'Rust', 'Swift', 'Kotlin', 
    'PHP', 'Perl', 'R', 'MATLAB', 'Scala', 'Dart', 'Lua', 'Haskell', 'Elixir', 'Clojure', 'F#', 'Objective-C',
    # Web Frontend
    'HTML', 'HTML5', 'CSS', 'CSS3', 'SASS', 'SCSS', 'LESS', 'React', 'ReactJS', 'React.js', 'Angular', 'AngularJS', 
    'Vue', 'Vue.js', 'VueJS', 'Svelte', 'Next.js', 'NextJS', 'Nuxt.js', 'Gatsby', 'jQuery', 'Bootstrap', 
    'Tailwind', 'TailwindCSS', 'Material UI', 'Material-UI', 'Redux', 'Zustand', 'MobX',
    # Web Backend
    'Node.js', 'NodeJS', 'Express', 'Express.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'Spring Boot', 'SpringBoot',
    'Laravel', 'Rails', 'Ruby on Rails', 'ASP.NET', '.NET', 'NestJS', 'Koa', 'Hapi', 'Fiber', 'Gin', 'Echo',
    # Databases
    'SQL', 'MySQL', 'PostgreSQL', 'Postgres', 'SQLite', 'Oracle', 'SQL Server', 'MSSQL', 'MongoDB', 'NoSQL',
    'Redis', 'Cassandra', 'DynamoDB', 'Firebase', 'Firestore', 'Elasticsearch', 'Neo4j', 'MariaDB', 'CouchDB',
    # Cloud & DevOps
    'AWS', 'Amazon Web Services', 'Azure', 'Microsoft Azure', 'GCP', 'Google Cloud', 'Cloud Computing',
    'Docker', 'Kubernetes', 'K8s', 'Terraform', 'Ansible', 'Jenkins', 'CI/CD', 'GitHub Actions', 'GitLab CI',
    'CircleCI', 'Travis CI', 'ArgoCD', 'Helm', 'Prometheus', 'Grafana', 'ELK', 'Nginx', 'Apache',
    # Data & ML/AI
    'Machine Learning', 'ML', 'Deep Learning', 'DL', 'Artificial Intelligence', 'AI', 'Data Science', 
    'Data Analysis', 'Data Analytics', 'Data Engineering', 'Big Data', 'NLP', 'Natural Language Processing',
    'Computer Vision', 'Neural Networks', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Sklearn',
    'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'OpenCV', 'NLTK', 'SpaCy', 'Hugging Face',
    'XGBoost', 'LightGBM', 'Random Forest', 'SVM', 'Regression', 'Classification', 'Clustering',
    # LLM & Generative AI
    'LLM', 'Large Language Models', 'GPT', 'ChatGPT', 'OpenAI', 'LangChain', 'RAG', 'Prompt Engineering',
    'Gemini', 'Claude', 'BERT', 'Transformers', 'Fine-tuning', 'Vector Database', 'Embeddings',
    # Mobile
    'Android', 'iOS', 'React Native', 'Flutter', 'Kotlin', 'Swift', 'Xamarin', 'Mobile Development',
    'Mobile App', 'SwiftUI', 'Jetpack Compose',
    # Tools & Practices
    'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN', 'Jira', 'Confluence', 'Slack', 'VS Code', 'IntelliJ',
    'Postman', 'Swagger', 'OpenAPI', 'REST', 'REST API', 'RESTful', 'GraphQL', 'gRPC', 'WebSocket', 'API',
    'Microservices', 'Monolith', 'MVC', 'MVVM', 'Design Patterns', 'SOLID', 'OOP', 'Functional Programming',
    'TDD', 'BDD', 'Unit Testing', 'Integration Testing', 'Selenium', 'Cypress', 'Jest', 'Mocha', 'PyTest',
    'Agile', 'Scrum', 'Kanban', 'DevOps', 'SRE', 'Linux', 'Unix', 'Bash', 'Shell', 'PowerShell',
    # Soft Skills
    'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Project Management', 'Time Management',
]


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text using word boundary matching
    Returns properly capitalized skill names
    """
    found = set()
    text_lower = text.lower()
    
    for skill in TECH_SKILLS:
        # Create pattern with word boundaries
        escaped = re.escape(skill.lower())
        # Handle special cases like C++ and C#
        if skill in ['C++', 'C#', 'C']:
            pattern = r'\b' + escaped
        else:
            pattern = r'\b' + escaped + r'\b'
        
        if re.search(pattern, text_lower):
            found.add(skill)
    
    # Remove duplicates with different cases (keep proper casing)
    skill_map = {}
    for skill in found:
        key = skill.lower().replace('.', '').replace('-', '').replace(' ', '')
        if key not in skill_map or len(skill) > len(skill_map[key]):
            skill_map[key] = skill
    
    return sorted(skill_map.values(), key=str.lower)


async def gemini_extract_skills(text: str) -> List[str]:
    """Use Gemini to extract skills from resume text"""
    if not GEMINI_AVAILABLE:
        return []
    
    try:
        prompt = f"""Extract all technical and professional skills from this resume text.
        
Resume text:
{text[:3000]}

Return ONLY a JSON array of skill names, like: ["Python", "React", "AWS", "Machine Learning"]
No explanations, just the array. Include:
- Programming languages
- Frameworks and libraries
- Tools and platforms
- Cloud services
- Databases
- Methodologies
- Soft skills mentioned"""
        
        response = GoogleAPI.generate_content(prompt)
        if response:
            # Clean and parse response
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()
            
            import json
            try:
                skills = json.loads(response)
                if isinstance(skills, list):
                    return [s for s in skills if isinstance(s, str)]
            except:
                pass
        return []
    except Exception as e:
        print(f"Gemini skill extraction failed: {e}")
        return []




# ==================== Pydantic Models ====================

class ResumeAnalysisResponse(BaseModel):
    text: str
    skills: List[str]
    ats_score: int
    ats_analysis: Dict
    improvements: Optional[Dict] = None


class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class JobMatchResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    recommended_courses: List[Dict]
    ai_feedback: Optional[str] = None


class ResumeTextRequest(BaseModel):
    text: str
    job_description: Optional[str] = ""


# ==================== Helper Functions ====================

def calculate_ats_score(text: str, skills: List[str], job_description: str = "") -> Dict:
    """Calculate ATS score based on resume text analysis"""
    score_components = {}
    total_score = 0
    
    # 1. Length check (0-15 points)
    word_count = len(text.split())
    if word_count >= 400:
        score_components['length'] = 15
    elif word_count >= 200:
        score_components['length'] = 10
    else:
        score_components['length'] = 5
    total_score += score_components['length']
    
    # 2. Skills count (0-25 points)
    skills_count = len(skills)
    if skills_count >= 10:
        score_components['skills'] = 25
    elif skills_count >= 5:
        score_components['skills'] = 15
    elif skills_count >= 2:
        score_components['skills'] = 10
    else:
        score_components['skills'] = 5
    total_score += score_components['skills']
    
    # 3. Section keywords (0-20 points)
    sections = ['experience', 'education', 'skills', 'projects', 'summary', 'objective']
    text_lower = text.lower()
    section_count = sum(1 for s in sections if s in text_lower)
    score_components['sections'] = min(20, section_count * 4)
    total_score += score_components['sections']
    
    # 4. Contact info (0-15 points)
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+', text))
    has_phone = bool(re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', text))
    has_linkedin = 'linkedin' in text_lower
    contact_score = (5 if has_email else 0) + (5 if has_phone else 0) + (5 if has_linkedin else 0)
    score_components['contact'] = contact_score
    total_score += score_components['contact']
    
    # 5. Action verbs (0-15 points)
    action_verbs = ['developed', 'created', 'led', 'managed', 'implemented', 'designed', 
                    'built', 'achieved', 'improved', 'increased', 'reduced', 'launched']
    action_count = sum(1 for verb in action_verbs if verb in text_lower)
    score_components['action_verbs'] = min(15, action_count * 3)
    total_score += score_components['action_verbs']
    
    # 6. Metrics/Numbers (0-10 points)
    number_pattern = r'\b\d+[%+]?\b'
    numbers = re.findall(number_pattern, text)
    score_components['metrics'] = min(10, len(numbers) * 2)
    total_score += score_components['metrics']
    
    return {
        'overall_score': min(100, total_score),
        'components': score_components,
        'word_count': word_count,
        'skills_found': skills_count,
        'feedback': generate_feedback(score_components)
    }


def generate_feedback(components: Dict) -> List[str]:
    """Generate feedback based on score components"""
    feedback = []
    
    if components.get('length', 0) < 15:
        feedback.append("Consider adding more detail to your resume - aim for 400+ words")
    if components.get('skills', 0) < 20:
        feedback.append("Add more technical skills to your resume")
    if components.get('sections', 0) < 16:
        feedback.append("Include standard sections: Experience, Education, Skills, Projects")
    if components.get('contact', 0) < 15:
        feedback.append("Ensure you have email, phone, and LinkedIn profile listed")
    if components.get('action_verbs', 0) < 10:
        feedback.append("Use more action verbs like 'developed', 'implemented', 'led'")
    if components.get('metrics', 0) < 6:
        feedback.append("Quantify your achievements with numbers and percentages")
    
    if not feedback:
        feedback.append("Great resume! Keep it updated with your latest achievements")
    
    return feedback


def generate_improvements(text: str, ats_result: Dict, job_description: str = "") -> Dict:
    """Generate improvement suggestions"""
    return {
        'suggestions': ats_result.get('feedback', []),
        'priority_areas': [
            area for area, score in ats_result.get('components', {}).items()
            if score < 10
        ],
        'strength_areas': [
            area for area, score in ats_result.get('components', {}).items()
            if score >= 15
        ]
    }


def calculate_job_match(resume_skills: List[str], job_description: str) -> Dict:
    """Calculate job-resume matching score"""
    jd_lower = job_description.lower()
    
    # Extract skills from job description
    all_skills = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'Go', 'Rust',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
        'Machine Learning', 'Deep Learning', 'AI', 'TensorFlow', 'PyTorch',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Agile', 'Scrum',
        'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices', 'Linux'
    ]
    
    jd_skills = [skill for skill in all_skills if skill.lower() in jd_lower]
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    matched = [skill for skill in jd_skills if skill.lower() in resume_skills_lower]
    missing = [skill for skill in jd_skills if skill.lower() not in resume_skills_lower]
    
    if len(jd_skills) > 0:
        match_score = int((len(matched) / len(jd_skills)) * 100)
    else:
        match_score = 50  # Default if no skills found in JD
    
    return {
        'match_score': match_score,
        'matched_skills': matched,
        'missing_skills': missing
    }


def get_course_recommendations(missing_skills: List[str]) -> List[Dict]:
    """Get course recommendations for missing skills"""
    course_db = {
        'Python': {'title': 'Python for Everybody', 'platform': 'Coursera', 'url': 'https://coursera.org/python', 'duration': '8 weeks'},
        'JavaScript': {'title': 'JavaScript: Understanding the Weird Parts', 'platform': 'Udemy', 'url': 'https://udemy.com/js', 'duration': '12 hours'},
        'React': {'title': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://udemy.com/react', 'duration': '48 hours'},
        'AWS': {'title': 'AWS Certified Solutions Architect', 'platform': 'AWS Training', 'url': 'https://aws.training', 'duration': '40 hours'},
        'Docker': {'title': 'Docker & Kubernetes: The Practical Guide', 'platform': 'Udemy', 'url': 'https://udemy.com/docker', 'duration': '24 hours'},
        'Machine Learning': {'title': 'Machine Learning by Andrew Ng', 'platform': 'Coursera', 'url': 'https://coursera.org/ml', 'duration': '11 weeks'},
        'SQL': {'title': 'SQL for Data Science', 'platform': 'Coursera', 'url': 'https://coursera.org/sql', 'duration': '4 weeks'},
        'Git': {'title': 'Git Complete: The definitive guide', 'platform': 'Udemy', 'url': 'https://udemy.com/git', 'duration': '6 hours'},
    }
    
    recommendations = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        if skill in course_db:
            recommendations.append(course_db[skill])
        else:
            recommendations.append({
                'title': f'Learn {skill} - Complete Course',
                'platform': 'Various',
                'url': f'https://www.google.com/search?q={skill}+course',
                'duration': 'Self-paced'
            })
    
    return recommendations


async def get_gemini_analysis(resume_text: str, job_description: str, missing_skills: List[str]) -> str:
    """Get AI-powered analysis using Gemini"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        prompt = f"""
Analyze this resume against the job description and provide specific, actionable feedback.

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:1000]}

MISSING SKILLS: {', '.join(missing_skills[:10])}

Provide:
1. 3 specific improvements for the resume
2. How to address the skill gaps
3. Interview preparation tips for this role

Keep response under 300 words, be specific and actionable.
"""
        response = GoogleAPI.generate_content(prompt)
        return response
    except Exception as e:
        print(f"Gemini analysis failed: {e}")
        return None


# ==================== API Endpoints ====================

@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze resume file (PDF, DOCX, TXT)"""
    import io
    import tempfile
    
    try:
        contents = await file.read()
        file_type = file.content_type or ''
        file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
        
        text = None
        if file_type == 'application/pdf' or file_extension == 'pdf':
            file_like = io.BytesIO(contents)
            text = extract_text_from_pdf(file_like)
        elif 'wordprocessingml' in file_type or file_extension == 'docx':
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                tmp.write(contents)
                tmp_path = tmp.name
            try:
                text = extract_text_from_docx(tmp_path)
            finally:
                os.unlink(tmp_path)
        elif file_type == 'text/plain' or file_extension == 'txt':
            text = contents.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, DOCX, or TXT")
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract text from resume. If this is a scanned PDF, please try uploading a text-based PDF or DOCX file."
            )
        
        # Extract skills using pattern matching
        pattern_skills = extract_skills(text)
        
        # Also try Gemini for more comprehensive extraction
        gemini_skills = await gemini_extract_skills(text)
        
        # Combine both (unique skills)
        all_skills = set(pattern_skills)
        for skill in gemini_skills:
            # Only add if not already present (case-insensitive check)
            if skill.lower() not in [s.lower() for s in all_skills]:
                all_skills.add(skill)
        
        skills_list = sorted(list(all_skills), key=str.lower)
        
        ats_result = calculate_ats_score(text, skills_list)
        improvements = generate_improvements(text, ats_result)
        
        return ResumeAnalysisResponse(
            text=text,
            skills=skills_list,
            ats_score=ats_result.get('overall_score', 0),
            ats_analysis=ats_result,
            improvements=improvements
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@router.post("/analyze-text")
async def analyze_resume_text(request: ResumeTextRequest):
    """Analyze resume text with optional job description matching"""
    try:
        text = request.text
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Resume text is too short")

        # Extract skills using pattern matching
        pattern_skills = extract_skills(text)
        
        # Also try Gemini for more comprehensive extraction
        gemini_skills = await gemini_extract_skills(text)
        
        # Combine both (unique skills)
        all_skills = set(pattern_skills)
        for skill in gemini_skills:
            if skill.lower() not in [s.lower() for s in all_skills]:
                all_skills.add(skill)
        
        skills_list = sorted(list(all_skills), key=str.lower)
        
        ats_result = calculate_ats_score(text, skills_list, request.job_description or "")
        improvements = generate_improvements(text, ats_result, request.job_description or "")
        
        response = {
            "skills": skills_list,
            "ats_score": ats_result.get('overall_score', 0),
            "ats_analysis": ats_result,
            "improvements": improvements
        }
        
        # If job description provided, add matching analysis
        if request.job_description and len(request.job_description) > 50:
            match_result = calculate_job_match(skills_list, request.job_description)
            response["job_match"] = match_result
            response["recommended_courses"] = get_course_recommendations(match_result['missing_skills'])
            
            # Get Gemini AI analysis
            ai_feedback = await get_gemini_analysis(text, request.job_description, match_result['missing_skills'])
            if ai_feedback:
                response["ai_feedback"] = ai_feedback
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/match-job", response_model=JobMatchResponse)
async def match_resume_to_job(request: JobMatchRequest):
    """
    Match resume against job description
    Returns matching score, skill gaps, and recommendations
    """
    try:
        resume_text = request.resume_text
        job_description = request.job_description
        
        if len(resume_text) < 50:
            raise HTTPException(status_code=400, detail="Resume text too short")
        if len(job_description) < 50:
            raise HTTPException(status_code=400, detail="Job description too short")
        
        # Extract skills from resume
        skills = extract_skills(resume_text)
        skills_list = list(skills) if isinstance(skills, set) else skills
        
        # Calculate match
        match_result = calculate_job_match(skills_list, job_description)
        
        # Get course recommendations
        courses = get_course_recommendations(match_result['missing_skills'])
        
        # Generate suggestions
        suggestions = []
        if match_result['match_score'] < 50:
            suggestions.append("Your profile needs significant improvement for this role")
        elif match_result['match_score'] < 70:
            suggestions.append("You're a partial match - focus on acquiring missing skills")
        else:
            suggestions.append("You're a strong candidate for this role!")
        
        for skill in match_result['missing_skills'][:3]:
            suggestions.append(f"Consider learning {skill} to improve your match")
        
        # Get AI analysis
        ai_feedback = await get_gemini_analysis(resume_text, job_description, match_result['missing_skills'])
        
        return JobMatchResponse(
            match_score=match_result['match_score'],
            matched_skills=match_result['matched_skills'],
            missing_skills=match_result['missing_skills'],
            suggestions=suggestions,
            recommended_courses=courses,
            ai_feedback=ai_feedback
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resume: {str(e)}")

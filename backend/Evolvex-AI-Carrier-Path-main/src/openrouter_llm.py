"""
OpenRouter LLM Integration
Replaces local Llama/Ollama with cloud-based OpenRouter API
Model: allenai/olmo-3.1-32b-think:free
"""

import os
import time
import requests
import json
import streamlit as st
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter Configuration
# Try Streamlit secrets first (for Streamlit Cloud), then environment variable
try:
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
except:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# SPEED OPTIMIZED: Using faster model without reasoning overhead
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")
FALLBACK_MODEL = "allenai/olmo-3.1-32b-think:free"  # Fallback if primary fails

# SPEED OPTIMIZED Configuration
MAX_PROMPT_CHARS = int(os.getenv("LLM_MAX_PROMPT_CHARS", "4000"))  # Reduced for faster processing
REQUEST_TIMEOUT_SECS = int(os.getenv("LLM_REQUEST_TIMEOUT_SECS", "30"))  # Reduced timeout for speed
MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "2"))  # Fewer retries for speed

__all__ = [
    "is_openrouter_available",
    "call_openrouter_llm",
    "enhance_resume_section",
    "generate_project_ideas",
    "generate_cover_letter",
    "generate_ai_career_suggestions",
    "generate_ai_course_suggestions",
]

# Backward-compatible cache decorator
try:
    cache_resource = st.cache_resource  # Streamlit >= 1.18
except AttributeError:
    def cache_resource(func):  # no-op for older versions
        return func


@cache_resource
def is_openrouter_available() -> bool:
    """Check if OpenRouter API is accessible"""
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEFAULT_MODEL,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10
            },
            timeout=5
        )
        return response.status_code in [200, 400]  # 400 means API is accessible but request might be invalid
    except Exception as e:
        print(f"OpenRouter availability check failed: {e}")
        return False


def _truncate(text: str, limit: int = MAX_PROMPT_CHARS) -> str:
    """Truncate text to avoid exceeding API limits"""
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + "\n\n...[truncated]"


def call_openrouter_llm(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 1024,  # SPEED OPTIMIZED: Reduced from 2048
    enable_reasoning: bool = False,  # SPEED OPTIMIZED: Disabled by default for 3x faster responses
    system_message: Optional[str] = None
) -> str:
    """
    Call OpenRouter API with the specified model
    
    Args:
        prompt (str): The user prompt to send
        model (str): Model name (default: allenai/olmo-3.1-32b-think:free)
        temperature (float): Temperature for response generation (0.0-1.0)
        max_tokens (int): Maximum tokens in response
        enable_reasoning (bool): Enable reasoning mode for better responses
        system_message (str): Optional system message for context
    
    Returns:
        str: Generated response from the model
    """
    
    # Prepare messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": _truncate(prompt)})
    
    # Prepare request payload
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    # Enable reasoning for better quality responses
    if enable_reasoning:
        payload["reasoning"] = {"enabled": True}
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    last_exc = None
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Show progress in Streamlit if available
            try:
                with st.spinner(f'🤖 Generating AI response (attempt {attempt})...'):
                    response = requests.post(
                        OPENROUTER_URL,
                        headers=headers,
                        json=payload,
                        timeout=REQUEST_TIMEOUT_SECS
                    )
            except:
                # Not in Streamlit context
                print(f'🤖 Generating AI response (attempt {attempt})...')
                response = requests.post(
                    OPENROUTER_URL,
                    headers=headers,
                    json=payload,
                    timeout=REQUEST_TIMEOUT_SECS
                )
            
            # Check response status
            if response.status_code == 200:
                result = response.json()
                
                # Extract content from response
                if 'choices' in result and len(result['choices']) > 0:
                    message = result['choices'][0].get('message', {})
                    content = message.get('content', '').strip()
                    
                    if content:
                        # Log reasoning if available
                        reasoning_details = message.get('reasoning_details')
                        if reasoning_details:
                            print(f"🧠 Reasoning tokens used: {reasoning_details.get('reasoning_tokens', 0)}")
                        
                        return content
                    else:
                        return "Error: Empty response from model"
                else:
                    return f"Error: Invalid response structure: {result}"
            
            elif response.status_code == 401:
                return "Error: Invalid API key. Please check your OpenRouter API key."
            
            elif response.status_code == 429:
                error_msg = "⚠️ Rate limit reached. Retrying..."
                try:
                    st.warning(error_msg)
                except:
                    print(error_msg)
                time.sleep(2 * attempt)
                continue
            
            else:
                error_data = response.json() if response.text else {}
                error_message = error_data.get('error', {}).get('message', response.text)
                return f"Error: API returned status {response.status_code}: {error_message}"
        
        except requests.exceptions.Timeout:
            last_exc = "Request timed out"
            if attempt < MAX_RETRIES:
                try:
                    st.warning(f"⚠️ Attempt {attempt} timed out, retrying...")
                except:
                    print(f"⚠️ Attempt {attempt} timed out, retrying...")
                time.sleep(1 * attempt)
                continue
            return "Error: Request timed out. Please try again."
        
        except requests.exceptions.ConnectionError as e:
            last_exc = str(e)
            if attempt < MAX_RETRIES:
                try:
                    st.warning(f"⚠️ Connection error, retrying...")
                except:
                    print(f"⚠️ Connection error, retrying...")
                time.sleep(1 * attempt)
                continue
            return "Error: Cannot connect to OpenRouter API. Please check your internet connection."
        
        except Exception as e:
            last_exc = str(e)
            error_msg = f"❌ Unexpected error: {str(e)}"
            try:
                st.error(error_msg)
            except:
                print(error_msg)
            return f"Error: {str(e)}"
    
    return f"Error: All retry attempts failed. Last error: {last_exc}"


def _generate_resume_improvements_fallback(resume_text: str, jd_text: str, missing_skills: List[str]) -> str:
    """
    Generate comprehensive resume improvements without LLM using intelligent analysis
    """
    top_missing = list(dict.fromkeys([s.strip() for s in missing_skills]))[:8]
    
    # Simple keyword analysis
    jd_keywords = set()
    if jd_text:
        import re
        words = re.findall(r'\b[A-Za-z]{3,}\b', jd_text.lower())
        common_buzzwords = {'experience', 'skills', 'required', 'preferred', 'years', 'team', 'work'}
        jd_keywords = set([w for w in words if w not in common_buzzwords][:10])
    
    improvements = [
        "### 🚀 AI-Powered Resume Enhancement Recommendations",
        "\n**Immediate Action Items:**",
        "\n• **Professional Summary**: Add a compelling 2-3 line summary highlighting your value proposition",
        "• **Keywords Optimization**: Integrate job-specific terms naturally throughout your resume", 
        "• **Quantify Achievements**: Add metrics (percentages, dollar amounts, time saved) to your accomplishments",
        "• **Skills Section**: Create a dedicated technical skills section with relevant technologies",
        "• **Action Verbs**: Start each bullet point with strong action verbs (Led, Developed, Optimized, Implemented)"
    ]
    
    if jd_keywords:
        improvements.extend([
            "\n**Job-Specific Keywords to Include:**",
            f"\n• Integrate these terms: {', '.join(list(jd_keywords)[:6])}",
            "• Use them naturally in your experience descriptions and skills section"
        ])
    
    if top_missing:
        improvements.extend([
            "\n**Address Missing Skills:**",
            "• **Highlight Transferable Experience**: Show how your current experience relates to required skills"
        ])
        for skill in top_missing[:5]:
            improvements.append(f"  - For {skill}: Describe any related projects, coursework, or self-study")
    
    improvements.extend([
        "\n**Professional Formatting:**",
        "• **Consistent Structure**: Use the same format for each role (Title, Company, Dates, Bullets)",
        "• **Bullet Point Optimization**: Limit to 3-5 bullets per role, prioritize most relevant accomplishments",
        "• **Length Management**: Keep to 1-2 pages, focus on most recent and relevant experience",
        "\n**ATS Optimization:**",
        "• **Standard Sections**: Use clear headings (Experience, Education, Skills, Projects)",
        "• **Keyword Density**: Ensure important terms appear 2-3 times throughout the document",
        "• **Simple Formatting**: Avoid complex layouts, stick to standard fonts and bullet points",
        "\n✅ **Next Steps**: Review each section against these recommendations and update 2-3 bullets to better showcase your fit for this specific role."
    ])
    
    return "\n".join(improvements)


def enhance_resume_section(resume_text: str, jd_text: str, missing_skills: List[str]) -> str:
    """
    Enhance resume section using OpenRouter LLM with improved prompts
    """
    # Quick availability check and instant fallback
    if not is_openrouter_available():
        return _generate_resume_improvements_fallback(resume_text, jd_text, missing_skills)

    # Improved, more focused prompt for better results
    system_message = "You are an expert resume writer and career coach with 15+ years of experience helping candidates land their dream jobs."
    
    prompt = f"""Analyze the resume and job description below, then provide specific, actionable recommendations to improve the resume.

CURRENT RESUME:
{_truncate(resume_text, 2000)}

JOB DESCRIPTION:
{_truncate(jd_text, 2000)}

MISSING SKILLS TO ADDRESS:
{', '.join(missing_skills[:10])}

Provide 5-8 specific resume improvements in this format:
• [Section]: [Specific improvement with example]

Focus on:
1. Adding relevant keywords from the job description
2. Quantifying achievements with numbers/percentages
3. Highlighting transferable skills
4. Addressing missing skills through existing experience
5. Improving action verbs and impact statements

Resume Improvements:"""

    result = call_openrouter_llm(prompt, temperature=0.3, max_tokens=800, enable_reasoning=False, system_message=system_message)
    
    if isinstance(result, str) and result.startswith("Error:"):
        return _generate_resume_improvements_fallback(resume_text, jd_text, missing_skills)
    
    return result


def generate_project_ideas(resume_text: str, skills: List[str]) -> str:
    """
    Generate rich, recruiter-ready project ideas using OpenRouter LLM
    """
    skills_joined = ', '.join(skills)

    system_message = """You are a senior career coach and staff-level engineer who crafts standout portfolio projects that demonstrate real-world impact and hiring signals."""

    prompt = f"""Propose 3-5 high-impact, realistic project ideas tailored to the candidate.

Candidate Background:
RESUME TEXT:
{_truncate(resume_text, 2000)}

KNOWN SKILLS:
{skills_joined}

Requirements:
- Ideas must solve real problems (not toy demos)
- Balance ambition with feasibility (2-6 weeks per project)
- Each idea must be technically specific and implementation-ready
- Favor measurable outcomes and evaluation metrics
- Prefer modern, in-demand stacks aligned with the candidate's skills

Output Format (Markdown):
For each project, provide:
1) Title
2) One-line value proposition
3) Target users and real-world use cases
4) Tech stack (primary + optional alternatives)
5) Step-by-step implementation plan (5-10 concrete steps)
6) Data sources/APIs
7) Evaluation metrics and acceptance criteria
8) Stretch goals (2-3 scoped enhancements)
9) Resume bullets (2-3 STAR-format achievements)
10) Suggested timeline (week-by-week)
11) Suggested repo structure
12) Demo plan

Generate the projects now."""

    if not is_openrouter_available():
        return (
            "### Project Ideas (Fast Fallback)\n"
            "1. Metrics Dashboard: Build a small app that ingests CSV/JSON and renders KPI charts.\n"
            "2. Data ETL Mini-Pipeline: Extract from an API, clean with pandas, load to SQLite, expose a simple API.\n"
            "3. Resume Keyword Highlighter: Highlight JD-aligned keywords in a resume with a web UI.\n"
        )
    
    result = call_openrouter_llm(prompt, temperature=0.5, max_tokens=1500, enable_reasoning=False, system_message=system_message)
    
    if isinstance(result, str) and result.startswith("Error:"):
        return (
            "### Project Ideas (Fast Fallback)\n"
            "1. Metrics Dashboard: Build a small app that ingests CSV/JSON and renders KPI charts.\n"
            "2. Data ETL Mini-Pipeline: Extract from an API, clean with pandas, load to SQLite, expose a simple API.\n"
            "3. Resume Keyword Highlighter: Highlight JD-aligned keywords in a resume with a web UI.\n"
        )
    
    return result


def generate_cover_letter(resume_text: str, jd_text: str, skills: List[str]) -> str:
    """
    Generate a concise, tailored cover letter using OpenRouter LLM
    """
    skills_joined = ', '.join(skills)

    system_message = "You are an expert technical recruiter and senior hiring manager with deep knowledge of what makes compelling cover letters."

    prompt = f"""Draft a short, role-aligned cover letter (200-300 words) tailored to the given job description, grounded in the candidate's resume.

RESUME:
{_truncate(resume_text, 2000)}

JOB DESCRIPTION:
{_truncate(jd_text, 2000)}

KNOWN SKILLS:
{skills_joined}

Requirements:
- Use a professional, confident tone
- Reflect 2-3 specific JD requirements and map them to candidate strengths
- Include one brief accomplishment with measurable impact if present
- Avoid buzzwords and cliches
- End with a polite CTA to continue the conversation

Output: Plain text cover letter."""

    if not is_openrouter_available():
        return (
            "Dear Hiring Team,\n\n"
            "I'm excited to apply for this role. My background aligns with the position's core requirements, and I've delivered measurable results in related projects."
            " I'm particularly drawn to your focus on impact and quality. I'd welcome the chance to discuss how I can contribute.\n\n"
            "Best regards,\nYour Name"
        )
    
    result = call_openrouter_llm(prompt, temperature=0.4, max_tokens=600, enable_reasoning=False, system_message=system_message)
    
    if isinstance(result, str) and result.startswith("Error:"):
        return (
            "Dear Hiring Team,\n\n"
            "I'm excited to apply for this role. My background aligns with the position's core requirements, and I've delivered measurable results in related projects."
            " I'm particularly drawn to your focus on impact and quality. I'd welcome the chance to discuss how I can contribute.\n\n"
            "Best regards,\nYour Name"
        )
    
    return result


def generate_ai_career_suggestions(interest_data: dict, skill_data: dict) -> List[dict]:
    """
    Generate AI-powered career suggestions using OpenRouter based on user interests and skills
    """
    from career_webscraper import get_career_scraper
    
    # Prepare user profile
    academic_interests = interest_data.get('academic_interests', [])
    hobby_interests = interest_data.get('hobby_interests', [])
    work_environment = interest_data.get('work_environment', '')
    motivation = interest_data.get('motivation', '')
    learning_interests = skill_data.get('learning_interests', [])
    current_skills = skill_data.get('current_skills', {})
    experience_level = skill_data.get('experience_level', '')
    
    # Flatten current skills
    all_current_skills = []
    for category, skills in current_skills.items():
        all_current_skills.extend(skills)
    
    system_message = "You are an expert career counselor with deep knowledge of the Indian job market and career development."
    
    prompt = f"""Generate 4-6 personalized career recommendations in JSON format.

USER PROFILE:
Academic: {', '.join(academic_interests) if academic_interests else 'None'}
Hobbies: {', '.join(hobby_interests) if hobby_interests else 'None'}
Work Environment: {work_environment}
Motivation: {motivation}
Learning Interests: {', '.join(learning_interests) if learning_interests else 'None'}
Current Skills: {', '.join(all_current_skills) if all_current_skills else 'None'}
Experience: {experience_level}

Requirements:
- Suggest careers matching their profile
- Indian market salary ranges (₹1-20 LPA)
- Include learning paths
- Mix entry-level and growth positions

Output ONLY valid JSON in this exact format:
{{
  "careers": [
    {{
      "title": "Career Name",
      "description": "What this career involves",
      "skills_needed": ["Skill1", "Skill2"],
      "learning_path": "How to get started",
      "salary_range": "₹X-Y LPA",
      "growth": "High/Medium/Stable",
      "match_reason": "Why this fits",
      "entry_level": "Entry/Mid/Senior",
      "time_to_start": "X-Y months"
    }}
  ]
}}

Generate exactly 4-6 careers. Keep descriptions short and complete. Output ONLY the JSON, no additional text."""

    try:
        # Get real-time career data from web scraping
        scraper = get_career_scraper()
        web_career_data = {}
        
        if learning_interests:
            web_career_data = scraper.get_career_trends(learning_interests[:3])
        
        # Enhance prompt with real-time data
        if web_career_data:
            prompt += f"\n\nREAL-TIME MARKET DATA:\n"
            for skill, data in web_career_data.items():
                prompt += f"- {skill}: {data['job_count']} jobs, {data['avg_salary']}, {data['growth_trend']} growth\n"
        
        # Call OpenRouter API
        response = call_openrouter_llm(prompt, temperature=0.4, max_tokens=1200, enable_reasoning=False, system_message=system_message)
        
        if response and not response.startswith("Error:"):
            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in markdown
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.find("```", json_start)
                    json_str = response[json_start:json_end].strip()
                elif "```" in response:
                    json_start = response.find("```") + 3
                    json_end = response.find("```", json_start)
                    json_str = response[json_start:json_end].strip()
                else:
                    json_str = response.strip()
                
                # Parse JSON
                career_data = json.loads(json_str)
                careers = career_data.get('careers', [])
                
                # Validate and format the careers
                formatted_careers = []
                for career in careers:
                    if isinstance(career, dict) and 'title' in career:
                        formatted_career = {
                            'title': career.get('title', 'Unknown Career'),
                            'description': career.get('description', 'No description available'),
                            'skills_needed': career.get('skills_needed', []),
                            'learning_path': career.get('learning_path', 'No learning path specified'),
                            'salary_range': career.get('salary_range', '₹2-8 LPA'),
                            'growth': career.get('growth', 'Medium'),
                            'match_reason': career.get('match_reason', 'Good fit based on your profile'),
                            'entry_level': career.get('entry_level', 'Entry'),
                            'time_to_start': career.get('time_to_start', '3-6 months')
                        }
                        formatted_careers.append(formatted_career)
                
                if formatted_careers:
                    return formatted_careers
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {response[:500]}...")
        
        # Fall back to hardcoded suggestions
        return _get_fallback_career_suggestions(interest_data, skill_data)
        
    except Exception as e:
        print(f"Error generating AI career suggestions: {e}")
        return _get_fallback_career_suggestions(interest_data, skill_data)


def _get_fallback_career_suggestions(interest_data: dict, skill_data: dict) -> List[dict]:
    """Fallback career suggestions when AI is not available"""
    recommendations = []
    learning_interests = skill_data.get('learning_interests', [])
    
    # Tech careers
    tech_keywords = ['Programming', 'Data Science', 'Web Development', 'Mobile App Development', 
                   'Machine Learning', 'Cybersecurity', 'Cloud Computing']
    has_tech_interest = (interest_data.get('tech_score', 0) >= 1 or 
                        any(keyword in learning_interests for keyword in tech_keywords))
    
    if has_tech_interest:
        recommendations.extend([
            {
                'title': 'Software Developer',
                'description': 'Build applications and software solutions',
                'skills_needed': ['Programming', 'Problem Solving', 'Logic'],
                'learning_path': 'Start with Python or JavaScript basics',
                'salary_range': '₹3-15 LPA',
                'growth': 'High',
                'match_reason': 'Matches your technical interests and problem-solving skills',
                'entry_level': 'Entry',
                'time_to_start': '3-6 months'
            },
            {
                'title': 'Data Analyst',
                'description': 'Analyze data to help businesses make decisions',
                'skills_needed': ['Statistics', 'Excel', 'SQL', 'Python'],
                'learning_path': 'Learn Excel, SQL, and basic Python',
                'salary_range': '₹2-12 LPA',
                'growth': 'Very High',
                'match_reason': 'Great for analytical minds and data enthusiasts',
                'entry_level': 'Entry',
                'time_to_start': '2-4 months'
            }
        ])
    
    # Fallback recommendations
    if not recommendations:
        recommendations.extend([
            {
                'title': 'Customer Service Representative',
                'description': 'Help customers with their needs and inquiries',
                'skills_needed': ['Communication', 'Patience', 'Problem Solving'],
                'learning_path': 'Develop communication skills and learn customer service tools',
                'salary_range': '₹1.5-4 LPA',
                'growth': 'Stable',
                'match_reason': 'Good entry-level position for developing professional skills',
                'entry_level': 'Entry',
                'time_to_start': '1-2 months'
            }
        ])
    
    return recommendations


def generate_ai_course_suggestions(skills: List[str], user_profile: dict = None) -> List[dict]:
    """
    Generate AI-powered course suggestions using web scraping + OpenRouter LLM
    """
    from career_webscraper import get_career_scraper
    
    try:
        # Get real-time course data from web scraping
        scraper = get_career_scraper()
        web_course_data = scraper.get_course_recommendations(skills[:3])
        
        system_message = "You are a learning advisor with expertise in online education platforms and career development."
        
        # Create prompt for LLM to analyze and recommend courses
        prompt = f"""Analyze these real-time courses and recommend the best ones in JSON format.

SKILLS TO LEARN: {', '.join(skills)}

REAL-TIME COURSES FOUND:
"""
        
        for skill, courses in web_course_data.items():
            prompt += f"\n{skill}:\n"
            for course in courses[:3]:
                prompt += f"- {course['title']} ({course['platform']}) - {course['price']} - Rating: {course['rating']}\n"
        
        prompt += f"""
USER PROFILE:
{user_profile if user_profile else 'General learner'}

Requirements:
- Recommend 3-5 best courses from the real-time data
- Consider price, rating, and platform reputation
- Mix free and paid options
- Include learning path suggestions

Output ONLY valid JSON in this exact format:
{{
  "recommended_courses": [
    {{
      "title": "Course Title",
      "platform": "Platform Name",
      "price": "Price",
      "rating": "Rating",
      "url": "Course URL",
      "why_recommended": "Why this course is good",
      "learning_order": 1
    }}
  ],
  "learning_path": "Suggested learning sequence"
}}

Output ONLY the JSON, no additional text."""
        
        # Call OpenRouter for course recommendations
        response = call_openrouter_llm(prompt, temperature=0.4, max_tokens=1000, enable_reasoning=False, system_message=system_message)
        
        if response and not response.startswith("Error:"):
            try:
                # Extract JSON from response
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.find("```", json_start)
                    json_str = response[json_start:json_end].strip()
                elif "```" in response:
                    json_start = response.find("```") + 3
                    json_end = response.find("```", json_start)
                    json_str = response[json_start:json_end].strip()
                else:
                    json_str = response.strip()
                
                # Parse JSON
                course_data = json.loads(json_str)
                recommended_courses = course_data.get('recommended_courses', [])
                
                # Add web scraped data to recommendations
                enhanced_courses = []
                for course in recommended_courses:
                    enhanced_course = {
                        'title': course.get('title', 'Unknown Course'),
                        'platform': course.get('platform', 'Unknown Platform'),
                        'price': course.get('price', 'Free/Paid'),
                        'rating': course.get('rating', '4.5'),
                        'url': course.get('url', '#'),
                        'why_recommended': course.get('why_recommended', 'Good course for learning'),
                        'learning_order': course.get('learning_order', 1),
                        'duration': '4-8 weeks',
                        'skills_covered': skills[:3]
                    }
                    enhanced_courses.append(enhanced_course)
                
                return enhanced_courses
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error in course suggestions: {e}")
        
        # Fall back to web scraped courses
        fallback_courses = []
        for skill, courses in web_course_data.items():
            for course in courses[:2]:
                fallback_courses.append({
                    'title': course['title'],
                    'platform': course['platform'],
                    'price': course['price'],
                    'rating': course['rating'],
                    'url': course.get('url', '#'),
                    'why_recommended': f'Recommended for learning {skill}',
                    'learning_order': len(fallback_courses) + 1,
                    'duration': '4-8 weeks',
                    'skills_covered': [skill]
                })
        
        return fallback_courses[:5]
        
    except Exception as e:
        print(f"Error generating course suggestions: {e}")
        return []

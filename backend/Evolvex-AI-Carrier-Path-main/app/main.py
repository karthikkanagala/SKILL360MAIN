import streamlit as st
import requests
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from parsing import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from skills import extract_skills
from llm_enhancer import enhance_resume_section
from local_llm import generate_cover_letter, generate_ai_career_suggestions
from learning_resources import get_learning_resources
from course_suggestions import (
    get_course_suggestions, 
    get_learning_path, 
    get_skill_gap_courses,
    format_course_suggestions,
    get_platform_summary,
    get_ai_course_recommendations
)
from course_tracker import get_tracker, CourseStatus
from ai_networking import get_networking_engine, ConnectionType, EventType
from ai_realtime_analyzer import get_realtime_analyzer
from project_ideas import generate_project_ideas
from fit_classifier import predict_fit
from progress_tracker import get_progress_tracker
from interview_prep import (
    generate_interview_questions, 
    evaluate_answer, 
    generate_interview_tips,
    calculate_interview_readiness_score,
    get_question_by_type,
    get_question_by_difficulty
)
from github_analyzer import analyze_github_profile
from portfolio_analyzer import analyze_portfolio
from multi_source_integration import integrate_portfolio
from ui_components import (
    show_loading_animation, show_success_animation, create_animated_card,
    create_progress_ring, create_stat_card, create_timeline_item, create_badge
)
# Lazy import for NER to avoid Python 3.14 compatibility issues with spaCy
# Will be imported only when needed and if compatible

# Sidebar for instructions and info
with st.sidebar:
    st.markdown('# 📋 How to Use')
    st.markdown('---')
    
    st.markdown('''
    ### Step-by-Step Guide:
    
    **1. 📄 Upload Documents**
    - Upload your resume (PDF/DOCX)
    - Upload job/internship description (PDF/DOCX/TXT)
    
    **2. 🔍 Document Analysis**
    - Review extracted text
    - Check detected skills
    
    **3. 📊 Career Score & Matching**
    - View your career compatibility score
    - Identify missing skills
    
    **4. 🎯 AI Recommendations**
    - Get learning resources
    - Generate project ideas
    - Improve your resume with AI
    
    **5. 🎯 Interview Preparation**
    - Generate personalized questions
    - Practice with AI feedback
    - Get readiness assessment
    ''')
    
    st.markdown('---')
    st.markdown('### 🔒 Privacy Notice')
    st.info('Your documents are processed locally and never stored on our servers.')
    
    st.markdown('### 🛠️ Advanced Technology Stack')
    with st.expander('View Tech Details'):
        st.markdown('''
        **🚀 Advanced ML Engine:**
        - **XGBoost Classifier**: 78.14% accuracy
        - **Real Data**: 6,241 resume-job pairs
        - **Features**: 10,012 engineered features
        - **Performance**: 89.57% ROC AUC score
        
        **🤖 AI/NLP Stack:**
        - **Local Llama Model**: Resume enhancement & interview prep via Ollama
        - **spaCy NER**: Advanced skill extraction  
        - **TF-IDF Vectorization**: Text analysis
        - **Statistical Features**: Text processing
        - **Interview AI**: Personalized Q&A generation & evaluation
        
        **🔧 Framework & UI:**
        - **Streamlit**: Interactive interface
        - **scikit-learn**: ML pipeline
        - **PyPDF2, python-docx**: Document parsing
        - **Ollama API**: Local AI model integration
        ''')

# Load Custom CSS
def load_custom_css():
    css_file = os.path.join(os.path.dirname(__file__), '../.streamlit/style.css')
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass  # CSS file not found, use default styling

load_custom_css()

# Enhanced Title with Animation
st.markdown('''
<div style="text-align: center; margin-bottom: 2rem; animation: fadeIn 0.8s ease-in;">
    <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 Skill360
    </h1>
    <p style="font-size: 1.2rem; color: #e5e7eb; font-weight: 500;">
        AI-Powered Holistic Career Development Platform
    </p>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); border-radius: 16px; margin-bottom: 2rem; border-left: 4px solid #667eea; animation: slideInRight 0.6s ease-out;">
    <span style="font-size:1.1em; color:#ffffff; font-weight:500;">
        ✨ Resume Optimization • 🎯 Job Matching • 📊 Portfolio Analysis • 🌐 Career Growth
    </span>
</div>
''', unsafe_allow_html=True)

# Progress Tracking Dashboard
progress_tracker = get_progress_tracker()
progress_summary = progress_tracker.get_progress_summary()

# Display progress metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🔥 Streak Days",
        value=progress_summary["streak_days"],
        delta=f"{progress_summary['total_sessions']} sessions"
    )

with col2:
    st.metric(
        label="📊 Skills Assessed",
        value=progress_summary["skills_assessed"],
        delta="Keep learning!"
    )

with col3:
    st.metric(
        label="📝 Resumes Analyzed",
        value=progress_summary["resumes_analyzed"],
        delta="Improve your profile"
    )

with col4:
    st.metric(
        label="🎯 Interviews Practiced",
        value=progress_summary["interviews_practiced"],
        delta="Build confidence"
    )

with col5:
    st.metric(
        label="🏆 Achievements",
        value=progress_summary["achievements_count"],
        delta="Great progress!"
    )

# Recent achievements
recent_achievements = progress_tracker.get_recent_achievements(3)
if recent_achievements:
    st.markdown("### 🏆 Recent Achievements")
    achievement_cols = st.columns(len(recent_achievements))
    for i, achievement in enumerate(recent_achievements):
        with achievement_cols[i]:
            st.markdown(f"**{achievement['icon']} {achievement['name']}**")
            st.caption(achievement['description'])

# Learning insights
insights = progress_tracker.get_learning_insights()
if insights["recommendations"]:
    st.markdown("### 💡 Learning Insights")
    for recommendation in insights["recommendations"][:3]:
        st.info(f"💡 {recommendation}")

st.markdown("---")

# Enhanced NER extraction - Python 3.14 compatible
# Uses improved regex-based extraction with context awareness
try:
    # Import the Python 3.14 compatible NER extractor
    from ner_skill_extractor_py314 import extract_skills_ner
    use_ner = True
    st.success("✅ Enhanced skill extraction enabled (Python 3.14 compatible)")
except Exception as e:
    use_ner = False
    st.warning(f"⚠️ Could not load enhanced extractor: {str(e)[:100]}")

st.divider()
# LLM availability toggle/info (local lightweight check to avoid import issues)
def _is_ollama_available():
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False

llm_available = _is_ollama_available()
with st.sidebar:
    st.markdown('---')
    if llm_available:
        st.success('🧠 Local LLM detected (Ollama)')
    else:
        st.warning('🧠 Local LLM not detected — AI generation will use basic fallbacks')


st.markdown('## 📁 Upload Documents')
st.markdown('Upload your resume and job/internship description to get started with AI-powered career scoring and analysis.')

# Beginner mode toggle
st.markdown('---')
beginner_mode = st.checkbox('🎓 I\'m a beginner - I don\'t have a resume or job/internship description yet', 
                           help='Check this if you\'re just starting your career journey and need guidance')

if beginner_mode:
    st.markdown('## 🌟 Welcome, Future Professional!')
    st.markdown('Don\'t worry about not having a resume yet. Let\'s discover your interests, assess your skills, and create a personalized career roadmap for you!')
    
    # Beginner assessment tabs
    beginner_tab1, beginner_tab2, beginner_tab3, beginner_tab4 = st.tabs([
        '🎯 Interest Assessment', '📚 Skill Discovery', '🚀 Career Paths', '📝 Resume Builder'
    ])
    
    with beginner_tab1:
        st.markdown('### 🎯 Discover Your Interests')
        st.markdown('Answer these questions to help us understand what career paths might interest you.')
        
        # Interest assessment questions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('**What subjects did you enjoy most in school?**')
            academic_interests = st.multiselect(
                'Select all that apply:',
                ['Mathematics', 'Science', 'English/Literature', 'History', 'Art', 'Music', 'Physical Education', 'Computer Science', 'Business Studies', 'Languages'],
                key='academic_interests'
            )
            
            st.markdown('**What activities do you enjoy in your free time?**')
            hobby_interests = st.multiselect(
                'Select all that apply:',
                ['Coding/Programming', 'Design/Creativity', 'Reading', 'Sports', 'Gaming', 'Music', 'Writing', 'Problem Solving', 'Helping Others', 'Building Things', 'Research', 'Teaching'],
                key='hobby_interests'
            )
        
        with col2:
            st.markdown('**What type of work environment appeals to you?**')
            work_environment = st.selectbox(
                'Choose your preference:',
                ['Office with team collaboration', 'Remote work from home', 'Creative studio/workspace', 'Laboratory/research facility', 'Outdoor/field work', 'Startup environment', 'Corporate setting', 'Freelance/independent'],
                key='work_environment'
            )
            
            st.markdown('**What motivates you most?**')
            motivation = st.selectbox(
                'Choose your primary motivation:',
                ['Solving complex problems', 'Helping people', 'Creating new things', 'Learning continuously', 'Leading teams', 'Making money', 'Work-life balance', 'Making a difference'],
                key='motivation'
            )
        
        # Generate interest-based recommendations
        if st.button('🔍 Analyze My Interests', type='primary'):
            with st.spinner('🤖 Analyzing your interests and generating career suggestions...'):
                # Enhanced interest analysis with more comprehensive scoring
                all_interests = academic_interests + hobby_interests
                
                # Tech interest scoring - expanded keywords
                tech_keywords = ['Mathematics', 'Science', 'Computer Science', 'Coding/Programming', 
                               'Problem Solving', 'Building Things', 'Research']
                tech_interest = len([x for x in all_interests if x in tech_keywords])
                
                # Creative interest scoring - expanded keywords  
                creative_keywords = ['Art', 'Music', 'Design/Creativity', 'Writing', 'Reading']
                creative_interest = len([x for x in all_interests if x in creative_keywords])
                
                # Business interest scoring - expanded keywords
                business_keywords = ['Business Studies', 'Helping Others', 'Teaching', 'Languages']
                business_interest = len([x for x in all_interests if x in business_keywords])
                
                # Additional scoring based on work environment and motivation
                if work_environment in ['Office with team collaboration', 'Startup environment', 'Corporate setting']:
                    business_interest += 1
                elif work_environment in ['Creative studio/workspace', 'Laboratory/research facility']:
                    creative_interest += 1
                elif work_environment in ['Remote work from home', 'Freelance/independent']:
                    tech_interest += 1
                
                if motivation in ['Solving complex problems', 'Learning continuously']:
                    tech_interest += 1
                elif motivation in ['Creating new things', 'Making a difference']:
                    creative_interest += 1
                elif motivation in ['Helping people', 'Leading teams']:
                    business_interest += 1
                
                st.session_state.interest_analysis = {
                    'tech_score': tech_interest,
                    'creative_score': creative_interest,
                    'business_score': business_interest,
                    'academic_interests': academic_interests,
                    'hobby_interests': hobby_interests,
                    'work_environment': work_environment,
                    'motivation': motivation
                }
            st.success('✅ Interest analysis complete! Check the Career Paths tab for recommendations.')
    
    with beginner_tab2:
        st.markdown('### 📚 Skill Discovery & Assessment')
        st.markdown('Let\'s identify what skills you already have and what you\'d like to learn.')
        
        # Current skills assessment
        st.markdown('**What skills do you currently have? (Select all that apply)**')
        
        skill_categories = {
            'Technical Skills': ['Basic Computer Use', 'Microsoft Office', 'Social Media', 'Basic Programming', 'Web Design', 'Data Analysis', 'Digital Marketing'],
            'Soft Skills': ['Communication', 'Teamwork', 'Problem Solving', 'Time Management', 'Leadership', 'Creativity', 'Adaptability'],
            'Languages': ['English', 'Hindi', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Other'],
            'Academic Skills': ['Research', 'Writing', 'Mathematics', 'Science', 'Critical Thinking', 'Presentation', 'Project Management']
        }
        
        current_skills = {}
        for category, skills in skill_categories.items():
            st.markdown(f'**{category}:**')
            selected_skills = st.multiselect(
                f'Select your {category.lower()}:',
                skills,
                key=f'current_skills_{category.lower().replace(" ", "_")}'
            )
            current_skills[category] = selected_skills
        
        # Learning interests
        st.markdown('---')
        st.markdown('**What would you like to learn?**')
        learning_interests = st.multiselect(
            'Select areas you\'re interested in learning:',
            ['Programming (Python, JavaScript, etc.)', 'Data Science & Analytics', 'Web Development', 'Mobile App Development', 'Digital Marketing', 'Graphic Design', 'Project Management', 'Business Analysis', 'Cybersecurity', 'Cloud Computing', 'Machine Learning', 'UI/UX Design'],
            key='learning_interests'
        )
        
        # Experience level
        st.markdown('---')
        st.markdown('**What\'s your current experience level?**')
        experience_level = st.selectbox(
            'Choose your level:',
            ['Complete Beginner (No experience)', 'Some Experience (Basic knowledge)', 'Intermediate (Some projects done)', 'Advanced (Ready for professional work)'],
            key='experience_level'
        )
        
        # Generate skill recommendations
        if st.button('📊 Analyze My Skills', type='primary'):
            with st.spinner('🤖 Analyzing your skills and creating a learning plan...'):
                # Calculate skill scores
                total_current_skills = sum(len(skills) for skills in current_skills.values())
                
                st.session_state.skill_analysis = {
                    'current_skills': current_skills,
                    'learning_interests': learning_interests,
                    'experience_level': experience_level,
                    'total_skills': total_current_skills
                }
            st.success('✅ Skill analysis complete! Check the Career Paths tab for personalized recommendations.')
    
    with beginner_tab3:
        st.markdown('### 🚀 Discover Your Career Paths')
        st.markdown('Based on your interests and skills, here are some career paths that might suit you.')
        
        # Display recommendations if analysis is available
        if 'interest_analysis' in st.session_state and 'skill_analysis' in st.session_state:
            interest_data = st.session_state.interest_analysis
            skill_data = st.session_state.skill_analysis
            
            # Generate AI-powered career recommendations
            with st.spinner('🤖 AI is analyzing your profile and generating personalized career suggestions...'):
                recommendations = generate_ai_career_suggestions(interest_data, skill_data)
            
            # Display AI-powered recommendations
            if recommendations:
                st.markdown(f'**🎯 AI found {len(recommendations)} personalized career paths for you:**')
                
                for i, rec in enumerate(recommendations[:8]):  # Show top 8 AI suggestions
                    with st.expander(f"{rec['title']} - {rec['salary_range']}", expanded=False):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Description:** {rec['description']}")
                            st.markdown(f"**Skills Needed:** {', '.join(rec['skills_needed'])}")
                            st.markdown(f"**Learning Path:** {rec['learning_path']}")
                            
                            # Show AI reasoning if available
                            if 'match_reason' in rec:
                                st.markdown(f"**🤖 Why AI suggests this:** {rec['match_reason']}")
                            
                            # Show additional AI insights if available
                            if 'entry_level' in rec:
                                st.markdown(f"**Entry Level:** {rec['entry_level']}")
                            if 'time_to_start' in rec:
                                st.markdown(f"**Time to Start:** {rec['time_to_start']}")
                        
                        with col2:
                            st.metric('Growth Potential', rec['growth'])
                            st.metric('Salary Range', rec['salary_range'])
                            
                            if st.button(f'📚 Learn More', key=f'learn_more_{i}'):
                                st.info(f"Great choice! {rec['title']} is an excellent career path. Start by learning the basic skills mentioned above.")
            else:
                st.info("Please complete the Interest Assessment and Skill Discovery tabs first to get personalized career recommendations.")
        else:
            st.info("Please complete the Interest Assessment and Skill Discovery tabs first to get personalized career recommendations.")
    
    with beginner_tab4:
        st.markdown('### 📝 AI-Powered Resume Builder')
        st.markdown('Let\'s create your first resume based on your interests and skills!')
        
        if 'interest_analysis' in st.session_state and 'skill_analysis' in st.session_state:
            # Personal information
            st.markdown('**Personal Information:**')
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input('Full Name', key='resume_name')
                email = st.text_input('Email', key='resume_email')
                phone = st.text_input('Phone Number', key='resume_phone')
            
            with col2:
                location = st.text_input('Location (City, State)', key='resume_location')
                linkedin = st.text_input('LinkedIn Profile (optional)', key='resume_linkedin')
                github = st.text_input('GitHub Profile (optional)', key='resume_github')
            
            # Education
            st.markdown('---')
            st.markdown('**Education:**')
            col1, col2, col3 = st.columns(3)
            
            with col1:
                degree = st.selectbox('Degree Level', ['High School', 'Diploma', 'Bachelor\'s', 'Master\'s', 'Other'], key='resume_degree')
            with col2:
                field_of_study = st.text_input('Field of Study', key='resume_field')
            with col3:
                graduation_year = st.number_input('Graduation Year', min_value=2020, max_value=2030, value=2024, key='resume_year')
            
            # Generate resume
            if st.button('🚀 Generate My Resume', type='primary'):
                if full_name and email:
                    with st.spinner('🤖 Creating your personalized resume...'):
                        # Create a basic resume structure
                        resume_content = f"""
# {full_name}
{email} | {phone} | {location}
{f'LinkedIn: {linkedin}' if linkedin else ''} | {f'GitHub: {github}' if github else ''}

## Education
{degree} in {field_of_study} - {graduation_year}

## Skills
"""
                        
                        # Add skills from assessment
                        for category, skills in st.session_state.skill_analysis['current_skills'].items():
                            if skills:
                                resume_content += f"\n**{category}:** {', '.join(skills)}\n"
                        
                        resume_content += f"""
## Learning Interests
{', '.join(st.session_state.skill_analysis['learning_interests'])}

## Career Objective
Recent graduate with strong interest in technology and problem-solving. Eager to learn and contribute to innovative projects while developing professional skills in a dynamic environment.

## Projects (Suggested)
- Personal learning projects in {', '.join(st.session_state.skill_analysis['learning_interests'][:2])}
- Academic projects demonstrating analytical and problem-solving skills
- Online course completion certificates

## Additional Information
- Strong communication and teamwork skills
- Quick learner with passion for continuous improvement
- Familiar with modern technology and digital tools
"""
                        
                        st.session_state.generated_resume = resume_content
                    st.success('✅ Your resume has been generated!')
            
            # Display generated resume
            if 'generated_resume' in st.session_state:
                st.markdown('---')
                st.markdown('#### 📄 Your Generated Resume')
                st.markdown(st.session_state.generated_resume)
                
                # Download option
                st.download_button(
                    label='💾 Download Resume as Text',
                    data=st.session_state.generated_resume,
                    file_name=f'{full_name.replace(" ", "_")}_Resume.txt',
                    mime='text/plain'
                )
                
                if st.button('🔄 Generate New Resume'):
                    st.session_state.generated_resume = None
                    st.rerun()
        else:
            st.info("Please complete the Interest Assessment and Skill Discovery tabs first to generate your resume.")
    
    # Learning Resources for Beginners
    st.markdown('---')
    st.markdown('### 📚 Beginner Learning Resources')
    st.markdown('Get started with these carefully curated learning paths and resources.')
    
    # Learning resources tabs
    learning_tab1, learning_tab2, learning_tab3 = st.tabs(['🎯 Skill-Based Learning', '💼 Career-Specific Paths', '🆓 Free Resources'])
    
    with learning_tab1:
        st.markdown('#### 🎯 Learn by Skill Category')
        
        skill_learning_paths = {
            'Programming Basics': {
                'description': 'Start your coding journey with these beginner-friendly resources',
                'resources': [
                    {'name': 'Python for Beginners', 'platform': 'Codecademy', 'duration': '20 hours', 'cost': 'Free', 'url': 'https://www.codecademy.com/learn/learn-python-3'},
                    {'name': 'JavaScript Fundamentals', 'platform': 'freeCodeCamp', 'duration': '300 hours', 'cost': 'Free', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/'},
                    {'name': 'HTML & CSS Basics', 'platform': 'W3Schools', 'duration': '10 hours', 'cost': 'Free', 'url': 'https://www.w3schools.com/html/'},
                    {'name': 'Introduction to Programming', 'platform': 'Coursera', 'duration': '40 hours', 'cost': 'Free', 'url': 'https://www.coursera.org/learn/intro-programming'}
                ]
            },
            'Data Analysis': {
                'description': 'Learn to work with data and make data-driven decisions',
                'resources': [
                    {'name': 'Excel for Data Analysis', 'platform': 'LinkedIn Learning', 'duration': '15 hours', 'cost': 'Free Trial', 'url': 'https://www.linkedin.com/learning/excel-essential-training-microsoft-365'},
                    {'name': 'SQL for Beginners', 'platform': 'Khan Academy', 'duration': '8 hours', 'cost': 'Free', 'url': 'https://www.khanacademy.org/computing/computer-programming/sql'},
                    {'name': 'Introduction to Data Science', 'platform': 'edX', 'duration': '60 hours', 'cost': 'Free', 'url': 'https://www.edx.org/learn/data-science'},
                    {'name': 'Google Analytics Academy', 'platform': 'Google', 'duration': '12 hours', 'cost': 'Free', 'url': 'https://analytics.google.com/analytics/academy/'}
                ]
            },
            'Digital Marketing': {
                'description': 'Master the art of digital marketing and online promotion',
                'resources': [
                    {'name': 'Google Digital Marketing Course', 'platform': 'Google', 'duration': '40 hours', 'cost': 'Free', 'url': 'https://learndigital.withgoogle.com/digitalgarage'},
                    {'name': 'Social Media Marketing', 'platform': 'HubSpot Academy', 'duration': '6 hours', 'cost': 'Free', 'url': 'https://academy.hubspot.com/courses/social-media-marketing'},
                    {'name': 'Content Marketing Basics', 'platform': 'Coursera', 'duration': '20 hours', 'cost': 'Free', 'url': 'https://www.coursera.org/learn/content-marketing'},
                    {'name': 'Email Marketing Fundamentals', 'platform': 'Mailchimp', 'duration': '4 hours', 'cost': 'Free', 'url': 'https://mailchimp.com/marketing-glossary/email-marketing/'}
                ]
            },
            'Design & Creativity': {
                'description': 'Develop your creative skills and design thinking',
                'resources': [
                    {'name': 'Graphic Design Basics', 'platform': 'Canva Design School', 'duration': '8 hours', 'cost': 'Free', 'url': 'https://www.canva.com/designschool/'},
                    {'name': 'UI/UX Design Principles', 'platform': 'Figma', 'duration': '12 hours', 'cost': 'Free', 'url': 'https://www.figma.com/resource-library/'},
                    {'name': 'Adobe Creative Suite Basics', 'platform': 'Adobe', 'duration': '20 hours', 'cost': 'Free Trial', 'url': 'https://helpx.adobe.com/creative-suite/tutorials.html'},
                    {'name': 'Design Thinking Process', 'platform': 'IDEO U', 'duration': '6 hours', 'cost': 'Free', 'url': 'https://www.ideou.com/pages/design-thinking'}
                ]
            }
        }
        
        for skill_category, content in skill_learning_paths.items():
            with st.expander(f"{skill_category} - {content['description']}", expanded=False):
                st.markdown(f"**{content['description']}**")
                st.markdown("---")
                
                for resource in content['resources']:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{resource['name']}**")
                    with col2:
                        st.markdown(f"⏱️ {resource['duration']}")
                    with col3:
                        st.markdown(f"💰 {resource['cost']}")
                    with col4:
                        st.markdown(f"[🔗 Learn]({resource['url']})")
    
    with learning_tab2:
        st.markdown('#### 💼 Career-Specific Learning Paths')
        
        if 'interest_analysis' in st.session_state and 'skill_analysis' in st.session_state:
            st.markdown('**Personalized learning paths based on your interests:**')
            
            # Tech career path
            if st.session_state.interest_analysis['tech_score'] >= 2:
                st.markdown('##### 🖥️ Technology Career Path')
                st.markdown('**Phase 1: Foundation (2-3 months)**')
                st.markdown('- Learn basic programming (Python or JavaScript)')
                st.markdown('- Understand computer science fundamentals')
                st.markdown('- Practice problem-solving on platforms like HackerRank')
                
                st.markdown('**Phase 2: Specialization (3-6 months)**')
                st.markdown('- Choose a specialization (Web Dev, Data Science, Mobile, etc.)')
                st.markdown('- Build 2-3 projects to showcase your skills')
                st.markdown('- Learn version control with Git')
                
                st.markdown('**Phase 3: Professional Development (1-2 months)**')
                st.markdown('- Create a portfolio website')
                st.markdown('- Practice coding interviews')
                st.markdown('- Apply for internships or entry-level positions')
            
            # Creative career path
            if st.session_state.interest_analysis['creative_score'] >= 2:
                st.markdown('##### 🎨 Creative Career Path')
                st.markdown('**Phase 1: Design Fundamentals (1-2 months)**')
                st.markdown('- Learn design principles and color theory')
                st.markdown('- Master design tools (Figma, Adobe Creative Suite)')
                st.markdown('- Study successful designs and case studies')
                
                st.markdown('**Phase 2: Specialization (2-4 months)**')
                st.markdown('- Choose your focus (UI/UX, Graphic Design, Branding)')
                st.markdown('- Create a design portfolio with 5-10 projects')
                st.markdown('- Learn about user research and testing')
                
                st.markdown('**Phase 3: Professional Development (1-2 months)**')
                st.markdown('- Build a professional online presence')
                st.markdown('- Network with other designers')
                st.markdown('- Apply for design internships or freelance work')
            
            # Business career path
            if st.session_state.interest_analysis['business_score'] >= 2:
                st.markdown('##### 💼 Business Career Path')
                st.markdown('**Phase 1: Business Fundamentals (1-2 months)**')
                st.markdown('- Learn business analysis and project management')
                st.markdown('- Master Excel and data analysis tools')
                st.markdown('- Understand business processes and operations')
                
                st.markdown('**Phase 2: Specialization (2-4 months)**')
                st.markdown('- Choose your focus (Marketing, Operations, Finance)')
                st.markdown('- Learn industry-specific tools and software')
                st.markdown('- Complete relevant certifications')
                
                st.markdown('**Phase 3: Professional Development (1-2 months)**')
                st.markdown('- Build a professional network')
                st.markdown('- Create case studies and business proposals')
                st.markdown('- Apply for business internships or entry-level roles')
        else:
            st.info("Complete the Interest Assessment and Skill Discovery tabs to get personalized career learning paths.")
    
    with learning_tab3:
        st.markdown('#### 🆓 Free Learning Resources')
        st.markdown('High-quality free resources to kickstart your learning journey.')
        
        free_resources = {
            'Programming & Development': [
                {'name': 'freeCodeCamp', 'description': 'Complete coding bootcamp with certifications', 'url': 'https://www.freecodecamp.org/'},
                {'name': 'Codecademy', 'description': 'Interactive coding lessons (free tier available)', 'url': 'https://www.codecademy.com/'},
                {'name': 'W3Schools', 'description': 'Web development tutorials and references', 'url': 'https://www.w3schools.com/'},
                {'name': 'Khan Academy', 'description': 'Computer programming and computer science courses', 'url': 'https://www.khanacademy.org/computing/computer-programming'}
            ],
            'Data Science & Analytics': [
                {'name': 'Kaggle Learn', 'description': 'Data science micro-courses with hands-on practice', 'url': 'https://www.kaggle.com/learn'},
                {'name': 'DataCamp', 'description': 'Data science and analytics courses (free tier)', 'url': 'https://www.datacamp.com/'},
                {'name': 'Google Analytics Academy', 'description': 'Free analytics and data analysis courses', 'url': 'https://analytics.google.com/analytics/academy/'},
                {'name': 'IBM Data Science', 'description': 'Professional certificate in data science', 'url': 'https://www.coursera.org/professional-certificates/ibm-data-science'}
            ],
            'Design & Creativity': [
                {'name': 'Canva Design School', 'description': 'Graphic design tutorials and templates', 'url': 'https://www.canva.com/designschool/'},
                {'name': 'Figma Academy', 'description': 'UI/UX design courses and resources', 'url': 'https://www.figma.com/resource-library/'},
                {'name': 'Adobe Creative Cloud', 'description': 'Tutorials for Adobe software suite', 'url': 'https://helpx.adobe.com/creative-suite/tutorials.html'},
                {'name': 'YouTube Design Channels', 'description': 'Free design tutorials and inspiration', 'url': 'https://www.youtube.com/results?search_query=graphic+design+tutorial'}
            ],
            'Business & Marketing': [
                {'name': 'Google Digital Garage', 'description': 'Free digital marketing and business courses', 'url': 'https://learndigital.withgoogle.com/digitalgarage'},
                {'name': 'HubSpot Academy', 'description': 'Marketing, sales, and customer service courses', 'url': 'https://academy.hubspot.com/'},
                {'name': 'Coursera (Free Courses)', 'description': 'University-level courses with free audit option', 'url': 'https://www.coursera.org/'},
                {'name': 'edX', 'description': 'Free online courses from top universities', 'url': 'https://www.edx.org/'}
            ]
        }
        
        for category, resources in free_resources.items():
            with st.expander(f"{category}", expanded=False):
                for resource in resources:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{resource['name']}**")
                        st.markdown(f"_{resource['description']}_")
                    with col2:
                        st.markdown(f"[🔗 Visit]({resource['url']})")
    
    st.markdown('---')
    st.markdown('### 🎓 Ready to Start Your Career Journey?')
    st.markdown('Once you\'ve completed the assessments above, you can:')
    st.markdown('1. **Download your generated resume** from the Resume Builder tab')
    st.markdown('2. **Start learning** the skills recommended for your chosen career path')
    st.markdown('3. **Build projects** to showcase your abilities')
    st.markdown('4. **Apply for internships** or entry-level positions')
    st.markdown('5. **Come back here** to upload your updated resume and get more advanced career guidance!')
    
    # Option to switch to regular mode
    if st.button('📄 I have a resume now - Switch to Regular Mode'):
        st.session_state.beginner_mode = False
        st.rerun()

else:
    st.markdown('### 📄 Regular Mode')

# GitHub Profile Analysis Section - Always Visible
st.markdown('## 💻 GitHub Repository Analysis')
st.markdown('Analyze your GitHub profile to showcase your coding portfolio, projects, and contribution activity. Works independently or enhances your career score when combined with resume analysis.')

github_col1, github_col2 = st.columns([4, 1], gap="medium")

with github_col1:
    github_username = st.text_input(
        '🔗 Enter your GitHub username',
        placeholder='e.g., torvalds, github, or your username',
        help='We will analyze your public repositories and contributions',
        label_visibility="visible"
    )

with github_col2:
    st.markdown('<div style="height: 1.8rem;"></div>', unsafe_allow_html=True)
    analyze_button = st.button('🚀 Analyze', type='primary', use_container_width=True)

# Initialize session state for GitHub data
if 'github_data' not in st.session_state:
    st.session_state.github_data = None
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None

# Analyze GitHub profile when button clicked
if analyze_button and github_username:
    with st.spinner(f'🔍 Analyzing GitHub profile: @{github_username}...'):
        github_data = analyze_github_profile(github_username)
        
        if github_data and 'error' in github_data:
            # Handle errors
            if github_data['error'] == 'not_found':
                st.error(f"❌ {github_data['message']}")
                st.info("💡 **Suggestions:**\n- Check the spelling of the username\n- Ensure the profile is public\n- Try examples: `torvalds`, `github`, `microsoft`")
            elif github_data['error'] == 'rate_limit':
                st.warning(f"⚠️ {github_data['message']}")
                st.info("💡 You can continue with resume analysis while waiting for rate limits to reset.")
            else:
                st.error(f"⚠️ {github_data['message']}")
                st.info("💡 Please check your internet connection and try again.")
            st.session_state.github_data = None
            st.session_state.portfolio_data = None
        else:
            # Success!
            st.session_state.github_data = github_data
            st.success(f"✅ Successfully analyzed @{github_data['profile']['username']}'s profile!")
            
            # Run portfolio analysis
            with st.spinner('📊 Analyzing project portfolio...'):
                portfolio_data = analyze_portfolio(github_data)
                st.session_state.portfolio_data = portfolio_data
                if portfolio_data and 'error' not in portfolio_data:
                    st.success(f"✅ Portfolio analysis complete! Found {len(portfolio_data['projects'])} projects.")

# Display GitHub analysis if available
if st.session_state.github_data:
    github_data = st.session_state.github_data
    profile = github_data['profile']
    stats = github_data['statistics']
    languages = github_data['languages']
    
    st.markdown('---')
    st.markdown(f"### 👤 {profile['name']} (@{profile['username']})")
    
    if profile['bio'] and profile['bio'] != 'No bio available':
        st.markdown(f"*{profile['bio']}*")
    
    # Profile stats
    profile_cols = st.columns(5)
    with profile_cols[0]:
        st.metric('📦 Repositories', stats['total_repos'])
    with profile_cols[1]:
        st.metric('⭐ Stars', stats['total_stars'])
    with profile_cols[2]:
        st.metric('🍴 Forks', stats['total_forks'])
    with profile_cols[3]:
        st.metric('👥 Followers', profile['followers'])
    with profile_cols[4]:
        st.metric('💻 Languages', stats['languages_count'])
    
    # Contribution Score
    st.markdown('---')
    score_col1, score_col2 = st.columns([2, 1])
    
    with score_col1:
        st.markdown('### 🎯 GitHub Contribution Score')
        contribution_score = github_data['contribution_score']
        
        if contribution_score >= 80:
            st.success(f'🌟 Outstanding Contributor: {contribution_score}/100')
            score_color = '🟢'
        elif contribution_score >= 60:
            st.success(f'✅ Strong Contributor: {contribution_score}/100')
            score_color = '🟢'
        elif contribution_score >= 40:
            st.info(f'📈 Active Contributor: {contribution_score}/100')
            score_color = '🟡'
        else:
            st.info(f'🌱 Growing Contributor: {contribution_score}/100')
            score_color = '🟡'
        
        progress_cols = st.columns([8, 1])
        with progress_cols[0]:
            st.progress(contribution_score / 100)
        with progress_cols[1]:
            st.markdown(f"**{score_color}**")
    
    with score_col2:
        st.metric(
            'Activity Level',
            github_data['activity_level'],
            delta='Last 90 days'
        )
        account_years = github_data['account_age_days'] / 365
        st.metric(
            'Account Age',
            f'{account_years:.1f} years'
        )
    
    # Programming Languages
    if languages:
        st.markdown('---')
        st.markdown('### 💻 Programming Languages')
        
        lang_cols = st.columns(min(4, len(languages)))
        for idx, (lang, percentage) in enumerate(list(languages.items())[:8]):
            with lang_cols[idx % 4]:
                st.metric(lang, f'{percentage}%')
    
    # Top Repositories
    if github_data['top_repos']:
        st.markdown('---')
        st.markdown('### 🏆 Top Repositories')
        
        for repo in github_data['top_repos'][:3]:
            with st.expander(f"⭐ {repo['name']} ({repo['stars']} stars)"):
                st.markdown(f"**Language:** {repo['language']}")
                st.markdown(f"**Description:** {repo['description']}")
                st.markdown(f"**Stats:** ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks")
                st.markdown(f"[🔗 View on GitHub]({repo['url']})")
    
    # Portfolio Analysis Section
    if st.session_state.portfolio_data and 'error' not in st.session_state.portfolio_data:
        portfolio_data = st.session_state.portfolio_data
        summary = portfolio_data['summary']
        
        st.markdown('---')
        st.markdown('## 🎨 Project Portfolio Evaluation')
        
        # Overall Portfolio Rating
        st.markdown(f"### {summary['rating']} Portfolio")
        st.markdown(f"*{summary['message']}*")
        
        # Portfolio Scores
        score_cols = st.columns(3)
        with score_cols[0]:
            st.metric(
                '💪 Portfolio Strength',
                f"{portfolio_data['portfolio_strength']}/100",
                help='Overall quality and impact of projects'
            )
            st.progress(portfolio_data['portfolio_strength'] / 100)
        
        with score_cols[1]:
            st.metric(
                '🌈 Diversity Score',
                f"{portfolio_data['diversity_score']}/100",
                help='Technology stack and project type variety'
            )
            st.progress(portfolio_data['diversity_score'] / 100)
        
        with score_cols[2]:
            st.metric(
                '🎯 Skills Demonstrated',
                summary['skills_demonstrated'],
                help='Number of distinct skills shown through projects'
            )
        
        # Key Strengths
        if summary['strengths']:
            st.markdown('---')
            st.markdown('### ✨ Key Strengths')
            strength_cols = st.columns(len(summary['strengths']))
            for idx, strength in enumerate(summary['strengths']):
                with strength_cols[idx]:
                    st.success(f"✓ {strength}")
        
        # Project Analysis
        st.markdown('---')
        st.markdown('### 📋 Project Breakdown')
        
        project_cols = st.columns(2)
        
        with project_cols[0]:
            st.markdown('**By Complexity:**')
            complexity_dist = portfolio_data['categories']['by_complexity']
            for complexity, count in complexity_dist.items():
                complexity_emoji = {'Advanced': '🔥', 'Intermediate': '⚡', 'Beginner': '🌱'}
                st.write(f"{complexity_emoji.get(complexity, '•')} **{complexity}:** {count} project(s)")
        
        with project_cols[1]:
            st.markdown('**By Type:**')
            type_dist = portfolio_data['categories']['by_type']
            for proj_type, count in list(type_dist.most_common(4)):
                st.write(f"• **{proj_type}:** {count}")
        
        # Detailed Project Analysis
        st.markdown('---')
        st.markdown('### 🔍 Project Quality Analysis')
        
        for project in portfolio_data['projects']:
            with st.expander(f"**{project['name']}** - {project['complexity']} | Quality: {project['quality_score']}/100"):
                proj_cols = st.columns([2, 1])
                
                with proj_cols[0]:
                    st.markdown(f"**Description:** {project['description']}")
                    st.markdown(f"**Type:** {project['project_type']}")
                    st.markdown(f"**Primary Language:** {project['language']}")
                    
                    if project['skills']:
                        st.markdown(f"**Technologies Used:** {', '.join(project['skills'][:8])}")
                
                with proj_cols[1]:
                    st.metric('Quality Score', f"{project['quality_score']}/100")
                    st.metric('Impact Score', f"{project['impact_score']}/100")
                    st.metric('⭐ Stars', project['stars'])
                    st.metric('🍴 Forks', project['forks'])
        
        # Skill Demonstration
        if portfolio_data['skill_demonstration']['skills']:
            st.markdown('---')
            st.markdown('### 💼 Demonstrated Skills')
            
            skill_levels = portfolio_data['skill_demonstration']['skill_levels']
            
            # Group by proficiency
            strong_skills = [skill for skill, level in skill_levels.items() if level == 'Strong']
            moderate_skills = [skill for skill, level in skill_levels.items() if level == 'Moderate']
            basic_skills = [skill for skill, level in skill_levels.items() if level == 'Basic']
            
            if strong_skills:
                st.markdown('**🔥 Strong Proficiency** (3+ projects):')
                st.write(', '.join(strong_skills))
            
            if moderate_skills:
                st.markdown('**⚡ Moderate Proficiency** (2 projects):')
                st.write(', '.join(moderate_skills))
            
            if basic_skills:
                st.markdown('**🌱 Basic Exposure** (1 project):')
                st.write(', '.join(basic_skills))
        
        # Portfolio Gaps
        if portfolio_data['gaps']:
            st.markdown('---')
            st.markdown('### ⚠️ Portfolio Gaps & Areas to Improve')
            
            for gap in portfolio_data['gaps']:
                priority_color = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }
                
                with st.expander(f"{priority_color.get(gap['priority'], '•')} {gap['type']}: {gap['issue']}"):
                    st.markdown(f"**Priority:** {gap['priority']}")
                    st.markdown(f"**Suggestion:** {gap['suggestion']}")
        
        # Recommendations
        if portfolio_data['recommendations']:
            st.markdown('---')
            st.markdown('### 🚀 Actionable Recommendations')
            
            for idx, rec in enumerate(portfolio_data['recommendations'], 1):
                impact_emoji = {'High': '🔥', 'Medium': '⚡', 'Low': '💡'}
                
                with st.expander(f"{idx}. {rec['category']} - {impact_emoji.get(rec['impact'], '💡')} {rec['impact']} Impact"):
                    st.markdown(f"**Recommendation:** {rec['recommendation']}")
                    st.markdown(f"**Examples:**")
                    for example in rec['examples']:
                        st.markdown(f"  • {example}")
    
    st.markdown('---')

elif github_username and not analyze_button:
    st.info("👆 Click 'Analyze GitHub Profile' to fetch your GitHub statistics")

st.divider()

# Portfolio Website Analysis Section
st.markdown('## 🌐 Portfolio Website Analysis')
st.markdown('Analyze your portfolio website to get insights on quality, skills showcased, and professional presentation.')

portfolio_col1, portfolio_col2 = st.columns([4, 1], gap="medium")

with portfolio_col1:
    portfolio_url = st.text_input(
        '🔗 Enter your portfolio website URL',
        placeholder='e.g., https://yourname.dev or https://yourportfolio.com',
        help='We will analyze your portfolio for skills, projects, and professional presentation',
        label_visibility="visible"
    )

with portfolio_col2:
    st.markdown('<div style="height: 1.8rem;"></div>', unsafe_allow_html=True)
    analyze_portfolio_button = st.button('🔍 Analyze Website', type='primary', use_container_width=True, key='analyze_portfolio')

# Initialize session state for portfolio website data
if 'portfolio_website_data' not in st.session_state:
    st.session_state.portfolio_website_data = None

# Analyze portfolio website when button clicked
if analyze_portfolio_button and portfolio_url:
    with st.spinner(f'🔍 Analyzing portfolio website: {portfolio_url}...'):
        portfolio_website_data = integrate_portfolio(portfolio_url)
        
        if portfolio_website_data and 'error' in portfolio_website_data:
            st.error(f"❌ {portfolio_website_data['error']}")
            st.info("💡 **Suggestions:**\n- Check if the URL is correct and accessible\n- Ensure the website is publicly available\n- Try with https:// prefix")
            st.session_state.portfolio_website_data = None
        else:
            st.session_state.portfolio_website_data = portfolio_website_data
            st.success(f"✅ Successfully analyzed your portfolio website!")

# Display portfolio website analysis if available
if st.session_state.portfolio_website_data:
    portfolio_website_data = st.session_state.portfolio_website_data
    analysis = portfolio_website_data.get('analysis', {})
    
    st.markdown('---')
    st.markdown(f"### 🌐 Portfolio Website: {portfolio_website_data.get('url', 'Unknown')}")
    
    # Quality Score
    quality_score = portfolio_website_data.get('quality_score', 0)
    
    score_col1, score_col2 = st.columns([2, 1])
    
    with score_col1:
        st.markdown('### 🎯 Portfolio Quality Score')
        
        if quality_score >= 80:
            st.success(f'🌟 Excellent Portfolio: {quality_score}/100')
            score_color = '🟢'
        elif quality_score >= 60:
            st.success(f'✅ Good Portfolio: {quality_score}/100')
            score_color = '🟢'
        elif quality_score >= 40:
            st.info(f'📈 Developing Portfolio: {quality_score}/100')
            score_color = '🟡'
        else:
            st.warning(f'🌱 Needs Improvement: {quality_score}/100')
            score_color = '🟡'
        
        progress_cols = st.columns([8, 1])
        with progress_cols[0]:
            st.progress(quality_score / 100)
        with progress_cols[1]:
            st.markdown(f"**{score_color}**")
    
    with score_col2:
        st.metric(
            'Skills Found',
            analysis.get('skill_count', 0),
            delta='Technical skills'
        )
        st.metric(
            'Completeness',
            f"{sum([analysis.get('has_projects_section', False), analysis.get('has_contact_section', False), analysis.get('has_about_section', False)]) * 33}%"
        )
    
    # Portfolio Sections
    st.markdown('---')
    st.markdown('### 📋 Portfolio Sections')
    
    section_cols = st.columns(3)
    
    with section_cols[0]:
        if analysis.get('has_projects_section'):
            st.success('✅ Projects Section')
        else:
            st.error('❌ Projects Section Missing')
    
    with section_cols[1]:
        if analysis.get('has_contact_section'):
            st.success('✅ Contact Section')
        else:
            st.error('❌ Contact Section Missing')
    
    with section_cols[2]:
        if analysis.get('has_about_section'):
            st.success('✅ About Section')
        else:
            st.error('❌ About Section Missing')
    
    # Skills Found
    skills_mentioned = analysis.get('skills_mentioned', [])
    if skills_mentioned:
        st.markdown('---')
        st.markdown('### 💻 Skills Showcased on Your Website')
        
        # Display skills in a nice grid
        skill_cols = st.columns(4)
        for idx, skill in enumerate(skills_mentioned[:12]):  # Show top 12 skills
            with skill_cols[idx % 4]:
                st.markdown(f"🔹 **{skill}**")
        
        if len(skills_mentioned) > 12:
            st.caption(f"... and {len(skills_mentioned) - 12} more skills")
    
    # Social Links
    social_links = portfolio_website_data.get('social_links', {})
    if any(social_links.values()):
        st.markdown('---')
        st.markdown('### 🔗 Social Links Found')
        
        link_cols = st.columns(2)
        with link_cols[0]:
            if social_links.get('github'):
                st.success(f"✅ GitHub: @{social_links['github']}")
            else:
                st.warning("⚠️ GitHub link not found")
        
        with link_cols[1]:
            if social_links.get('linkedin'):
                st.success(f"✅ LinkedIn: {social_links['linkedin']}")
            else:
                st.warning("⚠️ LinkedIn link not found")
    
    # Recommendations
    st.markdown('---')
    st.markdown('### 💡 Portfolio Improvement Recommendations')
    
    recommendations = []
    
    if not analysis.get('has_projects_section'):
        recommendations.append("🎯 Add a dedicated Projects section to showcase your work")
    
    if not analysis.get('has_contact_section'):
        recommendations.append("📧 Add a Contact section with your email and social links")
    
    if not analysis.get('has_about_section'):
        recommendations.append("👤 Add an About/Bio section to introduce yourself")
    
    if analysis.get('skill_count', 0) < 5:
        recommendations.append("💻 Highlight more technical skills throughout your portfolio")
    
    if not social_links.get('github'):
        recommendations.append("🐙 Add your GitHub profile link to show your code")
    
    if not social_links.get('linkedin'):
        recommendations.append("💼 Add your LinkedIn profile for professional networking")
    
    if quality_score < 70:
        recommendations.append("✨ Improve overall design and content quality")
        recommendations.append("📝 Add detailed project descriptions with technologies used")
        recommendations.append("🎨 Ensure consistent styling and professional presentation")
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            st.info(f"{idx}. {rec}")
    else:
        st.success("🎉 Your portfolio looks great! Keep it updated with new projects.")
    
    st.markdown('---')

elif portfolio_url and not analyze_portfolio_button:
    st.info("👆 Click 'Analyze Website' to check your portfolio quality")

st.divider()

# Resume and Job Description Upload Section
st.markdown('## 📄 Resume & Job/Internship Matching (Optional)')
st.markdown('Upload your resume and job/internship description for comprehensive career scoring and skill gap analysis.')

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('### 📄 Your Resume')
    resume_file = st.file_uploader(
        'Choose your resume file', 
        type=['pdf', 'docx'], 
        help='Supported formats: PDF, DOCX (max 10MB)',
        key='resume_upload'
    )
    if resume_file:
        st.success(f'✅ {resume_file.name} uploaded successfully!')
        
with col2:
    st.markdown('### 💼 Job/Internship Description')
    jd_file = st.file_uploader(
        'Choose job/internship description file', 
        type=['pdf', 'docx', 'txt'], 
        help='Supported formats: PDF, DOCX, TXT (max 10MB)',
        key='jd_upload'
    )
    if jd_file:
        st.success(f'✅ {jd_file.name} uploaded successfully!')

resume_text = None
jd_text = None

if resume_file:
    if resume_file.type == 'application/pdf':
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        resume_text = extract_text_from_docx(resume_file)
    else:
        st.warning('Unsupported resume file type.')

if jd_file:
    if jd_file.type == 'application/pdf':
        jd_text = extract_text_from_pdf(jd_file)
    elif jd_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        jd_text = extract_text_from_docx(jd_file)
    elif jd_file.type == 'text/plain':
        jd_text = extract_text_from_txt(jd_file)
    else:
        st.warning('Unsupported Job/Internship Description file type.')

if resume_text or jd_text:
    st.markdown('---')
    st.markdown('## 🔍 Document Analysis')
    st.markdown('Review the extracted text and detected skills from your documents.')
    
    tab1, tab2 = st.tabs(['📄 Resume Analysis', '💼 Job/Internship Description Analysis'])
    
    with tab1:
        if resume_text:
            # Stats about resume
            word_count = len(resume_text.split())
            char_count = len(resume_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Word Count', word_count)
            with col2:
                st.metric('Character Count', char_count)
            with col3:
                st.metric('Status', 'Processed ✅')
            
            with st.expander('View Extracted Resume Text', expanded=False):
                st.text_area('Resume Content', resume_text, height=200, key='resume_text_display')
            
            # Skills extraction
            with st.spinner('🔍 Extracting skills from resume...'):
                if use_ner:
                    try:
                        resume_skills = extract_skills_ner(resume_text)
                    except Exception as e:
                        st.warning(f"Enhanced extraction failed, using basic extraction: {str(e)}")
                        resume_skills = extract_skills(resume_text)
                else:
                    resume_skills = extract_skills(resume_text)
                
                # Track progress
                progress_tracker.update_activity("resumes_analyzed")
                progress_tracker.update_activity("skills_assessed")
            
            if resume_skills:
                st.success(f'✅ Found {len(resume_skills)} skills in your resume')
                with st.expander(' Skills Detected in Resume', expanded=True):
                    # Display skills in a nice grid
                    cols = st.columns(3)
                    for i, skill in enumerate(sorted(resume_skills)):
                        with cols[i % 3]:
                            st.markdown(f'🔸 **{skill}**')
            else:
                st.warning('⚠️ No common technical skills detected in resume')
        else:
            st.info('📤 Upload a resume to see detailed analysis')
    
    with tab2:
        if jd_text:
            # Stats about job description
            word_count_jd = len(jd_text.split())
            char_count_jd = len(jd_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Word Count', word_count_jd)
            with col2:
                st.metric('Character Count', char_count_jd)
            with col3:
                st.metric('Status', 'Processed ✅')
            
            with st.expander('View Extracted Job/Internship Description Text', expanded=False):
                st.text_area('Job/Internship Description Content', jd_text, height=200, key='jd_text_display')
            
            # Skills extraction
            with st.spinner('🔍 Extracting required skills...'):
                if use_ner:
                    try:
                        jd_skills = extract_skills_ner(jd_text)
                    except Exception as e:
                        st.warning(f"Enhanced extraction failed, using basic extraction: {str(e)}")
                        jd_skills = extract_skills(jd_text)
                else:
                    jd_skills = extract_skills(jd_text)
            
            if jd_skills:
                st.success(f'✅ Found {len(jd_skills)} required skills')
                with st.expander('Skills Required for Job', expanded=True):
                    # Display skills in a nice grid
                    cols = st.columns(3)
                    for i, skill in enumerate(sorted(jd_skills)):
                        with cols[i % 3]:
                            st.markdown(f'🔹 **{skill}**')
            else:
                st.warning('⚠️ No common technical skills detected in job/internship description')
        else:
            st.info('📤 Upload a job/internship description to see detailed analysis')

if resume_text and jd_text and resume_skills and jd_skills:
    st.markdown('---')
    
    # Skill Match Analysis
    matched_skills = set(resume_skills) & set(jd_skills)
    missing_skills = set(jd_skills) - set(resume_skills)
    extra_skills = set(resume_skills) - set(jd_skills)
    match_score = len(matched_skills) / len(jd_skills) * 100 if jd_skills else 0
    
    st.markdown('## 📊 Career Score & Skill Match Analysis')
    st.markdown('Comprehensive analysis of how well your skills align with job/internship requirements.')
    
    # Display metrics in a beautiful card layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label='🎯 Career Score', 
            value=f'{match_score:.1f}%',
            delta=f"{match_score-50:.1f}% vs avg" if match_score > 0 else None
        )
    with col2:
        st.metric(
            label='✅ Matched Skills', 
            value=len(matched_skills),
            delta=f"{len(matched_skills)} found"
        )
    with col3:
        st.metric(
            label='❌ Missing Skills', 
            value=len(missing_skills),
            delta=f"{len(missing_skills)} to learn"
        )
    with col4:
        st.metric(
            label='Extra Skills', 
            value=len(extra_skills),
            delta=f"{len(extra_skills)} bonus"
        )
    
    # Enhanced progress bar with color coding and better messaging
    st.markdown('### 🏆 Compatibility Assessment')
    
    if match_score >= 80:
        st.success(f'🌟 Outstanding match! You have {match_score:.1f}% skill compatibility')
        progress_color = "🟢"
    elif match_score >= 60:
        st.success(f'✅ Excellent match! {match_score:.1f}% skill compatibility')
        progress_color = "🟢"
    elif match_score >= 40:
        st.warning(f'⚡ Good match with growth potential: {match_score:.1f}% compatibility')
        progress_color = "🟡"
    elif match_score >= 20:
        st.warning(f'🔄 Moderate match - skill development recommended: {match_score:.1f}% compatibility')
        progress_color = "🟡"
    else:
        st.error(f'🎯 Growth opportunity - consider targeted skill development: {match_score:.1f}% compatibility')
        progress_color = "🔴"
    
    # Progress bar
    progress_col1, progress_col2 = st.columns([8, 1])
    with progress_col1:
        st.progress(match_score/100)
    with progress_col2:
        st.markdown(f"**{progress_color}**")
    
    # Detailed skill breakdown with enhanced visualization
    with st.expander('🔍 Detailed Skill Breakdown', expanded=True):
        skill_tab1, skill_tab2, skill_tab3 = st.tabs(['✅ Matched Skills', '❌ Missing Skills', ' Extra Skills'])
        
        with skill_tab1:
            if matched_skills:
                st.markdown(f'**You have {len(matched_skills)} skills that match the job/internship requirements:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(matched_skills)):
                    with cols[i % 2]:
                        st.markdown(f'✅ **{skill}**')
            else:
                st.markdown('🚫 _No directly matched skills found_')
        
        with skill_tab2:
            if missing_skills:
                st.markdown(f'**Focus on developing these {len(missing_skills)} skills:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(missing_skills)):
                    with cols[i % 2]:
                        st.markdown(f'🎯 **{skill}**')
            else:
                st.markdown('🎉 _You have all required skills!_')
        
        with skill_tab3:
            if extra_skills:
                st.markdown(f'**You have {len(extra_skills)} additional valuable skills:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(extra_skills)):
                    with cols[i % 2]:
                        st.markdown(f'∙ **{skill}**')
            else:
                st.markdown('💼 _No additional skills detected beyond job requirements_')

    st.markdown('---')
    
    # Dedicated Skills Gap Analysis Section - More Prominent
    if missing_skills:
        st.markdown('## 🎯 Skills Gap Analysis - What You Need to Learn')
        st.markdown('These are the skills required by the job/internship that were not found in your resume. Focus on developing these to improve your candidacy.')
        
        # Create a more prominent display for missing skills
        gap_cols = st.columns([3, 1])
        
        with gap_cols[0]:
            # Display missing skills in a grid with priority indicators
            st.markdown('### 📚 Skills to Develop:')
            
            # Categorize missing skills by priority (this is a simple heuristic)
            priority_high = []
            priority_medium = []
            
            for skill in sorted(missing_skills):
                # High priority: common tech skills
                if skill.lower() in ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 'react', 'node', 'nodejs']:
                    priority_high.append(skill)
                else:
                    priority_medium.append(skill)
            
            if priority_high:
                st.markdown('**🔴 High Priority Skills:**')
                cols = st.columns(3)
                for i, skill in enumerate(priority_high):
                    with cols[i % 3]:
                        st.error(f'🎯 {skill}', icon="🔴")
            
            if priority_medium:
                st.markdown('**🟡 Important Skills:**')
                cols = st.columns(3)
                for i, skill in enumerate(priority_medium):
                    with cols[i % 3]:
                        st.warning(f'📖 {skill}', icon="🟡")
        
        with gap_cols[1]:
            st.metric(
                label='Skills Gap',
                value=f'{len(missing_skills)}',
                delta=f'-{len(missing_skills)} to learn',
                delta_color='inverse'
            )
            
            # Time estimate
            estimated_weeks = len(missing_skills) * 2  # Rough estimate: 2 weeks per skill
            st.metric(
                label='Est. Learning Time',
                value=f'{estimated_weeks} weeks',
                help='Estimated time to learn these skills at a moderate pace'
            )
        
        st.markdown('---')
    else:
        st.success('## ✅ No Skills Gap Detected!')
        st.markdown('🎉 You already have all the skills mentioned in the job/internship description. Great work!')
        st.markdown('---')
    
    # ML Fit Classifier with enhanced presentation
    st.markdown('## 🤖 Advanced AI Career Fit Assessment')
    st.markdown('Our enterprise-grade ML model (trained on 6,241 real resume-job pairs) analyzes your complete profile for accurate career predictions.')
    
    with st.spinner(' Advanced AI is analyzing your profile...'):
        # Try advanced ML model first with full text
        result = predict_fit(
            resume_text=resume_text,
            job_description=jd_text,
            match_score=match_score,
            num_matched=len(matched_skills),
            num_missing=len(missing_skills)
        )
    
    # Extract prediction details
    prediction = result['prediction']
    confidence = result['confidence']
    probabilities = result['probabilities']
    model_type = result.get('model_type', 'unknown')
    
    # Create assessment card with enhanced styling
    assessment_col1, assessment_col2 = st.columns([3, 1])
    
    with assessment_col1:
        if prediction in ['Good Fit', 'Potential Fit']:
            if prediction == 'Good Fit':
                st.success(f'🎉 **AI Prediction: {prediction}**')
                st.markdown('🚀 The advanced ML model indicates you are **excellently suited** for this role based on comprehensive analysis.')
            else:  # Potential Fit
                st.info(f'⭐ **AI Prediction: {prediction}**') 
                st.markdown('📈 The AI model shows **good potential** - with some skill development, you could be an excellent candidate.')
        else:  # No Fit
            st.warning(f'📊 **AI Prediction: {prediction}**')
            st.markdown('🎯 The AI suggests **focused skill development** to improve your alignment with this role.')
    
    with assessment_col2:
        # Enhanced confidence display
        if confidence > 0.8:
            confidence_level = "Very High"
            confidence_color = "🟢"
        elif confidence > 0.6:
            confidence_level = "High" 
            confidence_color = "🟢"
        elif confidence > 0.4:
            confidence_level = "Medium"
            confidence_color = "🟡"
        else:
            confidence_level = "Low"
            confidence_color = "🔴"
        
        st.metric(
            label='🎯 Career Fit Confidence', 
            value=f'{confidence*100:.1f}%',
            delta=f"{confidence_level} {confidence_color}"
        )
    
    # Assessment details focused on user-relevant information
    with st.expander('🔍 AI Assessment Details', expanded=False):
        # Detailed probabilities
        st.markdown('**📊 Prediction Confidence Breakdown:**')
        prob_cols = st.columns(len(probabilities))
        for i, (class_name, prob) in enumerate(probabilities.items()):
            with prob_cols[i]:
                st.metric(
                    label=class_name,
                    value=f'{prob*100:.1f}%',
                    delta="🎯" if class_name == prediction else ""
                )
        
        st.markdown('---')
        
        # Analysis factors
        st.markdown('**🔍 Factors analyzed by AI:**')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'📊 **Skill Match**: {match_score:.1f}%')
        with col2:
            st.markdown(f'✅ **Skills Matched**: {len(matched_skills)}')
        with col3:
            st.markdown(f'📚 **Skills to Develop**: {len(missing_skills)}')
        
        if model_type == 'advanced_ml':
            st.markdown('📝 **Text Analysis**: Resume & job description content, writing style, keyword density')
            st.markdown('📏 **Statistical Features**: Document length, vocabulary richness, sentence complexity')
            st.markdown('🔤 **TF-IDF Vectors**: 10,000+ text features capturing semantic similarity')
        
        st.markdown('---')
        
        # Enhanced recommendations
        if prediction == 'Good Fit':
            st.success('💡 **Recommendation**: You have an excellent profile for this role! Highlight your matched skills and relevant experience in your application.')
        elif prediction == 'Potential Fit':
            st.info('💡 **Recommendation**: You have good potential! Focus on developing 1-2 key missing skills and emphasize your transferable experience.')
        else:
            st.warning('💡 **Recommendation**: Focus on strategic skill development. Consider taking courses in the missing technical skills and building projects to demonstrate competency for this job/internship.')

    st.divider()
    
    # Learning Resources - Enhanced Section
    if missing_skills:
        st.markdown('## 📚 Learning Resources for Missing Skills')
        st.markdown('Start developing these skills today with curated learning resources!')
        
        resources = get_learning_resources(missing_skills)
        if resources:
            st.success(f'✅ Found learning resources for **{len(resources)}** out of **{len(missing_skills)}** missing skills')
            
            # Display resources in an enhanced format with better visibility
            st.markdown('### 🎓 Direct Learning Links:')
            resource_cols = st.columns(2)
            
            for idx, (skill, url) in enumerate(sorted(resources.items())):
                with resource_cols[idx % 2]:
                    with st.container():
                        st.markdown(f'''
                        <div style="padding: 10px; border-left: 3px solid #4CAF50; background-color: rgba(76, 175, 80, 0.1); margin-bottom: 10px;">
                            <strong>🎯 {skill.title()}</strong><br>
                            <a href="{url}" target="_blank" style="color: #4CAF50;">📖 Start Learning →</a>
                        </div>
                        ''', unsafe_allow_html=True)
            
            # Show skills without direct resources if any
            skills_without_resources = set(missing_skills) - set(resources.keys())
            if skills_without_resources:
                st.markdown('---')
                st.info(f'💡 **Additional skills to explore**: {", ".join(sorted(skills_without_resources))}')
                st.markdown('Search for these on: [Coursera](https://www.coursera.org) | [Udemy](https://www.udemy.com) | [YouTube](https://www.youtube.com) | [freeCodeCamp](https://www.freecodecamp.org)')
        else:
            st.info('💡 Consider searching for these skills on platforms like:')
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('🎓 [Coursera](https://www.coursera.org)')
            with col2:
                st.markdown('📺 [Udemy](https://www.udemy.com)')
            with col3:
                st.markdown('💻 [freeCodeCamp](https://www.freecodecamp.org)')
            with col4:
                st.markdown('📖 [YouTube](https://www.youtube.com)')
        
        st.divider()

    # Enhanced Course Suggestions
    if missing_skills or resume_skills:
        st.subheader('🎓 Comprehensive Course Recommendations')
        st.markdown('Get personalized course suggestions from top learning platforms to develop your skills.')
        
        # Course suggestion controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty_filter = st.selectbox(
                'Difficulty Level',
                ['All', 'Beginner', 'Intermediate', 'Advanced'],
                help='Filter courses by difficulty level'
            )
        
        with col2:
            course_type_filter = st.selectbox(
                'Course Type',
                ['All', 'Tutorial', 'Course', 'Specialization', 'Certification', 'Bootcamp'],
                help='Filter courses by type'
            )
        
        with col3:
            max_courses = st.slider(
                'Max Courses per Skill',
                min_value=1,
                max_value=5,
                value=3,
                help='Maximum number of courses to show per skill'
            )
        
        # Initialize session state for course suggestions
        if 'course_suggestions' not in st.session_state:
            st.session_state.course_suggestions = None
        if 'learning_path' not in st.session_state:
            st.session_state.learning_path = None
        
        # Generate course suggestions button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button('🎯 Get AI Course Recommendations', use_container_width=True, type='primary'):
                with st.spinner('🤖 AI is analyzing skills and finding real courses from the web...'):
                    # Get course suggestions for missing skills
                    target_skills = list(missing_skills)[:8] if missing_skills else list(resume_skills)[:5]
                    
                    # Apply filters
                    difficulty = difficulty_filter if difficulty_filter != 'All' else None
                    course_type = course_type_filter if course_type_filter != 'All' else None
                    
                    # Use AI-powered course recommendations
                    suggestions = get_ai_course_recommendations(
                        target_skills,
                        difficulty_preference=difficulty,
                        course_type_preference=course_type,
                        max_courses_per_skill=max_courses
                    )
                    
                    # Get learning path
                    learning_path = get_learning_path(target_skills)
                    
                    st.session_state.course_suggestions = suggestions
                    st.session_state.learning_path = learning_path
                
                st.success('✅ AI-powered course recommendations generated successfully!')
        
        with col2:
            if st.button('📚 Static Courses', use_container_width=True, help='Use pre-loaded course database'):
                with st.spinner('🔍 Loading course database...'):
                    # Get course suggestions for missing skills
                    target_skills = list(missing_skills)[:8] if missing_skills else list(resume_skills)[:5]
                    
                    # Apply filters
                    difficulty = difficulty_filter if difficulty_filter != 'All' else None
                    course_type = course_type_filter if course_type_filter != 'All' else None
                    
                    suggestions = get_course_suggestions(
                        target_skills,
                        difficulty_preference=difficulty,
                        course_type_preference=course_type,
                        max_courses_per_skill=max_courses
                    )
                    
                    # Get learning path
                    learning_path = get_learning_path(target_skills)
                    
                    st.session_state.course_suggestions = suggestions
                    st.session_state.learning_path = learning_path
                
                st.success('✅ Course recommendations loaded!')
        
        # Display course suggestions
        if st.session_state.course_suggestions:
            st.markdown('---')
            st.markdown('#### 🎯 Personalized Course Recommendations')
            
            # Platform summary with better styling
            platform_summary = get_platform_summary(st.session_state.course_suggestions)
            if platform_summary:
                st.markdown('**📊 Courses by Platform:**')
                platform_cols = st.columns(len(platform_summary))
                for i, (platform, count) in enumerate(platform_summary.items()):
                    with platform_cols[i]:
                        st.metric(platform, count)
                st.markdown('---')
            
            # Display courses in a more interactive way
            for skill, courses in st.session_state.course_suggestions.items():
                if courses:
                    with st.expander(f"📚 {skill.title()} - {len(courses)} courses", expanded=True):
                        for i, course in enumerate(courses):
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{course.title}**")
                                st.markdown(f"*{course.platform}* • {course.duration}")
                                if course.description:
                                    st.markdown(f"*{course.description[:100]}...*")
                                if course.skills_covered:
                                    st.markdown(f"**Skills:** {', '.join(course.skills_covered[:3])}")
                            
                            with col2:
                                if course.rating:
                                    st.markdown(f"⭐ {course.rating}")
                                st.markdown(f"**{course.difficulty.value}**")
                            
                            with col3:
                                if course.price:
                                    st.markdown(f"💰 {course.price}")
                                if course.url and course.url != '#':
                                    st.markdown(f"[🔗 Enroll]({course.url})")
                                else:
                                    st.markdown("🔗 Link N/A")
                            
                            if i < len(courses) - 1:
                                st.markdown("---")
            
            # Also show formatted version for copying
            with st.expander('📋 View All Courses (Text Format)', expanded=False):
                formatted_suggestions = format_course_suggestions(st.session_state.course_suggestions)
                st.markdown(formatted_suggestions)
            
            # Learning path section
            if st.session_state.learning_path:
                st.markdown('---')
                st.markdown('#### 🛤️ Structured Learning Path')
                st.markdown('Follow this structured path to develop your skills systematically:')
                
                path_tabs = st.tabs(['🌱 Foundation', '📈 Intermediate', '🚀 Advanced', '🎯 Specialization'])
                
                with path_tabs[0]:
                    if st.session_state.learning_path['foundation']:
                        st.markdown('**Start with these beginner courses:**')
                        for course in st.session_state.learning_path['foundation'][:3]:
                            st.markdown(f"• **{course.title}** ({course.platform}) - {course.duration}")
                            st.markdown(f"  [Enroll Here]({course.url})")
                    else:
                        st.info('No foundation courses found for your skills.')
                
                with path_tabs[1]:
                    if st.session_state.learning_path['intermediate']:
                        st.markdown('**Build on your foundation with these intermediate courses:**')
                        for course in st.session_state.learning_path['intermediate'][:3]:
                            st.markdown(f"• **{course.title}** ({course.platform}) - {course.duration}")
                            st.markdown(f"  [Enroll Here]({course.url})")
                    else:
                        st.info('No intermediate courses found for your skills.')
                
                with path_tabs[2]:
                    if st.session_state.learning_path['advanced']:
                        st.markdown('**Master your skills with these advanced courses:**')
                        for course in st.session_state.learning_path['advanced'][:3]:
                            st.markdown(f"• **{course.title}** ({course.platform}) - {course.duration}")
                            st.markdown(f"  [Enroll Here]({course.url})")
                    else:
                        st.info('No advanced courses found for your skills.')
                
                with path_tabs[3]:
                    if st.session_state.learning_path['specialization']:
                        st.markdown('**Earn certifications with these specialization programs:**')
                        for course in st.session_state.learning_path['specialization'][:3]:
                            st.markdown(f"• **{course.title}** ({course.platform}) - {course.duration}")
                            st.markdown(f"  [Enroll Here]({course.url})")
                    else:
                        st.info('No specialization courses found for your skills.')
            
            # Export options
            with st.expander('📋 Export Course Recommendations', expanded=False):
                st.text_area('Course Recommendations (Text Format)', formatted_suggestions, height=400, key='courses_copy')
                
                # Download as text file
                if st.button('💾 Download as Text File'):
                    st.download_button(
                        label='Download Course Recommendations',
                        data=formatted_suggestions,
                        file_name='course_recommendations.txt',
                        mime='text/plain'
                    )
            
            # Clear button
            if st.button('🗑️ Clear Course Recommendations', key='clear_courses'):
                st.session_state.course_suggestions = None
                st.session_state.learning_path = None
                st.rerun()
        
        st.divider()

    # Course Progress Tracking
    if missing_skills or resume_skills:
        st.subheader('📈 Course Progress Tracking')
        st.markdown('Track your learning progress and monitor your skill development journey.')
        
        # Initialize course tracker
        tracker = get_tracker()
        
        # Course tracking controls
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('### Add Course to Track')
            new_course_title = st.text_input('Course Title', placeholder='Enter course title')
            new_course_platform = st.selectbox('Platform', ['Coursera', 'Udemy', 'edX', 'freeCodeCamp', 'Other'])
            new_course_url = st.text_input('Course URL', placeholder='https://...')
            
            if st.button('➕ Add Course', type='primary'):
                if new_course_title and new_course_platform:
                    course_id = tracker.add_course(new_course_title, new_course_platform, new_course_url)
                    st.success(f'✅ Added "{new_course_title}" to your learning track!')
                    st.rerun()
                else:
                    st.error('Please fill in course title and platform.')
        
        with col2:
            # Learning statistics
            stats = tracker.get_learning_statistics()
            st.markdown('### 📊 Your Learning Stats')
            st.metric('Total Courses', stats['total_courses'])
            st.metric('Completed', stats['completed_courses'])
            st.metric('In Progress', stats['in_progress_courses'])
            st.metric('Completion Rate', f"{stats['completion_rate']}%")
        
        # Display tracked courses
        all_progress = tracker.get_all_progress()
        if all_progress:
            st.markdown('---')
            st.markdown('### 📚 Your Learning Journey')
            
            # Filter options
            status_filter = st.selectbox(
                'Filter by Status',
                ['All'] + [status.value for status in CourseStatus],
                key='status_filter'
            )
            
            # Display courses
            filtered_courses = all_progress
            if status_filter != 'All':
                filtered_courses = {
                    course_id: course for course_id, course in all_progress.items()
                    if course.status.value == status_filter
                }
            
            if filtered_courses:
                for course_id, course in filtered_courses.items():
                    with st.expander(f"{course.course_title} ({course.platform}) - {course.status.value}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**Status**: {course.status.value}")
                            st.markdown(f"**Progress**: {course.progress_percentage}%")
                            st.progress(course.progress_percentage / 100)
                        
                        with col2:
                            st.markdown(f"**Platform**: {course.platform}")
                            if course.start_date:
                                st.markdown(f"**Started**: {course.start_date[:10]}")
                            if course.completion_date:
                                st.markdown(f"**Completed**: {course.completion_date[:10]}")
                        
                        with col3:
                            if course.rating:
                                st.markdown(f"**Rating**: {'⭐' * course.rating}")
                            if course.actual_hours_spent > 0:
                                st.markdown(f"**Hours Spent**: {course.actual_hours_spent}")
                            if course.url:
                                st.markdown(f"[🔗 Course Link]({course.url})")
                        
                        # Update progress section
                        st.markdown("**Update Progress:**")
                        update_col1, update_col2, update_col3 = st.columns(3)
                        
                        with update_col1:
                            new_status = st.selectbox(
                                'Status',
                                [status.value for status in CourseStatus],
                                index=list(CourseStatus).index(course.status),
                                key=f'status_{course_id}'
                            )
                        
                        with update_col2:
                            new_progress = st.slider(
                                'Progress %',
                                min_value=0,
                                max_value=100,
                                value=course.progress_percentage,
                                key=f'progress_{course_id}'
                            )
                        
                        with update_col3:
                            new_hours = st.number_input(
                                'Hours Spent',
                                min_value=0,
                                value=course.actual_hours_spent,
                                key=f'hours_{course_id}'
                            )
                        
                        # Additional fields
                        new_notes = st.text_area(
                            'Notes',
                            value=course.notes,
                            placeholder='Add notes about your learning experience...',
                            key=f'notes_{course_id}'
                        )
                        
                        new_rating = st.selectbox(
                            'Rating (1-5 stars)',
                            [None, 1, 2, 3, 4, 5],
                            index=course.rating if course.rating else 0,
                            key=f'rating_{course_id}'
                        )
                        
                        # Update and delete buttons
                        button_col1, button_col2 = st.columns(2)
                        
                        with button_col1:
                            if st.button('💾 Update Progress', key=f'update_{course_id}'):
                                tracker.update_progress(
                                    course_id,
                                    status=CourseStatus(new_status),
                                    progress_percentage=new_progress,
                                    notes=new_notes,
                                    actual_hours_spent=new_hours,
                                    rating=new_rating
                                )
                                st.success('✅ Progress updated!')
                                st.rerun()
                        
                        with button_col2:
                            if st.button('🗑️ Delete Course', key=f'delete_{course_id}'):
                                tracker.delete_course(course_id)
                                st.success('✅ Course removed!')
                                st.rerun()
            else:
                st.info(f'No courses found with status: {status_filter}')
        
        # Export progress
        if all_progress:
            st.markdown('---')
            st.markdown('### 📋 Export Learning Progress')
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button('📄 Generate Progress Report'):
                    report = tracker.export_progress()
                    st.text_area('Learning Progress Report', report, height=400, key='progress_report')
            
            with col2:
                if st.button('💾 Download Progress Report'):
                    report = tracker.export_progress()
                    st.download_button(
                        label='Download Progress Report',
                        data=report,
                        file_name=f'learning_progress_{datetime.now().strftime("%Y%m%d")}.txt',
                        mime='text/plain'
                    )
        
        st.divider()

    # AI-Powered Networking & Mentorship
    if missing_skills or resume_skills:
        st.subheader('🤝 AI-Powered Networking & Mentorship')
        st.markdown('Connect with professionals, find mentors, and discover networking opportunities using real-time data.')
        
        # Initialize networking engine and real-time analyzer
        networking_engine = get_networking_engine()
        realtime_analyzer = get_realtime_analyzer()
        
        # Networking tabs
        networking_tab1, networking_tab2, networking_tab3, networking_tab4 = st.tabs([
            '🎯 Find Mentors', '📅 Networking Events', '💡 Market Insights', '🗺️ Learning Roadmap'
        ])
        
        with networking_tab1:
            st.markdown('### 🎯 Find Your Perfect Mentor')
            
            # Mentor search controls
            col1, col2, col3 = st.columns(3)
            
            with col1:
                mentorship_type = st.selectbox(
                    'Mentorship Type',
                    ['Career', 'Technical', 'Leadership', 'Industry'],
                    help='Type of mentorship you\'re looking for'
                )
            
            with col2:
                experience_level = st.selectbox(
                    'Your Experience Level',
                    ['Entry Level', 'Mid Level', 'Senior Level', 'Executive'],
                    help='Your current experience level'
                )
            
            with col3:
                if st.button('🔍 Find Mentors', type='primary'):
                    with st.spinner('🤖 AI is finding the best mentors for you...'):
                        target_skills = list(missing_skills)[:5] if missing_skills else list(resume_skills)[:5]
                        mentors = networking_engine.find_mentorship_opportunities(
                            target_skills, experience_level, mentorship_type
                        )
                        st.session_state.mentors = mentors
                    st.success(f'✅ Found {len(mentors)} potential mentors!')
            
            # Display mentors
            if 'mentors' in st.session_state and st.session_state.mentors:
                st.markdown('---')
                st.markdown('#### 🎯 Recommended Mentors')
                
                for i, mentor in enumerate(st.session_state.mentors[:5]):
                    with st.expander(f"{mentor.mentor_name} - {mentor.title} at {mentor.company}", expanded=False):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Expertise**: {', '.join(mentor.expertise_areas)}")
                            st.markdown(f"**Experience**: {mentor.experience_level}")
                            st.markdown(f"**Availability**: {mentor.availability}")
                            st.markdown(f"**Bio**: {mentor.bio}")
                        
                        with col2:
                            st.metric('Match Score', f"{mentor.match_score:.1%}")
                            st.markdown(f"**Contact**: {mentor.contact_info}")
                            
                            # Generate icebreaker
                            if st.button(f'💬 Get Icebreaker', key=f'icebreaker_{i}'):
                                common_skills = list(set(target_skills) & set(mentor.expertise_areas))
                                icebreakers = networking_engine.generate_networking_icebreakers(mentor, common_skills)
                                
                                st.markdown('**💬 Conversation Starters:**')
                                for icebreaker in icebreakers[:3]:
                                    st.markdown(f"• {icebreaker}")
        
        with networking_tab2:
            st.markdown('### 📅 Real-Time Networking Events')
            
            # Event search controls
            col1, col2 = st.columns(2)
            
            with col1:
                event_location = st.text_input('Location', value='Global', help='City, State, or "Global" for online events')
            
            with col2:
                if st.button('🔍 Find Events', type='primary'):
                    with st.spinner('🌐 Fetching live networking events...'):
                        target_skills = list(missing_skills)[:5] if missing_skills else list(resume_skills)[:5]
                        events = networking_engine.fetch_live_networking_events(target_skills, event_location)
                        st.session_state.networking_events = events
                    st.success(f'✅ Found {len(events)} networking events!')
            
            # Display events
            if 'networking_events' in st.session_state and st.session_state.networking_events:
                st.markdown('---')
                st.markdown('#### 📅 Upcoming Networking Events')
                
                for event in st.session_state.networking_events[:10]:
                    with st.expander(f"{event.title} - {event.date}", expanded=False):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"**Type**: {event.event_type.value}")
                            st.markdown(f"**Location**: {event.location}")
                            st.markdown(f"**Description**: {event.description}")
                            st.markdown(f"**Skills Focus**: {', '.join(event.skills_focus)}")
                        
                        with col2:
                            st.metric('Attendees', event.attendees_count)
                            st.metric('Relevance', f"{event.relevance_score:.1%}")
                        
                        with col3:
                            st.markdown(f"**Cost**: {event.cost}")
                            st.markdown(f"**Organizer**: {event.organizer}")
                            if event.url:
                                st.markdown(f"[🔗 Register Here]({event.url})")
        
        with networking_tab3:
            st.markdown('### 💡 Real-Time Market Insights')
            
            if st.button('📊 Analyze Market Trends', type='primary'):
                with st.spinner('🤖 AI is analyzing real-time market data...'):
                    target_skills = list(missing_skills)[:5] if missing_skills else list(resume_skills)[:5]
                    market_analysis = realtime_analyzer.analyze_market_trends(target_skills)
                    st.session_state.market_analysis = market_analysis
                st.success('✅ Market analysis complete!')
            
            if 'market_analysis' in st.session_state:
                analysis = st.session_state.market_analysis
                
                st.markdown('---')
                st.markdown('#### 📊 Live Market Analysis')
                
                # Display analysis
                st.markdown(analysis['analysis_text'])
                
                # Show data sources
                st.markdown('---')
                st.markdown('#### 📈 Supporting Data')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('**Job Market Summary:**')
                    for skill, data in analysis['job_market_summary'].items():
                        st.markdown(f"• **{skill}**: {data.get('job_postings', 0)} postings, {data.get('growth_rate', 'N/A')} growth")
                
                with col2:
                    st.markdown('**Trending News:**')
                    for news in analysis['trending_news'][:3]:
                        st.markdown(f"• [{news['title']}]({news['url']})")
                
                # Generate networking insights
                if st.button('🎯 Get Networking Insights'):
                    with st.spinner('🤖 Generating personalized networking insights...'):
                        target_role = st.selectbox('Target Role', ['Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer'])
                        networking_insights = realtime_analyzer.generate_networking_insights(target_skills, target_role)
                        st.session_state.networking_insights = networking_insights
                    st.success('✅ Networking insights generated!')
                
                if 'networking_insights' in st.session_state:
                    insights = st.session_state.networking_insights
                    st.markdown('---')
                    st.markdown('#### 🎯 Personalized Networking Strategy')
                    st.markdown(insights['insights_text'])
        
        with networking_tab4:
            st.markdown('### 🗺️ AI-Powered Learning Roadmap')
            
            # Roadmap controls
            col1, col2, col3 = st.columns(3)
            
            with col1:
                target_role = st.selectbox(
                    'Target Role',
                    ['Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer', 'ML Engineer'],
                    key='roadmap_role'
                )
            
            with col2:
                timeline_months = st.slider('Timeline (months)', 3, 24, 12)
            
            with col3:
                if st.button('🗺️ Generate Roadmap', type='primary'):
                    with st.spinner('🤖 AI is creating your personalized learning roadmap...'):
                        current_skills = list(resume_skills)[:10] if resume_skills else []
                        roadmap = realtime_analyzer.generate_personalized_learning_roadmap(
                            current_skills, target_role, timeline_months
                        )
                        st.session_state.learning_roadmap = roadmap
                    st.success('✅ Learning roadmap generated!')
            
            if 'learning_roadmap' in st.session_state:
                roadmap = st.session_state.learning_roadmap
                
                st.markdown('---')
                st.markdown('#### 🗺️ Your Personalized Learning Journey')
                st.markdown(roadmap['roadmap_text'])
                
                # Export roadmap
                with st.expander('📋 Export Learning Roadmap', expanded=False):
                    st.text_area('Learning Roadmap (Text Format)', roadmap['roadmap_text'], height=400, key='roadmap_copy')
                    
                    if st.button('💾 Download Roadmap'):
                        st.download_button(
                            label='Download Learning Roadmap',
                            data=roadmap['roadmap_text'],
                            file_name=f'learning_roadmap_{target_role}_{timeline_months}months.txt',
                            mime='text/plain'
                        )
        
        st.divider()

    # AI-Powered Recommendations with improved layout
    st.markdown('##  AI-Powered Recommendations')

    # Initialize session state for storing generated content
    if 'resume_improvements' not in st.session_state:
        st.session_state.resume_improvements = None
    if 'project_ideas' not in st.session_state:
        st.session_state.project_ideas = None
    if 'cover_letter' not in st.session_state:
        st.session_state.cover_letter = None
    
    # Resume Enhancement Section
    st.markdown('### 📝 Resume Enhancement')
    st.markdown('Improve your resume with AI-powered suggestions tailored to the job requirements.')
    
    if st.button(' Get Resume Improvements', use_container_width=True, type='primary'):
        with st.spinner(' Analyzing resume and generating improvements...'):
            improved = enhance_resume_section(resume_text, jd_text, list(missing_skills))
            st.session_state.resume_improvements = improved
        st.success('✅ Resume improvements generated successfully!')
    
    # Display resume improvements if they exist in session state
    if st.session_state.resume_improvements:
        st.markdown('---')
        st.markdown('####  AI Resume Suggestions')
        st.markdown(st.session_state.resume_improvements)
        
        # Option to copy or download
        with st.expander('📋 View in Text Format (for copying)', expanded=False):
            st.text_area('Resume Improvements', st.session_state.resume_improvements, height=400, key='resume_copy')
        
        # Clear button
        if st.button(' Clear Resume Suggestions', key='clear_resume'):
            st.session_state.resume_improvements = None
            st.rerun()
    
    st.markdown('---')
    
    # Project Ideas Section  
    st.markdown('###  Project Ideas Generator')
    st.markdown('Get personalized project ideas to strengthen your portfolio and demonstrate your skills.')
    
    if st.button(' Get Project Ideas', use_container_width=True, type='primary'):
        with st.spinner(' Generating personalized project ideas...'):
            ideas = generate_project_ideas(resume_text, resume_skills)
            st.session_state.project_ideas = ideas
        st.success('✅ Project ideas generated successfully!')
    
    # Display project ideas if they exist in session state
    if st.session_state.project_ideas:
        st.markdown('---')
        st.markdown('####  Personalized Project Suggestions')
        st.markdown(st.session_state.project_ideas)
        
        # Option to copy or download
        with st.expander(' View in Text Format (for copying)', expanded=False):
            st.text_area('Project Ideas', st.session_state.project_ideas, height=400, key='projects_copy')
        
        # Clear button
        if st.button(' Clear Project Ideas', key='clear_projects'):
            st.session_state.project_ideas = None
            st.rerun()

    st.markdown('---')

    # Cover Letter Generator Section
    st.markdown('###  Cover Letter Generator')
    st.markdown('Generate a concise, tailored cover letter aligned to the job description.')

    if st.button(' Generate Cover Letter', use_container_width=True, type='primary'):
        with st.spinner(' Drafting your tailored cover letter...'):
            cover = generate_cover_letter(resume_text, jd_text, list(matched_skills | missing_skills))
            st.session_state.cover_letter = cover
        st.success('✅ Cover letter generated successfully!')

    if st.session_state.cover_letter:
        st.markdown('---')
        st.markdown('####  Tailored Cover Letter')
        st.markdown(st.session_state.cover_letter)

        with st.expander(' View in Text Format (for copying)', expanded=False):
            st.text_area('Cover Letter', st.session_state.cover_letter, height=300, key='cover_letter_copy')

        if st.button(' Clear Cover Letter', key='clear_cover_letter'):
            st.session_state.cover_letter = None
            st.rerun()

    st.markdown('---')

    # AI-Powered Interview Preparation Section
    st.markdown('## 🎯 AI-Powered Interview Preparation')
    st.markdown('Get personalized interview questions and practice with AI-powered feedback to ace your interview.')

    # Initialize session state for interview prep
    if 'interview_questions' not in st.session_state:
        st.session_state.interview_questions = None
    if 'interview_tips' not in st.session_state:
        st.session_state.interview_tips = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'interview_evaluations' not in st.session_state:
        st.session_state.interview_evaluations = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    # Interview preparation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        question_count = st.selectbox('Number of Questions', [3, 5, 8, 10], index=1)
    
    with col2:
        question_type = st.selectbox('Question Type', ['All', 'Technical', 'Behavioral', 'Situational', 'System Design'])
    
    with col3:
        difficulty = st.selectbox('Difficulty Level', ['All', 'Easy', 'Medium', 'Hard'])

    # Generate questions button
    if st.button('🎯 Generate Interview Questions', use_container_width=True, type='primary'):
        with st.spinner('🤖 AI is generating personalized interview questions...'):
            questions = generate_interview_questions(resume_text, jd_text, list(resume_skills), question_count)
            
            # Filter questions based on selections
            if question_type != 'All':
                questions = get_question_by_type(questions, question_type.lower())
            if difficulty != 'All':
                questions = get_question_by_difficulty(questions, difficulty.lower())
            
            st.session_state.interview_questions = questions
            st.session_state.current_question_index = 0
            st.session_state.interview_evaluations = []
            st.session_state.user_answers = {}
        
        st.success(f'✅ Generated {len(questions)} personalized interview questions!')

    # Display interview questions and practice interface
    if st.session_state.interview_questions:
        st.markdown('---')
        st.markdown('### 📝 Interview Practice Session')
        
        questions = st.session_state.interview_questions
        current_index = st.session_state.current_question_index
        
        if current_index < len(questions):
            current_question = questions[current_index]
            
            # Question display
            st.markdown(f'**Question {current_index + 1} of {len(questions)}**')
            
            # Question type and difficulty badges
            col1, col2, col3 = st.columns([2, 2, 6])
            with col1:
                st.markdown(f'**Type:** {current_question.get("type", "N/A").title()}')
            with col2:
                st.markdown(f'**Difficulty:** {current_question.get("difficulty", "N/A").title()}')
            
            # Question text
            st.markdown(f'**{current_question.get("question", "No question available")}**')
            
            if current_question.get("follow_up"):
                with st.expander("💡 Follow-up Question"):
                    st.markdown(current_question["follow_up"])
            
            # Answer input
            answer_key = f'answer_{current_index}'
            user_answer = st.text_area(
                'Your Answer:',
                value=st.session_state.user_answers.get(answer_key, ''),
                height=150,
                key=answer_key,
                help='Take your time to provide a thoughtful answer. The AI will evaluate your response.'
            )
            
            # Store answer in session state
            st.session_state.user_answers[answer_key] = user_answer
            
            # Navigation and evaluation buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button('⬅️ Previous', disabled=current_index == 0):
                    st.session_state.current_question_index = max(0, current_index - 1)
                    st.rerun()
            
            with col2:
                if st.button('➡️ Next', disabled=current_index >= len(questions) - 1):
                    st.session_state.current_question_index = min(len(questions) - 1, current_index + 1)
                    st.rerun()
            
            with col3:
                if st.button('🎯 Evaluate Answer', type='primary', disabled=not user_answer.strip()):
                    with st.spinner('🤖 AI is evaluating your answer...'):
                        evaluation = evaluate_answer(current_question, user_answer, resume_text)
                        st.session_state.interview_evaluations.append(evaluation)
                        # Track progress
                        progress_tracker.update_activity("interviews_practiced")
                    st.success('✅ Answer evaluated! Check the feedback below.')
                    st.rerun()
            
            with col4:
                if st.button('🔄 Skip Question'):
                    st.session_state.current_question_index = min(len(questions) - 1, current_index + 1)
                    st.rerun()
            
            # Show evaluation if available
            if st.session_state.interview_evaluations and len(st.session_state.interview_evaluations) > current_index:
                evaluation = st.session_state.interview_evaluations[current_index]
                
                st.markdown('---')
                st.markdown('#### 📊 AI Evaluation & Feedback')
                
                # Overall score
                score = evaluation.get('overall_score', 0)
                rating = evaluation.get('rating', 'unknown')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric('Overall Score', f'{score}/100')
                with col2:
                    st.metric('Rating', rating.title())
                with col3:
                    # Progress bar for score
                    st.progress(score / 100)
                
                # Detailed scores
                scores = evaluation.get('scores', {})
                if scores:
                    st.markdown('**Detailed Scores:**')
                    score_cols = st.columns(len(scores))
                    for i, (metric, value) in enumerate(scores.items()):
                        with score_cols[i]:
                            st.metric(metric.replace('_', ' ').title(), f'{value}/100')
                
                # Strengths and improvements
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('**✅ Strengths:**')
                    for strength in evaluation.get('strengths', []):
                        st.markdown(f'• {strength}')
                
                with col2:
                    st.markdown('**🎯 Areas for Improvement:**')
                    for improvement in evaluation.get('improvements', []):
                        st.markdown(f'• {improvement}')
                
                # Detailed feedback
                if evaluation.get('detailed_feedback'):
                    st.markdown('**📝 Detailed Feedback:**')
                    st.info(evaluation['detailed_feedback'])
                
                # Follow-up suggestions
                if evaluation.get('follow_up_suggestions'):
                    st.markdown('**💡 Follow-up Suggestions:**')
                    for suggestion in evaluation['follow_up_suggestions']:
                        st.markdown(f'• {suggestion}')
        
        # Interview readiness assessment
        if st.session_state.interview_evaluations:
            st.markdown('---')
            st.markdown('### 🏆 Interview Readiness Assessment')
            
            readiness = calculate_interview_readiness_score(st.session_state.interview_evaluations)
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.metric('Overall Readiness Score', f'{readiness["overall_score"]}/100')
                st.metric('Readiness Level', readiness['readiness_level'])
                st.metric('Questions Practiced', readiness['total_questions'])
            
            with col2:
                st.markdown('**📈 Recommendations:**')
                for rec in readiness['recommendations']:
                    st.markdown(f'• {rec}')
            
            # Progress visualization
            st.markdown('**Progress Visualization:**')
            progress_cols = st.columns(len(st.session_state.interview_evaluations))
            for i, eval_data in enumerate(st.session_state.interview_evaluations):
                with progress_cols[i]:
                    score = eval_data.get('overall_score', 0)
                    st.progress(score / 100)
                    st.caption(f'Q{i+1}: {score}')

    # Interview tips section
    st.markdown('---')
    st.markdown('### 💡 Personalized Interview Tips')
    
    if st.button('🎯 Generate Interview Tips', use_container_width=True):
        with st.spinner('🤖 Generating personalized interview tips...'):
            tips = generate_interview_tips(jd_text, list(resume_skills))
            st.session_state.interview_tips = tips
        st.success('✅ Interview tips generated successfully!')
    
    if st.session_state.interview_tips:
        st.markdown('---')
        st.markdown('#### 🎯 AI-Generated Interview Tips')
        st.markdown(st.session_state.interview_tips)
        
        with st.expander('📋 View Tips in Text Format (for copying)', expanded=False):
            st.text_area('Interview Tips', st.session_state.interview_tips, height=300, key='tips_copy')
        
        if st.button(' Clear Interview Tips', key='clear_tips'):
            st.session_state.interview_tips = None
            st.rerun()

    # Reset interview session
    if st.session_state.interview_questions:
        st.markdown('---')
        if st.button('🔄 Reset Interview Session', type='secondary'):
            st.session_state.interview_questions = None
            st.session_state.interview_tips = None
            st.session_state.current_question_index = 0
            st.session_state.interview_evaluations = []
            st.session_state.user_answers = {}
            st.rerun()

else:
    st.info('Upload both resume and Job Description files to see skill match analysis and improvement suggestions.')

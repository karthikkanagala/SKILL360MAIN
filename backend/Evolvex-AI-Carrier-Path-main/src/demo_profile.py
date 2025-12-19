"""
Demo Profile Module
Provides demo profile data and profile completeness checking
"""

def check_profile_completeness(session_state: dict) -> dict:
    """
    Check the completeness of a user profile based on session state data
    
    Args:
        session_state: Dictionary containing profile data
        
    Returns:
        Dictionary with completeness percentage and missing sections
    """
    sections = {
        'resume': bool(session_state.get('resume_text')),
        'skills': bool(session_state.get('resume_skills')),
        'github': bool(session_state.get('github_analysis')),
        'certificates': bool(session_state.get('validated_certificates')),
        'activities': bool(session_state.get('activities')),
        'interview': bool(session_state.get('interview_evaluations')),
        'career_score': bool(session_state.get('career_score_data'))
    }
    
    completed = sum(sections.values())
    total = len(sections)
    percentage = int((completed / total) * 100)
    
    missing = [section for section, is_complete in sections.items() if not is_complete]
    
    return {
        'percentage': percentage,
        'completed_sections': completed,
        'total_sections': total,
        'sections': sections,
        'missing_sections': missing
    }


def get_demo_profile() -> dict:
    """
    Get a demo profile with sample data for testing and demonstration
    
    Returns:
        Dictionary containing sample profile data
    """
    return {
        'resume_text': '''
            John Doe
            Software Engineer
            
            SKILLS:
            - Python, JavaScript, TypeScript
            - React, Node.js, FastAPI
            - Machine Learning, TensorFlow, PyTorch
            - SQL, MongoDB, PostgreSQL
            - Git, Docker, Kubernetes
            
            EXPERIENCE:
            Senior Software Engineer at Tech Corp (2021-Present)
            - Led development of microservices architecture
            - Implemented CI/CD pipelines
            - Mentored junior developers
            
            Software Engineer at StartupXYZ (2019-2021)
            - Built full-stack web applications
            - Integrated third-party APIs
            - Optimized database performance
            
            EDUCATION:
            B.S. Computer Science, State University (2019)
            GPA: 3.8
            
            CERTIFICATIONS:
            - AWS Solutions Architect Associate
            - Google Cloud Professional Data Engineer
        ''',
        'resume_skills': [
            'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js',
            'FastAPI', 'Machine Learning', 'TensorFlow', 'PyTorch',
            'SQL', 'MongoDB', 'PostgreSQL', 'Git', 'Docker', 'Kubernetes'
        ],
        'ats_score': 85,
        'github_analysis': {
            'username': 'johndoe',
            'total_repos': 42,
            'total_stars': 156,
            'top_languages': ['Python', 'JavaScript', 'TypeScript'],
            'contribution_score': 78,
            'profile_quality': 'Excellent'
        },
        'validated_certificates': [
            {
                'name': 'AWS Solutions Architect Associate',
                'issuer': 'Amazon Web Services',
                'date': '2023-06',
                'status': 'verified',
                'credential_id': 'AWS-SAA-12345'
            },
            {
                'name': 'Google Cloud Professional Data Engineer',
                'issuer': 'Google Cloud',
                'date': '2023-03',
                'status': 'verified',
                'credential_id': 'GCP-DE-67890'
            }
        ],
        'activities': [
            {
                'name': 'Open Source Contributor',
                'description': 'Regular contributor to popular open source projects',
                'impact': 'high'
            },
            {
                'name': 'Tech Blog Writer',
                'description': 'Write technical articles on Medium and Dev.to',
                'impact': 'medium'
            }
        ],
        'interview_evaluations': [
            {
                'topic': 'System Design',
                'score': 85,
                'feedback': 'Strong understanding of distributed systems'
            },
            {
                'topic': 'Data Structures',
                'score': 90,
                'feedback': 'Excellent problem-solving skills'
            }
        ],
        'career_score_data': {
            'total_score': 82,
            'breakdown': {
                'skills': 85,
                'experience': 80,
                'education': 75,
                'certifications': 90,
                'projects': 78
            }
        }
    }


def load_demo_profile_to_session(session_state: dict) -> dict:
    """
    Load demo profile data into a session state dictionary
    
    Args:
        session_state: Dictionary to populate with demo data
        
    Returns:
        Updated session state with demo profile data
    """
    demo_profile = get_demo_profile()
    session_state.update(demo_profile)
    return session_state

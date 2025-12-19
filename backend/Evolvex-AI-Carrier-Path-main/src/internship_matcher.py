"""
Internship Matching System
Auto-matches candidates with relevant internships based on skills, interests, and profile
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict
import streamlit as st
from datetime import datetime
import re


class InternshipMatcher:
    """Matches candidates with relevant internships"""
    
    # Internship categories and requirements
    INTERNSHIP_CATEGORIES = {
        'Software Development': {
            'required_skills': ['Programming', 'Problem Solving', 'Data Structures'],
            'preferred_skills': ['Python', 'Java', 'C++', 'JavaScript', 'Git'],
            'keywords': ['software', 'developer', 'programming', 'coding', 'backend', 'frontend'],
            'avg_stipend_range': '₹10,000-30,000/month',
            'duration': '2-6 months'
        },
        'Data Science/Analytics': {
            'required_skills': ['Python', 'Statistics', 'Data Analysis'],
            'preferred_skills': ['Machine Learning', 'SQL', 'Pandas', 'NumPy', 'Visualization'],
            'keywords': ['data', 'analytics', 'machine learning', 'ai', 'ml', 'statistics'],
            'avg_stipend_range': '₹15,000-35,000/month',
            'duration': '3-6 months'
        },
        'Web Development': {
            'required_skills': ['HTML', 'CSS', 'JavaScript'],
            'preferred_skills': ['React', 'Node.js', 'MongoDB', 'Express', 'REST API'],
            'keywords': ['web', 'frontend', 'backend', 'fullstack', 'react', 'angular'],
            'avg_stipend_range': '₹8,000-25,000/month',
            'duration': '2-4 months'
        },
        'Mobile App Development': {
            'required_skills': ['Programming', 'Mobile Development'],
            'preferred_skills': ['Android', 'iOS', 'Flutter', 'React Native', 'Swift', 'Kotlin'],
            'keywords': ['mobile', 'android', 'ios', 'app development', 'flutter'],
            'avg_stipend_range': '₹12,000-28,000/month',
            'duration': '3-5 months'
        },
        'UI/UX Design': {
            'required_skills': ['Design', 'User Research', 'Prototyping'],
            'preferred_skills': ['Figma', 'Adobe XD', 'Sketch', 'User Testing', 'Wireframing'],
            'keywords': ['ui', 'ux', 'design', 'user experience', 'interface', 'figma'],
            'avg_stipend_range': '₹8,000-20,000/month',
            'duration': '2-4 months'
        },
        'Digital Marketing': {
            'required_skills': ['Marketing', 'Communication', 'Analytics'],
            'preferred_skills': ['SEO', 'Social Media', 'Content Marketing', 'Google Analytics'],
            'keywords': ['marketing', 'digital', 'seo', 'social media', 'content', 'campaigns'],
            'avg_stipend_range': '₹5,000-18,000/month',
            'duration': '2-4 months'
        },
        'Content Writing': {
            'required_skills': ['Writing', 'Communication', 'Research'],
            'preferred_skills': ['SEO Writing', 'Technical Writing', 'Copywriting', 'Editing'],
            'keywords': ['content', 'writing', 'copywriting', 'blog', 'technical writing'],
            'avg_stipend_range': '₹5,000-15,000/month',
            'duration': '2-3 months'
        },
        'Business Development': {
            'required_skills': ['Communication', 'Sales', 'Negotiation'],
            'preferred_skills': ['CRM', 'Market Research', 'Presentation', 'Client Management'],
            'keywords': ['business development', 'sales', 'bd', 'partnerships', 'client'],
            'avg_stipend_range': '₹8,000-22,000/month',
            'duration': '3-6 months'
        },
        'Graphic Design': {
            'required_skills': ['Design', 'Creativity', 'Visual Communication'],
            'preferred_skills': ['Photoshop', 'Illustrator', 'InDesign', 'Canva', 'Branding'],
            'keywords': ['graphic', 'design', 'visual', 'creative', 'photoshop', 'illustrator'],
            'avg_stipend_range': '₹6,000-18,000/month',
            'duration': '2-4 months'
        },
        'Cybersecurity': {
            'required_skills': ['Security', 'Networking', 'Problem Solving'],
            'preferred_skills': ['Penetration Testing', 'Security Analysis', 'Firewall', 'Encryption'],
            'keywords': ['security', 'cybersecurity', 'ethical hacking', 'penetration', 'network security'],
            'avg_stipend_range': '₹12,000-30,000/month',
            'duration': '3-6 months'
        },
        'Cloud Computing': {
            'required_skills': ['Cloud Platforms', 'Networking', 'Linux'],
            'preferred_skills': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'DevOps'],
            'keywords': ['cloud', 'aws', 'azure', 'gcp', 'devops', 'kubernetes'],
            'avg_stipend_range': '₹15,000-35,000/month',
            'duration': '3-6 months'
        },
        'Research': {
            'required_skills': ['Research', 'Analysis', 'Critical Thinking'],
            'preferred_skills': ['Academic Writing', 'Data Collection', 'Literature Review', 'Statistics'],
            'keywords': ['research', 'academic', 'study', 'analysis', 'investigation'],
            'avg_stipend_range': '₹8,000-20,000/month',
            'duration': '3-6 months'
        }
    }
    
    # Experience level requirements
    EXPERIENCE_LEVELS = {
        'Beginner': {
            'min_skills': 2,
            'min_projects': 0,
            'min_certifications': 0,
            'suitable_for': 'First-year students, career switchers'
        },
        'Intermediate': {
            'min_skills': 4,
            'min_projects': 1,
            'min_certifications': 1,
            'suitable_for': 'Second/third-year students, some project experience'
        },
        'Advanced': {
            'min_skills': 6,
            'min_projects': 3,
            'min_certifications': 2,
            'suitable_for': 'Final-year students, strong portfolio'
        }
    }
    
    def __init__(self):
        """Initialize the internship matcher"""
        pass
    
    def calculate_match_score(
        self,
        candidate_profile: Dict[str, Any],
        internship_category: str
    ) -> Dict[str, Any]:
        """
        Calculate match score between candidate and internship category
        
        Args:
            candidate_profile: Candidate's profile with skills, projects, etc.
            internship_category: Category of internship
        
        Returns:
            Match analysis with score and recommendations
        """
        category_info = self.INTERNSHIP_CATEGORIES.get(internship_category, {})
        
        if not category_info:
            return {'match_score': 0, 'error': 'Invalid category'}
        
        candidate_skills = set(skill.lower() for skill in candidate_profile.get('skills', []))
        required_skills = set(skill.lower() for skill in category_info.get('required_skills', []))
        preferred_skills = set(skill.lower() for skill in category_info.get('preferred_skills', []))
        
        # Calculate skill match
        required_match = len(candidate_skills & required_skills) / max(len(required_skills), 1)
        preferred_match = len(candidate_skills & preferred_skills) / max(len(preferred_skills), 1)
        
        # Base score from skills (60% weight)
        skill_score = (required_match * 0.7 + preferred_match * 0.3) * 60
        
        # Project relevance (20% weight)
        projects = candidate_profile.get('projects', [])
        relevant_projects = 0
        for project in projects:
            project_text = f"{project.get('name', '')} {project.get('description', '')}".lower()
            if any(keyword in project_text for keyword in category_info.get('keywords', [])):
                relevant_projects += 1
        
        project_score = min(relevant_projects * 10, 20)
        
        # Certifications (10% weight)
        certifications = candidate_profile.get('certifications', [])
        relevant_certs = 0
        for cert in certifications:
            cert_text = f"{cert.get('name', '')} {cert.get('provider', '')}".lower()
            if any(keyword in cert_text for keyword in category_info.get('keywords', [])):
                relevant_certs += 1
        
        cert_score = min(relevant_certs * 5, 10)
        
        # Experience level (10% weight)
        experience_score = self._calculate_experience_score(candidate_profile)
        
        # Total match score
        total_score = skill_score + project_score + cert_score + experience_score
        
        # Identify gaps
        missing_required = required_skills - candidate_skills
        missing_preferred = preferred_skills - candidate_skills
        
        match_analysis = {
            'match_score': min(total_score, 100),
            'skill_match_percentage': required_match * 100,
            'required_skills_met': len(candidate_skills & required_skills),
            'required_skills_total': len(required_skills),
            'preferred_skills_met': len(candidate_skills & preferred_skills),
            'relevant_projects': relevant_projects,
            'relevant_certifications': relevant_certs,
            'missing_required_skills': list(missing_required),
            'missing_preferred_skills': list(missing_preferred),
            'readiness_level': self._determine_readiness(total_score),
            'recommendations': self._generate_match_recommendations(
                total_score, missing_required, missing_preferred, relevant_projects
            ),
            'category_info': category_info
        }
        
        return match_analysis
    
    def _calculate_experience_score(self, profile: Dict[str, Any]) -> float:
        """Calculate experience level score"""
        score = 0
        
        # Projects
        projects = len(profile.get('projects', []))
        score += min(projects * 2, 4)
        
        # Certifications
        certs = len(profile.get('certifications', []))
        score += min(certs * 1.5, 3)
        
        # Extracurricular
        activities = len(profile.get('extracurricular', []))
        score += min(activities * 0.5, 3)
        
        return min(score, 10)
    
    def _determine_readiness(self, score: float) -> str:
        """Determine candidate readiness level"""
        if score >= 75:
            return 'Highly Ready - Strong Match'
        elif score >= 60:
            return 'Ready - Good Match'
        elif score >= 40:
            return 'Developing - Needs Preparation'
        else:
            return 'Early Stage - Significant Preparation Needed'
    
    def _generate_match_recommendations(
        self,
        score: float,
        missing_required: set,
        missing_preferred: set,
        relevant_projects: int
    ) -> List[str]:
        """Generate recommendations for improving match"""
        recommendations = []
        
        if score < 60:
            recommendations.append('🎯 Focus on building foundational skills before applying')
        
        if missing_required:
            recommendations.append(f'📚 Priority: Learn these required skills - {", ".join(list(missing_required)[:3])}')
        
        if missing_preferred and score < 80:
            recommendations.append(f'⭐ Recommended: Add these skills to stand out - {", ".join(list(missing_preferred)[:3])}')
        
        if relevant_projects == 0:
            recommendations.append('💡 Build 1-2 projects in this domain to demonstrate practical skills')
        elif relevant_projects < 2:
            recommendations.append('🚀 Add more domain-specific projects to strengthen your profile')
        
        if score >= 75:
            recommendations.append('✅ You\'re ready to apply! Prepare a strong resume highlighting relevant skills')
        elif score >= 60:
            recommendations.append('📈 You\'re on track! A few more skills/projects will make you highly competitive')
        
        return recommendations
    
    def find_best_matches(
        self,
        candidate_profile: Dict[str, Any],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find best internship matches for candidate
        
        Args:
            candidate_profile: Candidate's complete profile
            top_n: Number of top matches to return
        
        Returns:
            List of best matching internship categories with scores
        """
        matches = []
        
        for category in self.INTERNSHIP_CATEGORIES.keys():
            match_analysis = self.calculate_match_score(candidate_profile, category)
            matches.append({
                'category': category,
                'match_score': match_analysis['match_score'],
                'readiness': match_analysis['readiness_level'],
                'analysis': match_analysis
            })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches[:top_n]
    
    def generate_internship_roadmap(
        self,
        candidate_profile: Dict[str, Any],
        target_category: str
    ) -> Dict[str, Any]:
        """
        Generate a personalized roadmap to prepare for target internship
        
        Args:
            candidate_profile: Candidate's profile
            target_category: Target internship category
        
        Returns:
            Detailed roadmap with timeline and milestones
        """
        match_analysis = self.calculate_match_score(candidate_profile, target_category)
        category_info = self.INTERNSHIP_CATEGORIES.get(target_category, {})
        
        current_score = match_analysis['match_score']
        
        # Determine timeline based on current readiness
        if current_score >= 75:
            timeline = '1-2 weeks'
            phase = 'Application Ready'
        elif current_score >= 60:
            timeline = '2-4 weeks'
            phase = 'Final Preparation'
        elif current_score >= 40:
            timeline = '1-2 months'
            phase = 'Skill Building'
        else:
            timeline = '2-4 months'
            phase = 'Foundation Building'
        
        roadmap = {
            'current_score': current_score,
            'target_score': 80,
            'estimated_timeline': timeline,
            'current_phase': phase,
            'milestones': [],
            'action_items': [],
            'resources': []
        }
        
        # Generate milestones
        if match_analysis['missing_required_skills']:
            roadmap['milestones'].append({
                'title': 'Master Required Skills',
                'priority': 'High',
                'skills': match_analysis['missing_required_skills'][:3],
                'estimated_time': '2-4 weeks'
            })
        
        if match_analysis['relevant_projects'] < 2:
            roadmap['milestones'].append({
                'title': 'Build Domain Projects',
                'priority': 'High',
                'target': f'Create {2 - match_analysis["relevant_projects"]} relevant projects',
                'estimated_time': '3-6 weeks'
            })
        
        if match_analysis['missing_preferred_skills']:
            roadmap['milestones'].append({
                'title': 'Add Preferred Skills',
                'priority': 'Medium',
                'skills': match_analysis['missing_preferred_skills'][:3],
                'estimated_time': '2-3 weeks'
            })
        
        # Generate action items
        roadmap['action_items'] = [
            f'✓ Learn {skill}' for skill in match_analysis['missing_required_skills'][:3]
        ]
        roadmap['action_items'].extend([
            '✓ Build a portfolio project showcasing your skills',
            '✓ Earn a relevant certification',
            '✓ Update resume with new skills and projects',
            '✓ Prepare for technical interviews'
        ])
        
        # Add resources
        roadmap['resources'] = [
            f'Recommended courses for {target_category}',
            'Project ideas and tutorials',
            'Interview preparation guides',
            'Resume templates for internships'
        ]
        
        return roadmap


# Streamlit cached functions
@st.cache_data(ttl=3600)
def find_internship_matches(candidate_profile: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    """Cached internship matching"""
    matcher = InternshipMatcher()
    return matcher.find_best_matches(candidate_profile, top_n)


@st.cache_data(ttl=3600)
def generate_internship_roadmap(candidate_profile: Dict[str, Any], target_category: str) -> Dict[str, Any]:
    """Cached roadmap generation"""
    matcher = InternshipMatcher()
    return matcher.generate_internship_roadmap(candidate_profile, target_category)


@st.cache_data(ttl=3600)
def calculate_internship_match(candidate_profile: Dict[str, Any], category: str) -> Dict[str, Any]:
    """Cached match calculation"""
    matcher = InternshipMatcher()
    return matcher.calculate_match_score(candidate_profile, category)

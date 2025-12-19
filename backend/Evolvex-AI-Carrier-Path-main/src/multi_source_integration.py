"""
Multi-Source Data Integration
Integrates data from GitHub, portfolios, certificates, and learning platforms
"""

from typing import Dict, Any, List, Optional
import streamlit as st
from datetime import datetime
import requests
import re
from collections import defaultdict


class MultiSourceIntegrator:
    """Integrates data from multiple sources for comprehensive profile analysis"""
    
    SUPPORTED_PLATFORMS = {
        'GitHub': {
            'icon': '🐙',
            'api_base': 'https://api.github.com',
            'data_types': ['repositories', 'contributions', 'profile', 'languages']
        },
        'LinkedIn': {
            'icon': '💼',
            'data_types': ['profile', 'experience', 'education', 'certifications']
        },
        'LeetCode': {
            'icon': '💡',
            'api_base': 'https://leetcode.com',
            'data_types': ['problems_solved', 'ranking', 'contest_rating']
        },
        'HackerRank': {
            'icon': '🏅',
            'data_types': ['badges', 'certifications', 'skills']
        },
        'Coursera': {
            'icon': '🎓',
            'data_types': ['courses', 'specializations', 'certificates']
        },
        'Kaggle': {
            'icon': '📊',
            'api_base': 'https://www.kaggle.com/api/v1',
            'data_types': ['competitions', 'datasets', 'notebooks', 'ranking']
        },
        'Medium': {
            'icon': '✍️',
            'data_types': ['articles', 'followers', 'publications']
        },
        'Stack Overflow': {
            'icon': '📚',
            'api_base': 'https://api.stackexchange.com/2.3',
            'data_types': ['reputation', 'answers', 'questions', 'badges']
        }
    }
    
    def __init__(self):
        """Initialize the multi-source integrator"""
        self.integrated_data = {}
        self.data_sources = []
    
    def integrate_github_data(self, username: str) -> Dict[str, Any]:
        """
        Integrate GitHub profile data
        
        Args:
            username: GitHub username
        
        Returns:
            Integrated GitHub data
        """
        try:
            # Fetch user profile
            profile_url = f"https://api.github.com/users/{username}"
            response = requests.get(profile_url, timeout=10)
            
            if response.status_code != 200:
                return {'error': 'GitHub user not found', 'source': 'GitHub'}
            
            profile_data = response.json()
            
            # Fetch repositories
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
            repos_response = requests.get(repos_url, timeout=10)
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            # Process repositories
            languages = defaultdict(int)
            total_stars = 0
            total_forks = 0
            projects = []
            
            for repo in repos_data:
                if not repo.get('fork'):  # Exclude forked repos
                    total_stars += repo.get('stargazers_count', 0)
                    total_forks += repo.get('forks_count', 0)
                    
                    if repo.get('language'):
                        languages[repo['language']] += 1
                    
                    projects.append({
                        'name': repo.get('name'),
                        'description': repo.get('description', ''),
                        'language': repo.get('language', 'Unknown'),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'url': repo.get('html_url'),
                        'updated': repo.get('updated_at'),
                        'topics': repo.get('topics', [])
                    })
            
            integrated_data = {
                'source': 'GitHub',
                'username': username,
                'profile': {
                    'name': profile_data.get('name'),
                    'bio': profile_data.get('bio'),
                    'location': profile_data.get('location'),
                    'company': profile_data.get('company'),
                    'blog': profile_data.get('blog'),
                    'email': profile_data.get('email'),
                    'avatar_url': profile_data.get('avatar_url')
                },
                'stats': {
                    'public_repos': profile_data.get('public_repos', 0),
                    'followers': profile_data.get('followers', 0),
                    'following': profile_data.get('following', 0),
                    'total_stars': total_stars,
                    'total_forks': total_forks,
                    'account_age_days': (datetime.now() - datetime.strptime(
                        profile_data.get('created_at', '2020-01-01T00:00:00Z'),
                        '%Y-%m-%dT%H:%M:%SZ'
                    )).days
                },
                'languages': dict(languages),
                'projects': sorted(projects, key=lambda x: x['stars'], reverse=True),
                'top_languages': sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5],
                'integration_timestamp': datetime.now().isoformat(),
                'data_quality': 'high'
            }
            
            self.data_sources.append('GitHub')
            return integrated_data
            
        except Exception as e:
            return {
                'error': str(e),
                'source': 'GitHub',
                'data_quality': 'failed'
            }
    
    def integrate_portfolio_data(self, portfolio_url: str) -> Dict[str, Any]:
        """
        Integrate portfolio website data
        
        Args:
            portfolio_url: Portfolio website URL
        
        Returns:
            Integrated portfolio data
        """
        try:
            # Basic portfolio analysis
            response = requests.get(portfolio_url, timeout=10)
            
            if response.status_code != 200:
                return {'error': 'Portfolio not accessible', 'source': 'Portfolio'}
            
            content = response.text.lower()
            
            # Extract information using patterns
            skills_found = []
            skill_keywords = [
                'python', 'javascript', 'java', 'react', 'node', 'sql', 'mongodb',
                'machine learning', 'data science', 'web development', 'cloud',
                'aws', 'azure', 'docker', 'kubernetes'
            ]
            
            for skill in skill_keywords:
                if skill in content:
                    skills_found.append(skill.title())
            
            # Look for project sections
            has_projects = any(word in content for word in ['project', 'portfolio', 'work'])
            has_contact = any(word in content for word in ['contact', 'email', 'linkedin'])
            has_about = any(word in content for word in ['about', 'bio', 'profile'])
            
            # Extract links
            github_match = re.search(r'github\.com/([a-zA-Z0-9-]+)', content)
            linkedin_match = re.search(r'linkedin\.com/in/([a-zA-Z0-9-]+)', content)
            
            integrated_data = {
                'source': 'Portfolio',
                'url': portfolio_url,
                'analysis': {
                    'has_projects_section': has_projects,
                    'has_contact_section': has_contact,
                    'has_about_section': has_about,
                    'skills_mentioned': skills_found,
                    'skill_count': len(skills_found)
                },
                'social_links': {
                    'github': github_match.group(1) if github_match else None,
                    'linkedin': linkedin_match.group(1) if linkedin_match else None
                },
                'quality_score': self._calculate_portfolio_quality(
                    has_projects, has_contact, has_about, len(skills_found)
                ),
                'integration_timestamp': datetime.now().isoformat(),
                'data_quality': 'medium'
            }
            
            self.data_sources.append('Portfolio')
            return integrated_data
            
        except Exception as e:
            return {
                'error': str(e),
                'source': 'Portfolio',
                'data_quality': 'failed'
            }
    
    def integrate_leetcode_data(self, username: str) -> Dict[str, Any]:
        """
        Integrate LeetCode profile data
        
        Args:
            username: LeetCode username
        
        Returns:
            Integrated LeetCode data
        """
        try:
            # LeetCode GraphQL API (public data)
            query = """
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    username
                    submitStats {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                    profile {
                        ranking
                        reputation
                    }
                }
            }
            """
            
            # Note: This is a simplified version. Actual implementation would need proper API access
            integrated_data = {
                'source': 'LeetCode',
                'username': username,
                'stats': {
                    'problems_solved': 0,  # Would be fetched from API
                    'easy_solved': 0,
                    'medium_solved': 0,
                    'hard_solved': 0,
                    'ranking': 0,
                    'reputation': 0
                },
                'integration_timestamp': datetime.now().isoformat(),
                'data_quality': 'low',
                'note': 'Manual entry recommended - API access limited'
            }
            
            self.data_sources.append('LeetCode')
            return integrated_data
            
        except Exception as e:
            return {
                'error': str(e),
                'source': 'LeetCode',
                'data_quality': 'failed'
            }
    
    def integrate_certificate_platforms(self, certificates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate certificate data from multiple platforms
        
        Args:
            certificates: List of certificates with platform info
        
        Returns:
            Integrated certificate data
        """
        platform_stats = defaultdict(int)
        skill_categories = defaultdict(int)
        total_certificates = len(certificates)
        
        for cert in certificates:
            platform = cert.get('provider', 'Unknown')
            platform_stats[platform] += 1
            
            # Categorize by skill
            cert_name = cert.get('name', '').lower()
            if any(kw in cert_name for kw in ['data', 'analytics', 'ml', 'ai']):
                skill_categories['Data Science & AI'] += 1
            elif any(kw in cert_name for kw in ['web', 'frontend', 'backend', 'javascript']):
                skill_categories['Web Development'] += 1
            elif any(kw in cert_name for kw in ['cloud', 'aws', 'azure', 'gcp']):
                skill_categories['Cloud Computing'] += 1
            elif any(kw in cert_name for kw in ['security', 'cyber']):
                skill_categories['Cybersecurity'] += 1
            else:
                skill_categories['Other'] += 1
        
        integrated_data = {
            'source': 'Certificates',
            'total_certificates': total_certificates,
            'platforms': dict(platform_stats),
            'skill_categories': dict(skill_categories),
            'top_platform': max(platform_stats.items(), key=lambda x: x[1])[0] if platform_stats else 'None',
            'diversity_score': len(platform_stats) * 10,
            'integration_timestamp': datetime.now().isoformat(),
            'data_quality': 'high'
        }
        
        self.data_sources.append('Certificates')
        return integrated_data
    
    def integrate_learning_platforms(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate learning platform data (Coursera, Udemy, etc.)
        
        Args:
            learning_data: Learning progress data
        
        Returns:
            Integrated learning data
        """
        integrated_data = {
            'source': 'Learning Platforms',
            'courses_completed': learning_data.get('completed_courses', 0),
            'courses_in_progress': learning_data.get('in_progress_courses', 0),
            'total_learning_hours': learning_data.get('total_hours', 0),
            'platforms_used': learning_data.get('platforms', []),
            'skill_areas': learning_data.get('skill_areas', []),
            'completion_rate': self._calculate_completion_rate(learning_data),
            'learning_consistency': self._assess_learning_consistency(learning_data),
            'integration_timestamp': datetime.now().isoformat(),
            'data_quality': 'medium'
        }
        
        self.data_sources.append('Learning Platforms')
        return integrated_data
    
    def create_unified_profile(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create unified profile from all integrated sources
        
        Args:
            data_sources: Dictionary of all integrated data sources
        
        Returns:
            Unified comprehensive profile
        """
        unified_profile = {
            'profile_id': f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'data_sources': list(data_sources.keys()),
            'data_quality_score': self._calculate_overall_data_quality(data_sources),
            'completeness_score': self._calculate_completeness(data_sources),
            
            # Aggregated data
            'skills': self._aggregate_skills(data_sources),
            'projects': self._aggregate_projects(data_sources),
            'certifications': self._aggregate_certifications(data_sources),
            'achievements': self._aggregate_achievements(data_sources),
            'social_presence': self._aggregate_social_presence(data_sources),
            
            # Analytics
            'analytics': {
                'total_projects': self._count_total_projects(data_sources),
                'total_certifications': self._count_total_certifications(data_sources),
                'total_skills': len(self._aggregate_skills(data_sources)),
                'github_activity_score': self._calculate_github_score(data_sources),
                'learning_activity_score': self._calculate_learning_score(data_sources),
                'portfolio_quality_score': self._calculate_portfolio_score(data_sources)
            },
            
            # Recommendations
            'integration_recommendations': self._generate_integration_recommendations(data_sources),
            'missing_sources': self._identify_missing_sources(data_sources),
            
            # Raw data references
            'raw_data': data_sources
        }
        
        return unified_profile
    
    def _calculate_portfolio_quality(self, has_projects: bool, has_contact: bool, 
                                     has_about: bool, skill_count: int) -> float:
        """Calculate portfolio quality score"""
        score = 0
        score += 25 if has_projects else 0
        score += 25 if has_contact else 0
        score += 25 if has_about else 0
        score += min(skill_count * 2.5, 25)
        return score
    
    def _calculate_completion_rate(self, learning_data: Dict[str, Any]) -> float:
        """Calculate course completion rate"""
        completed = learning_data.get('completed_courses', 0)
        total = completed + learning_data.get('in_progress_courses', 0)
        return (completed / total * 100) if total > 0 else 0
    
    def _assess_learning_consistency(self, learning_data: Dict[str, Any]) -> str:
        """Assess learning consistency"""
        hours = learning_data.get('total_hours', 0)
        if hours >= 100:
            return 'High'
        elif hours >= 50:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_overall_data_quality(self, data_sources: Dict[str, Any]) -> float:
        """Calculate overall data quality score"""
        quality_scores = {
            'high': 100,
            'medium': 70,
            'low': 40,
            'failed': 0
        }
        
        total_score = 0
        count = 0
        
        for source_data in data_sources.values():
            if isinstance(source_data, dict) and 'data_quality' in source_data:
                quality = source_data['data_quality']
                total_score += quality_scores.get(quality, 50)
                count += 1
        
        return (total_score / count) if count > 0 else 50
    
    def _calculate_completeness(self, data_sources: Dict[str, Any]) -> float:
        """Calculate profile completeness"""
        total_sources = len(self.SUPPORTED_PLATFORMS)
        integrated_sources = len(data_sources)
        return (integrated_sources / total_sources) * 100
    
    def _aggregate_skills(self, data_sources: Dict[str, Any]) -> List[str]:
        """Aggregate skills from all sources"""
        skills = set()
        
        # From GitHub
        if 'github' in data_sources:
            github_data = data_sources['github']
            if 'languages' in github_data:
                skills.update(github_data['languages'].keys())
        
        # From Portfolio
        if 'portfolio' in data_sources:
            portfolio_data = data_sources['portfolio']
            if 'analysis' in portfolio_data and 'skills_mentioned' in portfolio_data['analysis']:
                skills.update(portfolio_data['analysis']['skills_mentioned'])
        
        # From Certificates
        if 'certificates' in data_sources:
            cert_data = data_sources['certificates']
            if 'skill_categories' in cert_data:
                skills.update(cert_data['skill_categories'].keys())
        
        return sorted(list(skills))
    
    def _aggregate_projects(self, data_sources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Aggregate projects from all sources"""
        projects = []
        
        if 'github' in data_sources:
            github_data = data_sources['github']
            if 'projects' in github_data:
                projects.extend(github_data['projects'])
        
        return projects
    
    def _aggregate_certifications(self, data_sources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Aggregate certifications"""
        if 'certificates' in data_sources:
            return data_sources.get('certificates', {}).get('all_certificates', [])
        return []
    
    def _aggregate_achievements(self, data_sources: Dict[str, Any]) -> List[str]:
        """Aggregate achievements from all sources"""
        achievements = []
        
        # GitHub achievements
        if 'github' in data_sources:
            github_data = data_sources['github']
            stats = github_data.get('stats', {})
            if stats.get('total_stars', 0) > 50:
                achievements.append(f"🌟 {stats['total_stars']} GitHub stars")
            if stats.get('followers', 0) > 100:
                achievements.append(f"👥 {stats['followers']} GitHub followers")
        
        # Certificate achievements
        if 'certificates' in data_sources:
            cert_count = data_sources['certificates'].get('total_certificates', 0)
            if cert_count >= 5:
                achievements.append(f"🎓 {cert_count} professional certifications")
        
        return achievements
    
    def _aggregate_social_presence(self, data_sources: Dict[str, Any]) -> Dict[str, str]:
        """Aggregate social media presence"""
        social = {}
        
        if 'github' in data_sources:
            social['github'] = data_sources['github'].get('username')
        
        if 'portfolio' in data_sources:
            links = data_sources['portfolio'].get('social_links', {})
            social.update({k: v for k, v in links.items() if v})
        
        return social
    
    def _count_total_projects(self, data_sources: Dict[str, Any]) -> int:
        """Count total projects"""
        return len(self._aggregate_projects(data_sources))
    
    def _count_total_certifications(self, data_sources: Dict[str, Any]) -> int:
        """Count total certifications"""
        if 'certificates' in data_sources:
            return data_sources['certificates'].get('total_certificates', 0)
        return 0
    
    def _calculate_github_score(self, data_sources: Dict[str, Any]) -> float:
        """Calculate GitHub activity score"""
        if 'github' not in data_sources:
            return 0
        
        github_data = data_sources['github']
        stats = github_data.get('stats', {})
        
        score = 0
        score += min(stats.get('public_repos', 0) * 5, 30)
        score += min(stats.get('total_stars', 0) * 2, 30)
        score += min(stats.get('followers', 0), 20)
        score += min(len(github_data.get('languages', {})) * 4, 20)
        
        return min(score, 100)
    
    def _calculate_learning_score(self, data_sources: Dict[str, Any]) -> float:
        """Calculate learning activity score"""
        if 'learning' not in data_sources:
            return 0
        
        learning_data = data_sources['learning']
        
        score = 0
        score += min(learning_data.get('courses_completed', 0) * 10, 40)
        score += min(learning_data.get('courses_in_progress', 0) * 5, 20)
        score += min(learning_data.get('total_learning_hours', 0) / 2, 40)
        
        return min(score, 100)
    
    def _calculate_portfolio_score(self, data_sources: Dict[str, Any]) -> float:
        """Calculate portfolio quality score"""
        if 'portfolio' in data_sources:
            return data_sources['portfolio'].get('quality_score', 0)
        return 0
    
    def _generate_integration_recommendations(self, data_sources: Dict[str, Any]) -> List[str]:
        """Generate recommendations for better integration"""
        recommendations = []
        
        if 'github' not in data_sources:
            recommendations.append("🐙 Connect your GitHub profile for project analysis")
        
        if 'portfolio' not in data_sources:
            recommendations.append("🌐 Add your portfolio website for comprehensive analysis")
        
        if 'certificates' not in data_sources or data_sources['certificates'].get('total_certificates', 0) < 3:
            recommendations.append("🎓 Add more certifications to strengthen your profile")
        
        if 'learning' not in data_sources:
            recommendations.append("📚 Track your learning progress for better insights")
        
        return recommendations
    
    def _identify_missing_sources(self, data_sources: Dict[str, Any]) -> List[str]:
        """Identify missing data sources"""
        integrated = set(data_sources.keys())
        all_sources = set(self.SUPPORTED_PLATFORMS.keys())
        missing = all_sources - integrated
        return sorted(list(missing))


# Streamlit cached functions
@st.cache_data(ttl=3600)
def integrate_github(username: str) -> Dict[str, Any]:
    """Cached GitHub integration"""
    integrator = MultiSourceIntegrator()
    return integrator.integrate_github_data(username)


@st.cache_data(ttl=3600)
def integrate_portfolio(url: str) -> Dict[str, Any]:
    """Cached portfolio integration"""
    integrator = MultiSourceIntegrator()
    return integrator.integrate_portfolio_data(url)


@st.cache_data(ttl=3600)
def create_unified_profile(data_sources: Dict[str, Any]) -> Dict[str, Any]:
    """Cached unified profile creation"""
    integrator = MultiSourceIntegrator()
    return integrator.create_unified_profile(data_sources)

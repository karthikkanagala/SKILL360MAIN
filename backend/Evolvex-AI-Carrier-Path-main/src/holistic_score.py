"""
Holistic Career Score Calculator
Comprehensive career readiness score combining all factors like a credit score
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
import streamlit as st
from datetime import datetime


class HolisticCareerScore:
    """Calculate comprehensive career readiness score (0-850, like credit score)"""
    
    # Score components and their weights
    SCORE_COMPONENTS = {
        'resume_quality': {
            'weight': 0.15,
            'max_points': 127.5,  # 15% of 850
            'description': 'Resume content, formatting, and ATS compatibility'
        },
        'skills_portfolio': {
            'weight': 0.20,
            'max_points': 170,  # 20% of 850
            'description': 'Technical and soft skills breadth and depth'
        },
        'project_portfolio': {
            'weight': 0.18,
            'max_points': 153,  # 18% of 850
            'description': 'Quality, diversity, and impact of projects'
        },
        'certifications': {
            'weight': 0.12,
            'max_points': 102,  # 12% of 850
            'description': 'Professional certifications and courses'
        },
        'extracurricular': {
            'weight': 0.10,
            'max_points': 85,  # 10% of 850
            'description': 'Hackathons, clubs, volunteering, leadership'
        },
        'github_activity': {
            'weight': 0.10,
            'max_points': 85,  # 10% of 850
            'description': 'Open source contributions and code quality'
        },
        'learning_progress': {
            'weight': 0.08,
            'max_points': 68,  # 8% of 850
            'description': 'Continuous learning and skill development'
        },
        'interview_readiness': {
            'weight': 0.07,
            'max_points': 59.5,  # 7% of 850
            'description': 'Interview preparation and practice'
        }
    }
    
    # Score ranges and their meanings
    SCORE_RANGES = {
        (750, 850): {
            'rating': 'Exceptional',
            'emoji': '🌟',
            'color': '#00C853',
            'description': 'Outstanding career readiness - Top tier candidate',
            'opportunities': 'Eligible for top companies, leadership roles, premium internships'
        },
        (650, 749): {
            'rating': 'Excellent',
            'emoji': '⭐',
            'color': '#64DD17',
            'description': 'Strong career profile - Highly competitive',
            'opportunities': 'Competitive for most positions, good internship prospects'
        },
        (550, 649): {
            'rating': 'Good',
            'emoji': '✨',
            'color': '#FFD600',
            'description': 'Solid foundation - Ready for entry-level roles',
            'opportunities': 'Suitable for entry-level positions and internships'
        },
        (450, 549): {
            'rating': 'Fair',
            'emoji': '📈',
            'color': '#FF6F00',
            'description': 'Developing profile - Needs improvement',
            'opportunities': 'May qualify for some internships, needs skill building'
        },
        (0, 449): {
            'rating': 'Building',
            'emoji': '🚀',
            'color': '#FF5252',
            'description': 'Early stage - Focus on fundamentals',
            'opportunities': 'Focus on learning, projects, and skill development'
        }
    }
    
    def __init__(self):
        """Initialize the holistic score calculator"""
        pass
    
    def calculate_comprehensive_score(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive career score from all profile components
        
        Args:
            profile_data: Complete profile with all components
                - resume_analysis: Resume quality metrics
                - skills: Skills list and proficiency
                - projects: Project portfolio
                - certifications: Certifications list
                - extracurricular: Activities list
                - github_stats: GitHub statistics
                - learning_progress: Course completion data
                - interview_scores: Interview practice results
        
        Returns:
            Comprehensive score analysis
        """
        component_scores = {}
        total_score = 0
        
        # Calculate each component score
        component_scores['resume_quality'] = self._score_resume(
            profile_data.get('resume_analysis', {})
        )
        
        component_scores['skills_portfolio'] = self._score_skills(
            profile_data.get('skills', []),
            profile_data.get('skill_proficiency', {})
        )
        
        component_scores['project_portfolio'] = self._score_projects(
            profile_data.get('projects', [])
        )
        
        component_scores['certifications'] = self._score_certifications(
            profile_data.get('certifications', [])
        )
        
        component_scores['extracurricular'] = self._score_extracurricular(
            profile_data.get('extracurricular', [])
        )
        
        component_scores['github_activity'] = self._score_github(
            profile_data.get('github_stats', {})
        )
        
        component_scores['learning_progress'] = self._score_learning(
            profile_data.get('learning_progress', {})
        )
        
        component_scores['interview_readiness'] = self._score_interview_prep(
            profile_data.get('interview_scores', {})
        )
        
        # Calculate weighted total
        for component, score_data in component_scores.items():
            weight = self.SCORE_COMPONENTS[component]['weight']
            max_points = self.SCORE_COMPONENTS[component]['max_points']
            weighted_score = (score_data['percentage'] / 100) * max_points
            total_score += weighted_score
            score_data['weighted_score'] = weighted_score
            score_data['max_points'] = max_points
        
        # Determine score range and rating
        score_info = self._get_score_info(total_score)
        
        # Generate insights and recommendations
        strengths = self._identify_strengths(component_scores)
        weaknesses = self._identify_weaknesses(component_scores)
        recommendations = self._generate_recommendations(component_scores, total_score)
        
        # Calculate percentile (simulated based on score)
        percentile = self._calculate_percentile(total_score)
        
        return {
            'total_score': round(total_score, 1),
            'max_score': 850,
            'rating': score_info['rating'],
            'emoji': score_info['emoji'],
            'color': score_info['color'],
            'description': score_info['description'],
            'opportunities': score_info['opportunities'],
            'percentile': percentile,
            'component_scores': component_scores,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'score_breakdown': self._create_score_breakdown(component_scores),
            'improvement_potential': self._calculate_improvement_potential(component_scores)
        }
    
    def _score_resume(self, resume_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Score resume quality (0-100)"""
        score = 0
        
        # ATS score component (40%)
        ats_score = resume_analysis.get('ats_score', 0)
        score += (ats_score / 100) * 40
        
        # Content quality (30%)
        has_summary = resume_analysis.get('has_summary', False)
        has_quantifiable = resume_analysis.get('has_quantifiable_achievements', False)
        has_keywords = resume_analysis.get('keyword_density', 0) > 0.5
        
        content_score = sum([has_summary, has_quantifiable, has_keywords]) / 3 * 30
        score += content_score
        
        # Formatting (20%)
        formatting_score = resume_analysis.get('formatting_score', 70)
        score += (formatting_score / 100) * 20
        
        # Completeness (10%)
        sections = resume_analysis.get('sections_count', 0)
        completeness = min(sections / 5, 1) * 10
        score += completeness
        
        return {
            'percentage': min(score, 100),
            'details': 'Resume quality and ATS compatibility'
        }
    
    def _score_skills(self, skills: List[str], proficiency: Dict[str, int]) -> Dict[str, float]:
        """Score skills portfolio (0-100)"""
        score = 0
        
        # Skill count (30%)
        skill_count = len(skills)
        count_score = min(skill_count / 15, 1) * 30
        score += count_score
        
        # Skill diversity (30%)
        categories = set()
        tech_keywords = ['python', 'java', 'javascript', 'sql', 'react']
        soft_keywords = ['communication', 'leadership', 'teamwork']
        
        has_tech = any(any(kw in skill.lower() for kw in tech_keywords) for skill in skills)
        has_soft = any(any(kw in skill.lower() for kw in soft_keywords) for skill in skills)
        
        diversity_score = (has_tech + has_soft) / 2 * 30
        score += diversity_score
        
        # Proficiency levels (40%)
        if proficiency:
            avg_proficiency = sum(proficiency.values()) / len(proficiency)
            proficiency_score = (avg_proficiency / 100) * 40
            score += proficiency_score
        else:
            score += 20  # Base score if no proficiency data
        
        return {
            'percentage': min(score, 100),
            'details': f'{skill_count} skills with varying proficiency'
        }
    
    def _score_projects(self, projects: List[Dict[str, Any]]) -> Dict[str, float]:
        """Score project portfolio (0-100)"""
        score = 0
        
        if not projects:
            return {'percentage': 0, 'details': 'No projects found'}
        
        # Project count (25%)
        count_score = min(len(projects) / 8, 1) * 25
        score += count_score
        
        # Project quality (50%)
        quality_scores = []
        for project in projects:
            proj_score = 0
            
            # Has description
            if project.get('description'):
                proj_score += 20
            
            # Has GitHub link
            if project.get('github_url'):
                proj_score += 20
            
            # Has live demo
            if project.get('demo_url'):
                proj_score += 20
            
            # Has stars/engagement
            stars = project.get('stars', 0)
            if stars > 0:
                proj_score += min(stars * 5, 20)
            
            # Complexity
            if 'complex' in project.get('description', '').lower():
                proj_score += 20
            
            quality_scores.append(min(proj_score, 100))
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        score += (avg_quality / 100) * 50
        
        # Diversity (25%)
        languages = set(p.get('language', 'Unknown') for p in projects)
        diversity_score = min(len(languages) / 4, 1) * 25
        score += diversity_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{len(projects)} projects across {len(languages)} technologies'
        }
    
    def _score_certifications(self, certifications: List[Dict[str, Any]]) -> Dict[str, float]:
        """Score certifications (0-100)"""
        score = 0
        
        if not certifications:
            return {'percentage': 0, 'details': 'No certifications'}
        
        # Count (30%)
        count_score = min(len(certifications) / 8, 1) * 30
        score += count_score
        
        # Quality/Trust (50%)
        trusted_providers = ['google', 'microsoft', 'aws', 'ibm', 'coursera', 'edx']
        trusted_count = sum(1 for cert in certifications 
                          if any(provider in cert.get('provider', '').lower() 
                                for provider in trusted_providers))
        
        quality_score = min(trusted_count / max(len(certifications), 1), 1) * 50
        score += quality_score
        
        # Recency (20%)
        recent_count = 0
        current_year = datetime.now().year
        for cert in certifications:
            if cert.get('date'):
                try:
                    year = int(cert['date'][:4])
                    if current_year - year <= 2:
                        recent_count += 1
                except:
                    pass
        
        recency_score = min(recent_count / max(len(certifications), 1), 1) * 20
        score += recency_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{len(certifications)} certifications, {trusted_count} from top providers'
        }
    
    def _score_extracurricular(self, activities: List[Dict[str, Any]]) -> Dict[str, float]:
        """Score extracurricular activities (0-100)"""
        score = 0
        
        if not activities:
            return {'percentage': 0, 'details': 'No extracurricular activities'}
        
        # Count (30%)
        count_score = min(len(activities) / 6, 1) * 30
        score += count_score
        
        # Leadership (40%)
        leadership_keywords = ['president', 'lead', 'founder', 'organizer', 'captain']
        leadership_count = sum(1 for activity in activities 
                             if any(kw in activity.get('role', '').lower() 
                                   for kw in leadership_keywords))
        
        leadership_score = min(leadership_count / max(len(activities), 1), 1) * 40
        score += leadership_score
        
        # Impact (30%)
        impact_count = sum(1 for activity in activities 
                         if activity.get('achievements') or activity.get('impact'))
        
        impact_score = min(impact_count / max(len(activities), 1), 1) * 30
        score += impact_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{len(activities)} activities, {leadership_count} leadership roles'
        }
    
    def _score_github(self, github_stats: Dict[str, Any]) -> Dict[str, float]:
        """Score GitHub activity (0-100)"""
        score = 0
        
        if not github_stats:
            return {'percentage': 0, 'details': 'No GitHub activity'}
        
        # Repository count (25%)
        repos = github_stats.get('public_repos', 0)
        repo_score = min(repos / 15, 1) * 25
        score += repo_score
        
        # Contributions (35%)
        contributions = github_stats.get('total_contributions', 0)
        contrib_score = min(contributions / 500, 1) * 35
        score += contrib_score
        
        # Stars received (20%)
        stars = github_stats.get('total_stars', 0)
        star_score = min(stars / 50, 1) * 20
        score += star_score
        
        # Consistency (20%)
        streak = github_stats.get('longest_streak', 0)
        consistency_score = min(streak / 30, 1) * 20
        score += consistency_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{repos} repos, {contributions} contributions, {stars} stars'
        }
    
    def _score_learning(self, learning_progress: Dict[str, Any]) -> Dict[str, float]:
        """Score learning progress (0-100)"""
        score = 0
        
        if not learning_progress:
            return {'percentage': 50, 'details': 'No learning data'}
        
        # Courses completed (40%)
        completed = learning_progress.get('completed_courses', 0)
        completion_score = min(completed / 10, 1) * 40
        score += completion_score
        
        # In progress (30%)
        in_progress = learning_progress.get('in_progress_courses', 0)
        progress_score = min(in_progress / 5, 1) * 30
        score += progress_score
        
        # Learning consistency (30%)
        hours = learning_progress.get('total_hours', 0)
        hours_score = min(hours / 100, 1) * 30
        score += hours_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{completed} completed, {in_progress} in progress'
        }
    
    def _score_interview_prep(self, interview_scores: Dict[str, Any]) -> Dict[str, float]:
        """Score interview readiness (0-100)"""
        score = 0
        
        if not interview_scores:
            return {'percentage': 40, 'details': 'No interview practice data'}
        
        # Practice count (30%)
        practice_count = interview_scores.get('questions_practiced', 0)
        practice_score = min(practice_count / 50, 1) * 30
        score += practice_score
        
        # Average performance (50%)
        avg_score = interview_scores.get('average_score', 0)
        performance_score = (avg_score / 100) * 50
        score += performance_score
        
        # Improvement trend (20%)
        improvement = interview_scores.get('improvement_rate', 0)
        trend_score = min(improvement / 20, 1) * 20
        score += trend_score
        
        return {
            'percentage': min(score, 100),
            'details': f'{practice_count} questions practiced, {avg_score}% avg score'
        }
    
    def _get_score_info(self, score: float) -> Dict[str, str]:
        """Get score range information"""
        for (min_score, max_score), info in self.SCORE_RANGES.items():
            if min_score <= score <= max_score:
                return info
        return self.SCORE_RANGES[(0, 449)]
    
    def _identify_strengths(self, component_scores: Dict[str, Dict]) -> List[str]:
        """Identify top strengths"""
        strengths = []
        
        sorted_components = sorted(
            component_scores.items(),
            key=lambda x: x[1]['percentage'],
            reverse=True
        )
        
        for component, score_data in sorted_components[:3]:
            if score_data['percentage'] >= 70:
                component_name = component.replace('_', ' ').title()
                strengths.append(f"✅ {component_name}: {score_data['percentage']:.1f}%")
        
        return strengths if strengths else ["🌱 Building foundation across all areas"]
    
    def _identify_weaknesses(self, component_scores: Dict[str, Dict]) -> List[str]:
        """Identify areas needing improvement"""
        weaknesses = []
        
        sorted_components = sorted(
            component_scores.items(),
            key=lambda x: x[1]['percentage']
        )
        
        for component, score_data in sorted_components[:3]:
            if score_data['percentage'] < 60:
                component_name = component.replace('_', ' ').title()
                weaknesses.append(f"⚠️ {component_name}: {score_data['percentage']:.1f}%")
        
        return weaknesses if weaknesses else ["✨ All areas performing well"]
    
    def _generate_recommendations(self, component_scores: Dict[str, Dict], total_score: float) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Find lowest scoring component
        lowest = min(component_scores.items(), key=lambda x: x[1]['percentage'])
        component_name = lowest[0].replace('_', ' ').title()
        
        recommendations.append(f"🎯 Priority: Improve {component_name} (currently {lowest[1]['percentage']:.1f}%)")
        
        # Score-based recommendations
        if total_score < 450:
            recommendations.append("📚 Focus on building foundational skills and completing 2-3 projects")
            recommendations.append("🎓 Earn 2-3 beginner certifications to validate your learning")
        elif total_score < 550:
            recommendations.append("💼 Build a strong portfolio with 4-5 quality projects")
            recommendations.append("🏆 Participate in hackathons or coding competitions")
        elif total_score < 650:
            recommendations.append("🚀 Focus on advanced skills and specialized certifications")
            recommendations.append("👥 Take on leadership roles in projects or communities")
        elif total_score < 750:
            recommendations.append("⭐ Contribute to open source projects to showcase expertise")
            recommendations.append("📈 Mentor others and share knowledge through blogs/talks")
        else:
            recommendations.append("🌟 Maintain excellence and explore cutting-edge technologies")
            recommendations.append("🎤 Build your personal brand through speaking and writing")
        
        return recommendations
    
    def _create_score_breakdown(self, component_scores: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Create detailed score breakdown"""
        breakdown = []
        
        for component, score_data in component_scores.items():
            breakdown.append({
                'component': component.replace('_', ' ').title(),
                'percentage': score_data['percentage'],
                'weighted_score': score_data['weighted_score'],
                'max_points': score_data['max_points'],
                'details': score_data['details']
            })
        
        # Sort by weighted score
        breakdown.sort(key=lambda x: x['weighted_score'], reverse=True)
        
        return breakdown
    
    def _calculate_improvement_potential(self, component_scores: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate potential score improvement"""
        current_total = sum(s['weighted_score'] for s in component_scores.values())
        max_total = 850
        
        potential_gain = max_total - current_total
        
        # Find component with most improvement potential
        max_gain_component = max(
            component_scores.items(),
            key=lambda x: (100 - x[1]['percentage']) * self.SCORE_COMPONENTS[x[0]]['weight']
        )
        
        component_name = max_gain_component[0].replace('_', ' ').title()
        potential_points = (100 - max_gain_component[1]['percentage']) / 100 * max_gain_component[1]['max_points']
        
        return {
            'total_potential_gain': round(potential_gain, 1),
            'best_improvement_area': component_name,
            'potential_points_from_best_area': round(potential_points, 1),
            'percentage_to_max': round((current_total / max_total) * 100, 1)
        }
    
    def _calculate_percentile(self, score: float) -> int:
        """Calculate approximate percentile based on score"""
        # Simulated percentile calculation
        if score >= 750:
            return 95 + int((score - 750) / 10)
        elif score >= 650:
            return 75 + int((score - 650) / 5)
        elif score >= 550:
            return 50 + int((score - 550) / 4)
        elif score >= 450:
            return 25 + int((score - 450) / 4)
        else:
            return int(score / 18)


# Streamlit cached function
@st.cache_data(ttl=3600)
def calculate_holistic_score(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cached holistic score calculation"""
    calculator = HolisticCareerScore()
    return calculator.calculate_comprehensive_score(profile_data)

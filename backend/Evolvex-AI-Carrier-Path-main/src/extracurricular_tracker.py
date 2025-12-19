"""
Extracurricular Activities Tracker
Tracks hackathons, club work, freelancing, volunteering, and other activities
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict
import streamlit as st


class ExtracurricularTracker:
    """Tracks and analyzes extracurricular activities"""
    
    ACTIVITY_TYPES = {
        'Hackathon': {
            'icon': '🏆',
            'weight': 1.5,
            'skills': ['Problem Solving', 'Teamwork', 'Time Management', 'Innovation'],
            'impact_keywords': ['winner', 'finalist', 'award', 'prize', 'top', 'champion']
        },
        'Club/Organization': {
            'icon': '👥',
            'weight': 1.2,
            'skills': ['Leadership', 'Teamwork', 'Organization', 'Communication'],
            'impact_keywords': ['president', 'lead', 'founder', 'organizer', 'coordinator']
        },
        'Freelancing': {
            'icon': '💼',
            'weight': 1.4,
            'skills': ['Client Management', 'Self-motivation', 'Business', 'Professional Communication'],
            'impact_keywords': ['client', 'project', 'delivered', 'revenue', 'satisfied']
        },
        'Volunteering': {
            'icon': '🤝',
            'weight': 1.1,
            'skills': ['Empathy', 'Social Responsibility', 'Teamwork', 'Communication'],
            'impact_keywords': ['impact', 'community', 'helped', 'served', 'benefited']
        },
        'Open Source': {
            'icon': '🌐',
            'weight': 1.3,
            'skills': ['Collaboration', 'Code Review', 'Version Control', 'Technical Writing'],
            'impact_keywords': ['contributor', 'maintainer', 'merged', 'pr', 'commits']
        },
        'Research': {
            'icon': '🔬',
            'weight': 1.4,
            'skills': ['Research', 'Analysis', 'Critical Thinking', 'Documentation'],
            'impact_keywords': ['published', 'paper', 'findings', 'study', 'research']
        },
        'Competition': {
            'icon': '🎯',
            'weight': 1.3,
            'skills': ['Competitive Spirit', 'Excellence', 'Preparation', 'Performance'],
            'impact_keywords': ['winner', 'rank', 'medal', 'award', 'champion']
        },
        'Workshop/Seminar': {
            'icon': '📚',
            'weight': 1.0,
            'skills': ['Learning', 'Networking', 'Knowledge Sharing', 'Professional Development'],
            'impact_keywords': ['speaker', 'presenter', 'organized', 'attended', 'participated']
        },
        'Mentoring': {
            'icon': '🎓',
            'weight': 1.2,
            'skills': ['Teaching', 'Patience', 'Communication', 'Leadership'],
            'impact_keywords': ['mentored', 'guided', 'taught', 'helped', 'trained']
        },
        'Content Creation': {
            'icon': '✍️',
            'weight': 1.1,
            'skills': ['Communication', 'Creativity', 'Marketing', 'Technical Writing'],
            'impact_keywords': ['blog', 'video', 'tutorial', 'views', 'followers']
        }
    }
    
    def __init__(self):
        """Initialize the extracurricular tracker"""
        pass
    
    def analyze_activity(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single extracurricular activity
        
        Args:
            activity: Dictionary containing activity information
                - type: Activity type (Hackathon, Club, etc.)
                - name: Activity name
                - role: Your role
                - description: Activity description
                - start_date: Start date
                - end_date: End date (optional for ongoing)
                - achievements: List of achievements
                - skills_used: Skills demonstrated
                - impact: Quantifiable impact
        
        Returns:
            Analysis with impact score and skill mapping
        """
        activity_type = activity.get('type', 'Other')
        type_info = self.ACTIVITY_TYPES.get(activity_type, {
            'icon': '📌',
            'weight': 1.0,
            'skills': [],
            'impact_keywords': []
        })
        
        analysis = {
            'type': activity_type,
            'icon': type_info['icon'],
            'base_weight': type_info['weight'],
            'impact_score': 0,
            'skills_demonstrated': [],
            'duration_months': 0,
            'leadership_level': 'Participant',
            'quantifiable_impact': False,
            'recommendations': []
        }
        
        # Calculate duration
        if activity.get('start_date'):
            try:
                start = datetime.strptime(activity['start_date'], '%Y-%m-%d')
                end = datetime.strptime(activity.get('end_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
                analysis['duration_months'] = max(1, (end - start).days // 30)
            except:
                analysis['duration_months'] = 1
        
        # Analyze role for leadership
        role = activity.get('role', '').lower()
        description = activity.get('description', '').lower()
        combined_text = f"{role} {description}"
        
        leadership_keywords = {
            'Executive': ['president', 'ceo', 'founder', 'director', 'head'],
            'Lead': ['lead', 'manager', 'coordinator', 'organizer', 'captain'],
            'Core Team': ['core', 'committee', 'board', 'team lead'],
            'Active Member': ['member', 'volunteer', 'contributor', 'participant']
        }
        
        for level, keywords in leadership_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                analysis['leadership_level'] = level
                break
        
        # Calculate impact score
        impact_score = type_info['weight'] * 20  # Base score
        
        # Leadership bonus
        leadership_multiplier = {
            'Executive': 2.0,
            'Lead': 1.5,
            'Core Team': 1.3,
            'Active Member': 1.0,
            'Participant': 0.8
        }
        impact_score *= leadership_multiplier.get(analysis['leadership_level'], 1.0)
        
        # Duration bonus
        if analysis['duration_months'] >= 12:
            impact_score *= 1.3
        elif analysis['duration_months'] >= 6:
            impact_score *= 1.15
        
        # Achievement bonus
        achievements = activity.get('achievements', [])
        if achievements:
            impact_score += len(achievements) * 5
            
            # Check for high-impact keywords
            achievements_text = ' '.join(achievements).lower()
            for keyword in type_info['impact_keywords']:
                if keyword in achievements_text:
                    impact_score += 10
                    analysis['quantifiable_impact'] = True
        
        # Impact metrics bonus
        impact = activity.get('impact', '').lower()
        if any(char.isdigit() for char in impact):
            impact_score += 15
            analysis['quantifiable_impact'] = True
        
        analysis['impact_score'] = min(impact_score, 100)
        
        # Extract skills
        skills_demonstrated = set(type_info['skills'])
        if activity.get('skills_used'):
            skills_demonstrated.update(activity['skills_used'])
        analysis['skills_demonstrated'] = list(skills_demonstrated)
        
        # Generate recommendations
        if not activity.get('achievements'):
            analysis['recommendations'].append('Add specific achievements or outcomes')
        if not analysis['quantifiable_impact']:
            analysis['recommendations'].append('Add quantifiable metrics (numbers, percentages, impact)')
        if not activity.get('skills_used'):
            analysis['recommendations'].append('List specific skills you used or developed')
        
        return analysis
    
    def analyze_all_activities(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Comprehensive analysis of all extracurricular activities
        
        Args:
            activities: List of activity dictionaries
        
        Returns:
            Complete analysis with scores, trends, and insights
        """
        analysis = {
            'total_activities': len(activities),
            'by_type': defaultdict(int),
            'total_impact_score': 0,
            'skills_gained': defaultdict(int),
            'leadership_experience': defaultdict(int),
            'timeline': [],
            'diversity_score': 0,
            'consistency_score': 0,
            'quality_score': 0,
            'activity_details': [],
            'strengths': [],
            'recommendations': [],
            'top_activities': []
        }
        
        if not activities:
            analysis['recommendations'].append('Start participating in extracurricular activities to build a well-rounded profile')
            return analysis
        
        total_impact = 0
        
        for activity in activities:
            # Analyze individual activity
            activity_analysis = self.analyze_activity(activity)
            
            # Aggregate data
            activity_type = activity_analysis['type']
            analysis['by_type'][activity_type] += 1
            total_impact += activity_analysis['impact_score']
            
            # Track skills
            for skill in activity_analysis['skills_demonstrated']:
                analysis['skills_gained'][skill] += 1
            
            # Track leadership
            analysis['leadership_experience'][activity_analysis['leadership_level']] += 1
            
            # Add to timeline
            if activity.get('start_date'):
                analysis['timeline'].append({
                    'date': activity['start_date'],
                    'name': activity.get('name', 'Unknown'),
                    'type': activity_type,
                    'role': activity.get('role', 'Participant')
                })
            
            # Store detailed analysis
            activity_detail = {
                'name': activity.get('name', 'Unknown'),
                'type': activity_type,
                'analysis': activity_analysis
            }
            analysis['activity_details'].append(activity_detail)
        
        # Sort timeline
        analysis['timeline'].sort(key=lambda x: x['date'], reverse=True)
        
        # Calculate scores
        analysis['total_impact_score'] = total_impact
        analysis['diversity_score'] = min(len(analysis['by_type']) * 15, 100)
        analysis['quality_score'] = min(total_impact / max(len(activities), 1), 100)
        
        # Consistency score based on timeline spread
        if len(analysis['timeline']) >= 2:
            # Activities spread over time is good
            analysis['consistency_score'] = min(len(set(t['date'][:7] for t in analysis['timeline'])) * 10, 100)
        else:
            analysis['consistency_score'] = 30
        
        # Identify top activities
        scored_activities = [(a['name'], a['analysis']['impact_score']) for a in analysis['activity_details']]
        analysis['top_activities'] = sorted(scored_activities, key=lambda x: x[1], reverse=True)[:5]
        
        # Generate strengths
        analysis['strengths'] = self._identify_strengths(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_activity_recommendations(analysis)
        
        return analysis
    
    def _identify_strengths(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify key strengths from activities"""
        strengths = []
        
        # Leadership strength
        leadership_count = sum(analysis['leadership_experience'].get(level, 0) 
                              for level in ['Executive', 'Lead', 'Core Team'])
        if leadership_count >= 2:
            strengths.append('🌟 Strong leadership experience across multiple activities')
        
        # Diversity strength
        if analysis['diversity_score'] >= 60:
            strengths.append('🎨 Diverse extracurricular portfolio showing well-rounded interests')
        
        # Technical activities
        tech_activities = sum(analysis['by_type'].get(t, 0) for t in ['Hackathon', 'Open Source', 'Research'])
        if tech_activities >= 3:
            strengths.append('💻 Strong technical engagement through hackathons and open source')
        
        # Consistency
        if analysis['consistency_score'] >= 70:
            strengths.append('📈 Consistent participation showing long-term commitment')
        
        # Impact
        if analysis['quality_score'] >= 70:
            strengths.append('⚡ High-impact activities with measurable outcomes')
        
        return strengths if strengths else ['✨ Building a foundation of extracurricular experience']
    
    def _generate_activity_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving extracurricular profile"""
        recommendations = []
        
        # Activity count
        if analysis['total_activities'] < 3:
            recommendations.append('🎯 Aim for 5-8 quality extracurricular activities to build a strong profile')
        elif analysis['total_activities'] > 15:
            recommendations.append('📋 Focus on depth over breadth - highlight your most impactful activities')
        
        # Diversity
        if analysis['diversity_score'] < 40:
            recommendations.append('🌈 Diversify your activities across different types (technical, leadership, social)')
        
        # Leadership
        leadership_count = sum(analysis['leadership_experience'].get(level, 0) 
                              for level in ['Executive', 'Lead'])
        if leadership_count == 0:
            recommendations.append('👑 Seek leadership roles to demonstrate initiative and management skills')
        
        # Technical activities
        tech_count = sum(analysis['by_type'].get(t, 0) for t in ['Hackathon', 'Open Source'])
        if tech_count == 0:
            recommendations.append('💻 Participate in hackathons or contribute to open source projects')
        
        # Consistency
        if analysis['consistency_score'] < 50:
            recommendations.append('📅 Maintain consistent participation over time rather than sporadic involvement')
        
        # Impact documentation
        low_impact_count = sum(1 for a in analysis['activity_details'] 
                              if not a['analysis']['quantifiable_impact'])
        if low_impact_count > len(analysis['activity_details']) / 2:
            recommendations.append('📊 Add quantifiable metrics to demonstrate your impact (numbers, percentages, outcomes)')
        
        # Specific activity suggestions
        if 'Hackathon' not in analysis['by_type']:
            recommendations.append('🏆 Participate in hackathons to showcase problem-solving and teamwork skills')
        if 'Freelancing' not in analysis['by_type'] and 'Open Source' not in analysis['by_type']:
            recommendations.append('💼 Consider freelancing or open source to gain real-world experience')
        
        return recommendations
    
    def get_extracurricular_score(self, activities: List[Dict[str, Any]]) -> float:
        """
        Calculate overall extracurricular score (0-100)
        
        Args:
            activities: List of activities
        
        Returns:
            Score from 0-100
        """
        if not activities:
            return 0
        
        analysis = self.analyze_all_activities(activities)
        
        # Weighted scoring
        quantity_score = min(len(activities) * 8, 25)  # Max 25 points
        quality_score = min(analysis['quality_score'] * 0.35, 35)  # Max 35 points
        diversity_score = min(analysis['diversity_score'] * 0.20, 20)  # Max 20 points
        consistency_score = min(analysis['consistency_score'] * 0.20, 20)  # Max 20 points
        
        total_score = quantity_score + quality_score + diversity_score + consistency_score
        
        return min(total_score, 100)


# Streamlit cached functions
@st.cache_data(ttl=3600)
def analyze_extracurricular_activities(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Cached extracurricular analysis"""
    tracker = ExtracurricularTracker()
    return tracker.analyze_all_activities(activities)


@st.cache_data(ttl=3600)
def get_extracurricular_score(activities: List[Dict[str, Any]]) -> float:
    """Cached extracurricular score calculation"""
    tracker = ExtracurricularTracker()
    return tracker.get_extracurricular_score(activities)

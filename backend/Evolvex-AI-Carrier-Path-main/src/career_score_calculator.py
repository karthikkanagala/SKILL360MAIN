"""
Career Score Calculator Module
Calculates holistic career score based on profile components
"""
import json
import os
from datetime import datetime


class CareerScoreCalculator:
    """Calculates comprehensive career score"""
    
    def __init__(self):
        self.score_history_file = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'career_score_history.json'
        )
        
    def calculate_career_score(self, profile_data: dict) -> dict:
        """
        Calculate career score from profile data
        
        Args:
            profile_data: Dictionary containing all profile components
            
        Returns:
            Dictionary with score and breakdown
        """
        scores = {}
        
        # Resume score (0-200)
        resume_data = profile_data.get('resume_data', {})
        if resume_data:
            ats_score = resume_data.get('ats_score', 50)
            skills_count = len(resume_data.get('skills', []))
            scores['resume'] = min(200, int(ats_score * 1.5 + skills_count * 3))
        else:
            scores['resume'] = 0
            
        # GitHub score (0-200)
        github_data = profile_data.get('github_data', {})
        if github_data:
            repos = github_data.get('total_repos', 0)
            stars = github_data.get('total_stars', 0)
            contribution_score = github_data.get('contribution_score', 0)
            scores['github'] = min(200, int(repos * 2 + stars * 0.5 + contribution_score))
        else:
            scores['github'] = 0
            
        # Certifications score (0-200)
        certificates = profile_data.get('certificates', [])
        if certificates:
            verified_count = sum(1 for c in certificates if c.get('status') == 'verified')
            scores['certifications'] = min(200, verified_count * 40)
        else:
            scores['certifications'] = 0
            
        # Activities score (0-200)
        activities = profile_data.get('activities', [])
        activity_summary = profile_data.get('activity_summary', {})
        if activities or activity_summary:
            activity_count = len(activities) if activities else activity_summary.get('count', 0)
            scores['activities'] = min(200, activity_count * 25)
        else:
            scores['activities'] = 0
            
        # Portfolio score (0-200)
        portfolio = profile_data.get('portfolio_analysis', {})
        if portfolio:
            quality = portfolio.get('quality_score', 50)
            scores['portfolio'] = min(200, int(quality * 2))
        else:
            scores['portfolio'] = 0
            
        # Calculate total (0-1000)
        total_score = sum(scores.values())
        
        result = {
            'total_score': total_score,
            'max_score': 1000,
            'percentage': round(total_score / 10, 1),
            'breakdown': scores,
            'level': self._get_level(total_score),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history
        self._save_to_history(result)
        
        return result
    
    def _get_level(self, score: int) -> str:
        """Get career level based on score"""
        if score >= 900:
            return 'Expert'
        elif score >= 750:
            return 'Advanced'
        elif score >= 500:
            return 'Intermediate'
        elif score >= 250:
            return 'Developing'
        else:
            return 'Beginner'
            
    def _save_to_history(self, result: dict):
        """Save score result to history file"""
        try:
            history = []
            if os.path.exists(self.score_history_file):
                with open(self.score_history_file, 'r') as f:
                    history = json.load(f)
            
            history.append({
                'score': result['total_score'],
                'timestamp': result['timestamp'],
                'breakdown': result['breakdown']
            })
            
            # Keep only last 50 entries
            history = history[-50:]
            
            with open(self.score_history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception:
            pass  # Silently fail on history save errors


def get_career_score_calculator() -> CareerScoreCalculator:
    """Get a career score calculator instance"""
    return CareerScoreCalculator()

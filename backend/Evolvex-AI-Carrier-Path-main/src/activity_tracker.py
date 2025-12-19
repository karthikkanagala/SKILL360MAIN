"""
Activity Tracker Module
Tracks and summarizes extracurricular and professional activities
"""
from typing import List, Dict


class ActivityTracker:
    """Tracks user activities and computes summaries"""
    
    def get_activity_summary(self, activities: List[Dict]) -> Dict:
        """
        Get summary of activities
        
        Args:
            activities: List of activity dictionaries
            
        Returns:
            Summary dictionary
        """
        if not activities:
            return {
                'count': 0,
                'categories': {},
                'impact_score': 0,
                'highlights': []
            }
        
        # Count by category
        categories = {}
        high_impact_count = 0
        
        for activity in activities:
            category = activity.get('category', 'Other')
            categories[category] = categories.get(category, 0) + 1
            if activity.get('impact') == 'high':
                high_impact_count += 1
        
        # Calculate impact score
        impact_weights = {'high': 30, 'medium': 20, 'low': 10}
        impact_score = sum(
            impact_weights.get(a.get('impact', 'low'), 10)
            for a in activities
        )
        
        return {
            'count': len(activities),
            'categories': categories,
            'impact_score': min(100, impact_score),
            'high_impact_count': high_impact_count,
            'highlights': [
                a.get('name', 'Activity') 
                for a in activities 
                if a.get('impact') == 'high'
            ][:5]
        }
    
    def add_activity(self, activities: List[Dict], activity: Dict) -> List[Dict]:
        """
        Add a new activity to the list
        
        Args:
            activities: Existing activities list
            activity: New activity to add
            
        Returns:
            Updated activities list
        """
        activities.append(activity)
        return activities


def get_activity_tracker() -> ActivityTracker:
    """Get an activity tracker instance"""
    return ActivityTracker()

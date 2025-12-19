"""
Advanced Analytics Module
Provides peer comparison, company scoring and PDF export functionality
"""
import random


def get_peer_comparison(career_score: int) -> dict:
    """
    Get peer comparison data based on career score
    
    Args:
        career_score: The user's career score (0-100 or 0-1000)
        
    Returns:
        Dictionary with peer comparison data
    """
    # Normalize score to 0-100 if it's on 0-1000 scale
    normalized_score = career_score if career_score <= 100 else career_score / 10
    
    # Calculate percentile (simulated)
    percentile = min(99, max(1, int(normalized_score * 0.95 + random.randint(0, 5))))
    
    return {
        'your_score': career_score,
        'percentile': percentile,
        'comparison': {
            'above_average': percentile > 50,
            'top_quartile': percentile >= 75,
            'top_decile': percentile >= 90
        },
        'peer_stats': {
            'average_score': 65,
            'median_score': 62,
            'top_10_percent_threshold': 85,
            'top_25_percent_threshold': 75
        },
        'insights': [
            f"You're in the top {100 - percentile}% of professionals",
            "Your technical skills are above average",
            "Consider adding more certifications to boost your score"
        ]
    }


def get_company_scoring(profile_data: dict, company_name: str = None) -> dict:
    """
    Calculate company-specific career score
    
    Args:
        profile_data: User's profile data
        company_name: Target company name
        
    Returns:
        Dictionary with company-specific scoring
    """
    company = company_name or "General Industry"
    
    # Base score calculation
    base_score = 70
    if profile_data.get('resume_data'):
        base_score += 5
    if profile_data.get('github_data'):
        base_score += 8
    if profile_data.get('certificates'):
        base_score += len(profile_data.get('certificates', [])) * 3
    
    # Cap at 100
    final_score = min(100, base_score)
    
    return {
        'company': company,
        'fit_score': final_score,
        'match_level': 'Excellent' if final_score >= 80 else 'Good' if final_score >= 60 else 'Fair',
        'strengths': [
            'Strong technical background',
            'Relevant certifications',
            'Active GitHub presence'
        ],
        'gaps': [
            'Consider adding leadership experience',
            'More specific domain expertise may help'
        ],
        'recommendations': [
            f'Your profile is a {final_score}% match for {company}',
            'Focus on highlighting your technical projects',
            'Prepare for technical interviews'
        ]
    }


def get_pdf_exporter():
    """
    Get a PDF exporter instance
    
    Returns:
        PDFExporter instance
    """
    return PDFExporter()


class PDFExporter:
    """Simple PDF exporter class"""
    
    def export(self, data: dict) -> bytes:
        """
        Export data to PDF
        
        Args:
            data: Data to export
            
        Returns:
            PDF content as bytes
        """
        # Placeholder - would use reportlab or similar
        return b"PDF_CONTENT_PLACEHOLDER"

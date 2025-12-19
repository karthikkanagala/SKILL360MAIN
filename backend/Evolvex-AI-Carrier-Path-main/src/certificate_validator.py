"""
Certificate Validation and Analysis Module
Analyzes certifications, validates authenticity, and provides skill mapping
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
from collections import defaultdict

class CertificateValidator:
    """Validates and analyzes professional certifications"""
    
    # Major certification providers and their patterns
    CERT_PROVIDERS = {
        'Coursera': {
            'pattern': r'coursera\.org/verify/([A-Z0-9]+)',
            'domains': ['coursera.org'],
            'trust_score': 95
        },
        'edX': {
            'pattern': r'credentials\.edx\.org/credentials/([a-f0-9-]+)',
            'domains': ['edx.org', 'credentials.edx.org'],
            'trust_score': 95
        },
        'Udemy': {
            'pattern': r'udemy\.com/certificate/([A-Z0-9]+)',
            'domains': ['udemy.com'],
            'trust_score': 85
        },
        'LinkedIn Learning': {
            'pattern': r'linkedin\.com/learning/certificates/([a-f0-9-]+)',
            'domains': ['linkedin.com'],
            'trust_score': 90
        },
        'Google': {
            'pattern': r'(google\.com/.*certificate|coursera\.org/.*google)',
            'domains': ['google.com', 'grow.google'],
            'trust_score': 98
        },
        'Microsoft': {
            'pattern': r'(microsoft\.com/.*certification|learn\.microsoft)',
            'domains': ['microsoft.com', 'learn.microsoft.com'],
            'trust_score': 98
        },
        'AWS': {
            'pattern': r'(aws\.amazon\.com/certification|aws\.training)',
            'domains': ['aws.amazon.com', 'aws.training'],
            'trust_score': 98
        },
        'IBM': {
            'pattern': r'(ibm\.com/.*badge|credly\.com/.*ibm)',
            'domains': ['ibm.com', 'yourlearning.ibm.com'],
            'trust_score': 95
        },
        'Oracle': {
            'pattern': r'(oracle\.com/.*certification|education\.oracle)',
            'domains': ['oracle.com', 'education.oracle.com'],
            'trust_score': 95
        },
        'Cisco': {
            'pattern': r'(cisco\.com/.*certification|learningnetwork\.cisco)',
            'domains': ['cisco.com'],
            'trust_score': 95
        },
        'CompTIA': {
            'pattern': r'comptia\.org',
            'domains': ['comptia.org', 'certmaster.comptia.org'],
            'trust_score': 92
        },
        'freeCodeCamp': {
            'pattern': r'freecodecamp\.org/certification',
            'domains': ['freecodecamp.org'],
            'trust_score': 88
        },
        'Udacity': {
            'pattern': r'udacity\.com/certificate',
            'domains': ['udacity.com'],
            'trust_score': 90
        },
        'Pluralsight': {
            'pattern': r'pluralsight\.com',
            'domains': ['pluralsight.com'],
            'trust_score': 88
        },
        'DataCamp': {
            'pattern': r'datacamp\.com/certificate',
            'domains': ['datacamp.com'],
            'trust_score': 87
        },
        'HackerRank': {
            'pattern': r'hackerrank\.com/certificates',
            'domains': ['hackerrank.com'],
            'trust_score': 85
        },
        'Credly': {
            'pattern': r'credly\.com/badges',
            'domains': ['credly.com'],
            'trust_score': 90
        }
    }
    
    # Certification categories and skill mappings
    CERT_CATEGORIES = {
        'Cloud Computing': {
            'keywords': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker', 'devops'],
            'skills': ['Cloud Architecture', 'Infrastructure', 'DevOps', 'Containerization'],
            'weight': 1.2
        },
        'Data Science': {
            'keywords': ['data science', 'machine learning', 'ai', 'deep learning', 'analytics', 'statistics'],
            'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'Data Analysis'],
            'weight': 1.3
        },
        'Web Development': {
            'keywords': ['web', 'frontend', 'backend', 'fullstack', 'javascript', 'react', 'node'],
            'skills': ['JavaScript', 'HTML', 'CSS', 'React', 'Node.js', 'Web Development'],
            'weight': 1.1
        },
        'Cybersecurity': {
            'keywords': ['security', 'cybersecurity', 'ethical hacking', 'penetration', 'cissp', 'ceh'],
            'skills': ['Network Security', 'Ethical Hacking', 'Security Analysis', 'Risk Management'],
            'weight': 1.3
        },
        'Database': {
            'keywords': ['sql', 'database', 'mongodb', 'postgresql', 'mysql', 'nosql'],
            'skills': ['SQL', 'Database Design', 'Data Modeling', 'Query Optimization'],
            'weight': 1.1
        },
        'Project Management': {
            'keywords': ['pmp', 'agile', 'scrum', 'project management', 'prince2'],
            'skills': ['Project Management', 'Agile', 'Scrum', 'Leadership'],
            'weight': 1.0
        },
        'Programming': {
            'keywords': ['python', 'java', 'c++', 'programming', 'coding', 'software'],
            'skills': ['Programming', 'Problem Solving', 'Algorithms', 'Data Structures'],
            'weight': 1.2
        },
        'Business Analytics': {
            'keywords': ['business analytics', 'bi', 'tableau', 'power bi', 'excel'],
            'skills': ['Business Intelligence', 'Data Visualization', 'Excel', 'Analytics'],
            'weight': 1.0
        },
        'Mobile Development': {
            'keywords': ['android', 'ios', 'mobile', 'flutter', 'react native', 'swift'],
            'skills': ['Mobile Development', 'iOS', 'Android', 'Cross-platform'],
            'weight': 1.1
        },
        'AI/ML': {
            'keywords': ['artificial intelligence', 'neural network', 'nlp', 'computer vision', 'tensorflow'],
            'skills': ['AI', 'Neural Networks', 'NLP', 'Computer Vision', 'TensorFlow'],
            'weight': 1.4
        }
    }
    
    def __init__(self):
        """Initialize the certificate validator"""
        pass
    
    def validate_certificate(self, cert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single certificate
        
        Args:
            cert_data: Dictionary containing certificate information
                - name: Certificate name
                - provider: Issuing organization
                - url: Certificate URL (optional)
                - date: Issue date (optional)
                - expiry: Expiry date (optional)
        
        Returns:
            Validation result with trust score and details
        """
        result = {
            'valid': False,
            'trust_score': 0,
            'provider_verified': False,
            'url_verified': False,
            'warnings': [],
            'recommendations': []
        }
        
        cert_name = cert_data.get('name', '').lower()
        provider = cert_data.get('provider', '').lower()
        url = cert_data.get('url', '')
        
        # Verify provider
        for known_provider, info in self.CERT_PROVIDERS.items():
            if known_provider.lower() in provider or known_provider.lower() in cert_name:
                result['provider_verified'] = True
                result['trust_score'] = info['trust_score']
                result['verified_provider'] = known_provider
                break
        
        # Verify URL if provided
        if url:
            for known_provider, info in self.CERT_PROVIDERS.items():
                if re.search(info['pattern'], url, re.IGNORECASE):
                    result['url_verified'] = True
                    if not result['provider_verified']:
                        result['provider_verified'] = True
                        result['trust_score'] = info['trust_score']
                        result['verified_provider'] = known_provider
                    break
        
        # Check for expiry
        if cert_data.get('expiry'):
            try:
                expiry_date = datetime.strptime(cert_data['expiry'], '%Y-%m-%d')
                if expiry_date < datetime.now():
                    result['warnings'].append('Certificate has expired')
                    result['trust_score'] *= 0.5
                elif (expiry_date - datetime.now()).days < 90:
                    result['warnings'].append('Certificate expires soon')
            except:
                pass
        
        # Overall validation
        if result['provider_verified'] or result['url_verified']:
            result['valid'] = True
        else:
            result['warnings'].append('Provider not recognized - manual verification recommended')
            result['trust_score'] = 50  # Base score for unverified
        
        # Add recommendations
        if not url:
            result['recommendations'].append('Add certificate URL for verification')
        if not cert_data.get('date'):
            result['recommendations'].append('Add issue date for better tracking')
        
        return result
    
    def analyze_certificates(self, certificates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Comprehensive analysis of all certificates
        
        Args:
            certificates: List of certificate dictionaries
        
        Returns:
            Complete analysis including skills, categories, and recommendations
        """
        analysis = {
            'total_certificates': len(certificates),
            'verified_count': 0,
            'trust_score_avg': 0,
            'categories': defaultdict(list),
            'skills_gained': defaultdict(int),
            'providers': defaultdict(int),
            'timeline': [],
            'warnings': [],
            'recommendations': [],
            'certificate_details': []
        }
        
        total_trust = 0
        
        for cert in certificates:
            # Validate certificate
            validation = self.validate_certificate(cert)
            
            cert_detail = {
                'name': cert.get('name', 'Unknown'),
                'provider': cert.get('provider', 'Unknown'),
                'validation': validation
            }
            
            if validation['valid']:
                analysis['verified_count'] += 1
            
            total_trust += validation['trust_score']
            
            # Categorize certificate
            cert_name = cert.get('name', '').lower()
            cert_desc = cert.get('description', '').lower()
            combined_text = f"{cert_name} {cert_desc}"
            
            matched_categories = []
            for category, info in self.CERT_CATEGORIES.items():
                if any(keyword in combined_text for keyword in info['keywords']):
                    analysis['categories'][category].append(cert.get('name'))
                    matched_categories.append(category)
                    
                    # Add skills
                    for skill in info['skills']:
                        analysis['skills_gained'][skill] += info['weight']
            
            cert_detail['categories'] = matched_categories
            
            # Track provider
            provider = validation.get('verified_provider', cert.get('provider', 'Other'))
            analysis['providers'][provider] += 1
            
            # Add to timeline
            if cert.get('date'):
                try:
                    issue_date = datetime.strptime(cert['date'], '%Y-%m-%d')
                    analysis['timeline'].append({
                        'date': cert['date'],
                        'name': cert.get('name'),
                        'provider': provider
                    })
                except:
                    pass
            
            # Collect warnings
            analysis['warnings'].extend(validation.get('warnings', []))
            
            analysis['certificate_details'].append(cert_detail)
        
        # Calculate averages
        if certificates:
            analysis['trust_score_avg'] = total_trust / len(certificates)
        
        # Sort timeline
        analysis['timeline'].sort(key=lambda x: x['date'], reverse=True)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_cert_recommendations(analysis)
        
        return analysis
    
    def _generate_cert_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on certificate analysis"""
        recommendations = []
        
        # Check certificate count
        if analysis['total_certificates'] < 3:
            recommendations.append('🎯 Consider earning more certifications to strengthen your profile (aim for 5-10 relevant certificates)')
        elif analysis['total_certificates'] > 20:
            recommendations.append('📋 Focus on quality over quantity - highlight your most relevant and recent certifications')
        
        # Check verification rate
        verification_rate = (analysis['verified_count'] / analysis['total_certificates'] * 100) if analysis['total_certificates'] > 0 else 0
        if verification_rate < 70:
            recommendations.append('🔍 Add certificate URLs for better verification (currently {}% verified)'.format(int(verification_rate)))
        
        # Check category diversity
        if len(analysis['categories']) < 2:
            recommendations.append('🌟 Diversify your certifications across multiple domains for a well-rounded profile')
        
        # Check for high-value certifications
        has_cloud = any('Cloud' in cat for cat in analysis['categories'].keys())
        has_ai = any('AI' in cat or 'Data Science' in cat for cat in analysis['categories'].keys())
        
        if not has_cloud:
            recommendations.append('☁️ Consider cloud certifications (AWS/Azure/GCP) - highly valued in the current market')
        if not has_ai:
            recommendations.append('🤖 AI/ML certifications are in high demand - consider adding them to your portfolio')
        
        # Check for expired certificates
        if any('expired' in w.lower() for w in analysis['warnings']):
            recommendations.append('🔄 Renew expired certifications or replace them with current ones')
        
        # Provider diversity
        if len(analysis['providers']) < 2:
            recommendations.append('🏢 Earn certifications from multiple providers for broader recognition')
        
        return recommendations
    
    def get_certificate_value_score(self, certificates: List[Dict[str, Any]]) -> float:
        """
        Calculate overall certificate portfolio value score (0-100)
        
        Args:
            certificates: List of certificates
        
        Returns:
            Score from 0-100
        """
        if not certificates:
            return 0
        
        analysis = self.analyze_certificates(certificates)
        
        # Scoring components
        quantity_score = min(len(certificates) * 5, 30)  # Max 30 points for quantity
        quality_score = (analysis['trust_score_avg'] / 100) * 40  # Max 40 points for quality
        diversity_score = min(len(analysis['categories']) * 5, 20)  # Max 20 points for diversity
        recency_score = 10  # Base score, could be enhanced with date analysis
        
        total_score = quantity_score + quality_score + diversity_score + recency_score
        
        return min(total_score, 100)


# Streamlit cached function
@st.cache_data(ttl=3600)
def analyze_certificates(certificates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Cached certificate analysis"""
    validator = CertificateValidator()
    return validator.analyze_certificates(certificates)


@st.cache_data(ttl=3600)
def get_certificate_value_score(certificates: List[Dict[str, Any]]) -> float:
    """Cached certificate value score calculation"""
    validator = CertificateValidator()
    return validator.get_certificate_value_score(certificates)

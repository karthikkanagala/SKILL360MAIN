"""
Certificate Analyzer Module
Provides certificate verification, text analysis, and GitHub scanning functionality
"""
import re
from typing import Dict, Any, List, Optional


class CertificateAnalyzer:
    """Analyzes certificates for authenticity and skill extraction"""
    
    TRUSTED_PLATFORMS = {
        'coursera': {
            'name': 'Coursera',
            'category': 'MOOC',
            'trust_score': 0.85,
            'url_patterns': [r'coursera\.org/verify', r'coursera\.org/account/accomplishments'],
            'cert_id_pattern': r'[A-Z0-9]{10,}'
        },
        'udemy': {
            'name': 'Udemy',
            'category': 'MOOC',
            'trust_score': 0.75,
            'url_patterns': [r'udemy\.com/certificate', r'ude\.my/'],
            'cert_id_pattern': r'UC-[A-Z0-9-]+'
        },
        'linkedin': {
            'name': 'LinkedIn Learning',
            'category': 'Professional',
            'trust_score': 0.80,
            'url_patterns': [r'linkedin\.com/learning/certificates'],
            'cert_id_pattern': r'[A-Za-z0-9]{20,}'
        },
        'aws': {
            'name': 'Amazon Web Services',
            'category': 'Industry',
            'trust_score': 0.95,
            'url_patterns': [r'aws\.amazon\.com/verification', r'credly\.com/badges'],
            'cert_id_pattern': r'[A-Z0-9]{10,}'
        },
        'google': {
            'name': 'Google Cloud',
            'category': 'Industry',
            'trust_score': 0.95,
            'url_patterns': [r'cloud\.google\.com', r'credential\.net'],
            'cert_id_pattern': r'[A-Z0-9]{10,}'
        },
        'microsoft': {
            'name': 'Microsoft',
            'category': 'Industry',
            'trust_score': 0.95,
            'url_patterns': [r'microsoft\.com/learning', r'credly\.com/badges'],
            'cert_id_pattern': r'[A-Z0-9]{10,}'
        },
        'edx': {
            'name': 'edX',
            'category': 'MOOC',
            'trust_score': 0.85,
            'url_patterns': [r'courses\.edx\.org', r'verify\.edx\.org'],
            'cert_id_pattern': r'[a-f0-9]{32}'
        },
        'hackerrank': {
            'name': 'HackerRank',
            'category': 'Professional',
            'trust_score': 0.80,
            'url_patterns': [r'hackerrank\.com/certificates'],
            'cert_id_pattern': r'[A-Z0-9]{10,}'
        },
        'credly': {
            'name': 'Credly',
            'category': 'Professional',
            'trust_score': 0.90,
            'url_patterns': [r'credly\.com/badges'],
            'cert_id_pattern': r'[a-f0-9-]{36}'
        }
    }
    
    CERTIFICATE_SKILLS = {
        'python': ['Python', 'Programming', 'Scripting'],
        'javascript': ['JavaScript', 'Web Development', 'Frontend'],
        'react': ['React', 'Frontend', 'UI Development'],
        'aws': ['AWS', 'Cloud Computing', 'DevOps'],
        'azure': ['Azure', 'Cloud Computing', 'Microsoft'],
        'google cloud': ['GCP', 'Cloud Computing', 'Big Data'],
        'machine learning': ['Machine Learning', 'AI', 'Data Science'],
        'deep learning': ['Deep Learning', 'Neural Networks', 'AI'],
        'data science': ['Data Science', 'Analytics', 'Statistics'],
        'kubernetes': ['Kubernetes', 'Container Orchestration', 'DevOps'],
        'docker': ['Docker', 'Containers', 'DevOps'],
        'sql': ['SQL', 'Databases', 'Data Management'],
        'cybersecurity': ['Cybersecurity', 'Security', 'InfoSec'],
        'blockchain': ['Blockchain', 'Web3', 'Distributed Systems']
    }


def verify_certificate_url(url: str) -> Dict[str, Any]:
    """
    Verify a certificate URL
    
    Args:
        url: Certificate verification URL
        
    Returns:
        Verification result dictionary
    """
    analyzer = CertificateAnalyzer()
    url_lower = url.lower()
    
    platform_found = None
    platform_info = None
    
    for platform_key, info in analyzer.TRUSTED_PLATFORMS.items():
        for pattern in info['url_patterns']:
            if re.search(pattern, url_lower):
                platform_found = platform_key
                platform_info = info
                break
        if platform_found:
            break
    
    if platform_info:
        return {
            'verified': True,
            'platform': platform_info['name'],
            'category': platform_info['category'],
            'trust_score': platform_info['trust_score'],
            'url': url,
            'message': f"Certificate URL verified for {platform_info['name']}"
        }
    else:
        return {
            'verified': False,
            'platform': 'Unknown',
            'category': 'Unknown',
            'trust_score': 0.3,
            'url': url,
            'message': "Could not verify certificate platform"
        }


def analyze_certificate_text(text: str, source: str = 'manual') -> Dict[str, Any]:
    """
    Analyze certificate text for skills and validity
    
    Args:
        text: Certificate text content
        source: Source of the certificate text
        
    Returns:
        Analysis result dictionary
    """
    analyzer = CertificateAnalyzer()
    text_lower = text.lower()
    
    # Extract skills
    skills_found = []
    for keyword, skill_list in analyzer.CERTIFICATE_SKILLS.items():
        if keyword in text_lower:
            for skill in skill_list:
                if skill not in skills_found:
                    skills_found.append(skill)
    
    # Detect platform
    platform_detected = None
    for platform_key, info in analyzer.TRUSTED_PLATFORMS.items():
        if platform_key in text_lower or info['name'].lower() in text_lower:
            platform_detected = info['name']
            break
    
    # Extract URLs
    urls = re.findall(r'https?://[^\s<>"]+', text)
    
    return {
        'success': True,
        'source': source,
        'skills': skills_found,
        'skill_count': len(skills_found),
        'platform': platform_detected or 'Unknown',
        'urls_found': urls,
        'text_length': len(text),
        'analysis_complete': True
    }


def scan_github_certificates(github_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Scan GitHub profile for certificate mentions
    
    Args:
        github_data: GitHub profile data
        
    Returns:
        List of found certificates
    """
    certificates = []
    
    # Check bio
    bio = github_data.get('bio', '') or ''
    
    # Check for certificate URLs in bio
    cert_patterns = [
        r'coursera\.org/verify/[A-Z0-9]+',
        r'credly\.com/badges/[a-f0-9-]+',
        r'credential\.net/[a-f0-9-]+',
        r'hackerrank\.com/certificates/[a-z0-9]+',
        r'udemy\.com/certificate/[A-Z0-9-]+'
    ]
    
    for pattern in cert_patterns:
        matches = re.findall(pattern, bio, re.IGNORECASE)
        for match in matches:
            certificates.append({
                'url': f'https://{match}',
                'source': 'github_bio',
                'verified': False
            })
    
    # Check repository descriptions
    repos = github_data.get('repositories', []) or []
    for repo in repos[:10]:  # Check top 10 repos
        description = repo.get('description', '') or ''
        for pattern in cert_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                certificates.append({
                    'url': f'https://{match}',
                    'source': f'repo:{repo.get("name", "unknown")}',
                    'verified': False
                })
    
    return certificates

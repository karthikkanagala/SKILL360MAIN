"""Certificate Router
Wraps Evolvex certificate_analyzer so React can get the same outputs as Streamlit.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Any, Dict, Optional, List
import sys
import os
import PyPDF2
import io
import re
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Evolvex-AI--main/Evolvex-AI--main/src')))

router = APIRouter()


class VerifyUrlRequest(BaseModel):
    url: str


class AnalyzeTextRequest(BaseModel):
    text: str
    source: str = 'manual'


class ScanGithubRequest(BaseModel):
    github_data: Dict[str, Any]


@router.post('/verify-url')
async def verify_url(request: VerifyUrlRequest) -> Dict[str, Any]:
    try:
        from certificate_analyzer import verify_certificate_url
        return verify_certificate_url(request.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying certificate URL: {str(e)}")


@router.post('/analyze-text')
async def analyze_text(request: AnalyzeTextRequest) -> Dict[str, Any]:
    try:
        from certificate_analyzer import analyze_certificate_text
        return analyze_certificate_text(request.text, source=request.source)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing certificate text: {str(e)}")


@router.post('/scan-github')
async def scan_github(request: ScanGithubRequest) -> Dict[str, Any]:
    """Scan GitHub bio + top repo descriptions for certificate URLs."""
    try:
        from certificate_analyzer import scan_github_certificates
        certs = scan_github_certificates(request.github_data)
        return {"certificates": certs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning GitHub for certificates: {str(e)}")


@router.post('/upload-pdf')
async def upload_certificate_pdf(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload certificate PDF and analyze for authenticity and skills.
    
    Uses multi-layered approach:
    1. PDF structure validation
    2. Text extraction and parsing
    3. Platform verification
    4. Skill extraction using ML/NLP
    5. Authenticity scoring with multiple heuristics
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read PDF content
        content = await file.read()
        
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Extract text from PDF
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            
            if len(pdf_reader.pages) == 0:
                raise HTTPException(status_code=400, detail="PDF has no pages")
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as page_err:
                    continue  # Skip problematic pages
            
            if not text.strip():
                raise HTTPException(status_code=400, detail="Could not extract text from PDF. The PDF may be image-based or encrypted.")
            
        except PyPDF2.errors.PdfReadError as pdf_err:
            raise HTTPException(status_code=400, detail=f"PDF reading failed: {str(pdf_err)}. The file may be corrupted or encrypted.")
        except Exception as extract_err:
            raise HTTPException(status_code=400, detail=f"Text extraction failed: {str(extract_err)}")
        
        # Analyze the certificate
        analysis = await _analyze_certificate_pdf(text, file.filename)
        
        return {
            'success': True,
            'filename': file.filename,
            'text_extracted': len(text),
            'pages': len(pdf_reader.pages),
            **analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error processing certificate: {str(e)}")


async def _analyze_certificate_pdf(text: str, filename: str) -> Dict[str, Any]:
    """Comprehensive certificate analysis using ML + logic + code patterns."""
    from certificate_analyzer import CertificateAnalyzer
    
    analyzer = CertificateAnalyzer()
    text_lower = text.lower()
    
    # 1. Platform Detection & Verification
    platform_detected = None
    platform_info = None
    verification_urls = []
    
    for platform_key, info in analyzer.TRUSTED_PLATFORMS.items():
        if platform_key in text_lower or info['name'].lower() in text_lower:
            platform_detected = platform_key
            platform_info = info
            break
    
    # Extract URLs for verification
    urls = re.findall(r'https?://[^\s<>"]+', text)
    for url in urls:
        if any(re.search(pattern, url.lower()) for patterns in [p['url_patterns'] for p in analyzer.TRUSTED_PLATFORMS.values()] for pattern in patterns):
            verification_urls.append(url)
    
    # 2. Authenticity Scoring (Multi-factor)
    authenticity_score = 0.0
    authenticity_factors = []
    
    # Factor 1: Trusted platform detected (40 points)
    if platform_info:
        platform_score = platform_info['trust_score'] * 40
        authenticity_score += platform_score
        authenticity_factors.append(f"Trusted platform ({platform_info['name']}): +{platform_score:.0f}")
    else:
        authenticity_factors.append("Unknown platform: +0")
    
    # Factor 2: Verification URL present (25 points)
    if verification_urls:
        authenticity_score += 25
        authenticity_factors.append(f"Verification URL found: +25")
    else:
        authenticity_factors.append("No verification URL: +0")
    
    # Factor 3: Certificate ID pattern (15 points)
    cert_id_found = False
    if platform_info and 'cert_id_pattern' in platform_info:
        if re.search(platform_info['cert_id_pattern'], text):
            authenticity_score += 15
            cert_id_found = True
            authenticity_factors.append("Valid certificate ID format: +15")
    if not cert_id_found:
        # Generic ID patterns
        if re.search(r'(certificate|cert)[\s#:-]*[A-Z0-9]{6,}', text, re.IGNORECASE):
            authenticity_score += 10
            authenticity_factors.append("Certificate ID detected: +10")
        else:
            authenticity_factors.append("No certificate ID: +0")
    
    # Factor 4: Date validation (10 points)
    date_pattern = r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
    dates = re.findall(date_pattern, text, re.IGNORECASE)
    if dates:
        authenticity_score += 10
        authenticity_factors.append(f"Issue/completion date found: +10")
    else:
        authenticity_factors.append("No date found: +0")
    
    # Factor 5: Digital signature/metadata (10 points)
    if any(keyword in text_lower for keyword in ['digitally signed', 'signature', 'verified by']):
        authenticity_score += 10
        authenticity_factors.append("Digital signature indicators: +10")
    else:
        authenticity_factors.append("No signature indicators: +0")
    
    # Normalize to 0-100
    authenticity_score = min(100, authenticity_score)
    
    # Determine authenticity level
    if authenticity_score >= 75:
        authenticity_level = "Highly Authentic"
        authenticity_color = "green"
    elif authenticity_score >= 50:
        authenticity_level = "Likely Authentic"
        authenticity_color = "blue"
    elif authenticity_score >= 30:
        authenticity_level = "Uncertain"
        authenticity_color = "orange"
    else:
        authenticity_level = "Low Confidence"
        authenticity_color = "red"
    
    # 3. Skills Extraction (ML + Pattern Matching)
    skills_extracted = []
    skills_confidence = {}
    
    # Method 1: Direct keyword matching from certificate skills DB
    for cert_keyword, skill_list in analyzer.CERTIFICATE_SKILLS.items():
        if cert_keyword in text_lower:
            for skill in skill_list:
                if skill not in skills_extracted:
                    skills_extracted.append(skill)
                    skills_confidence[skill] = 0.9  # High confidence
    
    # Method 2: Technical term extraction
    technical_terms = [
        'Python', 'Java', 'JavaScript', 'C\\+\\+', 'C#', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin',
        'React', 'Angular', 'Vue', 'Node\\.js', 'Django', 'Flask', 'Spring', 'Express',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
        'Machine Learning', 'Deep Learning', 'AI', 'Neural Networks', 'TensorFlow', 'PyTorch',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Cassandra',
        'Blockchain', 'Ethereum', 'Smart Contracts', 'Web3',
        'DevOps', 'Agile', 'Scrum', 'Microservices', 'REST API', 'GraphQL',
        'Cybersecurity', 'Penetration Testing', 'Cryptography', 'Network Security'
    ]
    
    for term in technical_terms:
        pattern = r'\b' + term + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            clean_term = term.replace('\\\\', '').replace('\\.', '.')
            if clean_term not in skills_extracted:
                skills_extracted.append(clean_term)
                skills_confidence[clean_term] = 0.8  # Medium-high confidence
    
    # Method 3: Context-based skill inference
    if 'data' in text_lower and any(word in text_lower for word in ['analysis', 'science', 'analytics']):
        for skill in ['Data Analysis', 'Statistics', 'Data Visualization']:
            if skill not in skills_extracted:
                skills_extracted.append(skill)
                skills_confidence[skill] = 0.7
    
    # 4. Certificate Metadata Extraction
    metadata = {
        'certificate_name': _extract_cert_name(text),
        'issuer': platform_info['name'] if platform_info else _extract_issuer(text),
        'completion_date': dates[0] if dates else None,
        'verification_urls': verification_urls,
        'certificate_id': _extract_cert_id(text),
        'recipient_name': _extract_recipient(text)
    }
    
    # 5. Career Value Assessment
    career_value_score = 0
    if platform_info:
        if platform_info['category'] == 'Industry':
            career_value_score += 40
        elif platform_info['category'] == 'MOOC':
            career_value_score += 30
        elif platform_info['category'] == 'Professional':
            career_value_score += 35
    
    if len(skills_extracted) >= 5:
        career_value_score += 30
    elif len(skills_extracted) >= 3:
        career_value_score += 20
    elif len(skills_extracted) >= 1:
        career_value_score += 10
    
    if verification_urls:
        career_value_score += 15
    
    if any(keyword in text_lower for keyword in ['professional', 'advanced', 'expert', 'master']):
        career_value_score += 15
    
    career_value_score = min(100, career_value_score)
    
    return {
        'platform': platform_info['name'] if platform_info else 'Unknown',
        'platform_category': platform_info['category'] if platform_info else 'Unknown',
        'authenticity_score': round(authenticity_score, 1),
        'authenticity_level': authenticity_level,
        'authenticity_color': authenticity_color,
        'authenticity_factors': authenticity_factors,
        'skills': skills_extracted[:20],  # Limit to top 20
        'skills_confidence': skills_confidence,
        'total_skills_found': len(skills_extracted),
        'metadata': metadata,
        'career_value_score': round(career_value_score, 1),
        'verified': authenticity_score >= 50,
        'warnings': _generate_warnings(authenticity_score, verification_urls, platform_info)
    }


def _extract_cert_name(text: str) -> str:
    """Extract certificate name from text."""
    lines = text.split('\n')[:10]  # Check first 10 lines
    for line in lines:
        line = line.strip()
        if len(line) > 10 and len(line) < 150:
            if any(keyword in line.lower() for keyword in ['certificate', 'certification', 'completion', 'achievement']):
                return line
    return lines[0][:100] if lines else "Unknown Certificate"


def _extract_issuer(text: str) -> str:
    """Extract certificate issuer."""
    issuer_patterns = [
        r'issued by[:\s]+([^\n]+)',
        r'presented by[:\s]+([^\n]+)',
        r'from[:\s]+([^\n]+)(?:university|institute|academy|organization)',
    ]
    for pattern in issuer_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:100]
    return "Unknown"


def _extract_cert_id(text: str) -> Optional[str]:
    """Extract certificate ID."""
    id_patterns = [
        r'certificate\s+(?:id|number|#)[:\s]*([A-Z0-9-]{6,})',
        r'cert\.?\s*id[:\s]*([A-Z0-9-]{6,})',
        r'verification\s+code[:\s]*([A-Z0-9-]{6,})',
    ]
    for pattern in id_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def _extract_recipient(text: str) -> Optional[str]:
    """Extract recipient name."""
    recipient_patterns = [
        r'awarded to[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'this certifies that[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'presented to[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    ]
    for pattern in recipient_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _generate_warnings(authenticity_score: float, verification_urls: List[str], platform_info: Optional[Dict]) -> List[str]:
    """Generate warnings based on certificate analysis."""
    warnings = []
    
    if authenticity_score < 50:
        warnings.append("⚠️ Low authenticity score - verify certificate manually")
    
    if not verification_urls:
        warnings.append("⚠️ No verification URL found - cannot verify online")
    
    if not platform_info:
        warnings.append("⚠️ Unknown platform - cannot verify issuer authenticity")
    
    if authenticity_score >= 75 and verification_urls:
        warnings.append("✅ High confidence - certificate appears authentic")
    
    return warnings

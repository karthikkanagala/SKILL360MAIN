"""
Python 3.14 Compatible NER Skill Extractor
Uses alternative NLP approaches without spaCy dependency
"""
import re
import streamlit as st
from skills import COMMON_SKILLS

@st.cache_data
def create_skill_patterns():
    """Create regex patterns for better skill matching"""
    patterns = {}
    for skill in COMMON_SKILLS:
        # Create word boundary patterns for whole word matching
        escaped_skill = re.escape(skill)
        # Match whole words, case-insensitive
        pattern = re.compile(r'\b' + escaped_skill + r'\b', re.IGNORECASE)
        patterns[skill] = pattern
    return patterns

def extract_skills_ner_py314(text):
    """
    Enhanced skill extraction without spaCy
    Uses regex patterns with word boundaries for more accurate matching
    """
    try:
        patterns = create_skill_patterns()
        skills_found = set()
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        for skill, pattern in patterns.items():
            if pattern.search(text_lower):
                skills_found.add(skill)
        
        # Additional context-aware matching
        # Look for common patterns like "experienced in X", "proficient in X", "knowledge of X"
        context_patterns = [
            r'(?:experience(?:d)?|proficient|skilled|knowledge|expertise|familiar)\s+(?:in|with|of)\s+([a-zA-Z0-9\+\#\.\-\s]+)',
            r'(?:using|worked with|developed with|built with|implemented)\s+([a-zA-Z0-9\+\#\.\-\s]+)',
        ]
        
        for pattern in context_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                extracted_text = match.group(1).strip()
                # Check if any skill is in the extracted text
                for skill in COMMON_SKILLS:
                    if skill.lower() in extracted_text:
                        skills_found.add(skill)
        
        return sorted(list(skills_found))
        
    except Exception as e:
        raise RuntimeError(f"Enhanced skill extraction failed: {str(e)}")

# Main function that tries different approaches
def extract_skills_ner(text):
    """
    Main NER extraction function with fallback support
    Tries spaCy first, falls back to enhanced regex-based extraction
    """
    # Try spaCy if available (Python < 3.14)
    try:
        import spacy
        from spacy.matcher import PhraseMatcher
        
        @st.cache_resource
        def load_nlp():
            try:
                return spacy.load("en_core_web_sm")
            except:
                return None
        
        nlp = load_nlp()
        if nlp is not None:
            doc = nlp(text)
            matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
            patterns = [nlp.make_doc(skill) for skill in COMMON_SKILLS]
            matcher.add("SKILLS", patterns)
            matches = matcher(doc)
            skills_found = list(set([doc[start:end].text for match_id, start, end in matches]))
            return skills_found
    except Exception:
        pass  # Fall through to alternative method
    
    # Use Python 3.14 compatible method
    return extract_skills_ner_py314(text)

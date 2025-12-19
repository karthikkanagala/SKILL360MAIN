"""
GitHub Analysis & Portfolio Router - Enhanced with Gemini AI
Provides comprehensive project portfolio analysis, not just counts
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Evolvex-AI-Carrier-Path-main/src')))

try:
    from github_analyzer import analyze_github_profile, GitHubAnalyzer
except ImportError as e:
    print(f"Warning: Could not import github_analyzer: {e}")

# Import Gemini
try:
    from database import GoogleAPI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

router = APIRouter()


class GitHubAnalysisRequest(BaseModel):
    username: str


class PortfolioAnalysisRequest(BaseModel):
    username: str
    target_role: Optional[str] = "Software Developer"


# ==================== Portfolio Analysis Functions ====================

def analyze_repo_quality(repo: Dict) -> Dict:
    """Analyze individual repository quality"""
    score = 0
    factors = []
    
    # Has description (10 points)
    if repo.get('description') and len(repo.get('description', '')) > 20:
        score += 10
        factors.append("Good description")
    elif repo.get('description'):
        score += 5
        factors.append("Has description")
    else:
        factors.append("Missing description")
    
    # Has stars (15 points max)
    stars = repo.get('stargazers_count', 0)
    if stars >= 10:
        score += 15
        factors.append(f"Popular ({stars} stars)")
    elif stars >= 5:
        score += 10
        factors.append(f"{stars} stars")
    elif stars > 0:
        score += 5
        factors.append(f"{stars} star(s)")
    
    # Has forks (10 points max)
    forks = repo.get('forks_count', 0)
    if forks >= 5:
        score += 10
        factors.append(f"Forked {forks} times")
    elif forks > 0:
        score += 5
        factors.append(f"{forks} fork(s)")
    
    # Has language (5 points)
    if repo.get('language'):
        score += 5
        factors.append(f"Built with {repo.get('language')}")
    
    # Is not a fork (10 points)
    if not repo.get('fork', False):
        score += 10
        factors.append("Original work")
    else:
        factors.append("Forked repository")
    
    # Has homepage/demo (10 points)
    if repo.get('homepage') and len(repo.get('homepage', '')) > 5:
        score += 10
        factors.append("Has live demo")
    
    # Repo size indicates substantial work (10 points)
    size = repo.get('size', 0)
    if size > 1000:
        score += 10
        factors.append("Substantial codebase")
    elif size > 100:
        score += 5
        factors.append("Moderate codebase")
    
    # Topics/tags (10 points)
    topics = repo.get('topics', [])
    if len(topics) >= 3:
        score += 10
        factors.append(f"Well-tagged ({len(topics)} topics)")
    elif len(topics) > 0:
        score += 5
        factors.append(f"{len(topics)} topic(s)")
    
    # Determine quality tier
    if score >= 60:
        tier = "Excellent"
    elif score >= 40:
        tier = "Good"
    elif score >= 25:
        tier = "Average"
    else:
        tier = "Basic"
    
    return {
        "name": repo.get('name', ''),
        "quality_score": min(100, score),
        "tier": tier,
        "factors": factors,
        "language": repo.get('language'),
        "description": repo.get('description', 'No description'),
        "stars": stars,
        "forks": forks,
        "has_demo": bool(repo.get('homepage')),
        "url": repo.get('html_url', '')
    }


def analyze_tech_diversity(repos: List[Dict]) -> Dict:
    """Analyze technology diversity in portfolio"""
    languages = {}
    frameworks_detected = set()
    
    # Common framework indicators in repo names/descriptions
    framework_keywords = {
        'react': 'React', 'angular': 'Angular', 'vue': 'Vue.js',
        'django': 'Django', 'flask': 'Flask', 'fastapi': 'FastAPI',
        'express': 'Express.js', 'nextjs': 'Next.js', 'next.js': 'Next.js',
        'node': 'Node.js', 'spring': 'Spring', 'laravel': 'Laravel',
        'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch', 'keras': 'Keras',
        'docker': 'Docker', 'kubernetes': 'Kubernetes', 'aws': 'AWS',
        'mongodb': 'MongoDB', 'postgres': 'PostgreSQL', 'mysql': 'MySQL',
        'graphql': 'GraphQL', 'rest-api': 'REST API', 'api': 'API Development',
        'machine-learning': 'Machine Learning', 'ml': 'Machine Learning',
        'data-science': 'Data Science', 'deep-learning': 'Deep Learning',
        'flutter': 'Flutter', 'react-native': 'React Native',
    }
    
    for repo in repos:
        # Count languages
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        
        # Detect frameworks from name, description, topics
        text = ' '.join([
            repo.get('name', ''),
            repo.get('description', ''),
            ' '.join(repo.get('topics', []))
        ]).lower()
        
        for keyword, framework in framework_keywords.items():
            if keyword in text:
                frameworks_detected.add(framework)
    
    # Calculate diversity score
    lang_count = len(languages)
    framework_count = len(frameworks_detected)
    
    if lang_count >= 5 and framework_count >= 4:
        diversity_tier = "Excellent"
        diversity_score = 100
    elif lang_count >= 3 and framework_count >= 2:
        diversity_tier = "Good"
        diversity_score = 75
    elif lang_count >= 2:
        diversity_tier = "Moderate"
        diversity_score = 50
    else:
        diversity_tier = "Limited"
        diversity_score = 25
    
    return {
        "languages": languages,
        "primary_language": max(languages, key=languages.get) if languages else "None",
        "language_count": lang_count,
        "frameworks_detected": list(frameworks_detected),
        "framework_count": framework_count,
        "diversity_score": diversity_score,
        "diversity_tier": diversity_tier
    }


def analyze_project_types(repos: List[Dict]) -> Dict:
    """Categorize projects by type"""
    categories = {
        "Web Applications": [],
        "API/Backend": [],
        "Mobile Apps": [],
        "Machine Learning/AI": [],
        "CLI Tools": [],
        "Libraries/Packages": [],
        "Data Projects": [],
        "DevOps/Infrastructure": [],
        "Other": []
    }
    
    type_keywords = {
        "Web Applications": ['website', 'webapp', 'web-app', 'frontend', 'landing', 'portfolio', 'dashboard', 'admin'],
        "API/Backend": ['api', 'backend', 'server', 'service', 'rest', 'graphql', 'microservice'],
        "Mobile Apps": ['android', 'ios', 'mobile', 'flutter', 'react-native', 'app'],
        "Machine Learning/AI": ['ml', 'machine-learning', 'ai', 'deep-learning', 'neural', 'tensorflow', 'pytorch', 'model', 'predict'],
        "CLI Tools": ['cli', 'command-line', 'terminal', 'tool', 'script'],
        "Libraries/Packages": ['library', 'package', 'npm', 'pip', 'sdk', 'module'],
        "Data Projects": ['data', 'analytics', 'visualization', 'etl', 'pipeline', 'scraper'],
        "DevOps/Infrastructure": ['docker', 'kubernetes', 'terraform', 'ansible', 'devops', 'deploy', 'ci-cd'],
    }
    
    for repo in repos:
        text = ' '.join([
            repo.get('name', ''),
            repo.get('description', ''),
            ' '.join(repo.get('topics', []))
        ]).lower()
        
        categorized = False
        for category, keywords in type_keywords.items():
            if any(kw in text for kw in keywords):
                categories[category].append(repo.get('name'))
                categorized = True
                break
        
        if not categorized:
            categories["Other"].append(repo.get('name'))
    
    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}
    
    return {
        "categories": categories,
        "primary_focus": max(categories, key=lambda k: len(categories[k])) if categories else "Mixed",
        "category_count": len(categories)
    }


async def get_ai_portfolio_review(repos: List[Dict], username: str, target_role: str) -> Dict:
    """Get AI-powered portfolio review"""
    if not GEMINI_AVAILABLE:
        return None
    
    try:
        # Prepare repo summaries
        repo_summaries = []
        for repo in repos[:10]:
            summary = f"- {repo.get('name')}: {repo.get('description', 'No description')} ({repo.get('language', 'Unknown')} | {repo.get('stargazers_count', 0)} stars)"
            repo_summaries.append(summary)
        
        prompt = f"""Analyze this GitHub portfolio for a {target_role} position:

USERNAME: {username}
REPOSITORIES:
{chr(10).join(repo_summaries)}

Provide comprehensive portfolio analysis:

1. PORTFOLIO STRENGTHS (What stands out positively)
2. PORTFOLIO GAPS (What's missing for {target_role} role)
3. PROJECT RECOMMENDATIONS (What to build next)
4. IMPROVEMENT SUGGESTIONS (How to enhance existing projects)
5. PRESENTATION TIPS (How to showcase better)
6. OVERALL ASSESSMENT (Ready for {target_role}? / 10)

Be specific and actionable. Consider what recruiters look for."""

        response = GoogleAPI.generate_content(prompt)
        
        return {
            "ai_review": response,
            "ai_powered": True
        }
    except Exception as e:
        print(f"AI review failed: {e}")
        return None


# ==================== API Endpoints ====================

@router.post("/analyze")
async def analyze_github(request: GitHubAnalysisRequest):
    """Analyze GitHub profile and repositories"""
    try:
        analysis = analyze_github_profile(request.username)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing GitHub profile: {str(e)}")


@router.post("/portfolio")
async def analyze_portfolio_deep(request: PortfolioAnalysisRequest):
    """
    Deep portfolio analysis - not just counts, but quality and depth
    """
    try:
        # Get GitHub data
        analyzer = GitHubAnalyzer()
        profile = analyzer.get_user_profile(request.username)
        
        if profile and 'error' in profile:
            raise HTTPException(status_code=404, detail=profile.get('message', 'User not found'))
        
        repos = analyzer.get_user_repos(request.username)
        
        if not repos:
            raise HTTPException(status_code=404, detail="No repositories found")
        
        # Filter out forks for quality analysis
        original_repos = [r for r in repos if not r.get('fork', False)]
        
        # Analyze each repo quality
        repo_analyses = [analyze_repo_quality(repo) for repo in original_repos[:20]]
        
        # Sort by quality score
        repo_analyses.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # Calculate overall portfolio score
        if repo_analyses:
            avg_quality = sum(r['quality_score'] for r in repo_analyses) / len(repo_analyses)
            top_projects = [r for r in repo_analyses if r['tier'] in ['Excellent', 'Good']]
        else:
            avg_quality = 0
            top_projects = []
        
        # Analyze tech diversity
        tech_diversity = analyze_tech_diversity(original_repos)
        
        # Analyze project types
        project_types = analyze_project_types(original_repos)
        
        # Calculate portfolio strength
        portfolio_strength = min(100, int(
            avg_quality * 0.4 +
            tech_diversity['diversity_score'] * 0.3 +
            min(100, len(top_projects) * 15) * 0.3
        ))
        
        # Determine tier
        if portfolio_strength >= 80:
            tier = "Outstanding"
        elif portfolio_strength >= 60:
            tier = "Strong"
        elif portfolio_strength >= 40:
            tier = "Developing"
        else:
            tier = "Beginner"
        
        # Get AI review
        ai_review = await get_ai_portfolio_review(repos, request.username, request.target_role)
        
        result = {
            "username": request.username,
            "target_role": request.target_role,
            "portfolio_summary": {
                "total_repos": len(repos),
                "original_projects": len(original_repos),
                "forked_repos": len(repos) - len(original_repos),
                "portfolio_strength": portfolio_strength,
                "tier": tier,
                "average_project_quality": round(avg_quality, 1)
            },
            "best_projects": repo_analyses[:5],
            "projects_needing_improvement": [r for r in repo_analyses if r['tier'] in ['Basic', 'Average']][:3],
            "tech_diversity": tech_diversity,
            "project_categories": project_types,
            "recommendations": generate_portfolio_recommendations(
                portfolio_strength, tech_diversity, project_types, request.target_role
            )
        }
        
        if ai_review:
            result["ai_review"] = ai_review.get("ai_review")
            result["ai_powered"] = True
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing portfolio: {str(e)}")


def generate_portfolio_recommendations(strength: int, diversity: Dict, types: Dict, target_role: str) -> List[str]:
    """Generate specific portfolio recommendations"""
    recommendations = []
    
    if strength < 60:
        recommendations.append("Add detailed README files to all projects with screenshots and setup instructions")
    
    if diversity['diversity_score'] < 50:
        recommendations.append(f"Diversify your tech stack - currently focused on {diversity['primary_language']}")
    
    if diversity['framework_count'] < 2:
        recommendations.append("Build projects with popular frameworks like React, Django, or Spring Boot")
    
    if "Web Applications" not in types.get('categories', {}) and "Software" in target_role:
        recommendations.append("Add full-stack web application projects to showcase end-to-end development")
    
    if "API/Backend" not in types.get('categories', {}):
        recommendations.append("Create REST API or microservice projects to demonstrate backend skills")
    
    if "Machine Learning" in target_role and "Machine Learning/AI" not in types.get('categories', {}):
        recommendations.append("Add ML/AI projects with Jupyter notebooks and trained models")
    
    if not recommendations:
        recommendations.append("Consider contributing to open-source projects to increase visibility")
        recommendations.append("Add CI/CD pipelines and deployment links to showcase DevOps knowledge")
    
    return recommendations


@router.get("/portfolio/tips")
async def get_portfolio_tips():
    """Get tips for improving GitHub portfolio"""
    return {
        "tips": [
            {
                "category": "Project Quality",
                "tips": [
                    "Write detailed README files with project description, screenshots, and setup instructions",
                    "Add a live demo link (use Vercel, Netlify, or GitHub Pages)",
                    "Include proper documentation and comments in code",
                    "Add meaningful topics/tags to each repository"
                ]
            },
            {
                "category": "Tech Diversity",
                "tips": [
                    "Build projects in different programming languages",
                    "Use popular frameworks (React, Django, Spring Boot)",
                    "Include both frontend and backend projects",
                    "Add DevOps/Cloud projects (Docker, Kubernetes, AWS)"
                ]
            },
            {
                "category": "Visibility",
                "tips": [
                    "Pin your best 6 repositories",
                    "Use consistent naming conventions",
                    "Add project screenshots and GIFs",
                    "Enable GitHub Pages for documentation"
                ]
            },
            {
                "category": "Contribution Quality",
                "tips": [
                    "Contribute to open-source projects",
                    "Write meaningful commit messages",
                    "Create pull requests with proper descriptions",
                    "Respond to issues on your repositories"
                ]
            }
        ]
    }

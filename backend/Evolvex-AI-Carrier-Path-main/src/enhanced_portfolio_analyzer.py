"""
Enhanced Portfolio Analyzer
Comprehensive portfolio analysis integrating projects, GitHub, certifications, and extracurricular activities
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
import streamlit as st
from datetime import datetime


class EnhancedPortfolioAnalyzer:
    """Enhanced portfolio analyzer with multi-dimensional evaluation"""
    
    PORTFOLIO_DIMENSIONS = {
        'Technical Depth': {
            'weight': 0.25,
            'components': ['projects', 'github', 'certifications'],
            'description': 'Technical skills and project complexity'
        },
        'Breadth & Diversity': {
            'weight': 0.20,
            'components': ['skills', 'languages', 'domains'],
            'description': 'Range of technologies and domains'
        },
        'Impact & Quality': {
            'weight': 0.20,
            'components': ['stars', 'forks', 'achievements'],
            'description': 'Project impact and code quality'
        },
        'Professional Growth': {
            'weight': 0.15,
            'components': ['certifications', 'learning', 'contributions'],
            'description': 'Continuous learning and development'
        },
        'Leadership & Collaboration': {
            'weight': 0.10,
            'components': ['extracurricular', 'team_projects', 'mentoring'],
            'description': 'Leadership roles and teamwork'
        },
        'Industry Readiness': {
            'weight': 0.10,
            'components': ['internships', 'freelancing', 'real_world_projects'],
            'description': 'Practical industry experience'
        }
    }
    
    PROJECT_QUALITY_CRITERIA = {
        'Documentation': {
            'weight': 0.20,
            'indicators': ['readme', 'wiki', 'docs', 'comments']
        },
        'Completeness': {
            'weight': 0.25,
            'indicators': ['demo', 'tests', 'ci/cd', 'deployment']
        },
        'Innovation': {
            'weight': 0.20,
            'indicators': ['unique', 'novel', 'creative', 'innovative']
        },
        'Complexity': {
            'weight': 0.20,
            'indicators': ['architecture', 'scalable', 'distributed', 'advanced']
        },
        'Community Impact': {
            'weight': 0.15,
            'indicators': ['stars', 'forks', 'contributors', 'issues']
        }
    }
    
    def __init__(self):
        """Initialize enhanced portfolio analyzer"""
        pass
    
    def analyze_comprehensive_portfolio(
        self,
        projects: List[Dict[str, Any]],
        github_data: Optional[Dict[str, Any]] = None,
        certifications: Optional[List[Dict[str, Any]]] = None,
        extracurricular: Optional[List[Dict[str, Any]]] = None,
        learning_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive portfolio analysis across all dimensions
        
        Args:
            projects: List of projects
            github_data: GitHub profile data
            certifications: List of certifications
            extracurricular: List of extracurricular activities
            learning_data: Learning progress data
        
        Returns:
            Comprehensive portfolio analysis
        """
        analysis = {
            'overall_score': 0,
            'dimension_scores': {},
            'project_analysis': {},
            'strengths': [],
            'areas_for_improvement': [],
            'recommendations': [],
            'portfolio_tier': '',
            'competitive_edge': [],
            'missing_elements': [],
            'standout_projects': [],
            'skill_demonstration': {},
            'industry_alignment': {}
        }
        
        # Analyze each dimension
        analysis['dimension_scores']['Technical Depth'] = self._analyze_technical_depth(
            projects, github_data, certifications
        )
        
        analysis['dimension_scores']['Breadth & Diversity'] = self._analyze_breadth_diversity(
            projects, github_data
        )
        
        analysis['dimension_scores']['Impact & Quality'] = self._analyze_impact_quality(
            projects, github_data
        )
        
        analysis['dimension_scores']['Professional Growth'] = self._analyze_professional_growth(
            certifications, learning_data
        )
        
        analysis['dimension_scores']['Leadership & Collaboration'] = self._analyze_leadership(
            extracurricular, projects
        )
        
        analysis['dimension_scores']['Industry Readiness'] = self._analyze_industry_readiness(
            projects, extracurricular
        )
        
        # Calculate overall score
        total_score = 0
        for dimension, score_data in analysis['dimension_scores'].items():
            weight = self.PORTFOLIO_DIMENSIONS[dimension]['weight']
            total_score += score_data['score'] * weight
        
        analysis['overall_score'] = round(total_score, 1)
        
        # Analyze individual projects
        analysis['project_analysis'] = self._analyze_projects_detailed(projects)
        
        # Identify standout projects
        analysis['standout_projects'] = self._identify_standout_projects(
            analysis['project_analysis']
        )
        
        # Analyze skill demonstration
        analysis['skill_demonstration'] = self._analyze_skill_demonstration(
            projects, certifications, extracurricular
        )
        
        # Determine portfolio tier
        analysis['portfolio_tier'] = self._determine_portfolio_tier(analysis['overall_score'])
        
        # Identify strengths and weaknesses
        analysis['strengths'] = self._identify_portfolio_strengths(analysis)
        analysis['areas_for_improvement'] = self._identify_improvement_areas(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_portfolio_recommendations(analysis)
        
        # Identify competitive edges
        analysis['competitive_edge'] = self._identify_competitive_edges(analysis)
        
        # Identify missing elements
        analysis['missing_elements'] = self._identify_missing_elements(analysis)
        
        # Industry alignment
        analysis['industry_alignment'] = self._analyze_industry_alignment(projects, certifications)
        
        return analysis
    
    def _analyze_technical_depth(
        self,
        projects: List[Dict[str, Any]],
        github_data: Optional[Dict[str, Any]],
        certifications: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Analyze technical depth"""
        score = 0
        details = []
        
        # Project complexity (40%)
        if projects:
            complex_projects = sum(1 for p in projects 
                                  if any(kw in str(p.get('description', '')).lower() 
                                        for kw in ['architecture', 'scalable', 'distributed', 'advanced']))
            complexity_score = min(complex_projects / max(len(projects), 1), 1) * 40
            score += complexity_score
            details.append(f"{complex_projects} complex projects")
        
        # GitHub activity (30%)
        if github_data:
            repos = github_data.get('stats', {}).get('public_repos', 0)
            github_score = min(repos / 20, 1) * 30
            score += github_score
            details.append(f"{repos} GitHub repositories")
        
        # Technical certifications (30%)
        if certifications:
            tech_certs = sum(1 for c in certifications 
                           if any(kw in c.get('name', '').lower() 
                                 for kw in ['programming', 'developer', 'engineer', 'architect']))
            cert_score = min(tech_certs / 5, 1) * 30
            score += cert_score
            details.append(f"{tech_certs} technical certifications")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_breadth_diversity(
        self,
        projects: List[Dict[str, Any]],
        github_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze breadth and diversity"""
        score = 0
        details = []
        
        # Language diversity (50%)
        languages = set()
        if projects:
            for project in projects:
                if project.get('language'):
                    languages.add(project['language'])
        
        if github_data and 'languages' in github_data:
            languages.update(github_data['languages'].keys())
        
        language_score = min(len(languages) / 6, 1) * 50
        score += language_score
        details.append(f"{len(languages)} programming languages")
        
        # Domain diversity (50%)
        domains = set()
        domain_keywords = {
            'Web': ['web', 'frontend', 'backend', 'fullstack'],
            'Mobile': ['android', 'ios', 'mobile', 'app'],
            'Data': ['data', 'analytics', 'ml', 'ai'],
            'Cloud': ['cloud', 'aws', 'azure', 'devops'],
            'Security': ['security', 'encryption', 'auth']
        }
        
        for project in projects:
            desc = str(project.get('description', '')).lower()
            for domain, keywords in domain_keywords.items():
                if any(kw in desc for kw in keywords):
                    domains.add(domain)
        
        domain_score = min(len(domains) / 4, 1) * 50
        score += domain_score
        details.append(f"{len(domains)} technical domains")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_impact_quality(
        self,
        projects: List[Dict[str, Any]],
        github_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze impact and quality"""
        score = 0
        details = []
        
        # GitHub stars (40%)
        total_stars = 0
        if github_data:
            total_stars = github_data.get('stats', {}).get('total_stars', 0)
        elif projects:
            total_stars = sum(p.get('stars', 0) for p in projects)
        
        star_score = min(total_stars / 100, 1) * 40
        score += star_score
        details.append(f"{total_stars} total stars")
        
        # Project quality indicators (40%)
        quality_count = 0
        if projects:
            for project in projects:
                desc = str(project.get('description', '')).lower()
                has_demo = project.get('demo_url') or 'demo' in desc
                has_docs = 'documentation' in desc or 'readme' in desc
                has_tests = 'test' in desc
                
                if has_demo or has_docs or has_tests:
                    quality_count += 1
        
        quality_score = min(quality_count / max(len(projects), 1), 1) * 40 if projects else 0
        score += quality_score
        details.append(f"{quality_count} high-quality projects")
        
        # Community engagement (20%)
        forks = 0
        if github_data:
            forks = github_data.get('stats', {}).get('total_forks', 0)
        
        engagement_score = min(forks / 50, 1) * 20
        score += engagement_score
        details.append(f"{forks} total forks")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_professional_growth(
        self,
        certifications: Optional[List[Dict[str, Any]]],
        learning_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze professional growth"""
        score = 0
        details = []
        
        # Certifications (60%)
        if certifications:
            cert_count = len(certifications)
            cert_score = min(cert_count / 8, 1) * 60
            score += cert_score
            details.append(f"{cert_count} certifications")
        
        # Learning activity (40%)
        if learning_data:
            completed = learning_data.get('courses_completed', 0)
            learning_score = min(completed / 10, 1) * 40
            score += learning_score
            details.append(f"{completed} courses completed")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_leadership(
        self,
        extracurricular: Optional[List[Dict[str, Any]]],
        projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze leadership and collaboration"""
        score = 0
        details = []
        
        # Extracurricular leadership (60%)
        if extracurricular:
            leadership_keywords = ['president', 'lead', 'founder', 'organizer', 'captain', 'head']
            leadership_count = sum(1 for activity in extracurricular 
                                  if any(kw in activity.get('role', '').lower() 
                                        for kw in leadership_keywords))
            
            leadership_score = min(leadership_count / max(len(extracurricular), 1), 1) * 60
            score += leadership_score
            details.append(f"{leadership_count} leadership roles")
        
        # Team projects (40%)
        team_projects = sum(1 for p in projects 
                          if any(kw in str(p.get('description', '')).lower() 
                                for kw in ['team', 'collaboration', 'group']))
        
        team_score = min(team_projects / max(len(projects), 1), 1) * 40 if projects else 0
        score += team_score
        details.append(f"{team_projects} team projects")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_industry_readiness(
        self,
        projects: List[Dict[str, Any]],
        extracurricular: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Analyze industry readiness"""
        score = 0
        details = []
        
        # Real-world projects (50%)
        real_world_keywords = ['production', 'deployed', 'live', 'client', 'commercial']
        real_world_count = sum(1 for p in projects 
                              if any(kw in str(p.get('description', '')).lower() 
                                    for kw in real_world_keywords))
        
        real_world_score = min(real_world_count / max(len(projects), 1), 1) * 50 if projects else 0
        score += real_world_score
        details.append(f"{real_world_count} real-world projects")
        
        # Internships/Freelancing (50%)
        if extracurricular:
            work_exp = sum(1 for activity in extracurricular 
                          if activity.get('type') in ['Freelancing', 'Internship', 'Work'])
            
            work_score = min(work_exp / 3, 1) * 50
            score += work_score
            details.append(f"{work_exp} work experiences")
        
        return {
            'score': min(score, 100),
            'details': details,
            'rating': self._get_dimension_rating(score)
        }
    
    def _analyze_projects_detailed(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detailed analysis of individual projects"""
        project_scores = []
        
        for project in projects:
            score = self._calculate_project_quality_score(project)
            project_scores.append({
                'name': project.get('name', 'Unknown'),
                'score': score,
                'language': project.get('language', 'Unknown'),
                'stars': project.get('stars', 0),
                'description': project.get('description', '')[:100]
            })
        
        # Sort by score
        project_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'total_projects': len(projects),
            'average_quality': sum(p['score'] for p in project_scores) / len(project_scores) if project_scores else 0,
            'top_projects': project_scores[:5],
            'all_projects': project_scores
        }
    
    def _calculate_project_quality_score(self, project: Dict[str, Any]) -> float:
        """Calculate quality score for a single project"""
        score = 0
        
        # Has description (20%)
        if project.get('description'):
            score += 20
        
        # Has stars (20%)
        stars = project.get('stars', 0)
        score += min(stars * 2, 20)
        
        # Has demo/deployment (20%)
        if project.get('demo_url') or 'deployed' in str(project.get('description', '')).lower():
            score += 20
        
        # Complexity indicators (20%)
        desc = str(project.get('description', '')).lower()
        complexity_keywords = ['architecture', 'scalable', 'distributed', 'advanced', 'complex']
        if any(kw in desc for kw in complexity_keywords):
            score += 20
        
        # Recent activity (20%)
        if project.get('updated'):
            try:
                updated = datetime.fromisoformat(project['updated'].replace('Z', '+00:00'))
                days_old = (datetime.now(updated.tzinfo) - updated).days
                if days_old < 180:  # Updated in last 6 months
                    score += 20
                elif days_old < 365:  # Updated in last year
                    score += 10
            except:
                pass
        
        return min(score, 100)
    
    def _identify_standout_projects(self, project_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify standout projects"""
        all_projects = project_analysis.get('all_projects', [])
        
        # Projects with score >= 70
        standout = [p for p in all_projects if p['score'] >= 70]
        
        return standout[:5]  # Top 5 standout projects
    
    def _analyze_skill_demonstration(
        self,
        projects: List[Dict[str, Any]],
        certifications: Optional[List[Dict[str, Any]]],
        extracurricular: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, List[str]]:
        """Analyze how skills are demonstrated"""
        skill_demo = defaultdict(list)
        
        # From projects
        for project in projects:
            lang = project.get('language')
            name = project.get('name', 'Project')
            if lang:
                skill_demo[lang].append(f"Project: {name}")
        
        # From certifications
        if certifications:
            for cert in certifications:
                cert_name = cert.get('name', '')
                skill_demo['Certifications'].append(cert_name)
        
        # From extracurricular
        if extracurricular:
            for activity in extracurricular:
                activity_type = activity.get('type', 'Activity')
                skill_demo['Extracurricular'].append(activity_type)
        
        return dict(skill_demo)
    
    def _determine_portfolio_tier(self, score: float) -> str:
        """Determine portfolio tier"""
        if score >= 85:
            return '🏆 Elite - Top 5%'
        elif score >= 75:
            return '⭐ Excellent - Top 15%'
        elif score >= 65:
            return '✨ Strong - Top 30%'
        elif score >= 50:
            return '📈 Developing - Top 50%'
        else:
            return '🌱 Building - Keep Growing'
    
    def _identify_portfolio_strengths(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify portfolio strengths"""
        strengths = []
        
        for dimension, score_data in analysis['dimension_scores'].items():
            if score_data['score'] >= 75:
                strengths.append(f"✅ {dimension}: {score_data['rating']}")
        
        return strengths if strengths else ["🌱 Building foundation across all areas"]
    
    def _identify_improvement_areas(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        for dimension, score_data in analysis['dimension_scores'].items():
            if score_data['score'] < 60:
                improvements.append(f"⚠️ {dimension}: {score_data['rating']}")
        
        return improvements if improvements else ["✨ All areas performing well"]
    
    def _generate_portfolio_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate portfolio recommendations"""
        recommendations = []
        
        # Find lowest scoring dimension
        lowest_dim = min(analysis['dimension_scores'].items(), key=lambda x: x[1]['score'])
        recommendations.append(f"🎯 Priority: Improve {lowest_dim[0]} (currently {lowest_dim[1]['score']:.1f}%)")
        
        # Based on overall score
        overall = analysis['overall_score']
        if overall < 50:
            recommendations.append("📚 Focus on building 3-5 quality projects across different domains")
            recommendations.append("🎓 Earn foundational certifications in your target field")
        elif overall < 65:
            recommendations.append("🚀 Add advanced projects showcasing complex problem-solving")
            recommendations.append("🏆 Participate in hackathons or coding competitions")
        elif overall < 80:
            recommendations.append("⭐ Contribute to open source projects to demonstrate collaboration")
            recommendations.append("📈 Take on leadership roles in technical communities")
        else:
            recommendations.append("🌟 Maintain excellence and explore cutting-edge technologies")
            recommendations.append("🎤 Share knowledge through blogs, talks, or mentoring")
        
        return recommendations
    
    def _identify_competitive_edges(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify competitive advantages"""
        edges = []
        
        for dimension, score_data in analysis['dimension_scores'].items():
            if score_data['score'] >= 80:
                edges.append(f"💎 Strong {dimension}")
        
        if len(analysis.get('standout_projects', [])) >= 3:
            edges.append("🌟 Multiple high-quality projects")
        
        return edges if edges else ["🌱 Building competitive advantages"]
    
    def _identify_missing_elements(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify missing portfolio elements"""
        missing = []
        
        if analysis['dimension_scores']['Technical Depth']['score'] < 50:
            missing.append("Complex technical projects")
        
        if analysis['dimension_scores']['Professional Growth']['score'] < 50:
            missing.append("Professional certifications")
        
        if analysis['dimension_scores']['Leadership & Collaboration']['score'] < 50:
            missing.append("Leadership experience")
        
        if analysis['dimension_scores']['Industry Readiness']['score'] < 50:
            missing.append("Real-world project experience")
        
        return missing if missing else ["✅ Portfolio is well-rounded"]
    
    def _analyze_industry_alignment(
        self,
        projects: List[Dict[str, Any]],
        certifications: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Analyze alignment with industry demands"""
        industry_trends = {
            'AI/ML': ['machine learning', 'ai', 'neural', 'deep learning', 'nlp'],
            'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker'],
            'Web3': ['blockchain', 'web3', 'crypto', 'smart contract'],
            'Full Stack': ['fullstack', 'mern', 'mean', 'frontend', 'backend'],
            'Data Science': ['data science', 'analytics', 'visualization', 'pandas']
        }
        
        alignment = defaultdict(int)
        
        for project in projects:
            desc = str(project.get('description', '')).lower()
            for industry, keywords in industry_trends.items():
                if any(kw in desc for kw in keywords):
                    alignment[industry] += 1
        
        if certifications:
            for cert in certifications:
                cert_name = cert.get('name', '').lower()
                for industry, keywords in industry_trends.items():
                    if any(kw in cert_name for kw in keywords):
                        alignment[industry] += 1
        
        return {
            'aligned_industries': dict(alignment),
            'top_alignment': max(alignment.items(), key=lambda x: x[1])[0] if alignment else 'General',
            'alignment_score': min(sum(alignment.values()) * 10, 100)
        }
    
    def _get_dimension_rating(self, score: float) -> str:
        """Get rating for dimension score"""
        if score >= 85:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 55:
            return 'Fair'
        else:
            return 'Needs Improvement'


# Streamlit cached function
@st.cache_data(ttl=3600)
def analyze_enhanced_portfolio(
    projects: List[Dict[str, Any]],
    github_data: Optional[Dict[str, Any]] = None,
    certifications: Optional[List[Dict[str, Any]]] = None,
    extracurricular: Optional[List[Dict[str, Any]]] = None,
    learning_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Cached enhanced portfolio analysis"""
    analyzer = EnhancedPortfolioAnalyzer()
    return analyzer.analyze_comprehensive_portfolio(
        projects, github_data, certifications, extracurricular, learning_data
    )

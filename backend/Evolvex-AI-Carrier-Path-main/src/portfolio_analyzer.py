"""
Portfolio Analyzer
Comprehensive analysis of GitHub project portfolios with quality assessment,
skill demonstration evaluation, and actionable recommendations
"""
import re
from collections import Counter, defaultdict
from datetime import datetime
import streamlit as st

class PortfolioAnalyzer:
    """Analyzes project portfolios for quality, diversity, and skill demonstration"""
    
    # Technology stack categorization
    TECH_CATEGORIES = {
        'Frontend': ['JavaScript', 'TypeScript', 'React', 'Vue', 'Angular', 'HTML', 'CSS', 'SCSS', 'Svelte'],
        'Backend': ['Python', 'Java', 'Go', 'Ruby', 'PHP', 'Node.js', 'C#', 'Rust', 'Kotlin'],
        'Mobile': ['Swift', 'Kotlin', 'Dart', 'React Native', 'Flutter', 'Objective-C'],
        'Data Science/ML': ['Python', 'R', 'Julia', 'MATLAB', 'Jupyter Notebook'],
        'DevOps': ['Shell', 'Docker', 'Kubernetes', 'Terraform', 'Ansible'],
        'Database': ['SQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra'],
        'Systems': ['C', 'C++', 'Rust', 'Assembly', 'Zig']
    }
    
    # Project complexity indicators
    COMPLEXITY_INDICATORS = {
        'high': ['machine learning', 'deep learning', 'distributed system', 'microservices', 
                 'kubernetes', 'blockchain', 'compiler', 'operating system', 'neural network',
                 'cloud architecture', 'scalability', 'real-time processing'],
        'medium': ['api', 'database', 'authentication', 'testing', 'ci/cd', 'deployment',
                   'rest', 'graphql', 'docker', 'web application', 'mobile app'],
        'beginner': ['todo', 'calculator', 'landing page', 'simple', 'basic', 'tutorial',
                     'practice', 'learning', 'clone']
    }
    
    # Quality indicators
    QUALITY_INDICATORS = {
        'readme': ['installation', 'usage', 'example', 'screenshot', 'demo', 'features', 'api', 'documentation'],
        'professional': ['license', 'contributing', 'tests', 'ci', 'badge', 'documentation'],
        'negative': ['fork', 'copy', 'clone', 'homework', 'assignment', 'course']
    }
    
    def __init__(self):
        self.repos_data = []
        self.analysis_results = {}
    
    def analyze_portfolio(self, github_analysis):
        """
        Comprehensive portfolio analysis
        
        Args:
            github_analysis: Output from GitHubAnalyzer.analyze_profile()
            
        Returns:
            dict with comprehensive portfolio evaluation
        """
        if 'error' in github_analysis:
            return github_analysis
        
        repos = github_analysis.get('top_repos', [])
        all_languages = github_analysis.get('languages', {})
        profile = github_analysis.get('profile', {})
        stats = github_analysis.get('statistics', {})
        
        if not repos:
            return {
                'error': 'no_repos',
                'message': 'No repositories available for portfolio analysis'
            }
        
        # Analyze each project
        project_analyses = []
        for repo in repos:
            project_analysis = self._analyze_project(repo)
            project_analyses.append(project_analysis)
        
        # Calculate portfolio metrics
        portfolio_strength = self._calculate_portfolio_strength(
            project_analyses, all_languages, stats
        )
        
        # Categorize projects
        project_categories = self._categorize_projects(project_analyses)
        
        # Identify demonstrated skills
        skill_demonstration = self._analyze_skill_demonstration(
            project_analyses, all_languages
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            project_analyses, skill_demonstration, all_languages, project_categories
        )
        
        # Calculate diversity score
        diversity_score = self._calculate_diversity_score(
            all_languages, project_categories
        )
        
        # Analyze portfolio gaps
        gaps = self._identify_portfolio_gaps(
            project_analyses, all_languages, skill_demonstration
        )
        
        return {
            'portfolio_strength': portfolio_strength,
            'diversity_score': diversity_score,
            'projects': project_analyses,
            'categories': project_categories,
            'skill_demonstration': skill_demonstration,
            'recommendations': recommendations,
            'gaps': gaps,
            'summary': self._generate_summary(
                portfolio_strength, diversity_score, project_analyses, skill_demonstration
            )
        }
    
    def _analyze_project(self, repo):
        """Analyze individual project quality and characteristics"""
        name = repo.get('name', '')
        description = (repo.get('description') or '').lower()
        stars = repo.get('stars', 0)
        forks = repo.get('forks', 0)
        language = repo.get('language', 'Unknown')
        
        # Determine complexity
        complexity = self._determine_complexity(name, description)
        
        # Calculate quality score
        quality_score = self._calculate_project_quality(
            name, description, stars, forks
        )
        
        # Identify project type
        project_type = self._identify_project_type(name, description, stars, forks)
        
        # Extract demonstrated skills
        skills = self._extract_project_skills(description, language)
        
        return {
            'name': name,
            'description': repo.get('description', 'No description'),
            'url': repo.get('url', ''),
            'language': language,
            'stars': stars,
            'forks': forks,
            'complexity': complexity,
            'quality_score': quality_score,
            'project_type': project_type,
            'skills': skills,
            'impact_score': self._calculate_impact_score(stars, forks)
        }
    
    def _determine_complexity(self, name, description):
        """Determine project complexity level"""
        text = f"{name.lower()} {description}".lower()
        
        high_count = sum(1 for indicator in self.COMPLEXITY_INDICATORS['high'] 
                        if indicator in text)
        medium_count = sum(1 for indicator in self.COMPLEXITY_INDICATORS['medium'] 
                          if indicator in text)
        beginner_count = sum(1 for indicator in self.COMPLEXITY_INDICATORS['beginner'] 
                            if indicator in text)
        
        if high_count >= 2 or (high_count >= 1 and medium_count >= 2):
            return 'Advanced'
        elif medium_count >= 2 or (high_count >= 1 and medium_count >= 1):
            return 'Intermediate'
        elif beginner_count >= 1:
            return 'Beginner'
        else:
            return 'Intermediate'  # Default
    
    def _calculate_project_quality(self, name, description, stars, forks):
        """Calculate project quality score (0-100)"""
        score = 0
        
        # Handle None description
        if description is None:
            description = ''
        
        # Description quality (30 points)
        if description:
            desc_length = len(description)
            if desc_length > 100:
                score += 30
            elif desc_length > 50:
                score += 20
            elif desc_length > 20:
                score += 10
        
        # Quality indicators from description (30 points)
        quality_words = sum(1 for word in self.QUALITY_INDICATORS['readme'] 
                           if word in description)
        score += min(30, quality_words * 5)
        
        # Community engagement (25 points)
        if stars > 50:
            score += 15
        elif stars > 10:
            score += 10
        elif stars > 1:
            score += 5
        
        if forks > 20:
            score += 10
        elif forks > 5:
            score += 5
        
        # Name quality (15 points)
        if len(name) > 5 and '-' in name or '_' in name:
            score += 10
        if not any(bad in name.lower() for bad in ['test', 'tmp', 'copy']):
            score += 5
        
        return min(100, score)
    
    def _identify_project_type(self, name, description, stars, forks):
        """Identify project type"""
        text = f"{name.lower()} {description}".lower()
        
        if stars > 100 or forks > 50:
            return 'Popular/Open Source'
        elif any(word in text for word in ['api', 'library', 'framework', 'package']):
            return 'Library/Tool'
        elif any(word in text for word in ['website', 'web app', 'application', 'platform']):
            return 'Web Application'
        elif any(word in text for word in ['mobile', 'android', 'ios', 'flutter']):
            return 'Mobile Application'
        elif any(word in text for word in ['bot', 'automation', 'script']):
            return 'Automation/Bot'
        elif any(word in text for word in ['machine learning', 'ml', 'ai', 'data']):
            return 'ML/Data Science'
        elif forks > stars * 0.5 and forks > 5:
            return 'Collaborative Project'
        else:
            return 'Personal Project'
    
    def _extract_project_skills(self, description, language):
        """Extract skills demonstrated in project"""
        skills = set()
        
        # Add primary language
        if language and language != 'Unknown':
            skills.add(language)
        
        # Common tech terms
        tech_terms = [
            'react', 'vue', 'angular', 'node', 'express', 'django', 'flask',
            'spring', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'mongodb', 'postgresql', 'mysql', 'redis', 'tensorflow', 'pytorch',
            'scikit-learn', 'pandas', 'numpy', 'api', 'rest', 'graphql',
            'typescript', 'javascript', 'python', 'java', 'golang'
        ]
        
        description_lower = (description or '').lower()
        for term in tech_terms:
            if term in description_lower:
                skills.add(term.title())
        
        return list(skills)
    
    def _calculate_impact_score(self, stars, forks):
        """Calculate project impact score"""
        impact = 0
        
        # Stars contribution (0-60)
        if stars > 100:
            impact += 60
        elif stars > 50:
            impact += 45
        elif stars > 20:
            impact += 30
        elif stars > 10:
            impact += 20
        elif stars > 5:
            impact += 10
        elif stars > 0:
            impact += 5
        
        # Forks contribution (0-40)
        if forks > 50:
            impact += 40
        elif forks > 20:
            impact += 30
        elif forks > 10:
            impact += 20
        elif forks > 5:
            impact += 10
        elif forks > 0:
            impact += 5
        
        return min(100, impact)
    
    def _calculate_portfolio_strength(self, projects, languages, stats):
        """Calculate overall portfolio strength (0-100)"""
        if not projects:
            return 0
        
        score = 0
        
        # Project quality average (30 points)
        avg_quality = sum(p['quality_score'] for p in projects) / len(projects)
        score += (avg_quality / 100) * 30
        
        # Complexity distribution (20 points)
        complexity_counts = Counter(p['complexity'] for p in projects)
        if complexity_counts.get('Advanced', 0) >= 2:
            score += 20
        elif complexity_counts.get('Advanced', 0) >= 1:
            score += 15
        elif complexity_counts.get('Intermediate', 0) >= 3:
            score += 12
        else:
            score += 5
        
        # Project impact (20 points)
        avg_impact = sum(p['impact_score'] for p in projects) / len(projects)
        score += (avg_impact / 100) * 20
        
        # Language diversity (15 points)
        language_count = len(languages)
        score += min(15, language_count * 2)
        
        # Repository count (15 points)
        total_repos = stats.get('total_repos', 0)
        if total_repos > 50:
            score += 15
        elif total_repos > 30:
            score += 12
        elif total_repos > 15:
            score += 9
        elif total_repos > 5:
            score += 6
        else:
            score += 3
        
        return min(100, round(score))
    
    def _categorize_projects(self, projects):
        """Categorize projects by type and complexity"""
        categories = {
            'by_complexity': Counter(p['complexity'] for p in projects),
            'by_type': Counter(p['project_type'] for p in projects),
            'high_quality': [p for p in projects if p['quality_score'] >= 70],
            'high_impact': [p for p in projects if p['impact_score'] >= 50]
        }
        
        return categories
    
    def _analyze_skill_demonstration(self, projects, languages):
        """Analyze which skills are demonstrated through projects"""
        demonstrated_skills = defaultdict(list)
        
        # From projects
        for project in projects:
            for skill in project['skills']:
                demonstrated_skills[skill].append(project['name'])
        
        # Add language proficiency levels
        skill_levels = {}
        for skill, project_list in demonstrated_skills.items():
            project_count = len(project_list)
            if project_count >= 3:
                skill_levels[skill] = 'Strong'
            elif project_count >= 2:
                skill_levels[skill] = 'Moderate'
            else:
                skill_levels[skill] = 'Basic'
        
        return {
            'skills': dict(demonstrated_skills),
            'skill_levels': skill_levels,
            'total_skills': len(demonstrated_skills)
        }
    
    def _calculate_diversity_score(self, languages, categories):
        """Calculate portfolio diversity score"""
        score = 0
        
        # Language diversity (40 points)
        language_count = len(languages)
        score += min(40, language_count * 4)
        
        # Tech category diversity (30 points)
        tech_categories_covered = set()
        for lang in languages.keys():
            for category, tech_list in self.TECH_CATEGORIES.items():
                if lang in tech_list:
                    tech_categories_covered.add(category)
        score += min(30, len(tech_categories_covered) * 6)
        
        # Project type diversity (30 points)
        project_type_count = len(categories['by_type'])
        score += min(30, project_type_count * 5)
        
        return min(100, round(score))
    
    def _identify_portfolio_gaps(self, projects, languages, skill_demonstration):
        """Identify gaps in portfolio"""
        gaps = []
        
        # Check for advanced projects
        advanced_count = sum(1 for p in projects if p['complexity'] == 'Advanced')
        if advanced_count == 0:
            gaps.append({
                'type': 'Complexity',
                'issue': 'No advanced-level projects',
                'priority': 'High',
                'suggestion': 'Add projects with advanced algorithms, system design, or ML/AI'
            })
        
        # Check for documentation
        well_documented = sum(1 for p in projects if p['quality_score'] >= 70)
        if well_documented < len(projects) * 0.5:
            gaps.append({
                'type': 'Documentation',
                'issue': 'Many projects lack good documentation',
                'priority': 'High',
                'suggestion': 'Add detailed READMEs with setup instructions, examples, and screenshots'
            })
        
        # Check for community engagement
        popular_projects = sum(1 for p in projects if p['stars'] > 10)
        if popular_projects == 0 and len(projects) > 3:
            gaps.append({
                'type': 'Impact',
                'issue': 'Low community engagement',
                'priority': 'Medium',
                'suggestion': 'Share projects on social media, dev communities, or add unique features'
            })
        
        # Check for tech diversity
        if len(languages) < 3:
            gaps.append({
                'type': 'Diversity',
                'issue': 'Limited technology stack',
                'priority': 'Medium',
                'suggestion': 'Explore projects in different languages or frameworks'
            })
        
        # Check for collaborative projects
        collab_count = sum(1 for p in projects if p['project_type'] == 'Collaborative Project')
        if collab_count == 0:
            gaps.append({
                'type': 'Collaboration',
                'issue': 'No collaborative/team projects',
                'priority': 'Medium',
                'suggestion': 'Contribute to open source or create projects with others'
            })
        
        return gaps
    
    def _generate_recommendations(self, projects, skill_demonstration, languages, categories):
        """Generate actionable portfolio recommendations"""
        recommendations = []
        
        # Based on complexity
        complexity_dist = categories['by_complexity']
        if complexity_dist.get('Advanced', 0) < 2:
            recommendations.append({
                'category': 'Project Complexity',
                'recommendation': 'Add 1-2 advanced projects showcasing system design or complex algorithms',
                'impact': 'High',
                'examples': ['Distributed cache system', 'Custom ML model from scratch', 'Real-time data pipeline']
            })
        
        # Based on skills
        total_skills = skill_demonstration['total_skills']
        if total_skills < 8:
            recommendations.append({
                'category': 'Skill Coverage',
                'recommendation': 'Expand skill demonstrations with projects in new domains',
                'impact': 'High',
                'examples': ['API development', 'Cloud deployment (AWS/Azure)', 'Mobile app development']
            })
        
        # Based on quality
        high_quality_count = len(categories['high_quality'])
        if high_quality_count < len(projects) * 0.7:
            recommendations.append({
                'category': 'Project Quality',
                'recommendation': 'Improve documentation and add professional touches to existing projects',
                'impact': 'High',
                'examples': ['Add comprehensive README', 'Include demo videos/GIFs', 'Add CI/CD badges']
            })
        
        # Based on impact
        high_impact_count = len(categories['high_impact'])
        if high_impact_count < 2:
            recommendations.append({
                'category': 'Community Impact',
                'recommendation': 'Focus on creating useful, shareable projects that solve real problems',
                'impact': 'Medium',
                'examples': ['Developer tools', 'Useful libraries', 'Educational resources']
            })
        
        # Based on project types
        if 'ML/Data Science' not in categories['by_type'] and len(projects) >= 3:
            recommendations.append({
                'category': 'Trending Skills',
                'recommendation': 'Add ML/AI projects to align with industry trends',
                'impact': 'Medium',
                'examples': ['Predictive model', 'NLP application', 'Computer vision project']
            })
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _generate_summary(self, strength, diversity, projects, skill_demonstration):
        """Generate portfolio summary"""
        
        # Determine overall rating
        avg_score = (strength + diversity) / 2
        
        if avg_score >= 80:
            rating = 'Excellent'
            message = 'Outstanding portfolio with diverse, high-quality projects'
        elif avg_score >= 65:
            rating = 'Strong'
            message = 'Solid portfolio demonstrating good technical breadth'
        elif avg_score >= 50:
            rating = 'Good'
            message = 'Decent portfolio with room for improvement'
        elif avg_score >= 35:
            rating = 'Developing'
            message = 'Growing portfolio, focus on quality and diversity'
        else:
            rating = 'Early Stage'
            message = 'Portfolio in early stages, build more projects'
        
        # Key strengths
        strengths = []
        if diversity >= 70:
            strengths.append('Diverse technology stack')
        if strength >= 70:
            strengths.append('High-quality projects')
        
        complexity_counts = Counter(p['complexity'] for p in projects)
        if complexity_counts.get('Advanced', 0) >= 2:
            strengths.append('Advanced technical skills')
        
        high_impact = sum(1 for p in projects if p['impact_score'] >= 60)
        if high_impact >= 2:
            strengths.append('Strong community engagement')
        
        if not strengths:
            strengths = ['Building foundation', 'Active development']
        
        return {
            'rating': rating,
            'message': message,
            'overall_score': round(avg_score),
            'strengths': strengths,
            'total_projects_analyzed': len(projects),
            'skills_demonstrated': skill_demonstration['total_skills']
        }


@st.cache_data(ttl=3600)
def analyze_portfolio(github_analysis):
    """Cached portfolio analysis function"""
    analyzer = PortfolioAnalyzer()
    return analyzer.analyze_portfolio(github_analysis)

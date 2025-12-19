"""
GitHub Repository Analyzer
Analyzes public GitHub profiles and repositories to generate contribution scores
Includes commit history and activity analysis with quality filtering
"Not every commit is a true commit" - filters meaningful contributions
"""
import requests
import re
from datetime import datetime, timedelta
from collections import Counter

class GitHubAnalyzer:
    """Analyzes GitHub profiles and repositories with quality commit filtering"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        
        # Patterns for trivial commits (not "true" commits)
        self.trivial_patterns = [
            # README and documentation
            r'^update\s*readme',
            r'^readme\s*update',
            r'^update\s*docs?$',
            r'^docs?\s*update',
            r'^documentation',
            r'^add\s*readme',
            r'^edit\s*readme',
            r'^updated?\s*readme\.md',
            # Typos and minor fixes
            r'^fix\s*typo',
            r'^typo\s*fix',
            r'^fixed?\s*typo',
            r'^typo',
            r'^minor\s*fix',
            r'^small\s*fix',
            r'^quick\s*fix',
            # Merge commits
            r'^merge\s*(branch|pull|request)',
            r'^merge\s*\w+\s*into',
            r"^merge\s*'",
            # Auto-generated
            r'^initial\s*commit$',
            r'^first\s*commit$',
            r'^create\s*\w+\.md$',
            r'^update\s*\w+\.md$',
            r'^add\s*\.\w+',  # add .gitignore, .env, etc.
            r'^added?\s*files?$',
            r'^auto\s*commit',
            # Version bumps
            r'^bump\s*version',
            r'^version\s*bump',
            r'^v\d+\.\d+',
            # Whitespace and formatting
            r'^whitespace',
            r'^formatting',
            r'^format\s*code',
            r'^lint',
            r'^cleanup$',
            r'^clean\s*up$',
            # Empty or very short
            r'^\.+$',
            r'^wip$',
            r'^temp$',
            r'^test$',
            r'^testing$',
            r'^asdf',
            r'^xxx',
            r'^fix$',
            r'^update$',
            r'^changes?$',
        ]
        
        # Compile patterns for efficiency
        self.trivial_regex = [re.compile(p, re.IGNORECASE) for p in self.trivial_patterns]
        
        # Patterns for quality commits
        self.quality_patterns = [
            r'^(feat|feature)[:\s]',     # Feature additions
            r'^(fix|bugfix)[:\s]',       # Bug fixes with context
            r'^(add|implement)',          # New implementations
            r'^(refactor|optimize)',      # Code improvements
            r'^(test|spec)[:\s]',        # Test additions
            r'^(perf|performance)',       # Performance improvements
            r'^(security|auth)',          # Security updates
            r'^(api|endpoint)',           # API changes
            r'^(database|db|schema)',     # Database changes
            r'^(deploy|release)',         # Deployment changes
        ]
        self.quality_regex = [re.compile(p, re.IGNORECASE) for p in self.quality_patterns]
    
    def is_quality_commit(self, commit_message: str) -> dict:
        """
        Analyze if a commit is a "true" quality commit
        Returns dict with is_quality, score, and reason
        """
        if not commit_message:
            return {"is_quality": False, "score": 0, "reason": "Empty message"}
        
        message = commit_message.strip().lower()
        
        # Check for trivial patterns
        for pattern in self.trivial_regex:
            if pattern.search(message):
                return {
                    "is_quality": False, 
                    "score": 0.2,  # Give partial credit
                    "reason": "Trivial commit (docs/typo/merge)"
                }
        
        # Check message length (too short = likely trivial)
        if len(message) < 5:
            return {
                "is_quality": False,
                "score": 0.1,
                "reason": "Message too short"
            }
        
        # Check for quality patterns (bonus points)
        for pattern in self.quality_regex:
            if pattern.search(message):
                return {
                    "is_quality": True,
                    "score": 1.5,  # Bonus for conventional commits
                    "reason": "High-quality conventional commit"
                }
        
        # Default: treat as quality if not trivial
        return {
            "is_quality": True,
            "score": 1.0,
            "reason": "Standard commit"
        }
    
    def get_user_profile(self, username):
        """Fetch GitHub user profile"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                return {'error': 'not_found', 'message': f'GitHub user "{username}" not found'}
            elif response.status_code == 403:
                return {'error': 'rate_limit', 'message': 'API rate limit reached. Please try again in a few minutes.'}
            elif response.status_code == 200:
                return response.json()
            else:
                return {'error': 'unknown', 'message': f'Error fetching profile: {response.status_code}'}
                
        except requests.exceptions.Timeout:
            return {'error': 'timeout', 'message': 'Request timed out. Check your internet connection.'}
        except requests.exceptions.RequestException as e:
            return {'error': 'connection', 'message': f'Connection error: {str(e)[:100]}'}
    
    def get_user_repos(self, username, max_repos=100):
        """Fetch user's public repositories"""
        try:
            url = f"{self.base_url}/users/{username}/repos"
            params = {'per_page': max_repos, 'sort': 'updated'}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception:
            return None
    
    def get_repo_languages(self, username, repo_name):
        """Get programming languages used in a repository"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception:
            return None
    
    def get_user_events(self, username, max_events=100):
        """Fetch user's recent events"""
        try:
            url = f"{self.base_url}/users/{username}/events/public"
            params = {'per_page': max_events}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception:
            return []
    
    def get_repo_commits(self, username, repo_name, max_commits=30):
        """Fetch commits for a specific repository"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}/commits"
            params = {'per_page': max_commits, 'author': username}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception:
            return []
    
    def analyze_commits(self, username, repos):
        """
        Analyze commit activity with quality filtering
        "Not every commit is a true commit"
        """
        total_commits = 0
        quality_commits = 0
        trivial_commits = 0
        weighted_score = 0
        recent_quality_commits = 0
        commits_by_repo = []
        commit_analysis = []
        
        for repo in repos[:10]:
            repo_name = repo.get('name', '')
            commits = self.get_repo_commits(username, repo_name, max_commits=50)
            
            repo_total = 0
            repo_quality = 0
            repo_trivial = 0
            
            for commit in commits:
                total_commits += 1
                repo_total += 1
                
                # Get commit message
                commit_info = commit.get('commit', {})
                message = commit_info.get('message', '').split('\n')[0]  # First line only
                
                # Analyze quality
                quality = self.is_quality_commit(message)
                weighted_score += quality['score']
                
                if quality['is_quality']:
                    quality_commits += 1
                    repo_quality += 1
                    
                    # Check if recent (last 30 days)
                    try:
                        date_str = commit_info.get('author', {}).get('date', '')
                        if date_str:
                            commit_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                            if (datetime.now() - commit_date).days <= 30:
                                recent_quality_commits += 1
                    except:
                        pass
                else:
                    trivial_commits += 1
                    repo_trivial += 1
                
                # Store for detailed analysis
                commit_analysis.append({
                    'repo': repo_name,
                    'message': message[:50],
                    'is_quality': quality['is_quality'],
                    'score': quality['score'],
                    'reason': quality['reason']
                })
            
            if repo_total > 0:
                commits_by_repo.append({
                    'repo': repo_name,
                    'total': repo_total,
                    'quality': repo_quality,
                    'trivial': repo_trivial,
                    'quality_ratio': round(repo_quality / repo_total * 100, 1)
                })
        
        # Calculate quality ratio
        quality_ratio = round(quality_commits / total_commits * 100, 1) if total_commits > 0 else 0
        
        # Calculate effective commit score (weighted)
        effective_commits = round(weighted_score) if weighted_score > 0 else 0
        
        # Activity summary based on quality commits
        activity_summary = self._get_quality_activity_summary(quality_commits, recent_quality_commits)
        
        # Sort repos by quality commits
        commits_by_repo.sort(key=lambda x: x['quality'], reverse=True)
        
        return {
            'total_commits': total_commits,
            'quality_commits': quality_commits,
            'trivial_commits': trivial_commits,
            'quality_ratio': quality_ratio,
            'effective_commit_score': effective_commits,
            'recent_quality_commits_30_days': recent_quality_commits,
            'top_repos_by_commits': commits_by_repo[:5],
            'activity_summary': activity_summary,
            'commit_quality_note': f"{quality_ratio}% of commits are meaningful contributions (not README updates, merges, or typo fixes)",
            'sample_analysis': commit_analysis[:10]  # First 10 for debugging/transparency
        }
    
    def _get_quality_activity_summary(self, quality_commits, recent_quality):
        """Generate activity summary based on QUALITY commits only"""
        if recent_quality >= 15:
            return "Very Active - Frequent quality contributions"
        elif recent_quality >= 8:
            return "Active - Regular meaningful commits"
        elif recent_quality >= 3:
            return "Moderately Active - Some quality contributions"
        elif recent_quality > 0:
            return "Occasional - Few meaningful commits recently"
        else:
            return "Inactive - No recent quality commits"
    
    def analyze_profile(self, username):
        """Complete profile analysis with quality commit filtering"""
        profile = self.get_user_profile(username)
        
        if profile and 'error' in profile:
            return profile
        
        repos = self.get_user_repos(username)
        
        if not repos:
            return {
                'error': 'no_repos',
                'message': 'Unable to fetch repositories or no public repositories found'
            }
        
        # Analyze repositories
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        total_watchers = sum(repo.get('watchers_count', 0) for repo in repos)
        
        # Get languages
        all_languages = Counter()
        for repo in repos[:20]:
            languages = self.get_repo_languages(username, repo['name'])
            if languages:
                all_languages.update(languages)
        
        total_bytes = sum(all_languages.values())
        language_breakdown = {}
        if total_bytes > 0:
            for lang, bytes_count in all_languages.most_common(10):
                percentage = (bytes_count / total_bytes) * 100
                language_breakdown[lang] = round(percentage, 1)
        
        # Top repositories
        top_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:5]
        
        # Analyze commits with quality filtering
        commit_analysis = self.analyze_commits(username, repos)
        
        # Calculate contribution score using QUALITY commits
        contribution_score = self._calculate_contribution_score(
            profile=profile,
            repos=repos,
            total_stars=total_stars,
            languages_count=len(all_languages),
            quality_commits=commit_analysis.get('quality_commits', 0),
            quality_ratio=commit_analysis.get('quality_ratio', 0)
        )
        
        # Activity level
        recent_repos = [r for r in repos if self._is_recent(r.get('updated_at', ''))]
        activity_level = commit_analysis.get('activity_summary', 'Unknown')
        
        return {
            'profile': {
                'username': profile.get('login', username),
                'name': profile.get('name', 'N/A'),
                'bio': profile.get('bio', 'No bio available'),
                'location': profile.get('location', 'N/A'),
                'company': profile.get('company', 'N/A'),
                'blog': profile.get('blog', ''),
                'followers': profile.get('followers', 0),
                'following': profile.get('following', 0),
                'public_repos': profile.get('public_repos', 0),
                'created_at': profile.get('created_at', ''),
                'avatar_url': profile.get('avatar_url', '')
            },
            'statistics': {
                'total_repos': len(repos),
                'total_stars': total_stars,
                'total_forks': total_forks,
                'total_watchers': total_watchers,
                'languages_count': len(all_languages)
            },
            'commits': commit_analysis,
            'languages': language_breakdown,
            'top_repos': [
                {
                    'name': repo['name'],
                    'description': repo.get('description', 'No description'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'language': repo.get('language', 'Unknown'),
                    'url': repo.get('html_url', '')
                }
                for repo in top_repos
            ],
            'contribution_score': contribution_score,
            'activity_level': activity_level,
            'account_age_days': self._calculate_account_age(profile.get('created_at', ''))
        }
    
    def _calculate_contribution_score(self, profile, repos, total_stars, languages_count, quality_commits=0, quality_ratio=0):
        """Calculate contribution score using QUALITY commits"""
        score = 0
        
        # Number of repositories (max 20 points)
        repo_count = len(repos)
        score += min(20, repo_count * 1.2)
        
        # Stars received (max 20 points)
        score += min(20, total_stars * 0.5)
        
        # Followers (max 15 points)
        followers = profile.get('followers', 0)
        score += min(15, followers * 0.3)
        
        # Language diversity (max 10 points)
        score += min(10, languages_count * 1.5)
        
        # QUALITY commits (max 25 points) - not total commits!
        score += min(25, quality_commits * 0.3)
        
        # Quality ratio bonus (max 10 points)
        score += min(10, quality_ratio * 0.1)
        
        return min(100, round(score))
    
    def _calculate_account_age(self, created_at):
        """Calculate account age in days"""
        try:
            created = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            age = (datetime.now() - created).days
            return age
        except:
            return 0
    
    def _is_recent(self, updated_at, days=90):
        """Check if repository was updated recently"""
        try:
            updated = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
            days_ago = (datetime.now() - updated).days
            return days_ago <= days
        except:
            return False


def analyze_github_profile(username):
    """Function to analyze GitHub profile"""
    analyzer = GitHubAnalyzer()
    return analyzer.analyze_profile(username)

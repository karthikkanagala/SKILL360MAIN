"""
GitHub Repository Analyzer
Analyzes public GitHub profiles and repositories to generate contribution scores
Includes commit history and activity analysis
"""
import requests
from datetime import datetime, timedelta
from collections import Counter

class GitHubAnalyzer:
    """Analyzes GitHub profiles and repositories"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        
    def get_user_profile(self, username):
        """
        Fetch GitHub user profile
        Returns: dict with user data or None if error
        """
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
        """
        Fetch user's public repositories
        Returns: list of repos or None if error
        """
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
        """
        Get programming languages used in a repository
        Returns: dict of languages or None
        """
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception:
            return None
    
    def get_user_events(self, username, max_events=100):
        """
        Fetch user's recent events (commits, pushes, etc.)
        Returns: list of events or empty list
        """
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
        """
        Fetch commits for a specific repository
        Returns: list of commits or empty list
        """
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
        Analyze commit activity across repositories
        Returns: dict with commit statistics
        """
        total_commits = 0
        recent_commits = 0
        commits_by_repo = []
        commit_dates = []
        
        # Get commits from top 10 repos
        for repo in repos[:10]:
            repo_name = repo.get('name', '')
            commits = self.get_repo_commits(username, repo_name, max_commits=50)
            
            repo_commit_count = len(commits)
            total_commits += repo_commit_count
            
            if repo_commit_count > 0:
                commits_by_repo.append({
                    'repo': repo_name,
                    'commits': repo_commit_count,
                    'latest': commits[0].get('commit', {}).get('author', {}).get('date', '') if commits else ''
                })
            
            # Count recent commits (last 30 days)
            for commit in commits:
                try:
                    date_str = commit.get('commit', {}).get('author', {}).get('date', '')
                    if date_str:
                        commit_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                        commit_dates.append(commit_date)
                        if (datetime.now() - commit_date).days <= 30:
                            recent_commits += 1
                except:
                    pass
        
        # Analyze events for additional commit info
        events = self.get_user_events(username)
        push_events = [e for e in events if e.get('type') == 'PushEvent']
        
        for event in push_events:
            payload = event.get('payload', {})
            commits_in_push = payload.get('commits', [])
            # Add to total if not already counted
            # (Events API shows more recent activity)
        
        # Calculate commit frequency
        if commit_dates:
            min_date = min(commit_dates)
            max_date = max(commit_dates)
            days_range = max(1, (max_date - min_date).days)
            commits_per_week = (len(commit_dates) / days_range) * 7
        else:
            commits_per_week = 0
        
        # Sort by commit count
        commits_by_repo.sort(key=lambda x: x['commits'], reverse=True)
        
        return {
            'total_commits': total_commits,
            'recent_commits_30_days': recent_commits,
            'commits_per_week': round(commits_per_week, 1),
            'push_events': len(push_events),
            'top_repos_by_commits': commits_by_repo[:5],
            'activity_summary': self._get_activity_summary(recent_commits, total_commits)
        }
    
    def _get_activity_summary(self, recent, total):
        """Generate activity summary text"""
        if recent >= 20:
            return "Very Active - Committing frequently"
        elif recent >= 10:
            return "Active - Regular contributions"
        elif recent >= 5:
            return "Moderately Active - Some recent activity"
        elif recent > 0:
            return "Occasional - Few recent commits"
        else:
            return "Inactive - No recent commits"
    
    def analyze_profile(self, username):
        """
        Complete profile analysis including commits
        Returns: comprehensive analysis dict
        """
        # Get profile
        profile = self.get_user_profile(username)
        
        if profile and 'error' in profile:
            return profile
        
        # Get repositories
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
        
        # Get languages across all repos
        all_languages = Counter()
        
        for repo in repos[:20]:  # Analyze top 20 repos to avoid rate limits
            languages = self.get_repo_languages(username, repo['name'])
            if languages:
                all_languages.update(languages)
        
        # Calculate language percentages
        total_bytes = sum(all_languages.values())
        language_breakdown = {}
        
        if total_bytes > 0:
            for lang, bytes_count in all_languages.most_common(10):
                percentage = (bytes_count / total_bytes) * 100
                language_breakdown[lang] = round(percentage, 1)
        
        # Find top repositories
        top_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:5]
        
        # Analyze commits
        commit_analysis = self.analyze_commits(username, repos)
        
        # Calculate contribution score (0-100)
        contribution_score = self._calculate_contribution_score(
            profile=profile,
            repos=repos,
            total_stars=total_stars,
            languages_count=len(all_languages),
            commits=commit_analysis.get('total_commits', 0)
        )
        
        # Calculate activity level
        recent_repos = [r for r in repos if self._is_recent(r.get('updated_at', ''))]
        activity_level = self._determine_activity_level(recent_repos, repos)
        
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
    
    def _calculate_contribution_score(self, profile, repos, total_stars, languages_count, commits=0):
        """Calculate contribution score (0-100)"""
        score = 0
        
        # Number of repositories (max 25 points)
        repo_count = len(repos)
        score += min(25, repo_count * 1.5)
        
        # Stars received (max 20 points)
        score += min(20, total_stars * 0.5)
        
        # Followers (max 15 points)
        followers = profile.get('followers', 0)
        score += min(15, followers * 0.3)
        
        # Language diversity (max 10 points)
        score += min(10, languages_count * 1.5)
        
        # Commit activity (max 20 points)
        score += min(20, commits * 0.2)
        
        # Account age bonus (max 10 points)
        account_age_days = self._calculate_account_age(profile.get('created_at', ''))
        years = account_age_days / 365
        score += min(10, years * 2)
        
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
    
    def _determine_activity_level(self, recent_repos, all_repos):
        """Determine activity level"""
        if not all_repos:
            return 'Unknown'
        
        active_ratio = len(recent_repos) / len(all_repos)
        
        if active_ratio >= 0.3:
            return 'Very Active'
        elif active_ratio >= 0.15:
            return 'Active'
        elif active_ratio >= 0.05:
            return 'Moderately Active'
        else:
            return 'Less Active'


# Remove streamlit dependency for FastAPI usage
def analyze_github_profile(username):
    """Function to analyze GitHub profile"""
    analyzer = GitHubAnalyzer()
    return analyzer.analyze_profile(username)

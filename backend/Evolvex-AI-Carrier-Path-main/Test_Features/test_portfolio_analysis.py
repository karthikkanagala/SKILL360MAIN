"""
Quick test to verify portfolio analysis works
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from github_analyzer import analyze_github_profile
from portfolio_analyzer import analyze_portfolio

print("Testing Portfolio Analysis Feature\n")
print("=" * 60)

# Test with a known GitHub profile
username = "torvalds"
print(f"\n[Step 1] Analyzing GitHub profile: @{username}")
print("-" * 60)

github_data = analyze_github_profile(username)

if 'error' in github_data:
    print(f"[ERROR] {github_data['message']}")
    exit(1)

print(f"[SUCCESS] GitHub analysis successful!")
print(f"   • Repositories: {github_data['statistics']['total_repos']}")
print(f"   • Stars: {github_data['statistics']['total_stars']}")
print(f"   • Languages: {len(github_data['languages'])}")
print(f"   • Contribution Score: {github_data['contribution_score']}/100")

print(f"\n[Step 2] Running Portfolio Analysis")
print("-" * 60)

portfolio_data = analyze_portfolio(github_data)

if 'error' in portfolio_data:
    print(f"[ERROR] Portfolio analysis error: {portfolio_data['message']}")
    exit(1)

print(f"[SUCCESS] Portfolio analysis successful!\n")

# Display results
summary = portfolio_data['summary']
print("PORTFOLIO EVALUATION RESULTS:")
print("=" * 60)
print(f"Overall Rating: {summary['rating']}")
print(f"Message: {summary['message']}")
print(f"Overall Score: {summary['overall_score']}/100")
print(f"\nPortfolio Strength: {portfolio_data['portfolio_strength']}/100")
print(f"Diversity Score: {portfolio_data['diversity_score']}/100")
print(f"Skills Demonstrated: {summary['skills_demonstrated']}")

print(f"\nKey Strengths:")
for strength in summary['strengths']:
    print(f"   - {strength}")

print(f"\nProject Breakdown:")
print(f"   Complexity Distribution:")
for complexity, count in portfolio_data['categories']['by_complexity'].items():
    print(f"      - {complexity}: {count} project(s)")

print(f"\nAnalyzed Projects:")
for project in portfolio_data['projects'][:3]:
    print(f"\n   - {project['name']}")
    print(f"     - Complexity: {project['complexity']}")
    print(f"     - Quality: {project['quality_score']}/100")
    print(f"     - Impact: {project['impact_score']}/100")
    print(f"     - Type: {project['project_type']}")

if portfolio_data['gaps']:
    print(f"\nPortfolio Gaps ({len(portfolio_data['gaps'])}):") 
    for gap in portfolio_data['gaps'][:3]:
        print(f"   - [{gap['priority']}] {gap['type']}: {gap['issue']}")

if portfolio_data['recommendations']:
    print(f"\nTop Recommendations:")
    for idx, rec in enumerate(portfolio_data['recommendations'][:3], 1):
        print(f"   {idx}. [{rec['impact']} Impact] {rec['recommendation']}")

print("\n" + "=" * 60)
print("[SUCCESS] Portfolio Analysis Feature Working Correctly!")
print("\nTo see this in the app:")
print("   1. Open http://localhost:8507")
print("   2. Enter 'torvalds' in GitHub username field")
print("   3. Click 'Analyze' button")
print("   4. Scroll down to see Portfolio Evaluation section")
print("=" * 60)

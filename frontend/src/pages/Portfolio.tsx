import React, { useState } from 'react';
import { githubApi } from '../lib/api';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function Portfolio() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [portfolio, setPortfolio] = useState<any>(null);
  const [error, setError] = useState('');

  const analyzePortfolio = async () => {
    if (!username.trim()) {
      setError('Please enter a GitHub username');
      return;
    }

    setLoading(true);
    setError('');
    setPortfolio(null);

    try {
      const response = await githubApi.portfolio(username.trim());
      setPortfolio(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze portfolio');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">📁 Portfolio Analysis</h1>
        <p className="text-gray-600">
          Analyze your GitHub portfolio to showcase your projects and contributions
        </p>
      </div>

      {/* Input Section */}
      <Card className="p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Enter GitHub Username</h2>
        <div className="flex gap-4">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && analyzePortfolio()}
            placeholder="e.g., torvalds"
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button
            onClick={analyzePortfolio}
            disabled={loading}
            className="px-6"
          >
            {loading ? 'Analyzing...' : 'Analyze Portfolio'}
          </Button>
        </div>
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
      </Card>

      {/* Results */}
      {portfolio && (
        <div className="space-y-6">
          {/* Portfolio Score */}
          {portfolio.portfolio_score !== undefined && (
            <Card className="p-6 bg-gradient-to-r from-blue-50 to-purple-50">
              <h2 className="text-2xl font-bold mb-2">Portfolio Score</h2>
              <div className="text-5xl font-bold text-blue-600">
                {portfolio.portfolio_score}/100
              </div>
              <p className="text-gray-600 mt-2">
                {portfolio.portfolio_score >= 80
                  ? 'Excellent portfolio!'
                  : portfolio.portfolio_score >= 60
                  ? 'Good portfolio, keep building!'
                  : 'Keep adding more projects to strengthen your portfolio'}
              </p>
            </Card>
          )}

          {/* Top Repositories */}
          {portfolio.top_repos && portfolio.top_repos.length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">🌟 Top Repositories</h2>
              <div className="grid gap-4">
                {portfolio.top_repos.map((repo: any, idx: number) => (
                  <div
                    key={idx}
                    className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-lg font-semibold text-blue-600">
                        {repo.name || repo.repo_name || `Repo ${idx + 1}`}
                      </h3>
                      <div className="flex gap-4 text-sm text-gray-600">
                        {repo.stars !== undefined && (
                          <span>⭐ {repo.stars}</span>
                        )}
                        {repo.forks !== undefined && (
                          <span>🍴 {repo.forks}</span>
                        )}
                      </div>
                    </div>
                    {repo.description && (
                      <p className="text-gray-700 mb-2">{repo.description}</p>
                    )}
                    {repo.language && (
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                        {repo.language}
                      </span>
                    )}
                    {repo.url && (
                      <a
                        href={repo.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm block mt-2"
                      >
                        View Repository →
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Project Highlights */}
          {portfolio.highlights && portfolio.highlights.length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">💡 Project Highlights</h2>
              <ul className="space-y-2">
                {portfolio.highlights.map((highlight: string, idx: number) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-green-600 mr-2">✓</span>
                    <span>{highlight}</span>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {/* Recommendations */}
          {portfolio.recommendations && portfolio.recommendations.length > 0 && (
            <Card className="p-6 bg-yellow-50 border-yellow-200">
              <h2 className="text-2xl font-bold mb-4">💡 Recommendations</h2>
              <ul className="space-y-2">
                {portfolio.recommendations.map((rec: string, idx: number) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-yellow-600 mr-2">→</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {/* Raw JSON (collapsible) */}
          <details className="mt-6">
            <summary className="cursor-pointer text-gray-600 hover:text-gray-900">
              View Raw JSON
            </summary>
            <pre className="mt-2 p-4 bg-gray-50 rounded-lg overflow-auto text-sm">
              {JSON.stringify(portfolio, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

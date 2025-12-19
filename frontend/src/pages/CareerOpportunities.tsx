import React, { useState } from 'react';
import { opportunitiesApi } from '../lib/api';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function CareerOpportunities() {
  const [skills, setSkills] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [location, setLocation] = useState('India');
  const [loading, setLoading] = useState(false);
  const [opportunities, setOpportunities] = useState<any>(null);
  const [error, setError] = useState('');

  const searchOpportunities = async () => {
    if (!skills.trim()) {
      setError('Please enter at least one skill');
      return;
    }

    setLoading(true);
    setError('');
    setOpportunities(null);

    try {
      const skillsArray = skills
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s);

      const response = await opportunitiesApi.search({
        skills: skillsArray,
        target_role: targetRole.trim() || undefined,
        location: location.trim() || undefined,
      });
      setOpportunities(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to search opportunities');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">💼 Career Opportunities</h1>
        <p className="text-gray-600">
          Discover career opportunities and market trends based on your skills
        </p>
      </div>

      {/* Search Form */}
      <Card className="p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block font-semibold mb-2">
              Your Skills (comma-separated) <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="e.g., Python, React, SQL, Machine Learning"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">Target Role (Optional)</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Software Engineer, Data Scientist"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">Location</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., India, USA, Remote"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <Button onClick={searchOpportunities} disabled={loading} className="w-full py-3">
            {loading ? 'Searching...' : 'Search Opportunities'}
          </Button>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </div>
      </Card>

      {/* Results */}
      {opportunities && (
        <div className="space-y-6">
          {/* Market Trends */}
          {opportunities.trends && Object.keys(opportunities.trends).length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">📈 Market Trends</h2>
              <div className="grid gap-4">
                {Object.entries(opportunities.trends).map(([skill, data]: [string, any]) => (
                  <div
                    key={skill}
                    className="p-4 border rounded-lg"
                  >
                    <h3 className="text-lg font-semibold mb-2 capitalize">{skill}</h3>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                      {data.demand && (
                        <div>
                          <span className="font-semibold text-gray-700">Demand:</span>
                          <span className="ml-2">{data.demand}</span>
                        </div>
                      )}
                      {data.growth && (
                        <div>
                          <span className="font-semibold text-gray-700">Growth:</span>
                          <span className="ml-2">{data.growth}</span>
                        </div>
                      )}
                      {data.avg_salary && (
                        <div>
                          <span className="font-semibold text-gray-700">Avg Salary:</span>
                          <span className="ml-2">{data.avg_salary}</span>
                        </div>
                      )}
                      {data.job_count !== undefined && (
                        <div>
                          <span className="font-semibold text-gray-700">Jobs:</span>
                          <span className="ml-2">{data.job_count}+ openings</span>
                        </div>
                      )}
                    </div>
                    {data.companies && data.companies.length > 0 && (
                      <div className="mt-3">
                        <span className="font-semibold text-gray-700">Top Hiring:</span>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {data.companies.slice(0, 5).map((company: string, idx: number) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                            >
                              {company}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Opportunities List */}
          {opportunities.opportunities && opportunities.opportunities.length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">🎯 Available Opportunities</h2>
              <div className="grid gap-4">
                {opportunities.opportunities.map((opp: any, idx: number) => (
                  <div
                    key={idx}
                    className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-blue-600">
                          {opp.title || opp.role || 'Opportunity'}
                        </h3>
                        <p className="text-gray-600">{opp.company}</p>
                      </div>
                      {opp.match_score !== undefined && (
                        <div className="text-right">
                          <div className="text-2xl font-bold text-green-600">
                            {opp.match_score}%
                          </div>
                          <div className="text-xs text-gray-600">Match</div>
                        </div>
                      )}
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                      {opp.location && <span>📍 {opp.location}</span>}
                      {opp.experience && <span>💼 {opp.experience}</span>}
                      {opp.salary && <span>💰 {opp.salary}</span>}
                      {opp.type && <span>🏢 {opp.type}</span>}
                    </div>

                    {opp.description && (
                      <p className="text-gray-700 mb-3 text-sm">{opp.description}</p>
                    )}

                    {opp.required_skills && opp.required_skills.length > 0 && (
                      <div className="mb-3">
                        <span className="text-sm font-semibold text-gray-700">Required Skills:</span>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {opp.required_skills.map((skill: string, sidx: number) => (
                            <span
                              key={sidx}
                              className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {opp.apply_url && (
                      <a
                        href={opp.apply_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                      >
                        Apply Now →
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Model Info */}
          {opportunities.model_used && (
            <p className="text-sm text-gray-500 text-center">
              Analysis Method: {opportunities.model_used}
            </p>
          )}

          {/* Raw JSON */}
          <details className="mt-6">
            <summary className="cursor-pointer text-gray-600 hover:text-gray-900">
              View Raw JSON
            </summary>
            <pre className="mt-2 p-4 bg-gray-50 rounded-lg overflow-auto text-sm">
              {JSON.stringify(opportunities, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

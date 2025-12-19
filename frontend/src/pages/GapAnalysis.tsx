import React, { useState } from 'react';
import { gapAnalysisApi } from '../lib/api';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function GapAnalysis() {
  const [targetRole, setTargetRole] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [currentSkills, setCurrentSkills] = useState('');
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState('');

  const analyzeGap = async () => {
    if (!targetRole.trim()) {
      setError('Please enter a target role');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const skillsArray = currentSkills
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s);

      const response = await gapAnalysisApi.analyze({
        target_role: targetRole.trim(),
        job_description: jobDescription.trim(),
        current_skills: skillsArray,
        resume_text: resumeText.trim(),
      });
      setAnalysis(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze skill gap');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🎯 Dream Role Gap Analysis</h1>
        <p className="text-gray-600">
          Identify skill gaps and get personalized recommendations for your target role
        </p>
      </div>

      {/* Input Form */}
      <Card className="p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block font-semibold mb-2">
              Target Role <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Machine Learning Engineer"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">
              Job Description (Optional)
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px]"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">
              Current Skills (comma-separated)
            </label>
            <input
              type="text"
              value={currentSkills}
              onChange={(e) => setCurrentSkills(e.target.value)}
              placeholder="e.g., Python, SQL, React, Git"
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">
              Resume Text (Optional)
            </label>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume here to extract additional skills..."
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px]"
            />
          </div>

          <Button onClick={analyzeGap} disabled={loading} className="w-full py-3">
            {loading ? 'Analyzing...' : 'Analyze Skill Gap'}
          </Button>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </div>
      </Card>

      {/* Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Summary */}
          {(analysis.match_percentage !== undefined ||
            analysis.model_used) && (
            <Card className="p-6 bg-gradient-to-r from-blue-50 to-purple-50">
              <h2 className="text-2xl font-bold mb-4">📊 Analysis Summary</h2>
              {analysis.match_percentage !== undefined && (
                <div className="mb-4">
                  <div className="text-5xl font-bold text-blue-600">
                    {analysis.match_percentage}%
                  </div>
                  <p className="text-gray-600 mt-2">Current Match</p>
                </div>
              )}
              {analysis.model_used && (
                <p className="text-sm text-gray-500">
                  Analysis Method: {analysis.model_used}
                </p>
              )}
            </Card>
          )}

          {/* Missing Skills */}
          {analysis.missing_skills && analysis.missing_skills.length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4 text-red-600">
                ❌ Skills to Acquire
              </h2>
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills.map((skill: string, idx: number) => (
                  <span
                    key={idx}
                    className="px-4 py-2 bg-red-100 text-red-700 rounded-full font-semibold"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </Card>
          )}

          {/* Recommended Courses */}
          {analysis.recommended_courses &&
            analysis.recommended_courses.length > 0 && (
              <Card className="p-6">
                <h2 className="text-2xl font-bold mb-4">📚 Recommended Courses</h2>
                <div className="grid gap-4">
                  {analysis.recommended_courses.map((course: any, idx: number) => (
                    <div
                      key={idx}
                      className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                    >
                      <h3 className="text-lg font-semibold text-blue-600 mb-2">
                        {course.title}
                      </h3>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-2">
                        {course.platform && <span>🏫 {course.platform}</span>}
                        {course.difficulty && <span>📊 {course.difficulty}</span>}
                        {course.duration && <span>⏱️ {course.duration}</span>}
                        {course.price && <span>💰 {course.price}</span>}
                      </div>
                      {course.description && (
                        <p className="text-gray-700 text-sm">{course.description}</p>
                      )}
                      {course.url && (
                        <a
                          href={course.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline text-sm block mt-2"
                        >
                          View Course →
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

          {/* Recommended Projects */}
          {analysis.recommended_projects &&
            analysis.recommended_projects.length > 0 && (
              <Card className="p-6">
                <h2 className="text-2xl font-bold mb-4">💡 Project Ideas</h2>
                <div className="grid gap-4">
                  {analysis.recommended_projects.map((project: any, idx: number) => (
                    <div
                      key={idx}
                      className="p-4 border rounded-lg hover:shadow-md transition-shadow"
                    >
                      <h3 className="text-lg font-semibold mb-2">
                        {project.title || project.name || `Project ${idx + 1}`}
                      </h3>
                      {project.description && (
                        <p className="text-gray-700 mb-2">{project.description}</p>
                      )}
                      {project.skills_used && project.skills_used.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {project.skills_used.map((skill: string, sidx: number) => (
                            <span
                              key={sidx}
                              className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                      {project.difficulty && (
                        <p className="text-sm text-gray-600 mt-2">
                          Difficulty: {project.difficulty}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}

          {/* Predicted Fit Score */}
          {analysis.predicted_fit_score !== undefined && (
            <Card className="p-6 bg-green-50 border-green-200">
              <h2 className="text-2xl font-bold mb-4">🎯 Potential Fit Score</h2>
              <div className="text-4xl font-bold text-green-600 mb-2">
                {analysis.predicted_fit_score}/100
              </div>
              <p className="text-gray-700">
                After acquiring the recommended skills and completing suggested
                projects, your estimated fit for this role
              </p>
            </Card>
          )}

          {/* Next Steps */}
          {analysis.next_steps && analysis.next_steps.length > 0 && (
            <Card className="p-6 bg-yellow-50 border-yellow-200">
              <h2 className="text-2xl font-bold mb-4">🚀 Next Steps</h2>
              <ol className="list-decimal list-inside space-y-2">
                {analysis.next_steps.map((step: string, idx: number) => (
                  <li key={idx} className="text-gray-700">
                    {step}
                  </li>
                ))}
              </ol>
            </Card>
          )}

          {/* Raw JSON */}
          <details className="mt-6">
            <summary className="cursor-pointer text-gray-600 hover:text-gray-900">
              View Raw JSON
            </summary>
            <pre className="mt-2 p-4 bg-gray-50 rounded-lg overflow-auto text-sm">
              {JSON.stringify(analysis, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

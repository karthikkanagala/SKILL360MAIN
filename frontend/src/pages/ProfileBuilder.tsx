import { useState } from 'react'
import { Github } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { careerScoreApi, githubApi, resumeApi } from '@/lib/api'
import { useProfile } from '@/context/ProfileContext'

export default function ProfileBuilder() {
  const { profile, setProfile, setCareerScore } = useProfile()
  const [githubUsername, setGithubUsername] = useState('')
  const [status, setStatus] = useState<string | null>(null)
  const [showResumeUpload, setShowResumeUpload] = useState(!profile.resume_text)

  const uploadResumeFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.name.match(/\.(pdf|docx)$/i)) {
      setStatus('❌ Only PDF and DOCX files are supported')
      return
    }

    setStatus('🤖 Analyzing with XGBoost AI (trained on 6000+ resumes)...')
    try {
      const res = await resumeApi.upload(file)
      setProfile((p) => ({
        ...p,
        resume_text: res.data.text,
        resume_skills: res.data.skills,
        ats_score: res.data.ats_score,
        ats_analysis: res.data.ats_analysis,
        resume_improvements: res.data.improvements,
      }))
      setStatus(`✅ ATS Score: ${res.data.ats_score}/100 | Skills: ${res.data.skills?.length || 0}`)
      setShowResumeUpload(false)
    } catch (err: any) {
      setStatus(`❌ ${err.response?.data?.detail || 'Upload failed'}`)
    }
  }

  const analyzeGitHub = async () => {
    if (!githubUsername.trim()) return
    setStatus('🔍 Analyzing GitHub...')
    try {
      const res = await githubApi.analyze(githubUsername.trim())
      if (res.data?.error) {
        setProfile((p) => ({ ...p, github_analysis: res.data }))
        setStatus(`❌ ${res.data.message || res.data.error}`)
        return
      }
      setProfile((p) => ({ ...p, github_analysis: res.data }))
      
      // Portfolio analysis
      try {
        const portRes = await githubApi.portfolio(githubUsername.trim())
        setProfile((p) => ({ ...p, portfolio_analysis: portRes.data }))
      } catch {}
      
      setStatus('✅ GitHub analysis complete')
    } catch (e: any) {
      setStatus(`❌ ${e?.response?.data?.detail || 'Failed'}`)
    }
  }

  const calculateCareerScore = async () => {
    if (!profile.resume_text) {
      setStatus('❌ Please upload resume first')
      return
    }
    setStatus('📊 Calculating...')
    try {
      const response = await careerScoreApi.calculate({
        resume_data: {
          ats_score: profile.ats_score || 0,
          skills: profile.resume_skills || [],
          text: profile.resume_text || '',
        },
        github_data: profile.github_analysis || {},
        portfolio_analysis: profile.portfolio_analysis || {},
        certificates: profile.validated_certificates || [],
        activities: profile.activities || [],
        interview_data: {},
        job_description: '',
      })
      setCareerScore(response.data)
      setProfile((p) => ({ ...p, career_score_data: response.data }))
      setStatus('✅ Career score calculated')
    } catch {
      setStatus('❌ Calculation failed')
    }
  }

  return (
    <div className="space-y-6 container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">📋 Build Your Profile</h1>
        <p className="text-gray-600">Upload your resume and connect GitHub</p>
      </div>

      {status && (
        <div className={`p-4 rounded-lg ${status.startsWith('❌') ? 'bg-red-50 text-red-700' : status.startsWith('✅') ? 'bg-green-50 text-green-700' : 'bg-blue-50 text-blue-700'}`}>
          {status}
        </div>
      )}

      {/* Resume Section */}
      <Card>
        <CardHeader>
          <CardTitle>📄 Resume Analysis</CardTitle>
          <CardDescription>Upload PDF/DOCX for AI-powered ATS scoring (XGBoost model)</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {profile.resume_text && !showResumeUpload ? (
            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="font-semibold">✅ Resume Loaded</p>
                <p className="text-sm text-gray-600">ATS Score: {profile.ats_score}/100 | Skills: {profile.resume_skills?.length || 0}</p>
              </div>
              <Button variant="outline" onClick={() => setShowResumeUpload(true)}>
                Upload New Resume
              </Button>

              {profile.ats_analysis && (
                <div className="space-y-4">
                  <h3 className="font-semibold">📊 Detailed ATS Analysis</h3>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div className="p-3 border rounded-lg">
                      <p className="text-xs text-gray-600">Content Quality</p>
                      <p className="text-lg font-bold">{profile.ats_analysis.scores?.content_quality || 0}/25</p>
                    </div>
                    <div className="p-3 border rounded-lg">
                      <p className="text-xs text-gray-600">Skills & Keywords</p>
                      <p className="text-lg font-bold">{profile.ats_analysis.scores?.skills_keywords || 0}/25</p>
                    </div>
                    <div className="p-3 border rounded-lg">
                      <p className="text-xs text-gray-600">Structure</p>
                      <p className="text-lg font-bold">{profile.ats_analysis.scores?.structure_formatting || 0}/20</p>
                    </div>
                    <div className="p-3 border rounded-lg">
                      <p className="text-xs text-gray-600">Experience</p>
                      <p className="text-lg font-bold">{profile.ats_analysis.scores?.experience_relevance || 0}/15</p>
                    </div>
                    <div className="p-3 border rounded-lg">
                      <p className="text-xs text-gray-600">Completeness</p>
                      <p className="text-lg font-bold">{profile.ats_analysis.scores?.completeness || 0}/15</p>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold text-green-600 mb-2">✨ Strengths</h4>
                      <ul className="text-sm space-y-1">
                        {(profile.ats_analysis.strengths || []).slice(0, 5).map((s: string, i: number) => (
                          <li key={i}>• {s}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold text-red-600 mb-2">⚠️ Weaknesses</h4>
                      <ul className="text-sm space-y-1">
                        {(profile.ats_analysis.weaknesses || []).slice(0, 5).map((s: string, i: number) => (
                          <li key={i}>• {s}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold text-blue-600 mb-2">🎯 Key Improvements</h4>
                      <ul className="text-sm space-y-1">
                        {(profile.ats_analysis.key_improvements || []).slice(0, 5).map((s: string, i: number) => (
                          <li key={i}>{i + 1}. {s}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {profile.resume_improvements && (
                <details className="border rounded-lg p-4">
                  <summary className="cursor-pointer font-semibold">🔧 Resume Improvement Plan</summary>
                  <div className="mt-4 space-y-3">
                    {profile.resume_improvements.immediate_fixes && (
                      <div>
                        <h4 className="font-semibold mb-2">Quick Fixes (10 min)</h4>
                        <ul className="text-sm space-y-1">
                          {profile.resume_improvements.immediate_fixes.slice(0, 5).map((f: string, i: number) => (
                            <li key={i}>• {f}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {profile.resume_improvements.keywords_to_add && (
                      <div>
                        <h4 className="font-semibold mb-2">Keywords to Add</h4>
                        <div className="flex flex-wrap gap-2">
                          {profile.resume_improvements.keywords_to_add.slice(0, 15).map((k: string) => (
                            <span key={k} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">{k}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </details>
              )}
            </div>
          ) : (
            <div>
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={uploadResumeFile}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              <p className="text-xs text-gray-500 mt-2">Supported: PDF, DOCX (max 10MB)</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* GitHub Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Github className="h-5 w-5" /> GitHub Profile
          </CardTitle>
          <CardDescription>Analyze repositories, languages, and contribution activity</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <input
              type="text"
              value={githubUsername}
              onChange={(e) => setGithubUsername(e.target.value)}
              placeholder="GitHub username (e.g., torvalds)"
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <Button onClick={analyzeGitHub} disabled={!githubUsername.trim()}>
              Analyze
            </Button>
          </div>

          {profile.github_analysis && !profile.github_analysis.error && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-3 border rounded-lg">
                  <p className="text-xs text-gray-600">Repositories</p>
                  <p className="text-lg font-bold">{profile.github_analysis.statistics?.total_repos || 0}</p>
                </div>
                <div className="p-3 border rounded-lg">
                  <p className="text-xs text-gray-600">Stars</p>
                  <p className="text-lg font-bold">{profile.github_analysis.statistics?.total_stars || 0}</p>
                </div>
                <div className="p-3 border rounded-lg">
                  <p className="text-xs text-gray-600">Followers</p>
                  <p className="text-lg font-bold">{profile.github_analysis.profile?.followers || 0}</p>
                </div>
                <div className="p-3 border rounded-lg">
                  <p className="text-xs text-gray-600">Activity</p>
                  <p className="text-lg font-bold">{profile.github_analysis.activity_level || 'N/A'}</p>
                </div>
              </div>

              {profile.github_analysis.languages && (
                <div>
                  <h4 className="font-semibold mb-2">Top Languages</h4>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(profile.github_analysis.languages).slice(0, 10).map(([lang, pct]: any) => (
                      <span key={lang} className="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">
                        {lang} {pct}%
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Career Score */}
      <Card>
        <CardHeader>
          <CardTitle>🎯 Career Score Calculation</CardTitle>
          <CardDescription>Combine all profile data to generate your career score</CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={calculateCareerScore} className="w-full" size="lg">
            Calculate Career Score
          </Button>
          {profile.career_score_data && (
            <div className="mt-4 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg text-center">
              <p className="text-6xl font-bold text-blue-600">{profile.career_score_data.total_score || 0}</p>
              <p className="text-gray-600 mt-2">out of 1000</p>
            </div>
          )}
        </CardContent>
      </Card>

      <p className="text-sm text-gray-500 text-center">
        ℹ️ For Certificates and Activities, use the dedicated pages in navigation
      </p>
    </div>
  )
}

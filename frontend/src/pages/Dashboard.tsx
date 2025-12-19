import { useEffect, useMemo, useState } from 'react'
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'
import { Award, BookOpen, Briefcase, Github, Target, Upload } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { careerScoreApi, internshipApi, learningApi, profileApi } from '@/lib/api'
import { useProfile } from '@/context/ProfileContext'

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a']

export default function Dashboard() {
  const { profile, setProfile, careerScore, setCareerScore, loading } = useProfile()

  const [calculatingScore, setCalculatingScore] = useState(false)
  const [internships, setInternships] = useState<any[]>([])
  const [learningPaths, setLearningPaths] = useState<any[]>([])
  const [profileStats, setProfileStats] = useState<any>(null)

  useEffect(() => {
    if (loading) return

    const run = async () => {
      try {
        const statsResponse = await profileApi.getStats(profile)
        setProfileStats(statsResponse.data)
      } catch {
        setProfileStats(null)
      }

      if (profile.resume_skills && profile.resume_skills.length > 0) {
        try {
          const response = await internshipApi.match({
            skills: profile.resume_skills,
            github_data: profile.github_analysis ?? undefined,
            career_score: careerScore?.total_score,
          })
          setInternships(response.data.matches?.slice(0, 4) || [])
        } catch {
          setInternships([])
        }

        try {
          const response = await learningApi.generateLearningPath({
            target_role: 'Software Engineer',
            current_skills: profile.resume_skills,
          })
          setLearningPaths([response.data])
        } catch {
          setLearningPaths([])
        }
      }
    }

    run()
  }, [loading, profile, careerScore])

  const handleCalculateScore = async () => {
    try {
      setCalculatingScore(true)
      const response = await careerScoreApi.calculate({
        resume_data: {
          ats_score: profile.ats_score,
          skills: profile.resume_skills || [],
          text: profile.resume_text || '',
        },
        github_data: profile.github_analysis || {},
        portfolio_analysis: profile.portfolio_analysis || {},
        certificates: profile.validated_certificates || [],
        activities: profile.activities || [],
        interview_data: {},
      })

      setCareerScore(response.data)
      setProfile((prev) => ({ ...prev, career_score_data: response.data }))
    } finally {
      setCalculatingScore(false)
    }
  }

  const radialData = useMemo(() => {
    if (!careerScore) return []
    return [{ name: 'Score', value: careerScore.total_score, fill: '#43e97b' }]
  }, [careerScore])

  const componentScoresData = useMemo(() => {
    if (!careerScore?.component_scores) return []
    return Object.entries(careerScore.component_scores).map(([key, value]) => ({
      name: key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
      value: typeof value === 'number' ? value : 0,
    }))
  }, [careerScore])

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28" />
          ))}
        </div>
        <Skeleton className="h-96" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Overview of your Skill Passport: score, progress, matches.</p>
        </div>
        <Button onClick={handleCalculateScore} disabled={calculatingScore}>
          <Target className="mr-2 h-4 w-4" />
          {calculatingScore ? 'Calculating…' : 'Recalculate Career Score'}
        </Button>
      </div>

      <Card className="bg-card/60">
        <CardHeader>
          <CardTitle>What is Skill Passport 360?</CardTitle>
          <CardDescription>
            A single dashboard that turns your scattered achievements (resume, GitHub, certificates, activities) into measurable career readiness.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="rounded-lg border border-border p-4 bg-background/40">
              <div className="text-sm font-semibold">How this helps you</div>
              <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                <li>• Get ATS score + improvement plan for your resume</li>
                <li>• Analyze your GitHub portfolio and activity</li>
                <li>• Track certificates + extracurriculars in one place</li>
                <li>• See a holistic career score (0–1000) and improve it over time</li>
              </ul>
            </div>
            <div className="rounded-lg border border-border p-4 bg-background/40">
              <div className="text-sm font-semibold">Quick start</div>
              <ol className="mt-2 space-y-1 text-sm text-muted-foreground list-decimal pl-5">
                <li>Open <span className="text-foreground">Profile Builder</span> and upload your resume.</li>
                <li>Run <span className="text-foreground">GitHub Analysis</span> with your username.</li>
                <li>Calculate <span className="text-foreground">Career Score</span> and review the breakdown.</li>
                <li>Check <span className="text-foreground">Internship Matching</span> for recommended roles.</li>
              </ol>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Resume ATS</CardTitle>
            <Upload className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profileStats?.ats_score || 0}/100</div>
            <p className="text-xs text-muted-foreground">{profileStats?.has_resume ? '✅ Resume loaded' : '⬜ No resume'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">GitHub Repos</CardTitle>
            <Github className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profile.github_analysis?.statistics?.total_repos || 0}</div>
            <p className="text-xs text-muted-foreground">{profileStats?.has_github ? '✅ Connected' : '⬜ Not connected'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Certificates</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profileStats?.cert_count || 0}</div>
            <p className="text-xs text-muted-foreground">
              {profileStats?.has_certificates ? '✅ Verified/added' : '⬜ None added'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Activities</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profileStats?.activity_count || 0}</div>
            <p className="text-xs text-muted-foreground">{profileStats?.has_activities ? '✅ Logged' : '⬜ None logged'}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" /> Holistic Career Score
            </CardTitle>
            <CardDescription>Career score (0–1000) from resume, GitHub, certificates, activities.</CardDescription>
          </CardHeader>
          <CardContent>
            {careerScore ? (
              <div className="relative flex items-center justify-center h-64">
                <ResponsiveContainer width="100%" height={280}>
                  <RadialBarChart
                    cx="50%"
                    cy="50%"
                    innerRadius="60%"
                    outerRadius="90%"
                    barSize={18}
                    data={radialData}
                    startAngle={90}
                    endAngle={-270}
                  >
                    <RadialBar dataKey="value" cornerRadius={10} fill="#43e97b" />
                  </RadialBarChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <div className="text-5xl font-bold text-green-300">{careerScore.total_score}</div>
                  <div className="text-sm text-muted-foreground">/ {careerScore.max_score}</div>
                  <div className="text-sm mt-1">{careerScore.label}</div>
                </div>
              </div>
            ) : (
              <div className="py-10 text-center text-muted-foreground">
                No career score yet. Go to <span className="text-foreground">Profile Builder</span> and add your data.
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Component Breakdown</CardTitle>
            <CardDescription>How the score is distributed across factors</CardDescription>
          </CardHeader>
          <CardContent>
            {componentScoresData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={componentScoresData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                    outerRadius={85}
                    dataKey="value"
                  >
                    {componentScoresData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="py-10 text-center text-muted-foreground">No component data yet</div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Briefcase className="h-5 w-5" /> Internship Matches
            </CardTitle>
            <CardDescription>Top matches based on your current skills</CardDescription>
          </CardHeader>
          <CardContent>
            {internships.length > 0 ? (
              <div className="space-y-4">
                {internships.map((internship: any, index: number) => (
                  <Card key={index} className="bg-secondary/50">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-lg">{internship.role || `Internship ${index + 1}`}</CardTitle>
                          <CardDescription>{internship.company || 'Company'}</CardDescription>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-semibold">{internship.stipend || 'N/A'}</div>
                          <div className="text-xs text-muted-foreground">{internship.location || 'Remote'}</div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2 mb-3">
                        {(internship.required_skills || []).slice(0, 4).map((skill: string, i: number) => (
                          <span key={i} className="px-2 py-1 text-xs bg-primary/20 rounded-md">
                            {skill}
                          </span>
                        ))}
                      </div>
                      <div className="flex items-center gap-2">
                        <Progress value={internship.match_score || 0} className="flex-1" />
                        <span className="text-sm font-medium">{internship.match_score || 0}%</span>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="py-10 text-center text-muted-foreground">
                No matches yet — add resume skills in Profile Builder.
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" /> Upskilling Paths
            </CardTitle>
            <CardDescription>AI-assisted suggestions (from backend)</CardDescription>
          </CardHeader>
          <CardContent>
            {learningPaths.length > 0 ? (
              <div className="space-y-3">
                {learningPaths.map((p: any, idx: number) => (
                  <div key={idx} className="rounded-lg border border-border p-3 bg-background/40">
                    <div className="text-sm font-semibold">{p?.target_role ?? 'Learning Path'}</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {typeof p?.learning_path === 'string' ? p.learning_path : 'Generated path'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-10 text-center text-muted-foreground">No learning paths yet</div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

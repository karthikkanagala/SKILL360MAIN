import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Progress } from '@/components/ui/progress'
import { RadialBarChart, RadialBar, ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import { 
  TrendingUp, 
  Award, 
  Code, 
  BookOpen, 
  Briefcase, 
  Target,
  Loader2,
  Upload,
  Github,
  GraduationCap,
  Activity,
  Sparkles,
  ShieldCheck,
  Users,
  Cpu,
  Brain,
  ArrowRight,
  CheckCircle2,
  Rocket
} from 'lucide-react'
import { careerScoreApi, profileApi, internshipApi, learningApi, systemApi } from '@/lib/api'

interface ProfileData {
  resume_text?: string
  resume_skills?: string[]
  ats_score?: number
  github_analysis?: any
  validated_certificates?: any[]
  activities?: any[]
  career_score_data?: any
}

interface CareerScore {
  total_score: number
  max_score: number
  label: string
  percentile: number
  trend: string
  component_scores?: any
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a']

export default function Landing() {
  const [profile, setProfile] = useState<ProfileData>({})
  const [careerScore, setCareerScore] = useState<CareerScore | null>(null)
  const [loading, setLoading] = useState(true)
  const [calculatingScore, setCalculatingScore] = useState(false)
  const [internships, setInternships] = useState<any[]>([])
  const [learningPaths, setLearningPaths] = useState<any[]>([])
  const [profileStats, setProfileStats] = useState<any>(null)
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null)

  const whyWeCreated = [
    {
      title: 'A single place to prove your skills',
      description:
        'Students and freshers usually have skills across resume, GitHub, certificates, and activities—but they are scattered. Skill Passport 360 brings them into one profile.',
    },
    {
      title: 'Make career progress measurable',
      description:
        'Instead of “I think I am ready”, you get clear metrics like ATS score, profile completeness, and a holistic career score to track growth over time.',
    },
    {
      title: 'Turn feedback into an action plan',
      description:
        'We wanted a platform that not only evaluates but also suggests what to learn next and what to build next, using ML-assisted insights.',
    },
  ]

  const whyUseUs = [
    'Instant resume ATS scoring + improvement suggestions',
    'GitHub portfolio analysis (projects, languages, consistency)',
    'Holistic career score (0–1000) with component breakdown',
    'Internship matching based on your skills and score',
    'Upskilling paths and project ideas tailored to your goals',
    'One dashboard that looks clean, modern, and easy to explain in interviews',
  ]

  const projectSections = [
    {
      id: 'features',
      title: 'What you get inside Skill Passport 360',
      items: [
        { icon: Target, label: 'Career Score', desc: 'A combined score that reflects your overall readiness.' },
        { icon: Upload, label: 'Resume + ATS', desc: 'Upload a resume and get ATS score + skills extraction.' },
        { icon: Github, label: 'GitHub Analyzer', desc: 'Analyze repos, languages, commits and portfolio strength.' },
        { icon: BookOpen, label: 'Learning Paths', desc: 'AI-assisted learning path suggestions for your target role.' },
        { icon: Briefcase, label: 'Internship Matching', desc: 'Matches internships to your skills and profile signals.' },
        { icon: Award, label: 'Certificates + Activities', desc: 'Track proof-of-work and achievements in one place.' },
      ],
    },
    {
      id: 'how-it-works',
      title: 'How it works (in simple steps)',
      steps: [
        { title: 'Add your data', desc: 'Resume, GitHub username, certificates, and activities.' },
        { title: 'AI/ML analysis', desc: 'Backend models compute scores, insights, and recommendations.' },
        { title: 'Dashboard output', desc: 'You get a clear dashboard to improve and showcase progress.' },
      ],
    },
    {
      id: 'tech',
      title: 'Tech stack / languages used',
      stack: [
        { label: 'Frontend', value: 'React + TypeScript + TailwindCSS (Vite)' },
        { label: 'Backend', value: 'Python + FastAPI (REST APIs)' },
        { label: 'ML / Analytics', value: 'Python ML modules (scoring, recommendations, NLP helpers)' },
        { label: 'Charts', value: 'Recharts' },
      ],
    },
  ]

  const teamMembers = [
    { name: 'Member 1', role: 'Frontend Developer', about: 'Built the UI, layouts, routing and charts.' },
    { name: 'Member 2', role: 'Backend Developer', about: 'Designed FastAPI routes and integrated the ML modules.' },
    { name: 'Member 3', role: 'ML Engineer', about: 'Worked on scoring logic, recommendations and analytics.' },
    { name: 'Member 4', role: 'Product / QA', about: 'Defined features, tested flows and improved UX copy.' },
  ]

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      setLoading(true)

      // Quick connectivity check (shows whether frontend <-> backend is connected)
      try {
        await systemApi.health()
        setBackendHealthy(true)
      } catch {
        setBackendHealthy(false)
      }

      // Load demo profile or existing profile
      const demoResponse = await profileApi.getDemo()
      const demoProfile = demoResponse.data
      setProfile(demoProfile)

      // Get profile stats
      const statsResponse = await profileApi.getStats(demoProfile)
      setProfileStats(statsResponse.data)

      // Load career score if exists
      if (demoProfile.career_score_data) {
        setCareerScore(demoProfile.career_score_data)
      }

      // Load internships and learning paths
      if (demoProfile.resume_skills) {
        loadInternships(demoProfile.resume_skills)
        loadLearningPaths(demoProfile.resume_skills)
      }
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadInternships = async (skills: string[]) => {
    try {
      const response = await internshipApi.match({
        skills,
        career_score: careerScore?.total_score,
      })
      setInternships(response.data.matches?.slice(0, 4) || [])
    } catch (error) {
      console.error('Error loading internships:', error)
    }
  }

  const loadLearningPaths = async (skills: string[]) => {
    try {
      // Get learning paths for top skills
      const topSkills = skills.slice(0, 3)
      const paths = await Promise.all(
        topSkills.map(() => 
          learningApi.generateLearningPath({
            target_role: 'Software Engineer',
            current_skills: skills,
          }).catch(() => null)
        )
      )
      setLearningPaths(paths.filter(Boolean).slice(0, 3))
    } catch (error) {
      console.error('Error loading learning paths:', error)
    }
  }

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
        certificates: profile.validated_certificates || [],
        activities: profile.activities || [],
        interview_data: {},
      })
      setCareerScore(response.data)
      setProfile(prev => ({ ...prev, career_score_data: response.data }))
    } catch (error) {
      console.error('Error calculating score:', error)
    } finally {
      setCalculatingScore(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 800) return '#43e97b' // Green
    if (score >= 700) return '#4facfe' // Blue
    if (score >= 600) return '#fa709a' // Pink
    if (score >= 500) return '#f093fb' // Purple
    return '#667eea' // Default
  }

  const getPercentileColor = (percentile: number) => {
    if (percentile >= 95) return 'text-green-400'
    if (percentile >= 85) return 'text-blue-400'
    if (percentile >= 70) return 'text-purple-400'
    return 'text-yellow-400'
  }

  // Prepare data for radial chart
  const radialData = careerScore ? [
    { name: 'Score', value: careerScore.total_score, fill: getScoreColor(careerScore.total_score) }
  ] : []

  // Prepare component scores for pie chart
  const componentScoresData = careerScore?.component_scores 
    ? Object.entries(careerScore.component_scores).map(([key, value]: [string, any]) => ({
        name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        value: typeof value === 'number' ? value : 0
      }))
    : []

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <Skeleton className="h-16 w-full" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <Skeleton key={i} className="h-32" />
            ))}
          </div>
          <Skeleton className="h-96 w-full" />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur supports-[backdrop-filter]:bg-card/60 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Rocket className="h-7 w-7 text-primary" />
              Skill Passport 360
            </h1>
            <p className="text-muted-foreground">Why we built it • Why you should use it • Live dashboard demo</p>
          </div>

          <nav className="flex flex-wrap gap-x-4 gap-y-2 text-sm">
            <a href="#why" className="text-muted-foreground hover:text-foreground transition-colors">Why</a>
            <a href="#benefits" className="text-muted-foreground hover:text-foreground transition-colors">Benefits</a>
            <a href="#project" className="text-muted-foreground hover:text-foreground transition-colors">Project</a>
            <a href="#demo" className="text-muted-foreground hover:text-foreground transition-colors">Dashboard</a>
            <a href="#about" className="text-muted-foreground hover:text-foreground transition-colors">About Us</a>
          </nav>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Section 1: Why Skill Passport 360 was created */}
        <section
          id="why"
          className="scroll-mt-24 relative overflow-hidden rounded-xl border border-border bg-gradient-to-br from-primary/15 via-background to-background"
        >
          <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top,rgba(99,102,241,0.25),transparent_55%)]" />
          <div className="relative p-6 md:p-10">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Sparkles className="h-4 w-4 text-primary" />
              <span>Skill Passport 360</span>
              <span className="opacity-50">•</span>
              <span>AI + ML powered career companion</span>
            </div>

            <h2 className="mt-4 text-3xl md:text-4xl font-bold tracking-tight">
              Built to help you prove skills, measure growth, and become internship/job ready.
            </h2>
            <p className="mt-3 text-muted-foreground max-w-3xl">
              This project was created to convert scattered career signals (resume + GitHub + certificates + activities)
              into one structured “passport” with clear scores, insights, and next steps.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Button
                onClick={() => document.querySelector('#demo')?.scrollIntoView({ behavior: 'smooth' })}
              >
                View Live Dashboard <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                onClick={() => document.querySelector('#about')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Meet the Team
              </Button>
            </div>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
              {whyWeCreated.map((item) => (
                <Card key={item.title} className="bg-card/70 backdrop-blur supports-[backdrop-filter]:bg-card/50">
                  <CardHeader>
                    <CardTitle className="text-lg">{item.title}</CardTitle>
                    <CardDescription>{item.description}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* Section 2: Why you should use our website */}
        <section id="benefits" className="scroll-mt-24">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-bold">Why you should use our website</h2>
          </div>
          <p className="text-muted-foreground mt-2 max-w-3xl">
            We focus on one thing: giving you a clean, explainable dashboard that turns your career data into decisions.
            Use the copy below as-is or edit it later.
          </p>

          <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-card/60">
              <CardHeader>
                <CardTitle className="text-lg">Key benefits</CardTitle>
                <CardDescription>Quick reasons to choose Skill Passport 360</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {whyUseUs.map((text) => (
                    <li key={text} className="flex items-start gap-3">
                      <CheckCircle2 className="h-5 w-5 text-primary mt-0.5" />
                      <span className="text-sm text-foreground/90">{text}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-card/60">
              <CardHeader>
                <CardTitle className="text-lg">What makes it different</CardTitle>
                <CardDescription>Random filler (you can modify later)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  Most tools evaluate only one area (resume OR GitHub OR courses). We combine them to give a 360° view.
                  The result is a simple story you can show to mentors, HR, and interviewers.
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-lg border border-border p-3">
                    <div className="flex items-center gap-2 text-sm font-semibold">
                      <Brain className="h-4 w-4 text-primary" />
                      ML Insights
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">Scoring + recommendations + analytics</div>
                  </div>
                  <div className="rounded-lg border border-border p-3">
                    <div className="flex items-center gap-2 text-sm font-semibold">
                      <Cpu className="h-4 w-4 text-primary" />
                      Fast APIs
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">FastAPI backend for modular features</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Section 3: Project details (ordered) */}
        <section id="project" className="scroll-mt-24 space-y-6">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-bold">Project sections (in order)</h2>
          </div>

          {/* 3A: Features */}
          <Card className="bg-card/60">
            <CardHeader>
              <CardTitle>{projectSections[0].title}</CardTitle>
              <CardDescription>These modules are connected with the backend APIs</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {projectSections[0].items.map((it: any) => {
                  const Icon = it.icon
                  return (
                    <div key={it.label} className="rounded-lg border border-border p-4 bg-background/40">
                      <div className="flex items-center gap-2 font-semibold">
                        <Icon className="h-4 w-4 text-primary" />
                        {it.label}
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">{it.desc}</p>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* 3B: How it works */}
          <Card className="bg-card/60">
            <CardHeader>
              <CardTitle>{projectSections[1].title}</CardTitle>
              <CardDescription>Simple flow from input → ML → dashboard</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {projectSections[1].steps.map((s: any, idx: number) => (
                  <div key={s.title} className="rounded-lg border border-border p-4 bg-background/40">
                    <div className="text-xs text-muted-foreground">Step {idx + 1}</div>
                    <div className="mt-1 font-semibold">{s.title}</div>
                    <div className="mt-1 text-sm text-muted-foreground">{s.desc}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* 3C: Tech stack */}
          <Card className="bg-card/60">
            <CardHeader>
              <CardTitle>{projectSections[2].title}</CardTitle>
              <CardDescription>Tech used by our team (edit freely later)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {projectSections[2].stack.map((row: any) => (
                  <div key={row.label} className="rounded-lg border border-border p-4 bg-background/40">
                    <div className="text-sm font-semibold">{row.label}</div>
                    <div className="text-sm text-muted-foreground mt-1">{row.value}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Section 4: Live dashboard (connected to backend) */}
        <section id="demo" className="scroll-mt-24">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-2xl font-bold">Live dashboard demo</h2>
              <p className="text-muted-foreground">These cards below are powered by the FastAPI + ML backend.</p>
            </div>

            <div className="flex items-center gap-2 text-sm">
              <span className="text-muted-foreground">Backend:</span>
              {backendHealthy === null ? (
                <span className="px-2 py-1 rounded-md border border-border bg-card/60">checking…</span>
              ) : backendHealthy ? (
                <span className="px-2 py-1 rounded-md border border-green-500/30 bg-green-500/10 text-green-300">connected</span>
              ) : (
                <span className="px-2 py-1 rounded-md border border-red-500/30 bg-red-500/10 text-red-300">not connected</span>
              )}
            </div>
          </div>
        </section>

        {/* Profile Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Resume ATS</CardTitle>
              <Upload className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{profileStats?.ats_score || 0}/100</div>
              <p className="text-xs text-muted-foreground">
                {profileStats?.has_resume ? '✅ Resume loaded' : '⬜ No resume'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">GitHub Repos</CardTitle>
              <Github className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {profile.github_analysis?.statistics?.total_repos || 0}
              </div>
              <p className="text-xs text-muted-foreground">
                {profileStats?.has_github ? '✅ Connected' : '⬜ Not connected'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Certificates</CardTitle>
              <GraduationCap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{profileStats?.cert_count || 0}</div>
              <p className="text-xs text-muted-foreground">
                {profileStats?.has_certificates ? '✅ Verified' : '⬜ None added'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Activities</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{profileStats?.activity_count || 0}</div>
              <p className="text-xs text-muted-foreground">
                {profileStats?.has_activities ? '✅ Logged' : '⬜ None logged'}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Career Score Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Radial Gauge Chart */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Holistic Career Score
              </CardTitle>
              <CardDescription>
                Comprehensive score based on resume, GitHub, certificates, and activities
              </CardDescription>
            </CardHeader>
            <CardContent>
              {calculatingScore ? (
                <div className="flex flex-col items-center justify-center h-64 space-y-4">
                  <Loader2 className="h-12 w-12 animate-spin text-primary" />
                  <p className="text-muted-foreground">Calculating your career score...</p>
                  <Skeleton className="h-4 w-64" />
                </div>
              ) : careerScore ? (
                <div className="space-y-6">
                  <div className="relative flex items-center justify-center h-64">
                    <ResponsiveContainer width="100%" height={300}>
                      <RadialBarChart
                        cx="50%"
                        cy="50%"
                        innerRadius="60%"
                        outerRadius="90%"
                        barSize={20}
                        data={radialData}
                        startAngle={90}
                        endAngle={-270}
                      >
                        <RadialBar
                          dataKey="value"
                          cornerRadius={10}
                          fill={getScoreColor(careerScore.total_score)}
                        />
                      </RadialBarChart>
                    </ResponsiveContainer>
                    <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                      <div className="text-5xl font-bold" style={{ color: getScoreColor(careerScore.total_score) }}>
                        {careerScore.total_score}
                      </div>
                      <div className="text-lg text-muted-foreground">/ {careerScore.max_score}</div>
                      <div className="text-sm font-medium mt-2">{careerScore.label}</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mt-6">
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${getPercentileColor(careerScore.percentile)}`}>
                        Top {100 - careerScore.percentile}%
                      </div>
                      <div className="text-xs text-muted-foreground">Percentile</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold">{careerScore.trend}</div>
                      <div className="text-xs text-muted-foreground">Trend</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold">
                        {careerScore.component_scores ? Object.keys(careerScore.component_scores).length : 0}
                      </div>
                      <div className="text-xs text-muted-foreground">Components</div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 space-y-4">
                  <Award className="h-16 w-16 text-muted-foreground" />
                  <p className="text-muted-foreground text-center">
                    Calculate your comprehensive career score (0-1000) based on all profile factors
                  </p>
                  <Button onClick={handleCalculateScore} disabled={calculatingScore}>
                    {calculatingScore ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Calculating...
                      </>
                    ) : (
                      <>
                        <Target className="mr-2 h-4 w-4" />
                        Calculate Career Score
                      </>
                    )}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Component Scores Pie Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Component Breakdown</CardTitle>
              <CardDescription>Score distribution across factors</CardDescription>
            </CardHeader>
            <CardContent>
              {componentScoresData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={componentScoresData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
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
                <div className="flex items-center justify-center h-64">
                  <p className="text-muted-foreground">No component scores available</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Internship Matching */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Internship Matching
              </CardTitle>
              <CardDescription>Top matches based on your profile</CardDescription>
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
                            <CardDescription>{internship.company || 'Company Name'}</CardDescription>
                          </div>
                          <div className="text-right">
                            <div className="text-sm font-semibold">{internship.stipend || 'N/A'}</div>
                            <div className="text-xs text-muted-foreground">{internship.location || 'Location'}</div>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="flex flex-wrap gap-2 mb-3">
                          {(internship.required_skills || []).slice(0, 3).map((skill: string, i: number) => (
                            <span key={i} className="px-2 py-1 text-xs bg-primary/20 rounded-md">
                              {skill}
                            </span>
                          ))}
                        </div>
                        <div className="flex items-center gap-2">
                          <Progress value={internship.match_score || 85} className="flex-1" />
                          <span className="text-sm font-medium">{internship.match_score || 85}% match</span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 space-y-4">
                  <Briefcase className="h-12 w-12 text-muted-foreground" />
                  <p className="text-muted-foreground text-center">
                    No internships matched yet. Build your profile to get personalized matches.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Upskilling Paths */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Upskilling Paths
              </CardTitle>
              <CardDescription>Recommended learning paths</CardDescription>
            </CardHeader>
            <CardContent>
              {learningPaths.length > 0 ? (
                <div className="space-y-4">
                  {learningPaths.map((_path, index) => (
                    <Card key={index} className="bg-secondary/50">
                      <CardHeader className="pb-3">
                        <CardTitle className="text-base">Path {index + 1}</CardTitle>
                        <CardDescription>Software Engineer Track</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center gap-2 mb-3">
                          <TrendingUp className="h-4 w-4 text-primary" />
                          <span className="text-sm">5 courses</span>
                        </div>
                        <Button variant="outline" size="sm" className="w-full">
                          View Path
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 space-y-4">
                  <BookOpen className="h-12 w-12 text-muted-foreground" />
                  <p className="text-muted-foreground text-center text-sm">
                    Get personalized learning paths based on your skills
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Skills Distribution */}
        {profile.resume_skills && profile.resume_skills.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5" />
                Skills Distribution
              </CardTitle>
              <CardDescription>Your technical skills breakdown</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {profile.resume_skills.slice(0, 20).map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 text-sm bg-primary/20 rounded-full border border-primary/30"
                  >
                    {skill}
                  </span>
                ))}
                {profile.resume_skills.length > 20 && (
                  <span className="px-3 py-1.5 text-sm text-muted-foreground">
                    +{profile.resume_skills.length - 20} more
                  </span>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Section 5: About us */}
        <section id="about" className="scroll-mt-24 space-y-6">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-bold">About Us</h2>
          </div>

          <Card className="bg-card/60">
            <CardHeader>
              <CardTitle>Team of 4 members</CardTitle>
              <CardDescription>
                Random intro text (edit later): We are a small team building an AI-assisted career platform for students.
                Our goal is to make career progress visible, trackable, and easy to present.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {teamMembers.map((m) => (
                  <div key={m.name} className="rounded-lg border border-border p-4 bg-background/40">
                    <div className="font-semibold">{m.name}</div>
                    <div className="text-sm text-primary/90 mt-1">{m.role}</div>
                    <div className="text-sm text-muted-foreground mt-2">{m.about}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card/60">
            <CardHeader>
              <CardTitle>Languages / tools we used</CardTitle>
              <CardDescription>Fillers you can modify later</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {[
                  'TypeScript',
                  'React',
                  'TailwindCSS',
                  'Vite',
                  'Python',
                  'FastAPI',
                  'Machine Learning',
                  'REST APIs',
                  'GitHub',
                ].map((t) => (
                  <span key={t} className="px-3 py-1.5 text-sm rounded-full border border-border bg-background/40">
                    {t}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>

          <footer className="pt-2 pb-10 text-center text-xs text-muted-foreground">
            © {new Date().getFullYear()} Skill Passport 360 • Built for project demo purposes
          </footer>
        </section>
      </div>
    </div>
  )
}


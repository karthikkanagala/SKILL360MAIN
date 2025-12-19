import { useEffect, useState } from 'react'
import { Briefcase } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { internshipApi } from '@/lib/api'
import { useProfile } from '@/context/ProfileContext'

function inputClass() {
  return 'w-full rounded-md border border-border bg-background/40 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/40'
}

export default function InternshipMatching() {
  const { profile, careerScore } = useProfile()
  const [location, setLocation] = useState('')
  const [matches, setMatches] = useState<any[]>([])
  const [status, setStatus] = useState<string | null>(null)

  const runMatch = async () => {
    const skills = profile.resume_skills || []
    if (skills.length === 0) {
      setStatus('Add resume skills first in Profile Builder.')
      return
    }

    setStatus('Matching internships…')
    try {
      const res = await internshipApi.match({
        skills,
        github_data: profile.github_analysis ?? undefined,
        career_score: careerScore?.total_score,
        location: location || undefined,
      })
      setMatches(res.data.matches || [])
      setStatus('Matches loaded ✅')
    } catch {
      setStatus('Match failed (check backend).')
    }
  }

  useEffect(() => {
    // Auto-run on first open if skills exist
    if ((profile.resume_skills || []).length > 0) runMatch()
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Internship Matching</h1>
        <p className="text-muted-foreground">Matches internships based on your skills and profile signals.</p>
      </div>

      {status && <div className="text-sm text-muted-foreground">{status}</div>}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Briefcase className="h-5 w-5" /> Match
          </CardTitle>
          <CardDescription>Uses /api/internship/match</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col md:flex-row gap-3 md:items-end">
          <div className="flex-1">
            <label className="text-xs text-muted-foreground">Location (optional)</label>
            <input className={inputClass()} value={location} onChange={(e) => setLocation(e.target.value)} />
          </div>
          <Button onClick={runMatch}>Run match</Button>
        </CardContent>
      </Card>

      <div className="space-y-4">
        {matches.length === 0 ? (
          <div className="text-sm text-muted-foreground">No matches yet.</div>
        ) : (
          matches.map((m, idx) => (
            <Card key={idx}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{m.role || `Internship ${idx + 1}`}</CardTitle>
                    <CardDescription>{m.company || 'Company'}</CardDescription>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold">{m.stipend || 'N/A'}</div>
                    <div className="text-xs text-muted-foreground">{m.location || 'Remote'}</div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex flex-wrap gap-2">
                  {(m.required_skills || []).slice(0, 10).map((s: string, i: number) => (
                    <span key={i} className="px-2 py-1 text-xs bg-primary/20 rounded-md">
                      {s}
                    </span>
                  ))}
                </div>

                <div className="flex items-center gap-2">
                  <Progress value={m.match_score || 0} className="flex-1" />
                  <div className="text-sm font-medium">{m.match_score || 0}%</div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}

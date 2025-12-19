import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { analyticsApi } from '@/lib/api'
import { useProfile } from '@/context/ProfileContext'

function inputClass() {
  return 'w-full rounded-md border border-border bg-background/40 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/40'
}

export default function Analytics() {
  const { profile, careerScore } = useProfile()

  const [peerComparison, setPeerComparison] = useState<any>(null)
  const [companyName, setCompanyName] = useState('')
  const [companyScore, setCompanyScore] = useState<any>(null)
  const [status, setStatus] = useState<string | null>(null)

  const runPeer = async () => {
    const score = careerScore?.total_score
    if (!score) {
      setStatus('Calculate career score first.')
      return
    }

    setStatus('Loading peer comparison…')
    try {
      const res = await analyticsApi.peerComparison(score)
      setPeerComparison(res.data)
      setStatus('Peer comparison loaded ✅')
    } catch {
      setStatus('Peer comparison failed (check backend).')
    }
  }

  const runCompany = async () => {
    setStatus('Calculating company scoring…')
    try {
      const res = await analyticsApi.companyScoring(profile, companyName || undefined)
      setCompanyScore(res.data)
      setStatus('Company scoring loaded ✅')
    } catch {
      setStatus('Company scoring failed (check backend).')
    }
  }

  const exportPdf = async () => {
    setStatus('Exporting PDF (demo endpoint)…')
    try {
      const res = await analyticsApi.exportPDF({ profile, careerScore })
      setStatus(res.data?.message || 'Exported')
    } catch {
      setStatus('Export PDF failed (check backend).')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted-foreground">Peer comparison + company-specific scoring.</p>
      </div>

      {status && <div className="text-sm text-muted-foreground">{status}</div>}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Peer Comparison</CardTitle>
            <CardDescription>Uses /api/analytics/peer-comparison</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button onClick={runPeer} disabled={!careerScore?.total_score}>
              Run peer comparison
            </Button>
            {peerComparison && (
              <pre className="text-xs rounded-md border border-border p-3 bg-black/30 overflow-auto">
                {JSON.stringify(peerComparison, null, 2)}
              </pre>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Company Scoring</CardTitle>
            <CardDescription>Uses /api/analytics/company-scoring</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <input
              className={inputClass()}
              placeholder="Company name (optional)"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
            />
            <div className="flex gap-2">
              <Button onClick={runCompany}>Calculate</Button>
              <Button variant="outline" onClick={exportPdf}>
                Export PDF (demo)
              </Button>
            </div>
            {companyScore && (
              <pre className="text-xs rounded-md border border-border p-3 bg-black/30 overflow-auto">
                {JSON.stringify(companyScore, null, 2)}
              </pre>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

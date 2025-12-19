import { useMemo, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { interviewApi } from '@/lib/api'
import { useProfile } from '@/context/ProfileContext'

function inputClass() {
  return 'w-full rounded-md border border-border bg-background/40 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/40'
}

export default function InterviewPrep() {
  const { profile } = useProfile()

  const [jobDescription, setJobDescription] = useState('')
  const [numQuestions, setNumQuestions] = useState(5)
  const [questions, setQuestions] = useState<any[]>([])
  const [selectedIndex, setSelectedIndex] = useState<number>(0)
  const [answer, setAnswer] = useState('')
  const [evaluation, setEvaluation] = useState<any>(null)
  const [status, setStatus] = useState<string | null>(null)

  const selectedQuestion = useMemo(() => questions[selectedIndex], [questions, selectedIndex])

  const generate = async () => {
    if (!profile.resume_text || profile.resume_text.trim().length < 50) {
      setStatus('Add resume text first in Profile Builder.')
      return
    }

    setStatus('Generating questions…')
    setEvaluation(null)

    try {
      const res = await interviewApi.generateQuestions({
        resume_text: profile.resume_text,
        job_description: jobDescription,
        num_questions: numQuestions,
      })
      setQuestions(res.data.questions || [])
      setSelectedIndex(0)
      setStatus('Questions generated ✅')
    } catch {
      setStatus('Failed to generate questions (check backend).')
    }
  }

  const evaluate = async () => {
    if (!selectedQuestion) return
    if (!answer.trim()) return

    setStatus('Evaluating answer…')
    try {
      const res = await interviewApi.evaluateAnswer({
        question: selectedQuestion,
        answer,
        resume_text: profile.resume_text || '',
      })
      setEvaluation(res.data)
      setStatus('Evaluation received ✅')
    } catch {
      setStatus('Failed to evaluate answer.')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Interview Prep</h1>
        <p className="text-muted-foreground">Generate questions from your resume and get feedback on answers.</p>
      </div>

      {status && <div className="text-sm text-muted-foreground">{status}</div>}

      <Card>
        <CardHeader>
          <CardTitle>Question Generator</CardTitle>
          <CardDescription>Uses backend endpoint /api/interview/generate-questions</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <textarea
            className={inputClass() + ' min-h-[120px]'}
            placeholder="Optional job description…"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <div className="flex items-center gap-3">
            <label className="text-sm text-muted-foreground"># Questions</label>
            <input
              className={inputClass()}
              style={{ maxWidth: 140 }}
              type="number"
              min={1}
              max={15}
              value={numQuestions}
              onChange={(e) => setNumQuestions(Number(e.target.value || 5))}
            />
            <Button onClick={generate}>Generate</Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Questions</CardTitle>
            <CardDescription>Select one question to answer.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {questions.length === 0 ? (
              <div className="text-sm text-muted-foreground">No questions yet.</div>
            ) : (
              <div className="space-y-2">
                {questions.map((q, idx) => (
                  <button
                    key={idx}
                    className={
                      'w-full text-left rounded-md border border-border px-3 py-2 text-sm ' +
                      (idx === selectedIndex ? 'bg-secondary' : 'bg-background/40 hover:bg-secondary/60')
                    }
                    onClick={() => setSelectedIndex(idx)}
                    type="button"
                  >
                    {q?.question || q?.title || `Question ${idx + 1}`}
                  </button>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Answer + Feedback</CardTitle>
            <CardDescription>Uses backend endpoint /api/interview/evaluate-answer</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm text-muted-foreground">Selected:</div>
            <div className="rounded-md border border-border p-3 bg-background/40 text-sm">
              {selectedQuestion?.question || selectedQuestion?.title || '—'}
            </div>

            <textarea
              className={inputClass() + ' min-h-[140px]'}
              placeholder="Write your answer…"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
            <Button onClick={evaluate} disabled={!selectedQuestion || !answer.trim()}>
              Evaluate Answer
            </Button>

            {evaluation && (
              <pre className="text-xs rounded-md border border-border p-3 bg-black/30 overflow-auto">
                {JSON.stringify(evaluation, null, 2)}
              </pre>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const teamMembers = [
  { name: 'Member 1', role: 'Frontend Developer', about: 'Built the UI, layouts, routing and charts.' },
  { name: 'Member 2', role: 'Backend Developer', about: 'Designed FastAPI routes and integrated the ML modules.' },
  { name: 'Member 3', role: 'ML Engineer', about: 'Worked on scoring logic, recommendations and analytics.' },
  { name: 'Member 4', role: 'Product / QA', about: 'Defined features, tested flows and improved UX copy.' },
]

export default function AboutUs() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">About Us</h1>
        <p className="text-muted-foreground">Team + tech used in this project.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Team of 4 members</CardTitle>
          <CardDescription>
            We are building an AI-assisted career platform to convert scattered achievements (resume, GitHub, certificates, activities)
            into one measurable Skill Passport.
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

      <Card>
        <CardHeader>
          <CardTitle>Languages / tools we used</CardTitle>
          <CardDescription>Frontend + backend stack</CardDescription>
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
        © {new Date().getFullYear()} Skill Passport 360
      </footer>
    </div>
  )
}

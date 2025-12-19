import { NavLink, Outlet } from 'react-router-dom'
import {
  Award,
  BarChart3,
  Briefcase,
  GraduationCap,
  LayoutDashboard,
  Rocket,
  UserRound,
  Users,
  FolderKanban,
  FileCheck,
  Target,
  Compass,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useProfile } from '@/context/ProfileContext'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/profile', label: 'Profile Builder', icon: UserRound },
  { to: '/portfolio', label: 'Portfolio', icon: FolderKanban },
  { to: '/certificates', label: 'Certificates', icon: FileCheck },
  { to: '/gap-analysis', label: 'Gap Analysis', icon: Target },
  { to: '/interview-prep', label: 'Interview Prep', icon: GraduationCap },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/internships', label: 'Internships', icon: Briefcase },
  { to: '/mentors', label: 'Mentorship', icon: Users },
  { to: '/opportunities', label: 'Opportunities', icon: Compass },
  { to: '/about', label: 'About Us', icon: Award },
]

export default function AppLayout() {
  const { backendHealthy } = useProfile()

  return (
    <div className="min-h-screen flex bg-background text-foreground">
      <aside className="w-64 border-r border-border bg-card/60 backdrop-blur supports-[backdrop-filter]:bg-card/50">
        <div className="px-4 py-4 flex items-center gap-2 border-b border-border">
          <Rocket className="h-5 w-5 text-primary" />
          <div className="font-semibold">Skill Passport 360</div>
        </div>

        <div className="p-4">
          <div className="text-xs text-muted-foreground mb-2">Navigation</div>
          <nav className="space-y-1">
            {navItems.map((it) => {
              const Icon = it.icon
              return (
                <NavLink
                  key={it.to}
                  to={it.to}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors',
                      'hover:bg-secondary/60 hover:text-foreground',
                      isActive ? 'bg-secondary text-foreground' : 'text-muted-foreground'
                    )
                  }
                >
                  <Icon className="h-4 w-4" />
                  {it.label}
                </NavLink>
              )
            })}
          </nav>

          <div className="mt-6 rounded-lg border border-border p-3 bg-background/40">
            <div className="text-xs text-muted-foreground">Backend status</div>
            {backendHealthy === null ? (
              <div className="mt-1 text-sm">checking…</div>
            ) : backendHealthy ? (
              <div className="mt-1 text-sm text-green-300">connected</div>
            ) : (
              <div className="mt-1 text-sm text-red-300">not connected</div>
            )}
          </div>
        </div>
      </aside>

      <main className="flex-1">
        <div className="max-w-7xl mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

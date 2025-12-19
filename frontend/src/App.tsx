import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import './App.css'

import AppLayout from '@/layouts/AppLayout'
import Landing from '@/pages/Landing'
import Dashboard from '@/pages/Dashboard'
import ProfileBuilder from '@/pages/ProfileBuilder'
import InterviewPrep from '@/pages/InterviewPrep'
import Analytics from '@/pages/Analytics'
import InternshipMatching from '@/pages/InternshipMatching'
import MentorshipMatching from '@/pages/MentorshipMatching'
import Portfolio from '@/pages/Portfolio'
import Certificates from '@/pages/Certificates'
import GapAnalysis from '@/pages/GapAnalysis'
import CareerOpportunities from '@/pages/CareerOpportunities'
import AboutUs from '@/pages/AboutUs'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default to the multi-page app (Dashboard + sidebar) */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/landing" element={<Landing />} />

        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<ProfileBuilder />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/certificates" element={<Certificates />} />
          <Route path="/gap-analysis" element={<GapAnalysis />} />
          <Route path="/interview-prep" element={<InterviewPrep />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/internships" element={<InternshipMatching />} />
          <Route path="/mentors" element={<MentorshipMatching />} />
          <Route path="/opportunities" element={<CareerOpportunities />} />
          <Route path="/about" element={<AboutUs />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App



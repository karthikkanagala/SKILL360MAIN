import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { profileApi, systemApi } from '@/lib/api'

export interface ProfileData {
  resume_text?: string
  resume_skills?: string[]
  ats_score?: number
  ats_analysis?: any
  resume_improvements?: any
  github_analysis?: any
  validated_certificates?: any[]
  activities?: any[]
  interview_evaluations?: any[]
  career_score_data?: any
  portfolio_analysis?: any
}

export interface CareerScore {
  total_score: number
  max_score: number
  label: string
  percentile: number
  trend: string
  component_scores?: Record<string, number>
}

type ProfileContextValue = {
  profile: ProfileData
  setProfile: React.Dispatch<React.SetStateAction<ProfileData>>
  careerScore: CareerScore | null
  setCareerScore: React.Dispatch<React.SetStateAction<CareerScore | null>>
  loading: boolean
  backendHealthy: boolean | null
  refreshDemo: () => Promise<void>
}

const ProfileContext = createContext<ProfileContextValue | undefined>(undefined)

export function ProfileProvider({ children }: { children: React.ReactNode }) {
  const [profile, setProfile] = useState<ProfileData>({})
  const [careerScore, setCareerScore] = useState<CareerScore | null>(null)
  const [loading, setLoading] = useState(true)
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null)

  const refreshDemo = async () => {
    setLoading(true)

    try {
      try {
        await systemApi.health()
        setBackendHealthy(true)
      } catch {
        setBackendHealthy(false)
      }

      const demoResponse = await profileApi.getDemo()
      const demoProfile = demoResponse.data
      setProfile(demoProfile)
      setCareerScore(demoProfile?.career_score_data ?? null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refreshDemo()
  }, [])

  const value = useMemo(
    () => ({
      profile,
      setProfile,
      careerScore,
      setCareerScore,
      loading,
      backendHealthy,
      refreshDemo,
    }),
    [profile, careerScore, loading, backendHealthy]
  )

  return <ProfileContext.Provider value={value}>{children}</ProfileContext.Provider>
}

export function useProfile() {
  const ctx = useContext(ProfileContext)
  if (!ctx) throw new Error('useProfile must be used within ProfileProvider')
  return ctx
}

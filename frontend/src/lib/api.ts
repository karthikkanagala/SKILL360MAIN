import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// System API
export const systemApi = {
  health: () => api.get('/health'),
  root: () => api.get('/'),
};

// Resume API
export const resumeApi = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  analyzeText: (text: string) => {
    return api.post('/api/resume/analyze-text', { text });
  },
};

// Career Score API
export const careerScoreApi = {
  calculate: (profileData: any) => {
    return api.post('/api/career-score/calculate', profileData);
  },
  getHistory: () => {
    return api.get('/api/career-score/history');
  },
};

// GitHub API
export const githubApi = {
  analyze: (username: string) => {
    return api.post('/api/github/analyze', { username });
  },
  portfolio: (username: string) => {
    return api.post('/api/github/portfolio', { username });
  },
};

// Interview API
export const interviewApi = {
  generateQuestions: (data: any) => {
    return api.post('/api/interview/generate-questions', data);
  },
  evaluateAnswer: (data: any) => {
    return api.post('/api/interview/evaluate-answer', data);
  },
};

// Learning API
export const learningApi = {
  searchCourses: (skill: string, difficulty?: string) => {
    return api.post('/api/learning/courses/search', { skill, difficulty });
  },
  getAIRecommendations: (skill: string) => {
    return api.post('/api/learning/courses/ai-recommendations', { skill });
  },
  generateLearningPath: (data: any) => {
    return api.post('/api/learning/learning-path', data);
  },
  generateProjectIdeas: (data: any) => {
    return api.post('/api/learning/project-ideas', data);
  },
  getResources: (skill: string) => {
    return api.get(`/api/learning/resources/${skill}`);
  },
};

// Analytics API
export const analyticsApi = {
  peerComparison: (careerScore: number) => {
    return api.post('/api/analytics/peer-comparison', { career_score: careerScore });
  },
  companyScoring: (profileData: any, companyName?: string) => {
    return api.post('/api/analytics/company-scoring', {
      profile_data: profileData,
      company_name: companyName,
    });
  },
  exportPDF: (data: any) => {
    return api.post('/api/analytics/export-pdf', data);
  },
};

// Internship API
export const internshipApi = {
  match: (data: any) => {
    return api.post('/api/internship/match', data);
  },
  listAll: () => {
    return api.get('/api/internship/list');
  },
};

// Profile API
export const profileApi = {
  checkCompleteness: (profile: any) => {
    return api.post('/api/profile/completeness', profile);
  },
  getDemo: () => {
    return api.get('/api/profile/demo');
  },
  getStats: (profile: any) => {
    return api.post('/api/profile/stats', profile);
  },
};

// Certificates API
export const certificatesApi = {
  verifyUrl: (url: string) => {
    return api.post('/api/certificates/verify-url', { url });
  },
  analyzeText: (text: string, source?: string) => {
    return api.post('/api/certificates/analyze-text', { text, source: source || 'manual' });
  },
  scanGithub: (githubData: any) => {
    return api.post('/api/certificates/scan-github', { github_data: githubData });
  },
  uploadPdf: (formData: FormData) => {
    return api.post('/api/certificates/upload-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Mentorship API
export const mentorshipApi = {
  match: (data: { skills: string[], experience_level?: string, mentorship_type?: string }) => {
    return api.post('/api/mentorship/match', data);
  },
};

// Opportunities API
export const opportunitiesApi = {
  search: (data: { skills: string[], target_role?: string, location?: string }) => {
    return api.post('/api/opportunities/search', data);
  },
};

// Gap Analysis API
export const gapAnalysisApi = {
  analyze: (data: {
    target_role: string,
    job_description?: string,
    current_skills?: string[],
    resume_text?: string
  }) => {
    return api.post('/api/gap-analysis/analyze', data);
  },
};



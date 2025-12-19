import { useState } from 'react';
import { Users } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useProfile } from '@/context/ProfileContext';
import { mentorshipApi } from '@/lib/api';

export default function MentorshipMatching() {
  const { profile } = useProfile();
  const [loading, setLoading] = useState(false);
  const [mentors, setMentors] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('Beginner');
  const [mentorshipType, setMentorshipType] = useState('Career');

  const searchMentors = async () => {
    const skills = profile.resume_skills || [];
    
    if (skills.length === 0) {
      setError('Please add resume skills first in Profile Builder');
      return;
    }

    setLoading(true);
    setError('');
    setMentors([]);

    try {
      const response = await mentorshipApi.match({
        skills: skills.map(s => String(s)),
        experience_level: experienceLevel,
        mentorship_type: mentorshipType,
      });
      setMentors(response.data.matches || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to find mentors');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">👥 Mentorship Matching</h1>
        <p className="text-gray-600">
          Find mentors who can guide you in your career journey
        </p>
      </div>

      {/* Search Form */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" /> Find Mentors
          </CardTitle>
          <CardDescription>
            Based on your skills from Profile Builder
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold mb-2">Experience Level</label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold mb-2">Mentorship Type</label>
              <select
                value={mentorshipType}
                onChange={(e) => setMentorshipType(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option>Career</option>
                <option>Technical</option>
                <option>Leadership</option>
                <option>General</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>Your Skills:</span>
            {profile.resume_skills && profile.resume_skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {profile.resume_skills.slice(0, 5).map((skill: any, idx: number) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs"
                  >
                    {skill}
                  </span>
                ))}
                {profile.resume_skills.length > 5 && (
                  <span className="text-xs text-gray-500">
                    +{profile.resume_skills.length - 5} more
                  </span>
                )}
              </div>
            ) : (
              <span className="text-red-500">No skills found. Add resume in Profile Builder.</span>
            )}
          </div>

          <Button
            onClick={searchMentors}
            disabled={loading || !profile.resume_skills || profile.resume_skills.length === 0}
            className="w-full"
          >
            {loading ? 'Searching...' : 'Find Mentors'}
          </Button>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Results */}
      {mentors.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">🎯 Recommended Mentors</h2>
          {mentors.map((mentor, idx) => (
            <Card key={idx}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-xl">{mentor.name}</CardTitle>
                    <CardDescription className="text-base">{mentor.role || mentor.title}</CardDescription>
                  </div>
                  {mentor.match_score !== undefined && (
                    <div className="text-right">
                      <div className="text-3xl font-bold text-green-600">
                        {mentor.match_score}%
                      </div>
                      <div className="text-xs text-gray-600">Match</div>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {mentor.bio && (
                  <p className="text-gray-700">{mentor.bio}</p>
                )}

                {mentor.expertise && mentor.expertise.length > 0 && (
                  <div>
                    <span className="font-semibold text-gray-700">Expertise:</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {mentor.expertise.map((skill: string, sidx: number) => (
                        <span
                          key={sidx}
                          className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {mentor.experience && (
                  <div className="text-sm text-gray-600">
                    <span className="font-semibold">Experience:</span> {mentor.experience}
                  </div>
                )}

                {mentor.contact && (
                  <div className="text-sm">
                    <span className="font-semibold text-gray-700">Contact:</span>{' '}
                    <a href={`mailto:${mentor.contact}`} className="text-blue-600 hover:underline">
                      {mentor.contact}
                    </a>
                  </div>
                )}

                {mentor.linkedin && (
                  <a
                    href={mentor.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                  >
                    Connect on LinkedIn →
                  </a>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

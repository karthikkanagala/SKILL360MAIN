import React, { useState } from 'react';
import { certificatesApi } from '../lib/api';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function Certificates() {
  const [activeTab, setActiveTab] = useState<'url' | 'text' | 'pdf'>('pdf');
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState('');

  const uploadPdf = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are supported');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File too large (max 10MB)');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    setUploadProgress('📄 Reading PDF...');

    try {
      const formData = new FormData();
      formData.append('file', file);

      setUploadProgress('🔍 Analyzing certificate...');
      const response = await certificatesApi.uploadPdf(formData);
      
      setResult(response.data);
      setUploadProgress('');
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to analyze certificate PDF';
      setError(errorMsg);
      setUploadProgress('');
      
      // Show specific error messages based on common issues
      if (errorMsg.includes('extract text')) {
        setError(errorMsg + ' This may be an image-based PDF. Try using OCR tools first or enter text manually in the "Analyze Text" tab.');
      }
    } finally {
      setLoading(false);
    }
  };

  const verifyUrl = async () => {
    if (!url.trim()) {
      setError('Please enter a certificate URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await certificatesApi.verifyUrl(url.trim());
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to verify certificate');
    } finally {
      setLoading(false);
    }
  };

  const analyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter certificate text');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await certificatesApi.analyzeText(text.trim());
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze certificate');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">🎓 Certificate Verification</h1>
        <p className="text-gray-600">
          Verify and analyze your professional certificates and certifications
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab('pdf')}
          className={`px-6 py-2 rounded-lg font-semibold ${
            activeTab === 'pdf'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          📄 Upload PDF
        </button>
        <button
          onClick={() => setActiveTab('url')}
          className={`px-6 py-2 rounded-lg font-semibold ${
            activeTab === 'url'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          🔗 Verify URL
        </button>
        <button
          onClick={() => setActiveTab('text')}
          className={`px-6 py-2 rounded-lg font-semibold ${
            activeTab === 'text'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          📝 Analyze Text
        </button>
      </div>

      {/* PDF Upload Tab */}
      {activeTab === 'pdf' && (
        <Card className="p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Upload Certificate PDF</h2>
          <p className="text-sm text-gray-600 mb-4">
            Upload your certificate PDF for comprehensive analysis including authenticity verification and skill extraction
          </p>
          <div className="space-y-4">
            <input
              type="file"
              accept=".pdf"
              onChange={uploadPdf}
              disabled={loading}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
            />
            {uploadProgress && (
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
                {uploadProgress}
              </div>
            )}
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">What we analyze:</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>✓ Certificate authenticity (multi-factor verification)</li>
              <li>✓ Platform/issuer validation</li>
              <li>✓ Skills extraction (ML-powered)</li>
              <li>✓ Career value assessment</li>
              <li>✓ Completion date & certificate ID</li>
              <li>✓ Verification URL detection</li>
            </ul>
          </div>
        </Card>
      )}

      {/* URL Verification Tab */}
      {activeTab === 'url' && (
        <Card className="p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Verify Certificate URL</h2>
          <p className="text-sm text-gray-600 mb-4">
            Enter a URL from platforms like Coursera, Udemy, LinkedIn Learning, etc.
          </p>
          <div className="flex gap-4">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && verifyUrl()}
              placeholder="https://www.coursera.org/account/accomplishments/..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Button onClick={verifyUrl} disabled={loading} className="px-6">
              {loading ? 'Verifying...' : 'Verify'}
            </Button>
          </div>
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </Card>
      )}

      {/* Text Analysis Tab */}
      {activeTab === 'text' && (
        <Card className="p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Analyze Certificate Text</h2>
          <p className="text-sm text-gray-600 mb-4">
            Paste your certificate details (title, issuer, date, etc.)
          </p>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Certificate Title: AWS Certified Solutions Architect&#10;Issuer: Amazon Web Services&#10;Date: January 2025&#10;Credential ID: ABC123..."
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[150px]"
          />
          <Button
            onClick={analyzeText}
            disabled={loading}
            className="mt-4 px-6"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </Button>
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </Card>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Authenticity Score (for PDF uploads) */}
          {result.authenticity_score !== undefined && (
            <Card className={`p-6 border-2 ${
              result.authenticity_score >= 75 ? 'bg-green-50 border-green-300' :
              result.authenticity_score >= 50 ? 'bg-blue-50 border-blue-300' :
              result.authenticity_score >= 30 ? 'bg-yellow-50 border-yellow-300' :
              'bg-red-50 border-red-300'
            }`}>
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold mb-2">
                    {result.authenticity_level}
                  </h2>
                  <div className="text-5xl font-bold mb-3" style={{ color: result.authenticity_color }}>
                    {result.authenticity_score}/100
                  </div>
                  <p className="text-gray-700 mb-4">Authenticity Score</p>
                </div>
                <div className={`px-4 py-2 rounded-full text-sm font-semibold ${
                  result.verified ? 'bg-green-600 text-white' : 'bg-gray-400 text-white'
                }`}>
                  {result.verified ? '✓ Verified' : '? Unverified'}
                </div>
              </div>
              
              {result.authenticity_factors && (
                <div className="mt-4 space-y-2">
                  <h3 className="font-semibold text-gray-700">Authenticity Factors:</h3>
                  {result.authenticity_factors.map((factor: string, idx: number) => (
                    <div key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                      <span>•</span>
                      <span>{factor}</span>
                    </div>
                  ))}
                </div>
              )}

              {result.warnings && result.warnings.length > 0 && (
                <div className="mt-4 space-y-2">
                  <h3 className="font-semibold text-gray-700">Alerts:</h3>
                  {result.warnings.map((warning: string, idx: number) => (
                    <div key={idx} className="text-sm p-2 bg-white rounded border">
                      {warning}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}

          {/* Certificate Details */}
          <Card className="p-6">
            <h2 className="text-2xl font-bold mb-4">📜 Certificate Information</h2>
            <div className="grid gap-4">
              {result.filename && (
                <div>
                  <label className="font-semibold text-gray-700">File:</label>
                  <p className="text-sm font-mono">{result.filename}</p>
                </div>
              )}
              {result.metadata?.certificate_name && (
                <div>
                  <label className="font-semibold text-gray-700">Certificate Name:</label>
                  <p className="text-lg">{result.metadata.certificate_name}</p>
                </div>
              )}
              {result.platform && (
                <div>
                  <label className="font-semibold text-gray-700">Platform:</label>
                  <p>{result.platform} {result.platform_category && `(${result.platform_category})`}</p>
                </div>
              )}
              {result.metadata?.issuer && result.metadata.issuer !== 'Unknown' && (
                <div>
                  <label className="font-semibold text-gray-700">Issuer:</label>
                  <p>{result.metadata.issuer}</p>
                </div>
              )}
              {result.metadata?.completion_date && (
                <div>
                  <label className="font-semibold text-gray-700">Completion Date:</label>
                  <p>{result.metadata.completion_date}</p>
                </div>
              )}
              {result.metadata?.certificate_id && (
                <div>
                  <label className="font-semibold text-gray-700">Certificate ID:</label>
                  <p className="font-mono text-sm bg-gray-100 px-2 py-1 rounded inline-block">
                    {result.metadata.certificate_id}
                  </p>
                </div>
              )}
              {result.metadata?.recipient_name && (
                <div>
                  <label className="font-semibold text-gray-700">Recipient:</label>
                  <p>{result.metadata.recipient_name}</p>
                </div>
              )}
              {result.metadata?.verification_urls && result.metadata.verification_urls.length > 0 && (
                <div>
                  <label className="font-semibold text-gray-700 mb-2 block">Verification URLs:</label>
                  {result.metadata.verification_urls.map((url: string, idx: number) => (
                    <a
                      key={idx}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline text-sm block truncate"
                    >
                      🔗 {url}
                    </a>
                  ))}
                </div>
              )}
              {result.text_extracted && (
                <div>
                  <label className="font-semibold text-gray-700">Text Extracted:</label>
                  <p className="text-sm text-gray-600">{result.text_extracted} characters from {result.pages} page(s)</p>
                </div>
              )}
            </div>
          </Card>

          {/* Skills Extracted */}
          {result.skills && result.skills.length > 0 && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">🎯 Skills Extracted</h2>
              <p className="text-sm text-gray-600 mb-4">
                Found {result.total_skills_found || result.skills.length} skills using ML + pattern matching
              </p>
              <div className="flex flex-wrap gap-2">
                {result.skills.map((skill: string, idx: number) => {
                  const confidence = result.skills_confidence?.[skill];
                  return (
                    <span
                      key={idx}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        confidence >= 0.9 ? 'bg-green-100 text-green-700' :
                        confidence >= 0.8 ? 'bg-blue-100 text-blue-700' :
                        'bg-gray-100 text-gray-700'
                      }`}
                      title={confidence ? `Confidence: ${(confidence * 100).toFixed(0)}%` : ''}
                    >
                      {skill}
                    </span>
                  );
                })}
              </div>
            </Card>
          )}

          {/* Career Value */}
          {result.career_value_score !== undefined && (
            <Card className="p-6 bg-gradient-to-r from-purple-50 to-blue-50">
              <h2 className="text-2xl font-bold mb-4">💼 Career Value Assessment</h2>
              <div className="mb-4">
                <div className="text-5xl font-bold text-purple-600 mb-2">
                  {result.career_value_score}/100
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
                  <div
                    className="bg-purple-600 h-3 rounded-full transition-all"
                    style={{ width: `${result.career_value_score}%` }}
                  ></div>
                </div>
                <p className="text-gray-700">
                  {result.career_value_score >= 80
                    ? '🌟 Highly valuable certification! Strong impact on career prospects.'
                    : result.career_value_score >= 60
                    ? '👍 Valuable certification with good career relevance.'
                    : result.career_value_score >= 40
                    ? '📚 Good foundation certification for skill development.'
                    : '📖 Entry-level certification - consider adding more specialized certs.'}
                </p>
              </div>
            </Card>
          )}

          {/* Validation Status (for URL/Text analysis) */}
          {result.valid !== undefined && (
            <Card
              className={`p-6 ${
                result.valid
                  ? 'bg-green-50 border-green-200'
                  : 'bg-yellow-50 border-yellow-200'
              }`}
            >
              <h2 className="text-2xl font-bold mb-2">
                {result.valid ? '✓ Verified' : '⚠ Unverified'}
              </h2>
              <p className="text-gray-700">
                {result.valid
                  ? 'This certificate appears to be valid'
                  : 'Could not automatically verify this certificate'}
              </p>
            </Card>
          )}

          {/* Legacy fields for URL/Text analysis */}
          {(result.title || result.issuer || result.date || result.credential_id) && !result.metadata && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">📜 Certificate Details</h2>
              <div className="grid gap-4">
                {result.title && (
                  <div>
                    <label className="font-semibold text-gray-700">Title:</label>
                    <p className="text-lg">{result.title}</p>
                  </div>
                )}
                {result.issuer && (
                  <div>
                    <label className="font-semibold text-gray-700">Issuer:</label>
                    <p>{result.issuer}</p>
                  </div>
                )}
                {result.date && (
                  <div>
                    <label className="font-semibold text-gray-700">
                      Issue Date:
                    </label>
                    <p>{result.date}</p>
                  </div>
                )}
                {result.credential_id && (
                  <div>
                    <label className="font-semibold text-gray-700">
                      Credential ID:
                    </label>
                    <p className="font-mono text-sm">{result.credential_id}</p>
                  </div>
                )}
              </div>
            </Card>
          )}

          {/* Career Value (legacy) */}
          {result.career_value !== undefined && (
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-4">💼 Career Value</h2>
              <div className="mb-4">
                <div className="text-4xl font-bold text-blue-600">
                  {result.career_value}/100
                </div>
                <p className="text-gray-600 mt-2">
                  {result.career_value >= 80
                    ? 'Highly valuable certification!'
                    : result.career_value >= 50
                    ? 'Valuable certification for your career'
                    : 'Good foundation certification'}
                </p>
              </div>
              {result.recommendation && (
                <p className="text-gray-700 italic">"{result.recommendation}"</p>
              )}
            </Card>
          )}

          {/* Message/Notes */}
          {result.message && (
            <Card className="p-6 bg-blue-50 border-blue-200">
              <p className="text-gray-700">{result.message}</p>
            </Card>
          )}

          {/* Raw JSON */}
          <details className="mt-6">
            <summary className="cursor-pointer text-gray-600 hover:text-gray-900">
              View Raw JSON
            </summary>
            <pre className="mt-2 p-4 bg-gray-50 rounded-lg overflow-auto text-sm">
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

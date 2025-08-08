import React, { useState, useEffect } from 'react';
import { Save, RefreshCw, AlertCircle, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const SettingsPage = () => {
  const [jobRequirements, setJobRequirements] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);

  useEffect(() => {
    fetchJobRequirements();
  }, []);

  const fetchJobRequirements = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/job-requirements');
      const data = await response.json();
      setJobRequirements(data.requirements || '');
    } catch (error) {
      console.error('Error fetching job requirements:', error);
      toast.error('Failed to fetch job requirements');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('/api/update-job-requirements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ requirements: jobRequirements }),
      });

      const result = await response.json();

      if (result.success) {
        toast.success('Job requirements updated successfully');
        setLastSaved(new Date());
      } else {
        toast.error(result.error || 'Failed to update job requirements');
      }
    } catch (error) {
      console.error('Error saving job requirements:', error);
      toast.error('Failed to save job requirements');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset the job requirements?')) {
      setJobRequirements('');
      setLastSaved(null);
      toast.success('Job requirements reset');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-500">
          Configure job requirements and system settings
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Job Requirements */}
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Job Requirements</h3>
              {lastSaved && (
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Last saved: {lastSaved.toLocaleTimeString()}
                </div>
              )}
            </div>

            {isLoading ? (
              <div className="flex items-center justify-center h-32">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Define Job Requirements
                  </label>
                  <textarea
                    value={jobRequirements}
                    onChange={(e) => setJobRequirements(e.target.value)}
                    placeholder="Enter the skills, experience, and qualifications required for the position..."
                    className="input-field h-64 resize-none"
                    rows="12"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Describe the ideal candidate profile. This will be used to calculate match scores for all candidates.
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="btn-primary flex items-center gap-2"
                  >
                    {isSaving ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="h-4 w-4" />
                        Save Requirements
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleReset}
                    className="btn-secondary flex items-center gap-2"
                  >
                    <RefreshCw className="h-4 w-4" />
                    Reset
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Requirements Guidelines */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Guidelines</h3>
            <div className="space-y-4 text-sm text-gray-600">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">What to include:</h4>
                <ul className="space-y-1 list-disc list-inside">
                  <li>Required technical skills (e.g., Python, React, AWS)</li>
                  <li>Experience level and years of experience</li>
                  <li>Educational requirements</li>
                  <li>Soft skills and competencies</li>
                  <li>Industry-specific knowledge</li>
                  <li>Certifications or licenses</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Tips for better matching:</h4>
                <ul className="space-y-1 list-disc list-inside">
                  <li>Be specific about skill levels (e.g., "Advanced Python" vs "Python")</li>
                  <li>Include both technical and soft skills</li>
                  <li>Mention industry experience if relevant</li>
                  <li>Specify required tools and technologies</li>
                  <li>Include any mandatory certifications</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* System Information */}
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">System Information</h3>
            <div className="space-y-3 text-sm">
              <div>
                <label className="text-gray-500">AI Model</label>
                <p className="text-gray-900">SpaCy + Scikit-learn</p>
              </div>
              <div>
                <label className="text-gray-500">Supported Formats</label>
                <p className="text-gray-900">PDF, DOCX, DOC, TXT</p>
              </div>
              <div>
                <label className="text-gray-500">Max File Size</label>
                <p className="text-gray-900">16 MB</p>
              </div>
              <div>
                <label className="text-gray-500">Processing Time</label>
                <p className="text-gray-900">5-15 seconds</p>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Match Scoring</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">High Match</span>
                <span className="badge badge-success">≥70%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Medium Match</span>
                <span className="badge badge-warning">40-69%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Low Match</span>
                <span className="badge badge-danger">&lt;40%</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Features</h3>
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>AI-powered resume parsing</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Skill matching algorithm</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Interview recommendations</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Customizable job requirements</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Candidate management</span>
              </div>
            </div>
          </div>

          <div className="card bg-blue-50 border-blue-200">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="text-sm font-medium text-blue-900">Note</h4>
                <p className="text-sm text-blue-700 mt-1">
                  Updating job requirements will recalculate match scores for all existing candidates.
                  This may take a few moments to complete.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;

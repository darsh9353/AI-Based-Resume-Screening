import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import toast from 'react-hot-toast';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [jobRequirements, setJobRequirements] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setUploadedFile(acceptedFiles[0]);
      setAnalysisResult(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt']
    },
    multiple: false,
    maxSize: 16 * 1024 * 1024 // 16MB
  });

  const handleUpload = async () => {
    if (!uploadedFile) {
      toast.error('Please select a file first');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', uploadedFile);
    formData.append('job_requirements', jobRequirements);

    try {
      const response = await fetch('/api/upload-resume', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        setAnalysisResult(result);
        toast.success('Resume analyzed successfully!');
        if (onUploadSuccess) {
          onUploadSuccess();
        }
      } else {
        toast.error(result.error || 'Failed to analyze resume');
      }
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Failed to upload resume. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.7) return 'text-green-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score) => {
    if (score >= 0.7) return 'badge-success';
    if (score >= 0.4) return 'badge-warning';
    return 'badge-danger';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Upload Resume</h1>
        <p className="mt-1 text-sm text-gray-500">
          Upload candidate resumes for AI-powered analysis and interview recommendations
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload Section */}
        <div className="space-y-6">
          {/* File Upload */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Resume</h3>
            
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                {isDragActive ? (
                  <p className="text-sm text-blue-600">Drop the file here...</p>
                ) : (
                  <div>
                    <p className="text-sm text-gray-600">
                      Drag and drop a resume file here, or click to select
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Supports PDF, DOCX, DOC, and TXT files (max 16MB)
                    </p>
                  </div>
                )}
              </div>
            </div>

            {uploadedFile && (
              <div className="mt-4 p-4 bg-green-50 rounded-lg">
                <div className="flex items-center">
                  <FileText className="h-5 w-5 text-green-600 mr-2" />
                  <span className="text-sm font-medium text-green-800">
                    {uploadedFile.name}
                  </span>
                  <span className="text-xs text-green-600 ml-2">
                    ({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Job Requirements */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Job Requirements</h3>
            <textarea
              value={jobRequirements}
              onChange={(e) => setJobRequirements(e.target.value)}
              placeholder="Enter job requirements, skills, and qualifications..."
              className="input-field h-32 resize-none"
              rows="6"
            />
            <p className="text-xs text-gray-500 mt-2">
              Describe the skills, experience, and qualifications required for the position.
              This will be used to calculate the match score.
            </p>
          </div>

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={!uploadedFile || isUploading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUploading ? (
              <div className="flex items-center justify-center">
                <Loader className="h-5 w-5 mr-2 animate-spin" />
                Analyzing Resume...
              </div>
            ) : (
              'Analyze Resume'
            )}
          </button>
        </div>

        {/* Analysis Results */}
        <div className="space-y-6">
          {analysisResult && (
            <>
              {/* Candidate Info */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Candidate Information</h3>
                <div className="space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Name</label>
                    <p className="text-sm text-gray-900">{analysisResult.resume_data.name}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Email</label>
                    <p className="text-sm text-gray-900">{analysisResult.resume_data.email}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Phone</label>
                    <p className="text-sm text-gray-900">{analysisResult.resume_data.phone}</p>
                  </div>
                </div>
              </div>

              {/* Match Score */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Match Analysis</h3>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-gray-900">
                      {((analysisResult.match_score || 0) * 100).toFixed(1)}%
                    </div>
                    <div className={`text-sm font-medium ${getScoreColor(analysisResult.match_score)}`}>
                      Match Score
                    </div>
                    <span className={`badge ${getScoreBadge(analysisResult.match_score)} mt-2`}>
                      {analysisResult.match_score >= 0.7 ? 'High Match' : 
                       analysisResult.match_score >= 0.4 ? 'Medium Match' : 'Low Match'}
                    </span>
                  </div>

                  {/* Matched Skills */}
                  {analysisResult.matched_skills && analysisResult.matched_skills.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Matched Skills</label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {analysisResult.matched_skills.map((skill, index) => (
                          <span key={index} className="badge badge-success">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Missing Skills */}
                  {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Missing Skills</label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {analysisResult.missing_skills.map((skill, index) => (
                          <span key={index} className="badge badge-danger">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Interview Recommendations */}
              {analysisResult.interview_recommendations && (
                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Interview Recommendations</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">Recommended Format</label>
                      <p className="text-sm text-gray-900">
                        {analysisResult.interview_recommendations.interview_format.format}
                      </p>
                      <p className="text-xs text-gray-500">
                        Duration: {analysisResult.interview_recommendations.interview_format.duration}
                      </p>
                    </div>

                    {analysisResult.interview_recommendations.general_recommendations && (
                      <div>
                        <label className="text-sm font-medium text-gray-700">Recommendation</label>
                        <p className="text-sm text-gray-900">
                          {analysisResult.interview_recommendations.general_recommendations.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Instructions */}
          {!analysisResult && (
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">How it works</h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-xs font-medium text-blue-600">1</span>
                  </div>
                  <p>Upload a resume file (PDF, DOCX, DOC, or TXT format)</p>
                </div>
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-xs font-medium text-blue-600">2</span>
                  </div>
                  <p>Enter job requirements to define the ideal candidate profile</p>
                </div>
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-xs font-medium text-blue-600">3</span>
                  </div>
                  <p>AI analyzes the resume and provides match score and interview recommendations</p>
                </div>
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-xs font-medium text-blue-600">4</span>
                  </div>
                  <p>Review detailed analysis and suggested interview questions</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeUpload;

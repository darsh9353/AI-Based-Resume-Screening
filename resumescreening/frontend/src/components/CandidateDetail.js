import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Mail, Phone, Calendar, FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const CandidateDetail = () => {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  const fetchCandidate = async () => {
    try {
      const response = await fetch(`/api/candidate/${id}`);
      const data = await response.json();
      
      if (data.candidate) {
        setCandidate(data.candidate);
      } else {
        toast.error('Candidate not found');
      }
    } catch (error) {
      console.error('Error fetching candidate:', error);
      toast.error('Failed to fetch candidate details');
    } finally {
      setLoading(false);
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

  const getScoreLabel = (score) => {
    if (score >= 0.7) return 'High Match';
    if (score >= 0.4) return 'Medium Match';
    return 'Low Match';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!candidate) {
    return (
      <div className="text-center py-8">
        <h3 className="text-lg font-medium text-gray-900">Candidate not found</h3>
        <p className="text-sm text-gray-500 mt-1">The candidate you're looking for doesn't exist.</p>
        <Link to="/candidates" className="btn-primary mt-4 inline-block">
          Back to Candidates
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/candidates" className="p-2 text-gray-400 hover:text-gray-600">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{candidate.name}</h1>
            <p className="text-sm text-gray-500">Candidate Profile & Analysis</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-2xl font-bold ${getScoreColor(candidate.match_score)}`}>
            {((candidate.match_score || 0) * 100).toFixed(0)}%
          </span>
          <span className={`badge ${getScoreBadge(candidate.match_score)}`}>
            {getScoreLabel(candidate.match_score)}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Candidate Information */}
        <div className="lg:col-span-1 space-y-6">
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Contact Information</h3>
            <div className="space-y-3">
              {candidate.email && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">{candidate.email}</span>
                </div>
              )}
              {candidate.phone && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">{candidate.phone}</span>
                </div>
              )}
              {candidate.upload_date && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">
                    Uploaded {formatDate(candidate.upload_date)}
                  </span>
                </div>
              )}
              {candidate.resume_file && (
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">{candidate.resume_file}</span>
                </div>
              )}
            </div>
          </div>

          {/* Skills Analysis */}
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Skills Analysis</h3>
            
            {/* All Skills */}
            {candidate.skills && candidate.skills.length > 0 && (
              <div className="mb-4">
                <label className="text-sm font-medium text-gray-700 mb-2 block">All Skills</label>
                <div className="flex flex-wrap gap-2">
                  {candidate.skills.map((skill, index) => (
                    <span key={index} className="badge badge-info">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Matched Skills */}
            {candidate.matched_skills && candidate.matched_skills.length > 0 && (
              <div className="mb-4">
                <label className="text-sm font-medium text-gray-700 mb-2 block">Matched Skills</label>
                <div className="flex flex-wrap gap-2">
                  {candidate.matched_skills.map((skill, index) => (
                    <span key={index} className="badge badge-success">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missing Skills */}
            {candidate.missing_skills && candidate.missing_skills.length > 0 && (
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Missing Skills</label>
                <div className="flex flex-wrap gap-2">
                  {candidate.missing_skills.map((skill, index) => (
                    <span key={index} className="badge badge-danger">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Education */}
          {candidate.education && candidate.education.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Education</h3>
              <div className="space-y-3">
                {candidate.education.map((edu, index) => (
                  <div key={index} className="text-sm text-gray-700">
                    {edu}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Experience */}
          {candidate.experience && candidate.experience.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Experience</h3>
              <div className="space-y-3">
                {candidate.experience.map((exp, index) => (
                  <div key={index} className="text-sm text-gray-700">
                    {exp}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Interview Recommendations */}
        <div className="lg:col-span-2 space-y-6">
          {candidate.interview_recommendations && (
            <>
              {/* Interview Format */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Interview Format</h3>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Recommended Format</label>
                    <p className="text-lg font-medium text-gray-900">
                      {candidate.interview_recommendations.interview_format.format}
                    </p>
                    <p className="text-sm text-gray-500">
                      Duration: {candidate.interview_recommendations.interview_format.duration}
                    </p>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Interview Stages</label>
                    <div className="mt-2 space-y-2">
                      {candidate.interview_recommendations.interview_format.stages.map((stage, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-xs font-medium text-blue-600">{index + 1}</span>
                          </div>
                          <span className="text-sm text-gray-700">{stage}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* General Recommendations */}
              {candidate.interview_recommendations.general_recommendations && (
                <div className="card">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Recommendations</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">Priority</label>
                      <p className="text-sm text-gray-900">
                        {candidate.interview_recommendations.general_recommendations.priority}
                      </p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Recommendation</label>
                      <p className="text-sm text-gray-900">
                        {candidate.interview_recommendations.general_recommendations.recommendation}
                      </p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Focus Areas</label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {candidate.interview_recommendations.general_recommendations.focus_areas.map((area, index) => (
                          <span key={index} className="badge badge-info">
                            {area}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Red Flags</label>
                      <p className="text-sm text-gray-900">
                        {candidate.interview_recommendations.general_recommendations.red_flags}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Interview Questions */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Suggested Interview Questions</h3>
                
                {/* Technical Questions */}
                {candidate.interview_recommendations.technical_questions && 
                 candidate.interview_recommendations.technical_questions.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Technical Questions</h4>
                    <div className="space-y-3">
                      {candidate.interview_recommendations.technical_questions.map((question, index) => (
                        <div key={index} className="flex items-start gap-3">
                          <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-xs font-medium text-blue-600">{index + 1}</span>
                          </div>
                          <p className="text-sm text-gray-700">{question}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Behavioral Questions */}
                {candidate.interview_recommendations.behavioral_questions && 
                 candidate.interview_recommendations.behavioral_questions.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Behavioral Questions</h4>
                    <div className="space-y-3">
                      {candidate.interview_recommendations.behavioral_questions.map((question, index) => (
                        <div key={index} className="flex items-start gap-3">
                          <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-xs font-medium text-green-600">{index + 1}</span>
                          </div>
                          <p className="text-sm text-gray-700">{question}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Follow-up Questions */}
                {candidate.interview_recommendations.follow_up_questions && 
                 candidate.interview_recommendations.follow_up_questions.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Follow-up Questions</h4>
                    <div className="space-y-3">
                      {candidate.interview_recommendations.follow_up_questions.map((question, index) => (
                        <div key={index} className="flex items-start gap-3">
                          <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-xs font-medium text-orange-600">{index + 1}</span>
                          </div>
                          <p className="text-sm text-gray-700">{question}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CandidateDetail;

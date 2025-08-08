import React, { useState, useEffect } from 'react';
import { Search, Filter, Eye, Trash2, Mail, Phone, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';

const Candidates = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterScore, setFilterScore] = useState('all');

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const response = await fetch('/api/candidates');
      const data = await response.json();
      setCandidates(data.candidates || []);
    } catch (error) {
      console.error('Error fetching candidates:', error);
      toast.error('Failed to fetch candidates');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (candidateId) => {
    if (!window.confirm('Are you sure you want to delete this candidate?')) {
      return;
    }

    try {
      const response = await fetch(`/api/delete-candidate/${candidateId}`, {
        method: 'DELETE',
      });

      const result = await response.json();

      if (result.success) {
        toast.success('Candidate deleted successfully');
        fetchCandidates();
      } else {
        toast.error(result.error || 'Failed to delete candidate');
      }
    } catch (error) {
      console.error('Error deleting candidate:', error);
      toast.error('Failed to delete candidate');
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

  const filteredCandidates = candidates.filter(candidate => {
    const matchesSearch = 
      candidate.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.skills?.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesFilter = filterScore === 'all' || 
      (filterScore === 'high' && candidate.match_score >= 0.7) ||
      (filterScore === 'medium' && candidate.match_score >= 0.4 && candidate.match_score < 0.7) ||
      (filterScore === 'low' && candidate.match_score < 0.4);

    return matchesSearch && matchesFilter;
  });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Candidates</h1>
        <p className="mt-1 text-sm text-gray-500">
          Manage and review all candidate profiles and analysis results
        </p>
      </div>

      {/* Search and Filter */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search candidates by name, email, or skills..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={filterScore}
              onChange={(e) => setFilterScore(e.target.value)}
              className="input-field"
            >
              <option value="all">All Scores</option>
              <option value="high">High Match (≥70%)</option>
              <option value="medium">Medium Match (40-69%)</option>
              <option value="low">Low Match (&lt;40%)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Candidates List */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            {filteredCandidates.length} candidate{filteredCandidates.length !== 1 ? 's' : ''}
          </h3>
        </div>

        {filteredCandidates.length === 0 ? (
          <div className="text-center py-8">
            <div className="mx-auto h-12 w-12 text-gray-400">
              <Search className="h-12 w-12" />
            </div>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No candidates found</h3>
            <p className="mt-1 text-sm text-gray-500">
              {candidates.length === 0 
                ? 'Upload resumes to get started with AI screening.'
                : 'Try adjusting your search or filter criteria.'
              }
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredCandidates.map((candidate) => (
              <div key={candidate.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <span className="text-sm font-medium text-blue-600">
                          {candidate.name?.charAt(0) || '?'}
                        </span>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">{candidate.name}</h4>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          {candidate.email && (
                            <div className="flex items-center gap-1">
                              <Mail className="h-3 w-3" />
                              {candidate.email}
                            </div>
                          )}
                          {candidate.phone && (
                            <div className="flex items-center gap-1">
                              <Phone className="h-3 w-3" />
                              {candidate.phone}
                            </div>
                          )}
                          {candidate.upload_date && (
                            <div className="flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {formatDate(candidate.upload_date)}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Skills */}
                    {candidate.skills && candidate.skills.length > 0 && (
                      <div className="mb-3">
                        <div className="flex flex-wrap gap-1">
                          {candidate.skills.slice(0, 5).map((skill, index) => (
                            <span key={index} className="badge badge-info text-xs">
                              {skill}
                            </span>
                          ))}
                          {candidate.skills.length > 5 && (
                            <span className="text-xs text-gray-500">
                              +{candidate.skills.length - 5} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Match Score */}
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        <span className={`text-lg font-bold ${getScoreColor(candidate.match_score)}`}>
                          {((candidate.match_score || 0) * 100).toFixed(0)}%
                        </span>
                        <span className={`badge ${getScoreBadge(candidate.match_score)}`}>
                          {getScoreLabel(candidate.match_score)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <a
                      href={`/candidate/${candidate.id}`}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="View Details"
                    >
                      <Eye className="h-4 w-4" />
                    </a>
                    <button
                      onClick={() => handleDelete(candidate.id)}
                      className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                      title="Delete Candidate"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Candidates;

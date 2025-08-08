import React, { useState, useEffect } from 'react';
import { Users, TrendingUp, Clock, CheckCircle, AlertCircle, XCircle, Upload, Settings, BarChart3 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = ({ statistics }) => {
  const [recentCandidates, setRecentCandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecentCandidates();
  }, []);

  const fetchRecentCandidates = async () => {
    try {
      const response = await fetch('/api/candidates');
      const data = await response.json();
      setRecentCandidates(data.candidates?.slice(0, 5) || []);
    } catch (error) {
      console.error('Error fetching recent candidates:', error);
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

  const chartData = statistics ? [
    { name: 'High Match', value: statistics.high_match_candidates, color: '#10B981' },
    { name: 'Medium Match', value: statistics.medium_match_candidates, color: '#F59E0B' },
    { name: 'Low Match', value: statistics.low_match_candidates, color: '#EF4444' },
  ] : [];

  const statsCards = [
    {
      title: 'Total Candidates',
      value: statistics?.total_candidates || 0,
      icon: Users,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'positive'
    },
    {
      title: 'High Match',
      value: statistics?.high_match_candidates || 0,
      icon: CheckCircle,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'positive'
    },
    {
      title: 'Average Score',
      value: `${((statistics?.average_match_score || 0) * 100).toFixed(1)}%`,
      icon: TrendingUp,
      color: 'bg-purple-500',
      change: '+2.1%',
      changeType: 'positive'
    },
    {
      title: 'Recent Uploads',
      value: statistics?.recent_uploads || 0,
      icon: Clock,
      color: 'bg-orange-500',
      change: '+15%',
      changeType: 'positive'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          AI-powered resume screening and interview recommendations
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statsCards.map((card) => (
          <div key={card.title} className="card">
            <div className="flex items-center">
              <div className={`flex-shrink-0 p-3 rounded-lg ${card.color}`}>
                <card.icon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {card.title}
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {card.value}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center">
                <span className="text-sm font-medium text-green-600">
                  {card.change}
                </span>
                <span className="text-sm text-gray-500 ml-2">from last month</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Match Distribution */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Match Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Candidates</h3>
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="space-y-4">
              {recentCandidates.length > 0 ? (
                recentCandidates.map((candidate) => (
                  <div key={candidate.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <span className="text-sm font-medium text-blue-600">
                            {candidate.name?.charAt(0) || '?'}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-900">{candidate.name}</p>
                        <p className="text-sm text-gray-500">{candidate.email}</p>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <span className={`badge ${getScoreBadge(candidate.match_score)}`}>
                        {((candidate.match_score || 0) * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <Users className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No candidates yet</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Upload resumes to get started with AI screening.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <a
            href="/upload"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Upload className="h-6 w-6 text-blue-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Upload Resume</p>
              <p className="text-xs text-gray-500">Add new candidate</p>
            </div>
          </a>
          <a
            href="/candidates"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Users className="h-6 w-6 text-green-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">View Candidates</p>
              <p className="text-xs text-gray-500">Browse all candidates</p>
            </div>
          </a>
          <a
            href="/settings"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Settings className="h-6 w-6 text-purple-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Settings</p>
              <p className="text-xs text-gray-500">Configure system</p>
            </div>
          </a>
          <div className="flex items-center p-4 border border-gray-200 rounded-lg bg-gray-50">
            <BarChart3 className="h-6 w-6 text-orange-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Analytics</p>
              <p className="text-xs text-gray-500">View insights</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

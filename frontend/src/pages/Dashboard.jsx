import { useEffect, useState } from 'react'
import { applicationsAPI } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    const id = localStorage.getItem('userId')
    if (id) {
      setUserId(id)
      fetchStats(id)
    }
  }, [])

  const fetchStats = async (id) => {
    try {
      setLoading(true)
      const response = await applicationsAPI.getStats(id)
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    )
  }

  const chartData = stats ? [
    { name: 'Pending', value: stats.pending },
    { name: 'Applied', value: stats.applied },
    { name: 'Interviewing', value: stats.interviewing },
    { name: 'Rejected', value: stats.rejected },
    { name: 'Accepted', value: stats.accepted },
  ] : []

  return (
    <div className="dashboard">
      <h2 className="mb-3">Dashboard</h2>

      {stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
              <h3>{stats.total}</h3>
              <p>Total Applications</p>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
              <h3>{stats.pending}</h3>
              <p>Pending</p>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
              <h3>{stats.applied}</h3>
              <p>Applied</p>
            </div>
            <div className="stat-card" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
              <h3>{stats.interviewing}</h3>
              <p>Interviewing</p>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Application Status Overview</h3>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-2 mt-3">
            <div className="card">
              <h3 className="card-title mb-2">Quick Actions</h3>
              <div className="flex gap-2">
                <button className="btn btn-primary" onClick={() => window.location.href = '/scraper'}>
                  Scrape New Jobs
                </button>
                <button className="btn btn-success" onClick={() => window.location.href = '/applications'}>
                  View Applications
                </button>
              </div>
            </div>

            <div className="card">
              <h3 className="card-title mb-2">Success Rate</h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2ecc71' }}>
                {stats.total > 0
                  ? ((stats.accepted / stats.total) * 100).toFixed(1)
                  : 0}%
              </div>
              <p style={{ color: '#7f8c8d', marginTop: '0.5rem' }}>
                {stats.accepted} accepted out of {stats.total} applications
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard

import { useEffect, useState } from 'react'
import { applicationsAPI } from '../services/api'

function Applications() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [selectedApp, setSelectedApp] = useState(null)
  const [generatingCoverLetter, setGeneratingCoverLetter] = useState(false)
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    const id = localStorage.getItem('userId')
    if (id) {
      setUserId(id)
    }
  }, [])

  useEffect(() => {
    if (userId) {
      fetchApplications()
    }
  }, [filter, userId])

  const fetchApplications = async () => {
    try {
      setLoading(true)
      const params = { user_id: userId }
      if (filter !== 'all') {
        params.status = filter
      }
      const response = await applicationsAPI.getAll(params)
      setApplications(response.data)
    } catch (error) {
      console.error('Error fetching applications:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (appId, newStatus) => {
    try {
      await applicationsAPI.update(appId, { status: newStatus })
      fetchApplications()
    } catch (error) {
      console.error('Error updating status:', error)
    }
  }

  const handleGenerateCoverLetter = async (appId) => {
    try {
      setGeneratingCoverLetter(true)
      const response = await applicationsAPI.generateCoverLetter(appId, 'professional')
      alert('Cover letter generated successfully!')
      setSelectedApp({ ...selectedApp, cover_letter: response.data.cover_letter })
      fetchApplications()
    } catch (error) {
      console.error('Error generating cover letter:', error)
      alert('Failed to generate cover letter. Check if OpenAI API key is configured.')
    } finally {
      setGeneratingCoverLetter(false)
    }
  }

  const getStatusBadgeClass = (status) => {
    const statusMap = {
      pending: 'badge-pending',
      applied: 'badge-applied',
      interviewing: 'badge-interviewing',
      rejected: 'badge-rejected',
      accepted: 'badge-accepted'
    }
    return `badge ${statusMap[status] || 'badge-pending'}`
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading applications...</p>
      </div>
    )
  }

  return (
    <div className="applications-page">
      <div className="flex-between mb-3">
        <h2>My Applications ({applications.length})</h2>
        <button className="btn btn-primary" onClick={fetchApplications}>
          Refresh
        </button>
      </div>

      {/* Filter buttons */}
      <div className="flex gap-2 mb-3">
        <button
          className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={`btn ${filter === 'pending' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('pending')}
        >
          Pending
        </button>
        <button
          className={`btn ${filter === 'applied' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('applied')}
        >
          Applied
        </button>
        <button
          className={`btn ${filter === 'interviewing' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('interviewing')}
        >
          Interviewing
        </button>
      </div>

      {applications.length === 0 ? (
        <div className="card text-center">
          <p>No applications found.</p>
          <button className="btn btn-primary mt-2" onClick={() => window.location.href = '/jobs'}>
            Browse Jobs
          </button>
        </div>
      ) : (
        <div className="grid">
          {applications.map((app) => (
            <div key={app.id} className="card">
              <div className="card-header">
                <div>
                  <h3 className="card-title">Application #{app.id}</h3>
                  <p style={{ color: '#7f8c8d', fontSize: '0.9rem', marginTop: '0.25rem' }}>
                    Job ID: {app.job_id}
                  </p>
                </div>
                <span className={getStatusBadgeClass(app.status)}>
                  {app.status}
                </span>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <p style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>
                  Created: {new Date(app.created_at).toLocaleDateString()}
                </p>
                {app.applied_at && (
                  <p style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>
                    Applied: {new Date(app.applied_at).toLocaleDateString()}
                  </p>
                )}
              </div>

              {app.notes && (
                <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#f8f9fa', borderRadius: '4px' }}>
                  <strong style={{ fontSize: '0.85rem' }}>Notes:</strong>
                  <p style={{ fontSize: '0.9rem', marginTop: '0.25rem' }}>{app.notes}</p>
                </div>
              )}

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ fontSize: '0.9rem', marginBottom: '0.5rem', display: 'block' }}>
                  <strong>Change Status:</strong>
                </label>
                <select
                  className="form-control"
                  value={app.status}
                  onChange={(e) => handleStatusChange(app.id, e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="applied">Applied</option>
                  <option value="interviewing">Interviewing</option>
                  <option value="rejected">Rejected</option>
                  <option value="accepted">Accepted</option>
                </select>
              </div>

              <div className="flex gap-2">
                <button
                  className="btn btn-primary"
                  onClick={() => setSelectedApp(app)}
                >
                  View Details
                </button>
                <button
                  className="btn btn-success"
                  onClick={() => handleGenerateCoverLetter(app.id)}
                  disabled={generatingCoverLetter}
                >
                  {generatingCoverLetter ? 'Generating...' : 'Generate Cover Letter'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Application Details Modal */}
      {selectedApp && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}
          onClick={() => setSelectedApp(null)}
        >
          <div
            style={{
              background: 'white',
              padding: '2rem',
              borderRadius: '8px',
              maxWidth: '800px',
              maxHeight: '80vh',
              overflow: 'auto',
              width: '90%'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex-between mb-3">
              <h2>Application #{selectedApp.id}</h2>
              <button className="btn btn-secondary" onClick={() => setSelectedApp(null)}>
                Close
              </button>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <p><strong>Status:</strong> <span className={getStatusBadgeClass(selectedApp.status)}>{selectedApp.status}</span></p>
              <p><strong>Job ID:</strong> {selectedApp.job_id}</p>
              <p><strong>Created:</strong> {new Date(selectedApp.created_at).toLocaleString()}</p>
              {selectedApp.applied_at && (
                <p><strong>Applied:</strong> {new Date(selectedApp.applied_at).toLocaleString()}</p>
              )}
            </div>

            {selectedApp.cover_letter ? (
              <div style={{ marginBottom: '1.5rem' }}>
                <h3 style={{ marginBottom: '0.5rem' }}>Cover Letter</h3>
                <div
                  style={{
                    background: '#f8f9fa',
                    padding: '1rem',
                    borderRadius: '4px',
                    whiteSpace: 'pre-wrap',
                    lineHeight: '1.6'
                  }}
                >
                  {selectedApp.cover_letter}
                </div>
                <button
                  className="btn btn-primary mt-2"
                  onClick={() => {
                    navigator.clipboard.writeText(selectedApp.cover_letter)
                    alert('Cover letter copied to clipboard!')
                  }}
                >
                  Copy to Clipboard
                </button>
              </div>
            ) : (
              <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
                <p style={{ color: '#7f8c8d' }}>No cover letter generated yet.</p>
                <button
                  className="btn btn-success mt-2"
                  onClick={() => handleGenerateCoverLetter(selectedApp.id)}
                  disabled={generatingCoverLetter}
                >
                  {generatingCoverLetter ? 'Generating...' : 'Generate Cover Letter'}
                </button>
              </div>
            )}

            {selectedApp.notes && (
              <div>
                <h3 style={{ marginBottom: '0.5rem' }}>Notes</h3>
                <p style={{ lineHeight: '1.6' }}>{selectedApp.notes}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Applications

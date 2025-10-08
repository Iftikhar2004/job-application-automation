import { useEffect, useState } from 'react'
import { jobsAPI, applicationsAPI } from '../services/api'

function Jobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedJob, setSelectedJob] = useState(null)
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    const id = localStorage.getItem('userId')
    setUserId(id)
    fetchJobs()
  }, [])

  const fetchJobs = async () => {
    try {
      setLoading(true)
      const response = await jobsAPI.getAll({ limit: 50 })
      setJobs(response.data)
    } catch (error) {
      console.error('Error fetching jobs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApply = async (jobId) => {
    try {
      await applicationsAPI.create({
        job_id: jobId,
        user_id: userId
      })
      alert('Application created successfully!')
    } catch (error) {
      console.error('Error creating application:', error)
      alert('Failed to create application. It may already exist.')
    }
  }

  const handleViewDetails = (job) => {
    setSelectedJob(job)
  }

  const handleCloseModal = () => {
    setSelectedJob(null)
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading jobs...</p>
      </div>
    )
  }

  return (
    <div className="jobs-page">
      <div className="flex-between mb-3">
        <h2>Available Jobs ({jobs.length})</h2>
        <button className="btn btn-primary" onClick={fetchJobs}>
          Refresh
        </button>
      </div>

      {jobs.length === 0 ? (
        <div className="card text-center">
          <p>No jobs found. Try scraping some jobs first!</p>
          <button className="btn btn-primary mt-2" onClick={() => window.location.href = '/scraper'}>
            Go to Scraper
          </button>
        </div>
      ) : (
        <div className="grid grid-2">
          {jobs.map((job) => (
            <div key={job.id} className="card">
              <div className="card-header">
                <h3 className="card-title">{job.title}</h3>
                {job.match_score && (
                  <span className="badge badge-applied">
                    Match: {job.match_score}%
                  </span>
                )}
              </div>

              <p style={{ fontWeight: 'bold', color: '#2c3e50', marginBottom: '0.5rem' }}>
                {job.company}
              </p>
              <p style={{ color: '#7f8c8d', fontSize: '0.9rem', marginBottom: '1rem' }}>
                Location: {job.location}
              </p>

              <p style={{ fontSize: '0.9rem', marginBottom: '1rem', lineHeight: '1.5' }}>
                {job.description.substring(0, 150)}...
              </p>

              {job.salary_min && job.salary_max && (
                <p style={{ color: '#27ae60', fontWeight: 'bold', marginBottom: '1rem' }}>
                  ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                </p>
              )}

              {job.required_skills && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong style={{ fontSize: '0.85rem' }}>Skills:</strong>
                  <div style={{ marginTop: '0.5rem' }}>
                    {JSON.parse(job.required_skills.replace(/'/g, '"')).slice(0, 5).map((skill, idx) => (
                      <span
                        key={idx}
                        style={{
                          display: 'inline-block',
                          background: '#ecf0f1',
                          padding: '0.25rem 0.5rem',
                          borderRadius: '4px',
                          fontSize: '0.8rem',
                          marginRight: '0.5rem',
                          marginBottom: '0.5rem'
                        }}
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex gap-2">
                <button className="btn btn-primary" onClick={() => handleApply(job.id)}>
                  Apply
                </button>
                <button className="btn btn-secondary" onClick={() => handleViewDetails(job)}>
                  View Details
                </button>
                <a
                  href={job.job_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary"
                >
                  Open Link
                </a>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Job Details Modal */}
      {selectedJob && (
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
          onClick={handleCloseModal}
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
              <h2>{selectedJob.title}</h2>
              <button className="btn btn-secondary" onClick={handleCloseModal}>
                Close
              </button>
            </div>

            <p style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
              {selectedJob.company}
            </p>
            <p style={{ color: '#7f8c8d', marginBottom: '1rem' }}>Location: {selectedJob.location}</p>

            {selectedJob.salary_min && selectedJob.salary_max && (
              <p style={{ color: '#27ae60', fontWeight: 'bold', marginBottom: '1rem' }}>
                ${selectedJob.salary_min.toLocaleString()} - ${selectedJob.salary_max.toLocaleString()}
              </p>
            )}

            <div style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ marginBottom: '0.5rem' }}>Description</h3>
              <p style={{ lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>{selectedJob.description}</p>
            </div>

            {selectedJob.requirements && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h3 style={{ marginBottom: '0.5rem' }}>Requirements</h3>
                <p style={{ lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>{selectedJob.requirements}</p>
              </div>
            )}

            <div style={{ marginTop: '1.5rem' }}>
              <button className="btn btn-primary" onClick={() => handleApply(selectedJob.id)}>
                Apply Now
              </button>
              <a
                href={selectedJob.job_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ marginLeft: '1rem' }}
              >
                View on {selectedJob.source}
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Jobs

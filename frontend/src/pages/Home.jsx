import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function Home() {
  const [showGuide, setShowGuide] = useState(false)
  const [hasProfile, setHasProfile] = useState(false)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    checkProfile()
  }, [])

  const checkProfile = async () => {
    try {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        setHasProfile(false)
        setLoading(false)
        return
      }
      await axios.get(`${API_BASE_URL}/api/users/${userId}/profile`)
      setHasProfile(true)
    } catch (error) {
      setHasProfile(false)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="home-page"><p>Loading...</p></div>
  }

  return (
    <div className="home-page">
      {/* Profile Alert */}
      {!hasProfile && (
        <div className="profile-alert">
          <h3>Welcome! Create Your Profile First</h3>
          <p>Before you start applying for jobs, please create your profile so we can generate personalized cover letters and match you with the right opportunities.</p>
          <button
            className="btn btn-primary"
            onClick={() => navigate('/profile')}
          >
            Create Profile Now
          </button>
        </div>
      )}

      {/* Hero Section */}
      <div className="hero-section">
        <h1 className="hero-title">Job Application Automation Platform</h1>
        <p className="hero-subtitle">
          Automate your job search with AI-powered tools. Find jobs, track applications, and generate cover letters automatically.
        </p>
      </div>

      {/* Quick Start Cards */}
      <div className="quick-start-section">
        <h2 className="section-title">Get Started in 3 Simple Steps</h2>

        <div className="steps-grid">
          {/* Step 1 */}
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Find Jobs</h3>
            <p>Search and scrape job postings from Indeed automatically</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/scraper')}
            >
              Start Scraping Jobs
            </button>
          </div>

          {/* Step 2 */}
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Browse & Match</h3>
            <p>View all scraped jobs with AI-powered skill matching scores</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/jobs')}
            >
              View Available Jobs
            </button>
          </div>

          {/* Step 3 */}
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Apply & Track</h3>
            <p>Create applications and generate AI cover letters automatically</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/applications')}
            >
              Manage Applications
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h2 className="section-title">Key Features</h2>

        <div className="features-grid">
          <div className="feature-card">
            <h4>Automated Job Scraping</h4>
            <p>Automatically scrape job postings from Indeed based on your search criteria</p>
          </div>

          <div className="feature-card">
            <h4>AI Skill Matching</h4>
            <p>Get match scores based on your skills and job requirements using NLP</p>
          </div>

          <div className="feature-card">
            <h4>AI Cover Letters</h4>
            <p>Generate personalized cover letters instantly with AI assistance</p>
          </div>

          <div className="feature-card">
            <h4>Application Tracking</h4>
            <p>Track all your applications in one place with status updates</p>
          </div>

          <div className="feature-card">
            <h4>Analytics Dashboard</h4>
            <p>View statistics and insights about your job search progress</p>
          </div>

          <div className="feature-card">
            <h4>Fast & Efficient</h4>
            <p>Save hours of manual job searching and application tracking</p>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="how-it-works-section">
        <h2 className="section-title">How It Works</h2>

        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div className="workflow-steps">
            <div className="workflow-step">
              <div className="workflow-step-header">
                <span className="workflow-badge">Step 1</span>
                <h4>Scrape Jobs</h4>
              </div>
              <p>Go to the <strong>Scraper</strong> page, enter your desired job title (e.g., "Python Developer") and location (e.g., "Remote"), then click "Start Scraping"</p>
            </div>

            <div className="workflow-arrow">↓</div>

            <div className="workflow-step">
              <div className="workflow-step-header">
                <span className="workflow-badge">Step 2</span>
                <h4>Review Jobs</h4>
              </div>
              <p>Visit the <strong>Jobs</strong> page to see all scraped jobs. Each job shows a match score, required skills, and salary information</p>
            </div>

            <div className="workflow-arrow">↓</div>

            <div className="workflow-step">
              <div className="workflow-step-header">
                <span className="workflow-badge">Step 3</span>
                <h4>Create Applications</h4>
              </div>
              <p>Click "Apply" on any job to create an application. The system will automatically generate a personalized cover letter</p>
            </div>

            <div className="workflow-arrow">↓</div>

            <div className="workflow-step">
              <div className="workflow-step-header">
                <span className="workflow-badge">Step 4</span>
                <h4>Track Progress</h4>
              </div>
              <p>Use the <strong>Applications</strong> page to track all your applications, update their status, and view generated cover letters</p>
            </div>

            <div className="workflow-arrow">↓</div>

            <div className="workflow-step">
              <div className="workflow-step-header">
                <span className="workflow-badge">Step 5</span>
                <h4>Monitor Dashboard</h4>
              </div>
              <p>Check the <strong>Dashboard</strong> for statistics, success rates, and visual insights about your job search</p>
            </div>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="help-section">
        <div className="card" style={{ background: '#e8f5e9', border: '2px solid #4caf50' }}>
          <h3 className="card-title mb-2">Need Help?</h3>
          <div className="help-content">
            <p><strong>First time here?</strong> Click "Start Scraping Jobs" above to begin!</p>
            <button
              className="btn btn-success mt-2"
              onClick={() => setShowGuide(!showGuide)}
            >
              {showGuide ? 'Hide' : 'Show'} Detailed Guide
            </button>
          </div>

          {showGuide && (
            <div className="detailed-guide mt-3">
              <h4>Detailed User Guide</h4>

              <div className="guide-section">
                <h5>Scraper Page</h5>
                <ul>
                  <li>Enter job keywords like "Software Engineer", "Data Scientist", etc.</li>
                  <li>Specify location: use city names, states, or "Remote" for remote jobs</li>
                  <li>Choose 1-5 pages (each page = ~10 jobs)</li>
                  <li>Wait 30-60 seconds for scraping to complete</li>
                  <li>Duplicate jobs are automatically filtered out</li>
                </ul>
              </div>

              <div className="guide-section">
                <h5>Jobs Page</h5>
                <ul>
                  <li><strong>Match Score:</strong> How well your skills match the job (0-100%)</li>
                  <li><strong>Skills:</strong> Key technologies and skills required</li>
                  <li><strong>Experience:</strong> Years of experience needed</li>
                  <li><strong>Salary:</strong> Expected salary range if available</li>
                  <li>Click "Apply" to create an application for any job</li>
                </ul>
              </div>

              <div className="guide-section">
                <h5>Applications Page</h5>
                <ul>
                  <li>View all your applications in one place</li>
                  <li>Update application status (Pending → Applied → Interviewing → Accepted/Rejected)</li>
                  <li>Click "Generate Cover Letter" to create AI-powered cover letters</li>
                  <li>Add notes to track interview dates, feedback, etc.</li>
                </ul>
              </div>

              <div className="guide-section">
                <h5>Dashboard Page</h5>
                <ul>
                  <li>View total applications and status breakdown</li>
                  <li>See your success rate percentage</li>
                  <li>Visualize application status with charts</li>
                  <li>Quick access buttons to other pages</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* CTA Section */}
      <div className="cta-section">
        <h2>Ready to automate your job search?</h2>
        <button
          className="btn btn-primary btn-large"
          onClick={() => navigate('/scraper')}
        >
          Get Started Now
        </button>
      </div>
    </div>
  )
}

export default Home

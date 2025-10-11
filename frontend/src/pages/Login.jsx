import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData)

      // Store user info in localStorage
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('userId', response.data.user_id)
      localStorage.setItem('userEmail', response.data.email)

      // Navigate to home page
      navigate('/')
      window.location.reload()
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-split-container">
        <div className="auth-left-panel">
          <div className="auth-brand">
            <div className="auth-logo">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zM10 4h4v3h-4V4zm10 16H4V9h16v11z" fill="white"/>
                <path d="M12 11c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm0 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z" fill="white"/>
              </svg>
            </div>
            <h1>JobTracker</h1>
            <p>Professional job application automation platform</p>
          </div>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-icon">✓</div>
              <div>
                <h3>Automated Job Scraping</h3>
                <p>Scrape jobs from Indeed automatically</p>
              </div>
            </div>
            <div className="auth-feature">
              <div className="feature-icon">✓</div>
              <div>
                <h3>Smart Matching</h3>
                <p>AI-powered skill matching and scoring</p>
              </div>
            </div>
            <div className="auth-feature">
              <div className="feature-icon">✓</div>
              <div>
                <h3>Cover Letters</h3>
                <p>Generate personalized cover letters</p>
              </div>
            </div>
          </div>
        </div>

        <div className="auth-right-panel">
          <div className="auth-form-container">
            <div className="auth-header">
              <h2>Welcome Back</h2>
              <p>Sign in to continue to your account</p>
            </div>

            {error && (
              <div className="error-alert">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="modern-auth-form">
              <div className="input-group">
                <label>Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="name@example.com"
                  required
                  className="modern-input"
                />
              </div>

              <div className="input-group">
                <label>Password</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  required
                  className="modern-input"
                />
              </div>

              <button
                type="submit"
                className="modern-btn-primary"
                disabled={loading}
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </button>
            </form>

            <div className="auth-divider">
              <span>New to JobTracker?</span>
            </div>

            <a href="/signup" className="modern-btn-secondary">
              Create an Account
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login

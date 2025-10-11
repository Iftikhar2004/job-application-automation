import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Jobs from './pages/Jobs'
import Applications from './pages/Applications'
import Scraper from './pages/Scraper'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Signup from './pages/Signup'

function Navigation() {
  const location = useLocation()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userEmail, setUserEmail] = useState('')
  const [showProfileMenu, setShowProfileMenu] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const email = localStorage.getItem('userEmail')
    setIsLoggedIn(!!token)
    setUserEmail(email || '')
  }, [location])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    localStorage.removeItem('userEmail')
    window.location.href = '/login'
  }

  const isActive = (path) => {
    return location.pathname === path ? 'nav-link-active' : ''
  }

  // Don't show navigation on login/signup pages
  if (location.pathname === '/login' || location.pathname === '/signup') {
    return null
  }

  return (
    <nav className="modern-navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <div className="logo-icon">🚀</div>
          <div className="logo-text">
            <h1>JobAuto</h1>
            <span>AI-Powered</span>
          </div>
        </Link>

        <div className="navbar-menu">
          {isLoggedIn ? (
            <>
              <Link to="/" className={`nav-link ${isActive('/')}`}>
                <span className="nav-icon">🏠</span>
                Home
              </Link>
              <Link to="/scraper" className={`nav-link ${isActive('/scraper')}`}>
                <span className="nav-icon">🔍</span>
                Scraper
              </Link>
              <Link to="/jobs" className={`nav-link ${isActive('/jobs')}`}>
                <span className="nav-icon">💼</span>
                Jobs
              </Link>
              <Link to="/applications" className={`nav-link ${isActive('/applications')}`}>
                <span className="nav-icon">📝</span>
                Applications
              </Link>
              <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
                <span className="nav-icon">📊</span>
                Dashboard
              </Link>

              <div className="navbar-profile">
                <button
                  className="profile-button"
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                >
                  <div className="profile-avatar">
                    {userEmail.charAt(0).toUpperCase()}
                  </div>
                  <span className="profile-arrow">▼</span>
                </button>

                {showProfileMenu && (
                  <div className="profile-dropdown">
                    <div className="profile-dropdown-header">
                      <div className="profile-email">{userEmail}</div>
                    </div>
                    <Link
                      to="/profile"
                      className="profile-dropdown-item"
                      onClick={() => setShowProfileMenu(false)}
                    >
                      <span className="nav-icon">👤</span>
                      My Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="profile-dropdown-item logout-item"
                    >
                      <span className="nav-icon">🚪</span>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className={`nav-link ${isActive('/login')}`}>
                Login
              </Link>
              <Link to="/signup" className="nav-link-cta">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

// Protected Route component
function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return children
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />

        <div className="container">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/jobs" element={
              <ProtectedRoute>
                <Jobs />
              </ProtectedRoute>
            } />
            <Route path="/applications" element={
              <ProtectedRoute>
                <Applications />
              </ProtectedRoute>
            } />
            <Route path="/scraper" element={
              <ProtectedRoute>
                <Scraper />
              </ProtectedRoute>
            } />
          </Routes>
        </div>

        <footer className="footer">
          <p>Built using React, FastAPI, and AI</p>
        </footer>
      </div>
    </Router>
  )
}

export default App

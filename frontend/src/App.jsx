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
    return location.pathname === path ? 'active' : ''
  }

  // Don't show navigation on login/signup pages
  if (location.pathname === '/login' || location.pathname === '/signup') {
    return null
  }

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-brand">
          <h1>Job Automation</h1>
          <p className="navbar-tagline">AI-Powered Job Search Platform</p>
        </div>
        <div className="nav-links">
          {isLoggedIn ? (
            <>
              <Link to="/" className={isActive('/')}>
                Home
              </Link>
              <Link to="/profile" className={isActive('/profile')}>
                Profile
              </Link>
              <Link to="/scraper" className={isActive('/scraper')}>
                Scraper
              </Link>
              <Link to="/jobs" className={isActive('/jobs')}>
                Jobs
              </Link>
              <Link to="/applications" className={isActive('/applications')}>
                Applications
              </Link>
              <Link to="/dashboard" className={isActive('/dashboard')}>
                Dashboard
              </Link>
              <div className="user-info">
                <span>{userEmail}</span>
                <button onClick={handleLogout} className="btn-logout">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className={isActive('/login')}>
                Login
              </Link>
              <Link to="/signup" className={isActive('/signup')}>
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

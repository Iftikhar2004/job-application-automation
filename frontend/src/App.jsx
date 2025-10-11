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
          <div className="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zM10 4h4v3h-4V4zm10 16H4V9h16v11z" fill="white"/>
              <path d="M12 11c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm0 4c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z" fill="white"/>
            </svg>
          </div>
          <div className="logo-text">
            <h1>JobTracker</h1>
            <span>Professional Edition</span>
          </div>
        </Link>

        <div className="navbar-menu">
          {isLoggedIn ? (
            <>
              <Link to="/" className={`nav-link ${isActive('/')}`}>
                Home
              </Link>
              <Link to="/scraper" className={`nav-link ${isActive('/scraper')}`}>
                Scraper
              </Link>
              <Link to="/jobs" className={`nav-link ${isActive('/jobs')}`}>
                Jobs
              </Link>
              <Link to="/applications" className={`nav-link ${isActive('/applications')}`}>
                Applications
              </Link>
              <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
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
                      My Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="profile-dropdown-item logout-item"
                    >
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
          <p>© 2024 JobTracker. Built with React & FastAPI.</p>
        </footer>
      </div>
    </Router>
  )
}

export default App

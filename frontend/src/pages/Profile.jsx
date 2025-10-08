import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const Profile = () => {
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState(null);
  const [userId, setUserId] = useState(null);
  const [formData, setFormData] = useState({
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    skills: '',
    experience_years: '',
    current_job_title: '',
    current_company: '',
    education: '',
    certifications: '',
    resume_text: '',
    professional_summary: '',
    linkedin_url: '',
    github_url: '',
    portfolio_url: '',
    desired_job_titles: '',
    desired_locations: '',
    desired_salary_min: '',
    remote_preference: 'any'
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    const id = localStorage.getItem('userId');
    if (id) {
      setUserId(id);
      fetchProfile(id);
    }
  }, []);

  const fetchProfile = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/users/${id}/profile`);
      const profileData = response.data;
      setProfile(profileData);

      // Parse JSON fields
      let skills = [];
      let education = [];
      let certifications = [];
      let desiredTitles = [];
      let desiredLocations = [];

      try { skills = JSON.parse(profileData.skills || '[]'); } catch(e) {}
      try { education = JSON.parse(profileData.education || '[]'); } catch(e) {}
      try { certifications = JSON.parse(profileData.certifications || '[]'); } catch(e) {}
      try { desiredTitles = JSON.parse(profileData.desired_job_titles || '[]'); } catch(e) {}
      try { desiredLocations = JSON.parse(profileData.desired_locations || '[]'); } catch(e) {}

      setFormData({
        phone: profileData.phone || '',
        address: profileData.address || '',
        city: profileData.city || '',
        state: profileData.state || '',
        zip_code: profileData.zip_code || '',
        skills: skills.join(', '),
        experience_years: profileData.experience_years || '',
        current_job_title: profileData.current_job_title || '',
        current_company: profileData.current_company || '',
        education: education.map(e => `${e.degree} - ${e.institution} (${e.year})`).join('\n'),
        certifications: certifications.join(', '),
        resume_text: profileData.resume_text || '',
        professional_summary: profileData.professional_summary || '',
        linkedin_url: profileData.linkedin_url || '',
        github_url: profileData.github_url || '',
        portfolio_url: profileData.portfolio_url || '',
        desired_job_titles: desiredTitles.join(', '),
        desired_locations: desiredLocations.join(', '),
        desired_salary_min: profileData.desired_salary_min || '',
        remote_preference: profileData.remote_preference || 'any'
      });
    } catch (error) {
      if (error.response && error.response.status === 404) {
        setMessage('No profile found. Please create your profile.');
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const skills = formData.skills.split(',').map(s => s.trim()).filter(s => s);
      const certifications = formData.certifications.split(',').map(c => c.trim()).filter(c => c);
      const desired_job_titles = formData.desired_job_titles.split(',').map(t => t.trim()).filter(t => t);
      const desired_locations = formData.desired_locations.split(',').map(l => l.trim()).filter(l => l);

      const education = [];
      if (formData.education) {
        const eduLines = formData.education.split('\n');
        for (const line of eduLines) {
          if (line.trim()) {
            const parts = line.split('-');
            if (parts.length >= 2) {
              const degree = parts[0].trim();
              const rest = parts.slice(1).join('-');
              const yearMatch = rest.match(/\((\d{4})\)/);
              const year = yearMatch ? yearMatch[1] : '';
              const institution = rest.replace(/\(\d{4}\)/, '').trim();
              education.push({ degree, institution, year });
            }
          }
        }
      }

      const profileData = {
        phone: formData.phone,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        zip_code: formData.zip_code,
        skills,
        experience_years: parseInt(formData.experience_years) || 0,
        current_job_title: formData.current_job_title,
        current_company: formData.current_company,
        education,
        certifications,
        resume_text: formData.resume_text,
        professional_summary: formData.professional_summary,
        linkedin_url: formData.linkedin_url,
        github_url: formData.github_url,
        portfolio_url: formData.portfolio_url,
        desired_job_titles,
        desired_locations,
        desired_salary_min: parseFloat(formData.desired_salary_min) || null,
        remote_preference: formData.remote_preference
      };

      await axios.post(`${API_BASE_URL}/api/users/${userId}/profile`, profileData);
      setMessage('Profile saved successfully!');
      fetchProfile(userId);
    } catch (error) {
      setMessage('Error saving profile: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>My Profile</h1>
        <p>Complete your profile to generate personalized cover letters and apply for jobs</p>
      </div>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="profile-form">
        <section className="form-section">
          <h2>Personal Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                placeholder="+1 (555) 123-4567"
              />
            </div>

            <div className="form-group full-width">
              <label>Address</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                placeholder="123 Main Street"
              />
            </div>

            <div className="form-group">
              <label>City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                placeholder="New York"
              />
            </div>

            <div className="form-group">
              <label>State</label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleInputChange}
                placeholder="NY"
              />
            </div>

            <div className="form-group">
              <label>ZIP Code</label>
              <input
                type="text"
                name="zip_code"
                value={formData.zip_code}
                onChange={handleInputChange}
                placeholder="10001"
              />
            </div>
          </div>
        </section>

        <section className="form-section">
          <h2>Professional Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Current Job Title</label>
              <input
                type="text"
                name="current_job_title"
                value={formData.current_job_title}
                onChange={handleInputChange}
                placeholder="Senior Software Engineer"
              />
            </div>

            <div className="form-group">
              <label>Current Company</label>
              <input
                type="text"
                name="current_company"
                value={formData.current_company}
                onChange={handleInputChange}
                placeholder="Tech Corp"
              />
            </div>

            <div className="form-group">
              <label>Years of Experience *</label>
              <input
                type="number"
                name="experience_years"
                value={formData.experience_years}
                onChange={handleInputChange}
                required
                min="0"
                placeholder="5"
              />
            </div>

            <div className="form-group full-width">
              <label>Skills * (comma-separated)</label>
              <input
                type="text"
                name="skills"
                value={formData.skills}
                onChange={handleInputChange}
                required
                placeholder="Python, JavaScript, React, Node.js, SQL"
              />
            </div>

            <div className="form-group full-width">
              <label>Certifications (comma-separated)</label>
              <input
                type="text"
                name="certifications"
                value={formData.certifications}
                onChange={handleInputChange}
                placeholder="AWS Certified, PMP, Scrum Master"
              />
            </div>

            <div className="form-group full-width">
              <label>Education (one per line: Degree - Institution (Year))</label>
              <textarea
                name="education"
                value={formData.education}
                onChange={handleInputChange}
                rows="3"
                placeholder="Bachelor of Science in Computer Science - MIT (2018)"
              />
            </div>

            <div className="form-group full-width">
              <label>Professional Summary</label>
              <textarea
                name="professional_summary"
                value={formData.professional_summary}
                onChange={handleInputChange}
                rows="4"
                placeholder="Experienced software engineer with a passion for building scalable applications..."
              />
            </div>
          </div>
        </section>

        <section className="form-section">
          <h2>Links</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>LinkedIn URL</label>
              <input
                type="url"
                name="linkedin_url"
                value={formData.linkedin_url}
                onChange={handleInputChange}
                placeholder="https://linkedin.com/in/yourprofile"
              />
            </div>

            <div className="form-group">
              <label>GitHub URL</label>
              <input
                type="url"
                name="github_url"
                value={formData.github_url}
                onChange={handleInputChange}
                placeholder="https://github.com/yourusername"
              />
            </div>

            <div className="form-group full-width">
              <label>Portfolio URL</label>
              <input
                type="url"
                name="portfolio_url"
                value={formData.portfolio_url}
                onChange={handleInputChange}
                placeholder="https://yourportfolio.com"
              />
            </div>
          </div>
        </section>

        <section className="form-section">
          <h2>Job Preferences</h2>
          <div className="form-grid">
            <div className="form-group full-width">
              <label>Desired Job Titles (comma-separated)</label>
              <input
                type="text"
                name="desired_job_titles"
                value={formData.desired_job_titles}
                onChange={handleInputChange}
                placeholder="Software Engineer, Full Stack Developer, Backend Engineer"
              />
            </div>

            <div className="form-group full-width">
              <label>Desired Locations (comma-separated)</label>
              <input
                type="text"
                name="desired_locations"
                value={formData.desired_locations}
                onChange={handleInputChange}
                placeholder="New York, San Francisco, Remote"
              />
            </div>

            <div className="form-group">
              <label>Minimum Desired Salary</label>
              <input
                type="number"
                name="desired_salary_min"
                value={formData.desired_salary_min}
                onChange={handleInputChange}
                placeholder="100000"
              />
            </div>

            <div className="form-group">
              <label>Remote Preference</label>
              <select
                name="remote_preference"
                value={formData.remote_preference}
                onChange={handleInputChange}
              >
                <option value="any">Any</option>
                <option value="remote">Remote Only</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">On-site</option>
              </select>
            </div>
          </div>
        </section>

        <section className="form-section">
          <h2>Resume</h2>
          <div className="form-group full-width">
            <label>Resume Text</label>
            <textarea
              name="resume_text"
              value={formData.resume_text}
              onChange={handleInputChange}
              rows="10"
              placeholder="Paste your full resume here..."
            />
          </div>
        </section>

        <div className="form-actions">
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>

      <style jsx>{`
        .container {
          max-width: 900px;
          margin: 0 auto;
          padding: 20px;
        }

        .header {
          margin-bottom: 30px;
        }

        .header h1 {
          margin: 0 0 10px 0;
          color: #333;
        }

        .header p {
          margin: 0;
          color: #666;
        }

        .message {
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .message.success {
          background-color: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
        }

        .message.error {
          background-color: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
        }

        .profile-form {
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .form-section {
          padding: 30px;
          border-bottom: 1px solid #eee;
        }

        .form-section:last-of-type {
          border-bottom: none;
        }

        .form-section h2 {
          margin: 0 0 20px 0;
          color: #444;
          font-size: 1.3em;
        }

        .form-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
        }

        .form-group.full-width {
          grid-column: 1 / -1;
        }

        .form-group label {
          margin-bottom: 8px;
          font-weight: 600;
          color: #555;
          font-size: 0.9em;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
          padding: 10px 12px;
          border: 1px solid #ddd;
          border-radius: 6px;
          font-size: 14px;
          font-family: inherit;
          transition: border-color 0.2s;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
          outline: none;
          border-color: #4CAF50;
        }

        .form-group textarea {
          resize: vertical;
        }

        .form-actions {
          padding: 20px 30px;
          text-align: right;
        }

        .btn-primary {
          background-color: #4CAF50;
          color: white;
          border: none;
          padding: 12px 30px;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .btn-primary:hover:not(:disabled) {
          background-color: #45a049;
        }

        .btn-primary:disabled {
          background-color: #ccc;
          cursor: not-allowed;
        }

        @media (max-width: 768px) {
          .form-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Profile;

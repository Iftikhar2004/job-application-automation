import { useState } from 'react'
import { scraperAPI } from '../services/api'

function Scraper() {
  const [formData, setFormData] = useState({
    query: 'Python',
    location: 'Remote',
    num_pages: 1,
    source: 'arbeitnow'
  })
  const [scraping, setScraping] = useState(false)
  const [result, setResult] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: name === 'num_pages' ? parseInt(value) : value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      setScraping(true)
      setResult(null)

      // Use sync endpoint to get immediate results
      const response = await scraperAPI.scrapeSync(formData)

      setResult(response.data)
      alert(`Scraping complete! Found ${response.data.jobs_found} jobs, saved ${response.data.jobs_saved} new jobs.`)
    } catch (error) {
      console.error('Error scraping jobs:', error)
      alert('Failed to scrape jobs. Please try again.')
    } finally {
      setScraping(false)
    }
  }

  return (
    <div className="scraper-page">
      <h2 className="mb-3">Job Scraper</h2>

      <div className="grid grid-2">
        <div className="card">
          <h3 className="card-title mb-3">Scrape Jobs</h3>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Job Title / Keywords</label>
              <input
                type="text"
                name="query"
                className="form-control"
                value={formData.query}
                onChange={handleChange}
                placeholder="e.g., Python Developer, Data Scientist"
                required
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                name="location"
                className="form-control"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., New York, Remote"
              />
            </div>

            <div className="form-group">
              <label>Source</label>
              <select
                name="source"
                className="form-control"
                value={formData.source}
                onChange={handleChange}
              >
                <option value="arbeitnow">Arbeitnow (Free API - Working)</option>
                <option value="indeed">Indeed (Currently Blocked)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Number of Pages (10 jobs per page)</label>
              <input
                type="number"
                name="num_pages"
                className="form-control"
                value={formData.num_pages}
                onChange={handleChange}
                min="1"
                max="5"
                required
              />
              <small style={{ color: '#7f8c8d' }}>
                Note: Scraping multiple pages may take longer
              </small>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={scraping}
              style={{ width: '100%' }}
            >
              {scraping ? 'Scraping...' : 'Start Scraping'}
            </button>
          </form>

          {scraping && (
            <div className="loading mt-3">
              <div className="spinner"></div>
              <p>Scraping in progress... This may take a minute.</p>
            </div>
          )}

          {result && (
            <div className="mt-3" style={{ padding: '1rem', background: '#d5f4e6', borderRadius: '4px' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#27ae60' }}>Scraping Complete!</h4>
              <p style={{ marginBottom: '0.25rem' }}>
                <strong>Jobs Found:</strong> {result.jobs_found}
              </p>
              <p style={{ marginBottom: '0.25rem' }}>
                <strong>New Jobs Saved:</strong> {result.jobs_saved}
              </p>
              <button
                className="btn btn-primary mt-2"
                onClick={() => window.location.href = '/jobs'}
              >
                View Jobs
              </button>
            </div>
          )}
        </div>

        <div>
          <div className="card mb-3">
            <h3 className="card-title mb-2">How to Use</h3>
            <ol style={{ paddingLeft: '1.5rem', lineHeight: '1.8' }}>
              <li>Enter the job title or keywords you're looking for</li>
              <li>Specify the location (or use "Remote" for remote jobs)</li>
              <li>Select the job board to scrape from</li>
              <li>Choose how many pages to scrape (1-5 pages)</li>
              <li>Click "Start Scraping" and wait for results</li>
              <li>View scraped jobs in the "Jobs" section</li>
            </ol>
          </div>

          <div className="card mb-3">
            <h3 className="card-title mb-2">Tips</h3>
            <ul style={{ paddingLeft: '1.5rem', lineHeight: '1.8' }}>
              <li>Use specific keywords for better results</li>
              <li>Start with 1 page to test, then increase if needed</li>
              <li>Duplicate jobs are automatically filtered out</li>
              <li>Jobs are analyzed automatically for skill matching</li>
            </ul>
          </div>

          <div className="card" style={{ background: '#fff3cd', border: '1px solid #ffc107' }}>
            <h3 className="card-title mb-2">Note</h3>
            <p style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>
              Web scraping should be done responsibly. This tool is for educational purposes.
              Always respect website terms of service and rate limits.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Scraper

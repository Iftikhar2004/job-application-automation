# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm installed

## Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

## Step 2: Frontend Setup

```bash
# Navigate to frontend directory (open new terminal)
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## Step 3: First Time Use

1. Open your browser to `http://localhost:5173`
2. You'll be redirected to the login page
3. Click **"Sign up"** to create a new account
4. Fill in:
   - Full Name
   - Email
   - Password (min 6 characters)
   - Confirm Password
5. Click **"Sign Up"**
6. Complete your profile with:
   - Personal information
   - Professional details
   - Skills (required)
   - Experience years (required)
   - Job preferences
7. Click **"Save Profile"**

## Step 4: Start Using

### Scrape Jobs:
1. Go to **Scraper** page
2. Enter job title (e.g., "Python Developer")
3. Enter location (e.g., "Remote" or "New York")
4. Select number of pages (1-5)
5. Click **"Start Scraping"**
6. Wait for jobs to be scraped (30-60 seconds)

### Browse Jobs:
1. Go to **Jobs** page
2. View all scraped jobs with match scores
3. Click **"View Details"** to see full description
4. Click **"Apply"** to create an application

### Track Applications:
1. Go to **Applications** page
2. View all your applications
3. Update status (Pending → Applied → Interviewing → Accepted/Rejected)
4. Generate cover letters
5. Add notes

### View Dashboard:
1. Go to **Dashboard** page
2. See application statistics
3. View success rates
4. Track progress

## Troubleshooting

### Backend Issues:

**Port already in use:**
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

**Module not found errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Database errors:**
```bash
# Delete and recreate database
rm job_automation.db
# Restart the backend (tables will be created automatically)
```

### Frontend Issues:

**Port already in use:**
```bash
# Vite will automatically ask to use a different port
# Or kill the process
lsof -ti:5173 | xargs kill -9
```

**Module not found:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Make sure backend is running on port 8000
- Check CORS configuration in `backend/app/main.py`

### Scraper Issues:

**No jobs found:**
- Indeed's HTML structure may have changed
- Try different search terms
- Check internet connection
- Indeed may be blocking requests (rate limiting)

**Scraping takes too long:**
- Reduce number of pages to 1
- Check delay setting in scraper (default 2 seconds)

## Environment Variables (Optional)

Create a `.env` file in the backend directory:

```env
# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./job_automation.db

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-this

# OpenAI for cover letter generation (optional)
OPENAI_API_KEY=your-openai-api-key

# Scraping settings
HEADLESS_BROWSER=True
SCRAPING_DELAY=2
```

## Production Deployment Notes

### Security:
1. Change `SECRET_KEY` in config
2. Use PostgreSQL instead of SQLite
3. Set up HTTPS
4. Configure proper CORS origins
5. Enable rate limiting

### Database:
```bash
# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/jobautomation
```

### Frontend Build:
```bash
cd frontend
npm run build
# Serve the dist folder with nginx or similar
```

### Backend Production:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Features Overview

### Completed Features:
- User authentication (login/signup)
- User profile management
- Job scraping from Indeed
- Job browsing with match scores
- Application tracking
- Cover letter generation (with OpenAI API)
- Dashboard with statistics
- No emojis (professional appearance)
- Secure password hashing
- JWT token authentication

### Missing/Optional Features:
- Email verification
- Password reset
- Resume upload and parsing
- Automatic job application
- Job alerts
- Interview scheduling
- Multiple job board support
- Job board APIs (currently uses scraping)

## Support

For issues or questions, refer to:
- `IMPLEMENTATION_SUMMARY.md` for detailed architecture
- `README.md` for project overview
- API documentation at `http://localhost:8000/docs` (when backend is running)

# Job Application Automation Platform

A full-stack web application that streamlines job searching, application tracking, and cover letter generation using modern web technologies, NLP analysis, and AI-powered automation.

## Features

### Core Functionality
- **User Authentication**: Secure signup/login system with JWT token-based authentication
- **Job Scraping**: Automated job collection from multiple sources (Arbeitnow API, Indeed)
- **Smart Job Analysis**: NLP-powered skill extraction, experience detection, and salary parsing
- **Application Tracking**: Comprehensive application management with status workflows
- **AI Cover Letters**: Automated, personalized cover letter generation using OpenAI
- **Match Scoring**: Intelligent compatibility scoring between user profiles and job requirements
- **Analytics Dashboard**: Visual insights into application statistics and trends

### User Features
- Secure user registration and authentication
- Personalized user profiles with skills and experience
- Job search with keyword and location filtering
- One-click job applications
- Application status management (pending, applied, interviewing, rejected, accepted)
- Custom notes for each application
- AI-generated cover letters with multiple tone options

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Web Scraping**: BeautifulSoup4, Requests, Arbeitnow API
- **NLP & ML**: Scikit-learn, spaCy, NLTK
- **AI**: OpenAI GPT API for cover letter generation
- **API Documentation**: Automatic OpenAPI (Swagger) docs

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Data Visualization**: Recharts
- **Styling**: Vanilla CSS with custom design system

### APIs & Services
- **Arbeitnow API**: Free job board API (no authentication required)
- **OpenAI API**: GPT-powered cover letter generation (optional)
- **Custom REST API**: Full backend API with comprehensive endpoints

## Project Structure

```
job-application-automation/
├── backend/
│   └── app/
│       ├── api/                    # API endpoints
│       │   ├── auth.py            # Authentication (signup, login)
│       │   ├── jobs.py            # Job management
│       │   ├── applications.py    # Application tracking
│       │   ├── users.py           # User & profile management
│       │   └── scraper.py         # Job scraping endpoints
│       ├── core/                   # Core configuration
│       │   ├── config.py          # Environment settings
│       │   └── database.py        # Database connection
│       ├── models/                 # Database models
│       │   └── models.py          # SQLAlchemy models
│       ├── scrapers/               # Job board scrapers
│       │   ├── arbeitnow_scraper.py  # Arbeitnow API (working)
│       │   ├── adzuna_scraper.py     # Adzuna API (optional)
│       │   └── indeed_scraper.py     # Indeed scraper (blocked)
│       ├── services/               # Business logic
│       │   ├── nlp_service.py     # NLP job analysis
│       │   └── cover_letter_service.py  # AI cover letters
│       └── main.py                # FastAPI application
├── frontend/
│   └── src/
│       ├── pages/                  # Page components
│       │   ├── Login.jsx          # Login page
│       │   ├── Signup.jsx         # Registration page
│       │   ├── Home.jsx           # Landing page
│       │   ├── Dashboard.jsx      # Analytics dashboard
│       │   ├── Jobs.jsx           # Job listings
│       │   ├── Applications.jsx   # Application management
│       │   ├── Scraper.jsx        # Job scraper interface
│       │   └── Profile.jsx        # User profile
│       ├── services/
│       │   └── api.js             # API service layer
│       ├── App.jsx                # Main app with routing
│       └── index.css              # Global styles
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment template
├── IMPLEMENTATION_SUMMARY.md      # Implementation details
├── SETUP_GUIDE.md                 # Quick setup guide
└── README.md                      # This file
```

## Database Schema

### Users
- User accounts with email and password (bcrypt hashed)
- Full name and timestamps

### User Profiles
- Skills (JSON array)
- Experience years
- Current job title and company
- Professional summary
- Education, certifications, portfolio URL

### Jobs
- Job postings from various sources
- NLP-analyzed skills and requirements
- Salary ranges, locations, descriptions
- Match scores with user profiles

### Job Applications
- Links users to jobs they've applied to
- Status tracking (pending → applied → interviewing → accepted/rejected)
- Cover letters and custom notes
- Application timestamps

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables (optional)**
```bash
cp .env.example .env
# Add your OpenAI API key to .env if you want AI cover letters
# OPENAI_API_KEY=sk-your-key-here
```

5. **Run the backend server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install Node dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

## Usage Guide

### 1. Create an Account

1. Navigate to the application homepage
2. Click "Sign Up" or go to `/signup`
3. Enter your email, full name, and password
4. Click "Sign Up" to create your account
5. You'll be redirected to create your profile

### 2. Complete Your Profile

1. After signup, fill in your professional information:
   - Current job title and company
   - Years of experience
   - Skills (comma-separated)
   - Professional summary
   - Education and certifications
2. Click "Save Profile"

### 3. Scrape Jobs

1. Navigate to the **Scraper** page
2. Enter job keywords (e.g., "Python Developer", "Software Engineer")
3. Enter location (e.g., "Remote", "New York")
4. Select source: **Arbeitnow** (working) or Indeed (currently blocked)
5. Choose number of pages (1-5 pages, 10 jobs per page)
6. Click "Start Scraping"
7. Wait for results - jobs are automatically analyzed and saved

### 4. Browse & Apply to Jobs

1. Go to the **Jobs** page
2. Browse available jobs with match scores
3. View job details including:
   - Required skills
   - Salary range (if available)
   - Company and location
   - Full description
4. Click "Apply" to create an application
5. Jobs show compatibility scores based on your profile

### 5. Manage Applications

1. Visit the **Applications** page
2. View all your applications
3. Filter by status: All, Pending, Applied, Interviewing
4. Update application status as you progress through interviews
5. Generate AI-powered cover letters
6. Add custom notes for each application
7. View application details and timeline

### 6. Track Your Progress

1. Visit the **Dashboard** page
2. View application statistics:
   - Total applications submitted
   - Status breakdown (pending, applied, interviewing, etc.)
   - Recent activity
3. Quick access to common actions

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and get JWT token

### Jobs
- `GET /api/jobs` - Get all jobs (with filters)
- `GET /api/jobs/{id}` - Get specific job details
- `POST /api/jobs` - Create new job
- `DELETE /api/jobs/{id}` - Delete job
- `POST /api/jobs/{id}/calculate-match` - Calculate match score with user profile

### Applications
- `GET /api/applications` - Get applications (filter by user_id, status)
- `GET /api/applications/{id}` - Get specific application
- `POST /api/applications` - Create new application
- `PUT /api/applications/{id}` - Update application status/notes
- `POST /api/applications/{id}/generate-cover-letter` - Generate AI cover letter
- `GET /api/applications/stats/user/{user_id}` - Get user application statistics

### Scraper
- `POST /api/scraper/scrape` - Start scraping (background task)
- `POST /api/scraper/scrape-sync` - Scrape jobs synchronously (wait for results)

### Users & Profiles
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user details
- `POST /api/users/{id}/profile` - Create/update user profile
- `GET /api/users/{id}/profile` - Get user profile

## NLP Features

The NLP service automatically analyzes job descriptions to extract:

1. **Technical Skills**: Identifies 100+ programming languages, frameworks, tools, and technologies
2. **Experience Requirements**: Extracts required years of experience from job descriptions
3. **Salary Information**: Parses salary ranges in various formats (annual, hourly, ranges)
4. **Seniority Level**: Detects if position is senior/lead/principal level
5. **Match Scoring**: Calculates 0-100% compatibility between user profile and job requirements

**Supported Skills Categories:**
- Programming languages (Python, JavaScript, Java, C++, etc.)
- Frameworks (React, Django, FastAPI, Spring, etc.)
- Databases (PostgreSQL, MongoDB, MySQL, etc.)
- Cloud platforms (AWS, Azure, GCP)
- DevOps tools (Docker, Kubernetes, Jenkins, etc.)
- And many more...

## AI Cover Letter Generation

The cover letter generator creates personalized, professional cover letters:

**Features:**
- Uses OpenAI GPT-3.5/4 for natural language generation
- Personalizes based on:
  - Job title and company
  - Job description and requirements
  - Your profile (skills, experience, current role)
- Supports multiple tones: professional, enthusiastic, formal
- Generates concise 3-4 paragraph letters
- Falls back to template-based generation if API key not configured

**Usage:**
1. Apply to a job
2. Go to Applications page
3. Click "Generate Cover Letter"
4. Review and copy the generated letter
5. Customize as needed

## Job Scraping Options

### Arbeitnow API (Recommended - Currently Working)
- Free API with no authentication
- International job listings (especially Europe)
- Tech-focused positions
- No rate limiting issues
- 10-50 jobs per search

### Adzuna API (Alternative - Requires API Key)
- Free tier: 1,000 calls/month
- Coverage: US, UK, and 15+ countries
- High-quality job data
- Get free API keys at: https://developer.adzuna.com/

### Indeed (Currently Blocked)
- Anti-bot protection blocks scraping
- Returns 403 Forbidden errors
- Not recommended for production use

**Recommendation**: Use Arbeitnow for testing and development. For production, consider Adzuna API or other official job board APIs.

## Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Authentication**: Secure token-based sessions
- **Protected Routes**: Frontend routes require authentication
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **CORS Configuration**: Restricted to allowed origins
- **Environment Variables**: Sensitive data stored in .env files

**Security Best Practices:**
- Never commit `.env` files to version control
- Use strong, unique passwords
- Keep API keys secret
- Update dependencies regularly
- Use HTTPS in production

## Troubleshooting

### Backend Issues

**Database errors:**
```bash
# Delete existing database and restart
rm job_automation.db
python -m uvicorn app.main:app --reload
```

**Port 8000 already in use:**
```bash
# Change port
python -m uvicorn app.main:app --reload --port 8001
```

**Module import errors:**
```bash
# Make sure you're in backend directory
cd backend
python -m uvicorn app.main:app --reload
```

**Authentication failing:**
- Check if user exists in database
- Verify password is correct
- Check browser console for errors
- Clear localStorage and try again

### Frontend Issues

**Port 5173 already in use:**
```bash
# Edit vite.config.js and change port
server: {
  port: 3001
}
```

**API connection errors:**
- Ensure backend is running on port 8000
- Check API_BASE_URL in frontend/src/services/api.js
- Verify CORS settings in backend/app/main.py

**Applications not showing:**
- Check if you're logged in
- Verify userId is stored in localStorage
- Check browser console for errors
- Refresh the page

### Scraping Issues

**No jobs found:**
- Try different search keywords
- Use Arbeitnow instead of Indeed
- Check internet connection
- Verify API is accessible

**Indeed returns 0 jobs:**
- Indeed blocks automated scraping
- Switch to Arbeitnow or get Adzuna API keys
- See SCRAPER_ISSUE.md for details

## Deployment

### Backend Deployment (Railway/Render/Heroku)

1. **Create Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Set environment variables:**
- `DATABASE_URL` (for PostgreSQL)
- `OPENAI_API_KEY` (optional)
- `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` (optional)

3. **Deploy:**
- Connect GitHub repository
- Configure build settings
- Deploy

### Frontend Deployment (Vercel/Netlify)

1. **Build the application:**
```bash
cd frontend
npm run build
```

2. **Update API URL:**
```javascript
// In frontend/src/services/api.js
const API_BASE_URL = 'https://your-backend-url.com'
```

3. **Deploy:**
- Upload `dist` folder
- Configure redirects for SPA routing
- Set environment variables if needed

## Future Enhancements

- [ ] Email notifications for new matching jobs
- [ ] Resume parsing and automatic skill extraction
- [ ] LinkedIn and Glassdoor integration
- [ ] Job alerts based on saved preferences
- [ ] Interview preparation resources
- [ ] Salary negotiation insights
- [ ] Application deadline reminders
- [ ] Chrome extension for one-click apply
- [ ] Mobile app (React Native)
- [ ] Team collaboration features

## Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation
- python-jose - JWT token handling
- bcrypt - Password hashing
- scikit-learn - Machine learning for NLP
- spaCy - Advanced NLP processing
- OpenAI - GPT API for text generation
- Requests - HTTP library
- BeautifulSoup4 - Web scraping

**Frontend:**
- React 18 - UI library
- Vite - Build tool and dev server
- React Router - Client-side routing
- Axios - HTTP client
- Recharts - Data visualization

**Database:**
- SQLite (development)
- PostgreSQL (production ready)

## License

This project is for educational and personal use. Please respect job board terms of service and rate limits when scraping.

## Contributing

This is a portfolio/learning project. Feel free to fork and customize for your own use!

**Suggestions and improvements are welcome via:**
- GitHub issues
- Pull requests
- Discussions

## Acknowledgments

- OpenAI for GPT API
- Arbeitnow for free job board API
- FastAPI community
- React and Vite teams

---

**Built for job seekers who want to automate repetitive tasks and focus on what matters - preparing for interviews and landing great opportunities.**

*Happy job hunting!*

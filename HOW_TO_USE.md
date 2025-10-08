# 📖 How to Use the Job Application Automation Platform

## 🚀 Quick Setup (First Time)

### Step 1: Start the Backend
```bash
# Navigate to the backend folder
cd /home/iftikhar-ali/Desktop/projects/job-application-automation/backend

# Start the FastAPI server
python -m app.main
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal window open!

---

### Step 2: Install & Start the Frontend

**Open a NEW terminal window** and run:

```bash
# Navigate to the frontend folder
cd /home/iftikhar-ali/Desktop/projects/job-application-automation/frontend

# Install dependencies (FIRST TIME ONLY)
npm install

# Start the development server
npm run dev
```

**You should see:**
```
  VITE ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

### Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5173
```

**You're all set!** 🎉

---

## 🎯 How to Use the Platform

### 1️⃣ **Home Page** (http://localhost:5173/)

This is your starting point with:
- Overview of all features
- Step-by-step guide
- Quick navigation buttons

**What to do:** Read the welcome guide and click "Get Started Now"

---

### 2️⃣ **Scraper Page** 🔍 (Navigate: Scraper)

**Purpose:** Find and save job postings automatically from Indeed

**How to use:**
1. **Enter Job Title:** Type what job you're looking for
   - Examples: "Python Developer", "Data Scientist", "Full Stack Engineer"

2. **Enter Location:** Where do you want to work?
   - Examples: "Remote", "New York", "San Francisco", "California"

3. **Choose Pages:** How many pages to scrape (1-5)
   - 1 page = ~10 jobs
   - Start with 1 page to test

4. **Click "Start Scraping"**
   - Wait 30-60 seconds
   - You'll see a success message with number of jobs found

5. **Click "View Jobs"** to see what was scraped

**Example:**
```
Job Title: Software Engineer
Location: Remote
Pages: 2
```

---

### 3️⃣ **Jobs Page** 💼 (Navigate: Jobs)

**Purpose:** Browse all scraped jobs with AI match scores

**What you'll see:**
- **Job Title & Company**
- **Match Score:** 0-100% (how well it matches your skills)
- **Skills Required:** Technologies needed
- **Experience:** Years required
- **Salary Range:** If available
- **Apply Button:** Click to create an application

**How to use:**
1. Browse through the jobs
2. Look at match scores to find best fits
3. Click "Apply" on jobs you like
4. This creates an application and generates a cover letter automatically

---

### 4️⃣ **Applications Page** 📝 (Navigate: Applications)

**Purpose:** Track all your job applications in one place

**What you'll see:**
- List of all applications
- Current status of each
- Cover letters (if generated)

**How to use:**

1. **View Applications:** See all jobs you've applied to

2. **Update Status:** Click status dropdown to change:
   - 🟡 **Pending:** Just created
   - 🔵 **Applied:** You've submitted the application
   - 🟣 **Interviewing:** Got an interview!
   - 🟢 **Accepted:** Got the job!
   - 🔴 **Rejected:** Didn't get it

3. **Generate Cover Letter:** Click button to create AI cover letter

4. **View Details:** Click on any application to see:
   - Job description
   - Cover letter
   - Your notes
   - Application date

5. **Add Notes:** Keep track of:
   - Interview dates
   - Follow-up reminders
   - Feedback received

---

### 5️⃣ **Dashboard Page** 📊 (Navigate: Dashboard)

**Purpose:** See statistics about your job search

**What you'll see:**
- **Total Applications:** How many jobs you've applied to
- **Status Breakdown:** Pending, Applied, Interviewing, etc.
- **Success Rate:** % of applications that led to offers
- **Visual Charts:** Bar charts showing your progress

**Quick Actions:**
- Button to scrape more jobs
- Button to view applications

---

## 💡 Common Workflows

### Workflow 1: First Time Use
```
1. Open Home Page
2. Click "Start Scraping Jobs"
3. Enter "Python Developer" and "Remote"
4. Click "Start Scraping"
5. Wait for results
6. Click "View Jobs"
7. Click "Apply" on a good match
8. Go to Applications to see your cover letter
```

### Workflow 2: Daily Job Search
```
1. Go to Scraper
2. Search for new jobs
3. Go to Jobs page
4. Sort by match score
5. Apply to top matches
6. Update application statuses in Applications page
7. Check Dashboard for progress
```

### Workflow 3: Track Applications
```
1. Go to Applications page
2. Update status when you submit applications
3. Add notes after interviews
4. Mark as "Accepted" or "Rejected" when decided
5. Check Dashboard to see success rate
```

---

## ⚠️ Important Notes

### Backend MUST Be Running
- The frontend needs the backend to work
- If you see errors, check that backend is running on http://localhost:8000
- Test backend: Open http://localhost:8000/docs in browser

### Network Issues
- If scraping fails, check your internet connection
- Some websites may block scraping - this is normal
- Try scraping fewer pages if it times out

### Data Storage
- All data is saved in `backend/job_automation.db`
- This is a SQLite database file
- Your data persists between sessions

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
```bash
# Make sure backend is running
cd backend
python -m app.main
```

### "npm install fails"
```bash
# Try with different registry or timeout
npm install --legacy-peer-deps --fetch-timeout=600000

# Or use yarn instead
yarn install
```

### "No jobs showing up"
```bash
# Reseed the database
cd backend
python seed_db.py
```

### "Scraping doesn't work"
- This is expected - web scraping can be unreliable
- Indeed may block automated requests
- Use the sample data instead for testing

---

## 🎨 Features Explained

### 🤖 AI Match Scoring
- Analyzes job descriptions using NLP
- Extracts required skills
- Compares with your skills
- Gives 0-100% match score

### ✍️ AI Cover Letter Generation
- Uses job details
- Personalizes to company and role
- Includes relevant skills
- Professional formatting

### 📊 Application Tracking
- Centralized dashboard
- Status updates
- Historical data
- Success metrics

---

## 📱 User Interface Tour

### Navigation Bar (Top)
- **🏠 Home:** Welcome page and guide
- **🔍 Scraper:** Find new jobs
- **💼 Jobs:** Browse scraped jobs
- **📝 Applications:** Track applications
- **📊 Dashboard:** View statistics

### Color Coding
- 🔵 **Blue:** Primary actions (Apply, Start Scraping)
- 🟢 **Green:** Success (Accepted, Complete)
- 🟡 **Yellow/Orange:** Pending, Warning
- 🔴 **Red:** Rejected, Danger

---

## 🎯 Tips for Best Results

1. **Start Small:** Scrape 1 page first to test
2. **Use Specific Keywords:** "Senior Python Developer" better than "Developer"
3. **Update Statuses:** Keep applications page current
4. **Check Match Scores:** Focus on 70%+ matches
5. **Customize Cover Letters:** Edit AI-generated letters before sending
6. **Add Notes:** Track interview dates and feedback

---

## 🆘 Need More Help?

1. **Check Home Page:** Has detailed guide with examples
2. **API Documentation:** http://localhost:8000/docs
3. **README:** Full technical documentation
4. **QUICKSTART:** Backend setup and testing

---

## 🎉 You're Ready!

**Start your automated job search now:**

1. Make sure backend is running
2. Start the frontend (`npm run dev`)
3. Open http://localhost:5173
4. Click "Start Scraping Jobs"
5. Begin your journey to finding the perfect role!

---

*Built with ❤️ using React, FastAPI, and AI*

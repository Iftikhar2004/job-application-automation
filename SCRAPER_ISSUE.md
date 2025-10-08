# Job Scraper Issue - Indeed Blocking Requests

## Problem

Indeed is blocking the scraper with **403 Forbidden** errors. This happens because:

1. Indeed has anti-bot protection
2. They detect automated scraping attempts
3. Your IP may be rate-limited or blocked

## Why Web Scraping is Problematic

- **Legal Issues**: Many websites' Terms of Service prohibit scraping
- **Blocking**: Sites use anti-bot technology (Cloudflare, reCAPTCHA, etc.)
- **Unstable**: HTML structure changes break scrapers
- **Rate Limiting**: Too many requests get you IP banned
- **Maintenance**: Requires constant updates when site changes

## Solutions

### Solution 1: Use Job Board APIs (RECOMMENDED)

Use official APIs instead of scraping. Here are free/affordable options:

#### A. Adzuna API (BEST FREE OPTION)
- **Website**: https://developer.adzuna.com/
- **Free Tier**: 1,000 calls/month
- **Coverage**: US, UK, and 15+ countries
- **Data Quality**: Excellent
- **Setup Time**: 5 minutes

**How to use:**
1. Sign up at https://developer.adzuna.com/
2. Get your App ID and App Key
3. Add to `.env` file:
   ```
   ADZUNA_APP_ID=your_app_id
   ADZUNA_APP_KEY=your_app_key
   ```
4. I've already created `adzuna_scraper.py` for you!

#### B. JSearch (RapidAPI)
- **Website**: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **Free Tier**: 2,500 requests/month
- **Coverage**: Indeed, LinkedIn, Glassdoor, ZipRecruiter
- **Data Quality**: Excellent
- **Cost**: Free tier available, paid tiers from $9.99/month

#### C. The Muse API
- **Website**: https://www.themuse.com/developers/api/v2
- **Free**: Yes
- **Coverage**: Tech and creative jobs
- **Limitations**: Smaller dataset

#### D. Arbeitnow API
- **Website**: https://arbeitnow.com/api
- **Free**: Yes
- **Coverage**: International jobs, especially Europe
- **No Auth Required**: Yes!

### Solution 2: Enhance Indeed Scraper (Less Reliable)

If you must scrape Indeed, try these techniques:

#### A. Add Delays
- Increase delay between requests to 5-10 seconds
- Randomize delays

#### B. Rotate User Agents
```python
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    # ... more user agents
]

headers = {
    'User-Agent': random.choice(user_agents)
}
```

#### C. Use Proxies
- Rotate IP addresses
- Use residential proxies (expensive)
- Services: Bright Data, Oxylabs, ScraperAPI

#### D. Use Browser Automation
- Selenium with real browser
- Playwright
- Slower but harder to detect

#### E. Use Scraping Services
- **ScraperAPI**: https://scraperapi.com (handles proxies, headless browsers, CAPTCHA)
- **Bright Data**: https://brightdata.com
- **Apify**: https://apify.com

### Solution 3: Hybrid Approach

1. Use APIs for job discovery (Adzuna, JSearch)
2. Scrape only specific company career pages
3. Let users manually paste job URLs

## Recommended Implementation

I recommend using **Adzuna API**:

### Steps:

1. **Get API Keys** (5 minutes)
   ```
   Visit: https://developer.adzuna.com/
   Sign up → Create App → Get App ID & Key
   ```

2. **Update Config**
   ```bash
   cd backend
   nano .env
   # Add:
   ADZUNA_APP_ID=your_app_id_here
   ADZUNA_APP_KEY=your_app_key_here
   ```

3. **Update Scraper Route**
   The scraper API already has the structure - just need to switch from Indeed to Adzuna:

   ```python
   # In app/api/scraper.py, change:
   from app.scrapers.indeed_scraper import IndeedScraper
   # To:
   from app.scrapers.adzuna_scraper import AdzunaScraper

   # And use:
   scraper = AdzunaScraper(app_id, app_key)
   ```

4. **Update Frontend**
   The frontend doesn't need changes - it just calls the same API endpoint!

## Quick Fix for Demo

For immediate testing without API keys, I can:

1. Create a mock scraper that returns sample data
2. Use the free Arbeitnow API (no auth required)
3. Add sample jobs to the database manually

Would you like me to:
- **Option A**: Set up Adzuna API (you need to get free API keys)
- **Option B**: Set up Arbeitnow API (no keys needed, but smaller dataset)
- **Option C**: Create mock scraper with sample data for testing
- **Option D**: Try to fix Indeed scraper with proxies/delays (unreliable)

## Current Status

✅ Backend working
✅ Frontend working
✅ Authentication working
✅ Database working
❌ Indeed scraper blocked by anti-bot protection

## Next Steps

Choose one of the options above and I'll implement it for you!

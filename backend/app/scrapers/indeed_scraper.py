import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndeedScraper:
    """Scraper for Indeed job postings"""

    def __init__(self, delay: int = 2):
        self.base_url = "https://www.indeed.com"
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

    def search_jobs(self, query: str, location: str = "", num_pages: int = 1) -> List[Dict]:
        """
        Search for jobs on Indeed

        Args:
            query: Job search query (e.g., "Python Developer")
            location: Location for job search
            num_pages: Number of pages to scrape

        Returns:
            List of job dictionaries
        """
        jobs = []

        for page in range(num_pages):
            start = page * 10
            search_url = f"{self.base_url}/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={start}"

            try:
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Try multiple selectors as Indeed's structure varies
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                if not job_cards:
                    job_cards = soup.find_all('div', class_=lambda x: x and 'cardOutline' in x)
                if not job_cards:
                    job_cards = soup.find_all('a', class_=lambda x: x and 'jcs-JobTitle' in x)
                    job_cards = [card.find_parent('div') for card in job_cards if card.find_parent('div')]

                logger.info(f"Found {len(job_cards)} job cards on page {page + 1}")

                for card in job_cards:
                    try:
                        job = self._parse_job_card(card)
                        if job and job.get('title') != 'N/A':
                            jobs.append(job)
                    except Exception as e:
                        logger.error(f"Error parsing job card: {e}")
                        continue

                logger.info(f"Scraped page {page + 1}/{num_pages} - Added {len([j for j in jobs if j])} valid jobs")
                time.sleep(self.delay)

            except Exception as e:
                logger.error(f"Error scraping page {page + 1}: {e}")
                continue

        return jobs

    def _parse_job_card(self, card) -> Dict:
        """Parse individual job card"""
        try:
            # Title - try multiple selectors
            title_elem = card.find('h2', class_='jobTitle')
            if not title_elem:
                title_elem = card.find('a', class_='jcs-JobTitle')
            if not title_elem:
                title_elem = card.find('span', title=True)
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            # Company - try multiple selectors
            company_elem = card.find('span', class_='companyName')
            if not company_elem:
                company_elem = card.find('span', attrs={'data-testid': 'company-name'})
            company = company_elem.get_text(strip=True) if company_elem else "N/A"

            # Location - try multiple selectors
            location_elem = card.find('div', class_='companyLocation')
            if not location_elem:
                location_elem = card.find('div', attrs={'data-testid': 'text-location'})
            location = location_elem.get_text(strip=True) if location_elem else "Remote"

            # Job URL
            link_elem = card.find('a', class_='jcs-JobTitle')
            if not link_elem:
                link_elem = card.find('a', href=True)
            job_url = f"{self.base_url}{link_elem['href']}" if link_elem and link_elem.get('href') else ""

            # Snippet (short description)
            snippet_elem = card.find('div', class_='job-snippet')
            if not snippet_elem:
                snippet_elem = card.find('div', attrs={'class': lambda x: x and 'snippet' in x.lower() if x else False})
            description = snippet_elem.get_text(strip=True) if snippet_elem else f"Position for {title} at {company}"

            # Salary (if available)
            salary_elem = card.find('span', class_='salary-snippet')
            if not salary_elem:
                salary_elem = card.find('div', attrs={'class': lambda x: x and 'salary' in x.lower() if x else False})
            salary = salary_elem.get_text(strip=True) if salary_elem else None

            # Only return if we have minimum required fields
            if title == "N/A" or company == "N/A":
                return None

            return {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'salary': salary,
                'job_url': job_url or f"{self.base_url}/jobs?q={title.replace(' ', '+')}",
                'source': 'Indeed',
                'posted_date': datetime.utcnow(),
                'scraped_at': datetime.utcnow()
            }

        except Exception as e:
            logger.error(f"Error in _parse_job_card: {e}")
            return None

    def get_job_details(self, job_url: str) -> Dict:
        """
        Scrape detailed job information from job URL

        Args:
            job_url: URL of the job posting

        Returns:
            Dictionary with detailed job information
        """
        try:
            response = requests.get(job_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Full job description
            description_elem = soup.find('div', id='jobDescriptionText')
            description = description_elem.get_text(strip=True) if description_elem else ""

            return {
                'description': description,
                'requirements': self._extract_requirements(description)
            }

        except Exception as e:
            logger.error(f"Error getting job details: {e}")
            return {}

    def _extract_requirements(self, description: str) -> str:
        """
        Extract requirements section from job description
        This is a simple implementation - can be enhanced with NLP
        """
        requirements_keywords = ['requirements', 'qualifications', 'skills', 'experience']
        lines = description.lower().split('\n')

        requirements = []
        capture = False

        for line in lines:
            if any(keyword in line for keyword in requirements_keywords):
                capture = True
                continue

            if capture:
                if line.strip() and not any(keyword in line for keyword in ['responsibilities', 'benefits', 'about']):
                    requirements.append(line)
                else:
                    break

        return '\n'.join(requirements)


if __name__ == "__main__":
    # Test the scraper
    scraper = IndeedScraper()
    jobs = scraper.search_jobs("Python Developer", "New York", num_pages=1)

    print(f"\nFound {len(jobs)} jobs")
    for i, job in enumerate(jobs[:3], 1):
        print(f"\n--- Job {i} ---")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['job_url']}")

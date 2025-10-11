import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Scraper for LinkedIn job postings (public listings)"""

    def __init__(self, delay: int = 2):
        self.base_url = "https://www.linkedin.com"
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def search_jobs(self, query: str, location: str = "", num_pages: int = 1) -> List[Dict]:
        """Search for jobs on LinkedIn"""
        jobs = []

        for page in range(num_pages):
            start = page * 25
            search_url = f"{self.base_url}/jobs/search/?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&start={start}"

            try:
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')

                logger.info(f"LinkedIn: Found {len(job_cards)} job cards on page {page + 1}")

                for card in job_cards:
                    try:
                        job = self._parse_job_card(card)
                        if job and job.get('title') != 'N/A':
                            jobs.append(job)
                    except Exception as e:
                        logger.error(f"Error parsing LinkedIn job card: {e}")
                        continue

                time.sleep(self.delay)

            except Exception as e:
                logger.error(f"Error scraping LinkedIn page {page + 1}: {e}")
                continue

        return jobs

    def _parse_job_card(self, card) -> Dict:
        """Parse individual LinkedIn job card"""
        try:
            title_elem = card.find('h3', class_='base-search-card__title')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            company_elem = card.find('h4', class_='base-search-card__subtitle')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"

            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "Remote"

            link_elem = card.find('a', class_='base-card__full-link')
            job_url = link_elem['href'] if link_elem and link_elem.get('href') else ""

            description = f"{title} position at {company} in {location}"

            if title == "N/A" or company == "N/A":
                return None

            return {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'salary': None,
                'job_url': job_url,
                'source': 'LinkedIn',
                'posted_date': datetime.utcnow(),
                'scraped_at': datetime.utcnow()
            }

        except Exception as e:
            logger.error(f"Error in LinkedIn _parse_job_card: {e}")
            return None

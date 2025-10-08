import requests
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdzunaScraper:
    """
    Scraper for Adzuna Job Board API

    Get free API keys from: https://developer.adzuna.com/
    Free tier: 1000 calls/month
    """

    def __init__(self, app_id: str = None, app_key: str = None):
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        # Demo credentials - replace with your own from https://developer.adzuna.com/
        self.app_id = app_id or "YOUR_APP_ID"  # Get from Adzuna
        self.app_key = app_key or "YOUR_APP_KEY"  # Get from Adzuna
        self.country = "us"  # United States

    def search_jobs(self, query: str, location: str = "", num_pages: int = 1) -> List[Dict]:
        """
        Search for jobs using Adzuna API

        Args:
            query: Job search query (e.g., "Python Developer")
            location: Location for job search (e.g., "New York" or "Remote")
            num_pages: Number of pages to fetch (each page has ~10 results)

        Returns:
            List of job dictionaries
        """
        jobs = []
        results_per_page = 10

        for page in range(num_pages):
            try:
                url = f"{self.base_url}/{self.country}/search/{page + 1}"

                params = {
                    'app_id': self.app_id,
                    'app_key': self.app_key,
                    'what': query,
                    'where': location,
                    'results_per_page': results_per_page,
                    'content-type': 'application/json'
                }

                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                results = data.get('results', [])

                logger.info(f"Found {len(results)} jobs on page {page + 1}")

                for job in results:
                    try:
                        job_data = self._parse_job(job)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing job: {e}")
                        continue

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page {page + 1}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error on page {page + 1}: {e}")
                continue

        logger.info(f"Total jobs scraped: {len(jobs)}")
        return jobs

    def _parse_job(self, job: Dict) -> Dict:
        """Parse individual job from Adzuna API response"""
        try:
            # Extract salary range if available
            salary_min = job.get('salary_min')
            salary_max = job.get('salary_max')

            # Build location string
            location = job.get('location', {}).get('display_name', 'Not specified')

            return {
                'title': job.get('title', 'No title'),
                'company': job.get('company', {}).get('display_name', 'Company not specified'),
                'location': location,
                'description': job.get('description', 'No description available'),
                'salary': f"${salary_min} - ${salary_max}" if salary_min and salary_max else None,
                'job_url': job.get('redirect_url', ''),
                'source': 'Adzuna',
                'posted_date': self._parse_date(job.get('created')),
                'scraped_at': datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error in _parse_job: {e}")
            return None

    def _parse_date(self, date_str: str) -> datetime:
        """Parse date from API response"""
        try:
            if date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            pass
        return datetime.utcnow()


if __name__ == "__main__":
    # Test the scraper
    print("\nNote: This requires Adzuna API credentials")
    print("Get them free from: https://developer.adzuna.com/\n")

    scraper = AdzunaScraper()
    jobs = scraper.search_jobs("Python Developer", "New York", num_pages=1)

    print(f"\nFound {len(jobs)} jobs")
    for i, job in enumerate(jobs[:3], 1):
        print(f"\n--- Job {i} ---")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['job_url']}")

import requests
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArbeitnowScraper:
    """
    Scraper for Arbeitnow Job Board API
    Free API with no authentication required
    Good for international jobs, especially tech roles
    """

    def __init__(self):
        self.base_url = "https://www.arbeitnow.com/api/job-board-api"

    def search_jobs(self, query: str, location: str = "", num_pages: int = 1) -> List[Dict]:
        """
        Search for jobs using Arbeitnow API

        Args:
            query: Job search query (e.g., "Python Developer")
            location: Location for job search (not used by this API)
            num_pages: Number of pages to fetch

        Returns:
            List of job dictionaries
        """
        jobs = []

        try:
            # Arbeitnow API doesn't support pagination the same way
            # We'll fetch and filter results
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get('data', [])

            logger.info(f"Fetched {len(results)} total jobs from Arbeitnow")

            # Filter jobs based on query
            query_lower = query.lower()
            filtered_jobs = []

            for job in results:
                title = job.get('title', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                description = job.get('description', '').lower()

                # Check if query matches title, tags, or description
                if query_lower in title or query_lower in tags or query_lower in description:
                    filtered_jobs.append(job)

            # Limit results based on num_pages (10 per page)
            limit = num_pages * 10
            filtered_jobs = filtered_jobs[:limit]

            logger.info(f"Found {len(filtered_jobs)} jobs matching '{query}'")

            for job in filtered_jobs:
                try:
                    job_data = self._parse_job(job)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error parsing job: {e}")
                    continue

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching jobs from Arbeitnow: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        logger.info(f"Total jobs parsed: {len(jobs)}")
        return jobs

    def _parse_job(self, job: Dict) -> Dict:
        """Parse individual job from Arbeitnow API response"""
        try:
            # Extract location
            location = job.get('location', 'Remote')
            if not location:
                location = 'Remote'

            # Build description from available fields
            description = job.get('description', '')
            if not description:
                tags = job.get('tags', [])
                description = f"Position requires skills in: {', '.join(tags)}" if tags else "No description available"

            # Build company name
            company = job.get('company_name', 'Company not specified')

            return {
                'title': job.get('title', 'No title'),
                'company': company,
                'location': location,
                'description': description,
                'salary': None,  # Arbeitnow doesn't provide salary info
                'job_url': job.get('url', ''),
                'source': 'Arbeitnow',
                'posted_date': self._parse_date(job.get('created_at')),
                'scraped_at': datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error in _parse_job: {e}")
            return None

    def _parse_date(self, timestamp) -> datetime:
        """Parse date from API response"""
        try:
            if timestamp:
                # Arbeitnow uses Unix timestamp
                return datetime.fromtimestamp(int(timestamp))
        except:
            pass
        return datetime.utcnow()


if __name__ == "__main__":
    # Test the scraper
    scraper = ArbeitnowScraper()
    jobs = scraper.search_jobs("Python", num_pages=1)

    print(f"\nFound {len(jobs)} jobs")
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n--- Job {i} ---")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['job_url']}")

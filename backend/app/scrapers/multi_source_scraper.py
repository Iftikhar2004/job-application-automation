from typing import List, Dict
import logging
from .indeed_scraper import IndeedScraper
from .linkedin_scraper import LinkedInScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiSourceScraper:
    """Scraper that aggregates jobs from multiple sources"""

    def __init__(self, delay: int = 2):
        self.scrapers = {
            'indeed': IndeedScraper(delay=delay),
            'linkedin': LinkedInScraper(delay=delay)
        }

    def search_jobs(self, query: str, location: str = "", num_pages: int = 1, sources: List[str] = None) -> List[Dict]:
        """
        Search for jobs across multiple sources

        Args:
            query: Job search query
            location: Location for job search
            num_pages: Number of pages per source
            sources: List of sources to use (default: all)

        Returns:
            Aggregated list of jobs from all sources
        """
        if sources is None:
            sources = list(self.scrapers.keys())

        all_jobs = []

        for source in sources:
            if source not in self.scrapers:
                logger.warning(f"Unknown source: {source}")
                continue

            try:
                logger.info(f"Scraping {source}...")
                jobs = self.scrapers[source].search_jobs(query, location, num_pages)
                logger.info(f"Found {len(jobs)} jobs from {source}")
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Error scraping {source}: {e}")
                continue

        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()

        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        logger.info(f"Total unique jobs: {len(unique_jobs)}")
        return unique_jobs

    def get_available_sources(self) -> List[str]:
        """Get list of available job sources"""
        return list(self.scrapers.keys())

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.scrapers.multi_source_scraper import MultiSourceScraper
from app.models.models import Job
from app.services.nlp_service import NLPJobAnalyzer
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

nlp_analyzer = NLPJobAnalyzer()
multi_scraper = MultiSourceScraper()


# Pydantic schemas
class ScrapeRequest(BaseModel):
    query: str
    location: str = ""
    num_pages: int = 1
    sources: List[str] = ["indeed", "linkedin"]  # Multiple sources


class ScrapeResponse(BaseModel):
    message: str
    jobs_found: int
    jobs_saved: int


def scrape_and_save_jobs(
    query: str,
    location: str,
    num_pages: int,
    sources: List[str],
    db: Session
):
    """Background task to scrape and save jobs from multiple sources"""
    try:
        # Use multi-source scraper
        jobs = multi_scraper.search_jobs(query, location, num_pages, sources)

        saved_count = 0

        for job_data in jobs:
            try:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.job_url == job_data['job_url']).first()
                if existing_job:
                    continue

                # Analyze job with NLP
                analysis = nlp_analyzer.analyze_job(
                    job_data.get('description', ''),
                    job_data.get('requirements', '')
                )

                # Create job entry
                db_job = Job(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    job_url=job_data['job_url'],
                    source=job_data['source'],
                    posted_date=job_data.get('posted_date', datetime.utcnow()),
                    scraped_at=datetime.utcnow(),
                    required_skills=str(analysis['required_skills']),
                    experience_required=analysis['experience_years'],
                    is_active=True
                )

                # Extract salary if available
                if job_data.get('salary'):
                    salary_range = nlp_analyzer.extract_salary_range(job_data['salary'])
                    db_job.salary_min = salary_range.get('min')
                    db_job.salary_max = salary_range.get('max')

                db.add(db_job)
                saved_count += 1

            except Exception as e:
                logger.error(f"Error saving job: {e}")
                continue

        db.commit()
        logger.info(f"Scraping complete: {saved_count} jobs saved")

    except Exception as e:
        logger.error(f"Error in scrape_and_save_jobs: {e}")
        db.rollback()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_jobs(
    scrape_request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Scrape jobs from specified source

    Args:
        scrape_request: Scraping parameters (query, location, pages, source)

    Returns:
        Response with scraping status
    """
    available_sources = multi_scraper.get_available_sources()
    invalid_sources = [s for s in scrape_request.sources if s not in available_sources]

    if invalid_sources:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sources: {invalid_sources}. Available: {available_sources}"
        )

    # Add scraping task to background
    background_tasks.add_task(
        scrape_and_save_jobs,
        scrape_request.query,
        scrape_request.location,
        scrape_request.num_pages,
        scrape_request.sources,
        db
    )

    return ScrapeResponse(
        message=f"Scraping started from: {', '.join(scrape_request.sources)}",
        jobs_found=0,
        jobs_saved=0
    )


@router.post("/scrape-sync", response_model=ScrapeResponse)
def scrape_jobs_sync(
    scrape_request: ScrapeRequest,
    db: Session = Depends(get_db)
):
    """
    Scrape jobs synchronously (blocks until complete)

    Args:
        scrape_request: Scraping parameters

    Returns:
        Response with number of jobs found and saved
    """
    available_sources = multi_scraper.get_available_sources()
    invalid_sources = [s for s in scrape_request.sources if s not in available_sources]

    if invalid_sources:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sources: {invalid_sources}. Available: {available_sources}"
        )

    try:
        jobs = multi_scraper.search_jobs(
            scrape_request.query,
            scrape_request.location,
            scrape_request.num_pages,
            scrape_request.sources
        )

        saved_count = 0

        for job_data in jobs:
            try:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.job_url == job_data['job_url']).first()
                if existing_job:
                    continue

                # Analyze job with NLP
                analysis = nlp_analyzer.analyze_job(
                    job_data.get('description', ''),
                    job_data.get('requirements', '')
                )

                # Create job entry
                db_job = Job(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    description=job_data['description'],
                    job_url=job_data['job_url'],
                    source=job_data['source'],
                    posted_date=job_data.get('posted_date', datetime.utcnow()),
                    scraped_at=datetime.utcnow(),
                    required_skills=str(analysis['required_skills']),
                    experience_required=analysis['experience_years'],
                    is_active=True
                )

                # Extract salary if available
                if job_data.get('salary'):
                    salary_range = nlp_analyzer.extract_salary_range(job_data['salary'])
                    db_job.salary_min = salary_range.get('min')
                    db_job.salary_max = salary_range.get('max')

                db.add(db_job)
                saved_count += 1

            except Exception as e:
                logger.error(f"Error saving job: {e}")
                continue

        db.commit()

        return ScrapeResponse(
            message="Scraping completed",
            jobs_found=len(jobs),
            jobs_saved=saved_count
        )

    except Exception as e:
        logger.error(f"Error scraping jobs: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

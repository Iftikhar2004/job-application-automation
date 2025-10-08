from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.scrapers.indeed_scraper import IndeedScraper
from app.scrapers.arbeitnow_scraper import ArbeitnowScraper
from app.models.models import Job
from app.services.nlp_service import NLPJobAnalyzer
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

nlp_analyzer = NLPJobAnalyzer()


# Pydantic schemas
class ScrapeRequest(BaseModel):
    query: str
    location: str = ""
    num_pages: int = 1
    source: str = "indeed"


class ScrapeResponse(BaseModel):
    message: str
    jobs_found: int
    jobs_saved: int


def scrape_and_save_jobs(
    query: str,
    location: str,
    num_pages: int,
    source: str,
    db: Session
):
    """Background task to scrape and save jobs"""
    try:
        if source.lower() == "indeed":
            scraper = IndeedScraper()
            jobs = scraper.search_jobs(query, location, num_pages)
        elif source.lower() == "arbeitnow":
            scraper = ArbeitnowScraper()
            jobs = scraper.search_jobs(query, location, num_pages)
        else:
            logger.error(f"Unsupported source: {source}")
            return

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
    if scrape_request.source.lower() not in ["indeed", "arbeitnow"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source: {scrape_request.source}. Supported: indeed, arbeitnow"
        )

    # Add scraping task to background
    background_tasks.add_task(
        scrape_and_save_jobs,
        scrape_request.query,
        scrape_request.location,
        scrape_request.num_pages,
        scrape_request.source,
        db
    )

    return ScrapeResponse(
        message=f"Scraping started for {scrape_request.source}",
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
    if scrape_request.source.lower() not in ["indeed", "arbeitnow"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source: {scrape_request.source}. Supported: indeed, arbeitnow"
        )

    try:
        if scrape_request.source.lower() == "indeed":
            scraper = IndeedScraper()
            jobs = scraper.search_jobs(
                scrape_request.query,
                scrape_request.location,
                scrape_request.num_pages
            )
        elif scrape_request.source.lower() == "arbeitnow":
            scraper = ArbeitnowScraper()
            jobs = scraper.search_jobs(
                scrape_request.query,
                scrape_request.location,
                scrape_request.num_pages
            )
        else:
            jobs = []

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

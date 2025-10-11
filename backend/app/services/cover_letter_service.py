from typing import Dict, Optional
import logging
import google.generativeai as genai
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """Generate personalized cover letters using Google Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.client = None
            logger.warning("Gemini API key not provided. Cover letter generation will use templates.")

    def generate_cover_letter(
        self,
        job_title: str,
        company: str,
        job_description: str,
        user_name: str,
        user_skills: list,
        user_experience: str,
        tone: str = "professional"
    ) -> str:
        """
        Generate a personalized cover letter

        Args:
            job_title: Job title
            company: Company name
            job_description: Full job description
            user_name: Applicant's name
            user_skills: List of user's skills
            user_experience: User's experience summary
            tone: Tone of the letter (professional, enthusiastic, formal)

        Returns:
            Generated cover letter text
        """
        if self.client:
            return self._generate_with_ai(
                job_title, company, job_description,
                user_name, user_skills, user_experience, tone
            )
        else:
            return self._generate_template(
                job_title, company, job_description,
                user_name, user_skills, user_experience
            )

    def _generate_with_ai(
        self,
        job_title: str,
        company: str,
        job_description: str,
        user_name: str,
        user_skills: list,
        user_experience: str,
        tone: str
    ) -> str:
        """Generate cover letter using Gemini API"""
        try:
            skills_str = ", ".join(user_skills)

            prompt = f"""Write a professional, human-sounding cover letter for this job application. The letter should NOT look AI-generated.

Job Details:
- Position: {job_title}
- Company: {company}
- Job Description: {job_description}

Candidate Details:
- Name: {user_name}
- Skills: {skills_str}
- Experience: {user_experience}

CRITICAL REQUIREMENTS:
1. Write ONLY the body paragraphs - NO placeholder headers like [Your Name], [Date], [Address], etc.
2. Start directly with "Dear Hiring Manager," or "Dear [Company] Team,"
3. Write 3-4 concise paragraphs (250-300 words total)
4. Use a {tone} tone
5. Make it sound natural and conversational, NOT robotic
6. Highlight 2-3 relevant skills that match the job requirements
7. Show genuine enthusiasm for the role and company
8. Include specific details from the job description
9. End with "Best regards," or "Sincerely," followed by just the name: {user_name}
10. NO brackets, NO placeholders, NO instructions to the reader
11. Write in first person and make it personal

Example of what NOT to do: "[Your experience]", "[ Briefly mention...]", "[Company Address]"
Example of what TO do: Direct, complete sentences with real content.

Write the cover letter now:"""

            response = self.client.generate_content(prompt)
            cover_letter = response.text.strip()
            logger.info(f"Generated AI cover letter for {job_title} at {company}")
            return cover_letter

        except Exception as e:
            logger.error(f"Error generating AI cover letter: {e}")
            return self._generate_template(job_title, company, job_description,
                                          user_name, user_skills, user_experience)

    def _generate_template(
        self,
        job_title: str,
        company: str,
        job_description: str,
        user_name: str,
        user_skills: list,
        user_experience: str
    ) -> str:
        """Generate cover letter using template (fallback)"""
        skills_str = ", ".join(user_skills[:5])  # Top 5 skills

        template = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my background in {user_experience}, I am confident that I would be a valuable addition to your team.

My technical expertise includes {skills_str}, which align well with the requirements outlined in your job posting. Throughout my career, I have successfully delivered high-quality solutions and collaborated effectively with cross-functional teams to achieve project goals.

I am particularly drawn to {company} because of your commitment to innovation and excellence in the industry. I am excited about the opportunity to contribute my skills and experience to help drive your projects forward.

Thank you for considering my application. I look forward to the opportunity to discuss how my background and skills would be a great fit for your team.

Sincerely,
{user_name}
"""

        logger.info(f"Generated template cover letter for {job_title} at {company}")
        return template

    def customize_cover_letter(
        self,
        base_letter: str,
        customization_notes: str
    ) -> str:
        """
        Customize an existing cover letter based on user notes

        Args:
            base_letter: Existing cover letter
            customization_notes: User's customization requirements

        Returns:
            Customized cover letter
        """
        if not self.client:
            return base_letter

        try:
            prompt = f"""
You are an expert at customizing cover letters. Given this cover letter:

{base_letter}

Please customize it according to these requirements:
{customization_notes}

Keep the same professional tone and format.
"""

            response = self.client.generate_content(prompt)
            customized = response.text.strip()
            logger.info("Cover letter customized successfully")
            return customized

        except Exception as e:
            logger.error(f"Error customizing cover letter: {e}")
            return base_letter

    def generate_multiple_versions(
        self,
        job_title: str,
        company: str,
        job_description: str,
        user_name: str,
        user_skills: list,
        user_experience: str,
        num_versions: int = 3
    ) -> list:
        """
        Generate multiple versions of cover letter with different tones

        Args:
            Similar to generate_cover_letter
            num_versions: Number of versions to generate

        Returns:
            List of cover letter versions
        """
        tones = ["professional", "enthusiastic", "formal"][:num_versions]
        versions = []

        for tone in tones:
            letter = self.generate_cover_letter(
                job_title, company, job_description,
                user_name, user_skills, user_experience, tone
            )
            versions.append({
                "tone": tone,
                "content": letter
            })

        return versions


if __name__ == "__main__":
    # Test the generator
    generator = CoverLetterGenerator()

    letter = generator.generate_cover_letter(
        job_title="Senior Python Developer",
        company="Tech Corp",
        job_description="We need a Python developer with FastAPI and ML experience",
        user_name="John Doe",
        user_skills=["Python", "FastAPI", "Machine Learning", "Docker"],
        user_experience="5 years as a full-stack developer",
        tone="professional"
    )

    print("\n--- Generated Cover Letter ---")
    print(letter)

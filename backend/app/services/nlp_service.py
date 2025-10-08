import re
from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLPJobAnalyzer:
    """Analyze job descriptions using NLP techniques"""

    def __init__(self):
        self.common_skills = self._load_common_skills()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)

    def _load_common_skills(self) -> Set[str]:
        """Load common technical skills for matching"""
        return {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',

            # Web Technologies
            'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask', 'fastapi',
            'html', 'css', 'sass', 'webpack', 'nextjs', 'redux', 'graphql', 'rest',

            # Data Science & ML
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
            'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'jupyter', 'data analysis', 'statistics', 'neural networks',

            # Databases
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'dynamodb', 'sqlite', 'oracle', 'sql server',

            # DevOps & Cloud
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'ci/cd',
            'terraform', 'ansible', 'linux', 'bash', 'nginx',

            # Other
            'agile', 'scrum', 'rest api', 'microservices', 'testing', 'tdd', 'unit testing',
            'selenium', 'pytest', 'jest', 'api', 'websockets', 'async'
        }

    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from job description

        Args:
            text: Job description text

        Returns:
            List of identified skills
        """
        text_lower = text.lower()
        found_skills = []

        for skill in self.common_skills:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return found_skills

    def extract_experience_years(self, text: str) -> int:
        """
        Extract required years of experience from job description

        Args:
            text: Job description text

        Returns:
            Number of years of experience required (default: 0)
        """
        # Patterns like "3+ years", "5-7 years", "minimum 2 years"
        patterns = [
            r'(\d+)\+?\s*(?:to|\-)\s*(\d+)?\s*years?',
            r'minimum\s+(\d+)\s*years?',
            r'(\d+)\+\s*years?',
            r'at least\s+(\d+)\s*years?'
        ]

        text_lower = text.lower()
        years = []

        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    years.extend([int(y) for y in match if y and y.isdigit()])
                else:
                    if match.isdigit():
                        years.append(int(match))

        return min(years) if years else 0

    def extract_salary_range(self, text: str) -> Dict[str, float]:
        """
        Extract salary range from job description

        Args:
            text: Job description or salary text

        Returns:
            Dictionary with min and max salary
        """
        # Patterns like "$80,000 - $120,000", "$80k-$100k", "80-100K"
        patterns = [
            r'\$(\d{2,3}),?(\d{3})\s*-\s*\$?(\d{2,3}),?(\d{3})',  # $80,000 - $120,000
            r'\$(\d{2,3})k\s*-\s*\$?(\d{2,3})k',  # $80k-$100k
            r'(\d{2,3})k\s*-\s*(\d{2,3})k',  # 80k-100k
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 4:  # Full format with commas
                    min_sal = float(groups[0] + groups[1])
                    max_sal = float(groups[2] + groups[3])
                elif len(groups) == 2:  # K format
                    min_sal = float(groups[0]) * 1000
                    max_sal = float(groups[1]) * 1000

                return {'min': min_sal, 'max': max_sal}

        return {'min': None, 'max': None}

    def calculate_match_score(self, job_description: str, user_skills: List[str],
                             user_experience: int) -> float:
        """
        Calculate match score between job and user profile

        Args:
            job_description: Job description text
            user_skills: List of user's skills
            user_experience: User's years of experience

        Returns:
            Match score between 0 and 100
        """
        # Extract job requirements
        required_skills = self.extract_skills(job_description)
        required_experience = self.extract_experience_years(job_description)

        # Skill matching (70% weight)
        if required_skills:
            user_skills_lower = [s.lower() for s in user_skills]
            matching_skills = len(set(required_skills) & set(user_skills_lower))
            skill_score = (matching_skills / len(required_skills)) * 70
        else:
            skill_score = 35  # Neutral score if no skills detected

        # Experience matching (30% weight)
        if required_experience > 0:
            if user_experience >= required_experience:
                exp_score = 30
            else:
                # Partial credit if close to requirement
                exp_score = (user_experience / required_experience) * 30
        else:
            exp_score = 15  # Neutral score if no experience requirement

        total_score = min(skill_score + exp_score, 100)
        return round(total_score, 2)

    def analyze_job(self, job_description: str, requirements: str = "") -> Dict:
        """
        Comprehensive job analysis

        Args:
            job_description: Full job description
            requirements: Separate requirements section (if available)

        Returns:
            Dictionary with analysis results
        """
        full_text = f"{job_description} {requirements}"

        analysis = {
            'required_skills': self.extract_skills(full_text),
            'experience_years': self.extract_experience_years(full_text),
            'salary_range': self.extract_salary_range(full_text),
            'text_length': len(full_text),
            'is_senior_role': self._is_senior_role(full_text)
        }

        logger.info(f"Job analysis complete: {len(analysis['required_skills'])} skills found")
        return analysis

    def _is_senior_role(self, text: str) -> bool:
        """Check if job is for senior level"""
        senior_keywords = ['senior', 'lead', 'principal', 'staff', 'architect', 'director']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in senior_keywords)

    def compare_jobs(self, job_descriptions: List[str]) -> List[float]:
        """
        Compare similarity between multiple job descriptions

        Args:
            job_descriptions: List of job description texts

        Returns:
            Similarity scores matrix
        """
        if len(job_descriptions) < 2:
            return []

        try:
            tfidf_matrix = self.vectorizer.fit_transform(job_descriptions)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            return similarity_matrix.tolist()
        except Exception as e:
            logger.error(f"Error comparing jobs: {e}")
            return []


if __name__ == "__main__":
    # Test the analyzer
    analyzer = NLPJobAnalyzer()

    sample_job = """
    We are looking for a Senior Python Developer with 5+ years of experience.
    Required skills: Python, Django, FastAPI, PostgreSQL, Docker, AWS.
    Experience with React and TypeScript is a plus.
    Salary: $120,000 - $150,000
    """

    user_skills = ['python', 'django', 'fastapi', 'postgresql', 'docker']
    user_exp = 6

    analysis = analyzer.analyze_job(sample_job)
    print("\n--- Job Analysis ---")
    print(f"Skills: {analysis['required_skills']}")
    print(f"Experience: {analysis['experience_years']} years")
    print(f"Salary: ${analysis['salary_range']['min']:,.0f} - ${analysis['salary_range']['max']:,.0f}")
    print(f"Senior Role: {analysis['is_senior_role']}")

    match_score = analyzer.calculate_match_score(sample_job, user_skills, user_exp)
    print(f"\nMatch Score: {match_score}%")

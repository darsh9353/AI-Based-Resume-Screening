import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter

class SkillMatcher:
    def __init__(self):
        self.job_requirements = ""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        
        # Skill categories and their weights
        self.skill_categories = {
            'technical': 1.0,
            'soft_skills': 0.8,
            'tools': 0.9,
            'languages': 0.7,
            'frameworks': 0.9,
            'databases': 0.8,
            'cloud': 0.9
        }
        
        # Common skill synonyms
        self.skill_synonyms = {
            'js': 'javascript',
            'react.js': 'react',
            'node.js': 'nodejs',
            'c++': 'cpp',
            'c#': 'csharp',
            'asp.net': 'aspnet',
            'machine learning': 'ml',
            'artificial intelligence': 'ai',
            'data science': 'datascience',
            'dev ops': 'devops',
            'ui/ux': 'ui ux',
            'ui/ux design': 'ui ux design'
        }

    def update_requirements(self, requirements):
        """Update job requirements"""
        self.job_requirements = requirements.lower()

    def normalize_skills(self, skills):
        """Normalize and clean skills"""
        normalized = []
        for skill in skills:
            skill_lower = skill.lower().strip()
            
            # Apply synonyms
            for synonym, replacement in self.skill_synonyms.items():
                if synonym in skill_lower:
                    skill_lower = skill_lower.replace(synonym, replacement)
            
            # Clean up common variations
            skill_lower = re.sub(r'[^\w\s]', '', skill_lower)
            skill_lower = skill_lower.strip()
            
            if skill_lower and len(skill_lower) > 1:
                normalized.append(skill_lower)
        
        return normalized

    def extract_skills_from_text(self, text):
        """Extract skills from text using pattern matching"""
        skills = set()
        text_lower = text.lower()
        
        # Common skill patterns
        skill_patterns = [
            r'\b(?:python|java|javascript|js|c\+\+|c#|php|ruby|swift|kotlin|go|rust|scala|r|matlab)\b',
            r'\b(?:html|css|react|angular|vue|node\.?js|express|django|flask|spring|asp\.?net|laravel)\b',
            r'\b(?:mysql|postgresql|mongodb|redis|oracle|sql\s+server|sqlite|dynamodb|cassandra)\b',
            r'\b(?:aws|azure|google\s+cloud|docker|kubernetes|terraform|jenkins|git|github|gitlab)\b',
            r'\b(?:pandas|numpy|scikit-learn|tensorflow|pytorch|matplotlib|seaborn|jupyter|spark|hadoop)\b',
            r'\b(?:android|ios|react\s+native|flutter|xamarin)\b',
            r'\b(?:selenium|junit|pytest|mocha|jest|cypress|postman|soapui)\b',
            r'\b(?:figma|adobe\s+xd|sketch|photoshop|illustrator|invision|zeplin)\b',
            r'\b(?:agile|scrum|kanban|jira|confluence|trello|asana|monday\.com)\b',
            r'\b(?:leadership|communication|teamwork|problem\s+solving|critical\s+thinking|time\s+management|adaptability)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            skills.update(matches)
        
        return list(skills)

    def calculate_exact_match_score(self, candidate_skills, required_skills):
        """Calculate exact match score"""
        if not required_skills:
            return 0.0
        
        candidate_set = set(candidate_skills)
        required_set = set(required_skills)
        
        if not required_set:
            return 0.0
        
        # Calculate precision and recall
        matched = len(candidate_set.intersection(required_set))
        precision = matched / len(candidate_set) if candidate_set else 0
        recall = matched / len(required_set) if required_set else 0
        
        # F1 score
        if precision + recall == 0:
            return 0.0
        
        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score

    def calculate_semantic_similarity(self, candidate_skills, required_skills):
        """Calculate semantic similarity using TF-IDF and cosine similarity"""
        if not candidate_skills or not required_skills:
            return 0.0
        
        # Combine skills into text documents
        candidate_text = ' '.join(candidate_skills)
        required_text = ' '.join(required_skills)
        
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([candidate_text, required_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.0

    def calculate_skill_coverage(self, candidate_skills, required_skills):
        """Calculate skill coverage percentage"""
        if not required_skills:
            return 0.0
        
        candidate_set = set(candidate_skills)
        required_set = set(required_skills)
        
        matched = len(candidate_set.intersection(required_set))
        coverage = matched / len(required_set) if required_set else 0
        
        return coverage

    def categorize_skills(self, skills):
        """Categorize skills by type"""
        categories = {
            'technical': [],
            'soft_skills': [],
            'tools': [],
            'languages': [],
            'frameworks': [],
            'databases': [],
            'cloud': []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # Programming languages
            if skill_lower in ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab']:
                categories['languages'].append(skill)
            # Frameworks
            elif skill_lower in ['react', 'angular', 'vue', 'express', 'django', 'flask', 'spring', 'asp.net', 'laravel']:
                categories['frameworks'].append(skill)
            # Databases
            elif skill_lower in ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite', 'dynamodb', 'cassandra']:
                categories['databases'].append(skill)
            # Cloud/DevOps
            elif skill_lower in ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git', 'github', 'gitlab']:
                categories['cloud'].append(skill)
            # Tools
            elif skill_lower in ['selenium', 'junit', 'pytest', 'mocha', 'jest', 'cypress', 'postman', 'soapui', 'figma', 'adobe xd', 'sketch', 'photoshop', 'illustrator']:
                categories['tools'].append(skill)
            # Soft skills
            elif skill_lower in ['leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking', 'time management', 'adaptability']:
                categories['soft_skills'].append(skill)
            # Technical skills (catch-all for other technical skills)
            else:
                categories['technical'].append(skill)
        
        return categories

    def calculate_weighted_score(self, candidate_skills, required_skills):
        """Calculate weighted score based on skill categories"""
        candidate_categories = self.categorize_skills(candidate_skills)
        required_categories = self.categorize_skills(required_skills)
        
        total_score = 0
        total_weight = 0
        
        for category, weight in self.skill_categories.items():
            candidate_cat_skills = candidate_categories.get(category, [])
            required_cat_skills = required_categories.get(category, [])
            
            if required_cat_skills:
                category_score = self.calculate_exact_match_score(candidate_cat_skills, required_cat_skills)
                total_score += category_score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0

    def match_skills(self, candidate_skills, job_requirements):
        """Main method to match candidate skills against job requirements"""
        # Normalize skills
        candidate_skills = self.normalize_skills(candidate_skills)
        
        # Extract skills from job requirements
        required_skills = self.extract_skills_from_text(job_requirements)
        required_skills = self.normalize_skills(required_skills)
        
        # Calculate different types of scores
        exact_match_score = self.calculate_exact_match_score(candidate_skills, required_skills)
        semantic_similarity = self.calculate_semantic_similarity(candidate_skills, required_skills)
        skill_coverage = self.calculate_skill_coverage(candidate_skills, required_skills)
        weighted_score = self.calculate_weighted_score(candidate_skills, required_skills)
        
        # Combine scores (weighted average)
        final_score = (
            exact_match_score * 0.4 +
            semantic_similarity * 0.3 +
            skill_coverage * 0.2 +
            weighted_score * 0.1
        )
        
        # Find matched and missing skills
        candidate_set = set(candidate_skills)
        required_set = set(required_skills)
        
        matched_skills = list(candidate_set.intersection(required_set))
        missing_skills = list(required_set - candidate_set)
        
        # Add bonus for having additional relevant skills
        if len(candidate_skills) > len(required_skills):
            additional_skills = len(candidate_skills) - len(required_skills)
            bonus = min(additional_skills * 0.05, 0.1)  # Max 10% bonus
            final_score = min(final_score + bonus, 1.0)
        
        return final_score, matched_skills, missing_skills

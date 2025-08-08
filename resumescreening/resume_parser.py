import spacy
import re
import PyPDF2
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeParser:
    def __init__(self):
        # Load SpaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy model not found. Please run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Common skills database
        self.skills_db = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net', 'laravel'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite', 'dynamodb', 'cassandra'],
            'cloud': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git', 'github', 'gitlab'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter', 'spark', 'hadoop'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'terraform', 'ansible', 'chef', 'puppet'],
            'testing': ['selenium', 'junit', 'pytest', 'mocha', 'jest', 'cypress', 'postman', 'soapui'],
            'design': ['figma', 'adobe xd', 'sketch', 'photoshop', 'illustrator', 'invision', 'zeplin'],
            'project_management': ['agile', 'scrum', 'kanban', 'jira', 'confluence', 'trello', 'asana', 'monday.com'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking', 'time management', 'adaptability']
        }
        
        # Education keywords
        self.education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'school', 'academy', 'institute']
        
        # Experience keywords
        self.experience_keywords = ['experience', 'work', 'job', 'position', 'role', 'responsibility', 'achievement', 'project']

    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def extract_text_from_docx(self, filepath):
        """Extract text from DOCX file"""
        try:
            doc = Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""

    def extract_text_from_txt(self, filepath):
        """Extract text from TXT file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""

    def extract_text(self, filepath):
        """Extract text from various file formats"""
        file_extension = filepath.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(filepath)
        elif file_extension == 'docx':
            return self.extract_text_from_docx(filepath)
        elif file_extension == 'txt':
            return self.extract_text_from_txt(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def extract_name(self, text):
        """Extract candidate name using NLP"""
        if not self.nlp:
            return "Unknown"
        
        doc = self.nlp(text[:1000])  # Analyze first 1000 characters
        
        # Look for person names
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        
        # Fallback: look for patterns like "Name: John Doe" or "John Doe"
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line.split()) <= 4:  # Name should be 1-4 words
                # Check if it looks like a name (contains letters and possibly spaces)
                if re.match(r'^[A-Za-z\s]+$', line) and len(line) > 2:
                    return line
        
        return "Unknown"

    def extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""

    def extract_phone(self, text):
        """Extract phone number"""
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            return ''.join(phones[0])
        return ""

    def extract_skills(self, text):
        """Extract skills from text"""
        skills = set()
        text_lower = text.lower()
        
        # Extract skills from skills database
        for category, skill_list in self.skills_db.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.add(skill.lower())
        
        # Look for skill patterns in text
        skill_patterns = [
            r'\b(?:proficient in|skilled in|experience with|knowledge of)\s+([^,\n]+)',
            r'\b(?:technologies?|tools?|languages?|frameworks?):\s*([^,\n]+)',
            r'\b(?:expertise in|specialized in)\s+([^,\n]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # Clean and split skills
                skill_terms = re.split(r'[,;&]', match)
                for term in skill_terms:
                    term = term.strip()
                    if len(term) > 2 and len(term) < 50:
                        skills.add(term)
        
        return list(skills)

    def extract_education(self, text):
        """Extract education information"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in self.education_keywords):
                # Get the next few lines as education details
                education_text = line
                for j in range(1, 4):  # Look at next 3 lines
                    if i + j < len(lines):
                        education_text += " " + lines[i + j]
                education.append(education_text.strip())
        
        return education

    def extract_experience(self, text):
        """Extract work experience"""
        experience = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in self.experience_keywords):
                # Get the next few lines as experience details
                experience_text = line
                for j in range(1, 5):  # Look at next 4 lines
                    if i + j < len(lines):
                        experience_text += " " + lines[i + j]
                experience.append(experience_text.strip())
        
        return experience

    def parse_resume(self, filepath):
        """Main method to parse resume and extract all information"""
        try:
            # Extract text from file
            text = self.extract_text(filepath)
            
            if not text:
                raise ValueError("Could not extract text from file")
            
            # Extract information
            name = self.extract_name(text)
            email = self.extract_email(text)
            phone = self.extract_phone(text)
            skills = self.extract_skills(text)
            education = self.extract_education(text)
            experience = self.extract_experience(text)
            
            return {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'education': education,
                'experience': experience,
                'raw_text': text[:1000]  # Store first 1000 chars for debugging
            }
            
        except Exception as e:
            print(f"Error parsing resume: {e}")
            return {
                'name': 'Unknown',
                'email': '',
                'phone': '',
                'skills': [],
                'education': [],
                'experience': [],
                'raw_text': ''
            }

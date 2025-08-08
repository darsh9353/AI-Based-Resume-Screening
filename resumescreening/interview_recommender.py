import random
from datetime import datetime

class InterviewRecommender:
    def __init__(self):
        # Interview question templates by category
        self.question_templates = {
            'technical': {
                'python': [
                    "Can you explain the difference between a list and a tuple in Python?",
                    "How would you handle memory management in a Python application?",
                    "Describe your experience with Python frameworks like Django or Flask.",
                    "How do you approach debugging complex Python applications?",
                    "What's your experience with Python data science libraries like pandas and numpy?"
                ],
                'javascript': [
                    "Explain the concept of closures in JavaScript.",
                    "How do you handle asynchronous operations in JavaScript?",
                    "What's the difference between var, let, and const?",
                    "Describe your experience with modern JavaScript frameworks.",
                    "How do you ensure code quality in JavaScript projects?"
                ],
                'java': [
                    "Explain the difference between abstract classes and interfaces in Java.",
                    "How do you handle memory management in Java applications?",
                    "Describe your experience with Spring framework.",
                    "How do you approach multithreading in Java?",
                    "What's your experience with Java testing frameworks?"
                ],
                'web_development': [
                    "How do you ensure responsive design across different devices?",
                    "Describe your experience with modern CSS frameworks.",
                    "How do you optimize website performance?",
                    "What's your approach to cross-browser compatibility?",
                    "How do you handle state management in web applications?"
                ],
                'databases': [
                    "Explain the difference between SQL and NoSQL databases.",
                    "How do you optimize database queries for performance?",
                    "Describe your experience with database design and normalization.",
                    "How do you handle database migrations?",
                    "What's your approach to database security?"
                ],
                'cloud': [
                    "Describe your experience with AWS services.",
                    "How do you approach infrastructure as code?",
                    "Explain your experience with containerization and orchestration.",
                    "How do you ensure security in cloud environments?",
                    "What's your experience with CI/CD pipelines?"
                ]
            },
            'behavioral': [
                "Tell me about a challenging project you worked on and how you overcame obstacles.",
                "Describe a situation where you had to learn a new technology quickly.",
                "How do you handle working with difficult team members?",
                "Tell me about a time when you had to make a difficult technical decision.",
                "How do you stay updated with the latest technology trends?",
                "Describe a situation where you had to mentor a junior developer.",
                "How do you handle tight deadlines and pressure?",
                "Tell me about a project where you had to collaborate with non-technical stakeholders."
            ],
            'problem_solving': [
                "How would you design a scalable web application architecture?",
                "Explain how you would implement a caching strategy for a high-traffic website.",
                "How would you approach debugging a production issue with limited information?",
                "Describe how you would design a database schema for a social media platform.",
                "How would you implement a real-time notification system?",
                "Explain your approach to API design and documentation.",
                "How would you handle data migration in a live system?",
                "Describe how you would implement a search functionality with filters."
            ]
        }
        
        # Interview format recommendations
        self.interview_formats = {
            'high_match': {
                'format': 'Comprehensive Technical + Behavioral',
                'duration': '2-3 hours',
                'stages': [
                    'Technical screening (1 hour)',
                    'System design discussion (45 minutes)',
                    'Behavioral interview (45 minutes)',
                    'Team fit discussion (30 minutes)'
                ]
            },
            'medium_match': {
                'format': 'Technical Assessment + Behavioral',
                'duration': '1.5-2 hours',
                'stages': [
                    'Technical assessment (1 hour)',
                    'Behavioral interview (45 minutes)',
                    'Skills gap discussion (15 minutes)'
                ]
            },
            'low_match': {
                'format': 'Skills Assessment + Learning Potential',
                'duration': '1-1.5 hours',
                'stages': [
                    'Basic technical assessment (45 minutes)',
                    'Learning ability discussion (30 minutes)',
                    'Growth potential evaluation (15 minutes)'
                ]
            }
        }
        
        # Follow-up questions based on missing skills
        self.follow_up_questions = {
            'python': "Would you be interested in learning Python? What's your approach to learning new programming languages?",
            'javascript': "How do you feel about learning JavaScript? What's your experience with frontend development?",
            'react': "Are you familiar with modern frontend frameworks? How do you approach learning new technologies?",
            'aws': "What's your experience with cloud platforms? How do you approach infrastructure management?",
            'docker': "Are you familiar with containerization? How do you approach deployment and DevOps?",
            'agile': "What's your experience with agile methodologies? How do you handle project management?",
            'leadership': "Describe your leadership experience. How do you motivate and guide team members?",
            'communication': "How do you communicate technical concepts to non-technical stakeholders?"
        }

    def get_technical_questions(self, skills, missing_skills):
        """Generate technical questions based on candidate skills and gaps"""
        questions = []
        
        # Add questions for existing skills
        for skill in skills:
            skill_lower = skill.lower()
            if 'python' in skill_lower:
                questions.extend(random.sample(self.question_templates['technical']['python'], 2))
            elif 'javascript' in skill_lower or 'js' in skill_lower:
                questions.extend(random.sample(self.question_templates['technical']['javascript'], 2))
            elif 'java' in skill_lower:
                questions.extend(random.sample(self.question_templates['technical']['java'], 2))
            elif any(web_tech in skill_lower for web_tech in ['html', 'css', 'react', 'angular', 'vue']):
                questions.extend(random.sample(self.question_templates['technical']['web_development'], 2))
            elif any(db in skill_lower for db in ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle']):
                questions.extend(random.sample(self.question_templates['technical']['databases'], 2))
            elif any(cloud in skill_lower for cloud in ['aws', 'azure', 'docker', 'kubernetes']):
                questions.extend(random.sample(self.question_templates['technical']['cloud'], 2))
        
        # Add general technical questions
        questions.extend(random.sample(self.question_templates['problem_solving'], 2))
        
        return questions[:5]  # Limit to 5 questions

    def get_behavioral_questions(self, experience_level):
        """Generate behavioral questions based on experience level"""
        if experience_level == 'senior':
            return random.sample(self.question_templates['behavioral'], 4)
        elif experience_level == 'mid':
            return random.sample(self.question_templates['behavioral'], 3)
        else:
            return random.sample(self.question_templates['behavioral'], 2)

    def determine_experience_level(self, experience, skills):
        """Determine candidate experience level"""
        if len(experience) > 3 or any('senior' in exp.lower() or 'lead' in exp.lower() for exp in experience):
            return 'senior'
        elif len(experience) > 1 or len(skills) > 8:
            return 'mid'
        else:
            return 'junior'

    def get_interview_format(self, match_score):
        """Get recommended interview format based on match score"""
        if match_score >= 0.7:
            return self.interview_formats['high_match']
        elif match_score >= 0.4:
            return self.interview_formats['medium_match']
        else:
            return self.interview_formats['low_match']

    def get_follow_up_questions(self, missing_skills):
        """Generate follow-up questions for missing skills"""
        follow_ups = []
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            if 'python' in skill_lower:
                follow_ups.append(self.follow_up_questions['python'])
            elif 'javascript' in skill_lower or 'js' in skill_lower:
                follow_ups.append(self.follow_up_questions['javascript'])
            elif 'react' in skill_lower:
                follow_ups.append(self.follow_up_questions['react'])
            elif 'aws' in skill_lower or 'azure' in skill_lower:
                follow_ups.append(self.follow_up_questions['aws'])
            elif 'docker' in skill_lower:
                follow_ups.append(self.follow_up_questions['docker'])
            elif 'agile' in skill_lower or 'scrum' in skill_lower:
                follow_ups.append(self.follow_up_questions['agile'])
            elif 'leadership' in skill_lower:
                follow_ups.append(self.follow_up_questions['leadership'])
            elif 'communication' in skill_lower:
                follow_ups.append(self.follow_up_questions['communication'])
        
        return follow_ups[:3]  # Limit to 3 follow-up questions

    def get_interview_recommendations(self, match_score):
        """Get general interview recommendations based on match score"""
        if match_score >= 0.8:
            return {
                'priority': 'High',
                'recommendation': 'Strong candidate - recommend immediate interview',
                'focus_areas': ['Technical depth', 'System design', 'Leadership potential'],
                'red_flags': 'Watch for overconfidence or lack of teamwork'
            }
        elif match_score >= 0.6:
            return {
                'priority': 'Medium-High',
                'recommendation': 'Good candidate - recommend interview with focus on gaps',
                'focus_areas': ['Technical skills', 'Learning ability', 'Cultural fit'],
                'red_flags': 'Assess willingness to learn missing skills'
            }
        elif match_score >= 0.4:
            return {
                'priority': 'Medium',
                'recommendation': 'Potential candidate - consider if willing to train',
                'focus_areas': ['Learning potential', 'Basic skills', 'Motivation'],
                'red_flags': 'Evaluate training investment vs. potential'
            }
        else:
            return {
                'priority': 'Low',
                'recommendation': 'Consider for junior role or training program',
                'focus_areas': ['Learning ability', 'Motivation', 'Cultural fit'],
                'red_flags': 'May require significant training investment'
            }

    def generate_recommendations(self, resume_data, match_score, matched_skills, missing_skills):
        """Generate comprehensive interview recommendations"""
        experience_level = self.determine_experience_level(resume_data.get('experience', []), resume_data.get('skills', []))
        
        # Get interview format
        interview_format = self.get_interview_format(match_score)
        
        # Generate questions
        technical_questions = self.get_technical_questions(resume_data.get('skills', []), missing_skills)
        behavioral_questions = self.get_behavioral_questions(experience_level)
        follow_up_questions = self.get_follow_up_questions(missing_skills)
        
        # Get general recommendations
        general_recommendations = self.get_interview_recommendations(match_score)
        
        return {
            'interview_format': interview_format,
            'technical_questions': technical_questions,
            'behavioral_questions': behavioral_questions,
            'follow_up_questions': follow_up_questions,
            'general_recommendations': general_recommendations,
            'experience_level': experience_level,
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'generated_at': datetime.now().isoformat()
        }

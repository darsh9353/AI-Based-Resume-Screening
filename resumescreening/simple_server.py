import json
import sqlite3
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SimpleResumeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'message': 'AI Resume Screening API',
                'status': 'running',
                'endpoints': [
                    '/api/upload-resume',
                    '/api/candidates',
                    '/api/statistics'
                ]
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/candidates':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            candidates = self.get_all_candidates()
            response = {'candidates': candidates}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/statistics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats = self.get_statistics()
            self.wfile.write(json.dumps(stats).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/api/upload-resume':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                # For demo purposes, create sample data without parsing the actual file
                resume_data = {
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'phone': '+1-555-0123',
                    'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
                    'experience': '5 years of software development experience',
                    'education': 'Bachelor of Computer Science'
                }
                
                # Default job requirements
                job_requirements = 'Python, JavaScript, React'
                required_skills = [skill.strip() for skill in job_requirements.split(',')]
                
                # Simple skill matching
                matched_skills = [skill for skill in resume_data['skills'] if skill in required_skills]
                missing_skills = [skill for skill in required_skills if skill not in resume_data['skills']]
                match_score = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
                
                # Generate interview recommendations
                interview_recommendations = {
                    'format': 'Technical + Behavioral',
                    'duration': '60 minutes',
                    'questions': [
                        'Tell me about your experience with Python',
                        'How do you handle state management in React?',
                        'Describe a challenging project you worked on'
                    ]
                }
                
                # Save to database
                candidate_id = self.save_candidate({
                    'name': resume_data['name'],
                    'email': resume_data['email'],
                    'phone': resume_data['phone'],
                    'skills': resume_data['skills'],
                    'experience': resume_data['experience'],
                    'education': resume_data['education'],
                    'match_score': match_score,
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills,
                    'interview_recommendations': interview_recommendations,
                    'resume_file': 'sample_resume.pdf',
                    'upload_date': datetime.now().isoformat()
                })
                
                response = {
                    'success': True,
                    'candidate_id': candidate_id,
                    'resume_data': resume_data,
                    'match_score': match_score,
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills,
                    'interview_recommendations': interview_recommendations
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                response = {'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def init_database(self):
        conn = sqlite3.connect('resume_screening.db')
        cursor = conn.cursor()
        
        # Create candidates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                skills TEXT,
                experience TEXT,
                education TEXT,
                match_score REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                interview_recommendations TEXT,
                resume_file TEXT,
                upload_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_candidate(self, candidate_data):
        conn = sqlite3.connect('resume_screening.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO candidates (name, email, phone, skills, experience, education, 
                                  match_score, matched_skills, missing_skills, 
                                  interview_recommendations, resume_file, upload_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate_data['name'],
            candidate_data['email'],
            candidate_data['phone'],
            json.dumps(candidate_data['skills']),
            candidate_data['experience'],
            candidate_data['education'],
            candidate_data['match_score'],
            json.dumps(candidate_data['matched_skills']),
            json.dumps(candidate_data['missing_skills']),
            json.dumps(candidate_data['interview_recommendations']),
            candidate_data['resume_file'],
            candidate_data['upload_date']
        ))
        
        candidate_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return candidate_id

    def get_all_candidates(self):
        conn = sqlite3.connect('resume_screening.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM candidates ORDER BY upload_date DESC')
        rows = cursor.fetchall()
        
        candidates = []
        for row in rows:
            candidates.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'skills': json.loads(row[4]) if row[4] else [],
                'experience': row[5],
                'education': row[6],
                'match_score': row[7],
                'matched_skills': json.loads(row[8]) if row[8] else [],
                'missing_skills': json.loads(row[9]) if row[9] else [],
                'interview_recommendations': json.loads(row[10]) if row[10] else {},
                'resume_file': row[11],
                'upload_date': row[12]
            })
        
        conn.close()
        return candidates

    def get_statistics(self):
        conn = sqlite3.connect('resume_screening.db')
        cursor = conn.cursor()
        
        # Total candidates
        cursor.execute('SELECT COUNT(*) FROM candidates')
        total_candidates = cursor.fetchone()[0]
        
        # Average match score
        cursor.execute('SELECT AVG(match_score) FROM candidates')
        avg_score = cursor.fetchone()[0] or 0
        
        # High match candidates (>80%)
        cursor.execute('SELECT COUNT(*) FROM candidates WHERE match_score > 80')
        high_match = cursor.fetchone()[0]
        
        # Medium match candidates (50-80%)
        cursor.execute('SELECT COUNT(*) FROM candidates WHERE match_score BETWEEN 50 AND 80')
        medium_match = cursor.fetchone()[0]
        
        # Low match candidates (<50%)
        cursor.execute('SELECT COUNT(*) FROM candidates WHERE match_score < 50')
        low_match = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_candidates': total_candidates,
            'average_score': round(avg_score, 2),
            'high_match': high_match,
            'medium_match': medium_match,
            'low_match': low_match
        }

def run_server():
    # Initialize database
    handler = SimpleResumeHandler()
    handler.init_database()
    
    server = HTTPServer(('localhost', 5000), SimpleResumeHandler)
    print("Starting AI Resume Screening Server...")
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    server.serve_forever()

if __name__ == '__main__':
    run_server()

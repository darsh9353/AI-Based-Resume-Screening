import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='resume_screening.db'):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create candidates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                skills TEXT,  -- JSON array
                experience TEXT,  -- JSON array
                education TEXT,  -- JSON array
                match_score REAL DEFAULT 0.0,
                matched_skills TEXT,  -- JSON array
                missing_skills TEXT,  -- JSON array
                interview_recommendations TEXT,  -- JSON object
                resume_file TEXT,
                upload_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create job_requirements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirements TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create interview_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                interview_date TEXT,
                interviewer TEXT,
                notes TEXT,
                rating INTEGER,
                status TEXT DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_candidate(self, candidate_data):
        """Save candidate data to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO candidates (
                    name, email, phone, skills, experience, education,
                    match_score, matched_skills, missing_skills,
                    interview_recommendations, resume_file, upload_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                candidate_data['name'],
                candidate_data['email'],
                candidate_data['phone'],
                json.dumps(candidate_data['skills']),
                json.dumps(candidate_data['experience']),
                json.dumps(candidate_data['education']),
                candidate_data['match_score'],
                json.dumps(candidate_data['matched_skills']),
                json.dumps(candidate_data['missing_skills']),
                json.dumps(candidate_data['interview_recommendations']),
                candidate_data['resume_file'],
                candidate_data['upload_date']
            ))
            
            candidate_id = cursor.lastrowid
            conn.commit()
            return candidate_id
            
        except Exception as e:
            print(f"Error saving candidate: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def get_candidate(self, candidate_id):
        """Get candidate by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            print(f"Error getting candidate: {e}")
            return None
        finally:
            conn.close()

    def get_all_candidates(self):
        """Get all candidates ordered by match score"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM candidates 
                ORDER BY match_score DESC, created_at DESC
            ''')
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error getting candidates: {e}")
            return []
        finally:
            conn.close()

    def update_candidate_score(self, candidate_id, match_score, matched_skills, missing_skills):
        """Update candidate match score and skills"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE candidates 
                SET match_score = ?, matched_skills = ?, missing_skills = ?
                WHERE id = ?
            ''', (
                match_score,
                json.dumps(matched_skills),
                json.dumps(missing_skills),
                candidate_id
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error updating candidate score: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete_candidate(self, candidate_id):
        """Delete candidate by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM candidates WHERE id = ?', (candidate_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def save_job_requirements(self, requirements):
        """Save job requirements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Delete existing requirements
            cursor.execute('DELETE FROM job_requirements')
            
            # Insert new requirements
            cursor.execute('''
                INSERT INTO job_requirements (requirements, updated_at)
                VALUES (?, ?)
            ''', (requirements, datetime.now().isoformat()))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error saving job requirements: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_job_requirements(self):
        """Get current job requirements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT requirements FROM job_requirements ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            
            if row:
                return row['requirements']
            return ""
            
        except Exception as e:
            print(f"Error getting job requirements: {e}")
            return ""
        finally:
            conn.close()

    def save_interview_session(self, session_data):
        """Save interview session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO interview_sessions (
                    candidate_id, interview_date, interviewer, notes, rating, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_data['candidate_id'],
                session_data['interview_date'],
                session_data['interviewer'],
                session_data['notes'],
                session_data['rating'],
                session_data['status']
            ))
            
            session_id = cursor.lastrowid
            conn.commit()
            return session_id
            
        except Exception as e:
            print(f"Error saving interview session: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def get_interview_sessions(self, candidate_id=None):
        """Get interview sessions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if candidate_id:
                cursor.execute('''
                    SELECT * FROM interview_sessions 
                    WHERE candidate_id = ? 
                    ORDER BY interview_date DESC
                ''', (candidate_id,))
            else:
                cursor.execute('''
                    SELECT * FROM interview_sessions 
                    ORDER BY interview_date DESC
                ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error getting interview sessions: {e}")
            return []
        finally:
            conn.close()

    def get_statistics(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total candidates
            cursor.execute('SELECT COUNT(*) as total FROM candidates')
            total_candidates = cursor.fetchone()['total']
            
            # High match candidates (>= 0.7)
            cursor.execute('SELECT COUNT(*) as high FROM candidates WHERE match_score >= 0.7')
            high_match = cursor.fetchone()['high']
            
            # Medium match candidates (0.4-0.7)
            cursor.execute('SELECT COUNT(*) as medium FROM candidates WHERE match_score >= 0.4 AND match_score < 0.7')
            medium_match = cursor.fetchone()['medium']
            
            # Low match candidates (< 0.4)
            cursor.execute('SELECT COUNT(*) as low FROM candidates WHERE match_score < 0.4')
            low_match = cursor.fetchone()['low']
            
            # Average match score
            cursor.execute('SELECT AVG(match_score) as avg_score FROM candidates')
            avg_score = cursor.fetchone()['avg_score'] or 0
            
            # Recent uploads (last 7 days)
            cursor.execute('''
                SELECT COUNT(*) as recent FROM candidates 
                WHERE created_at >= datetime('now', '-7 days')
            ''')
            recent_uploads = cursor.fetchone()['recent']
            
            return {
                'total_candidates': total_candidates,
                'high_match_candidates': high_match,
                'medium_match_candidates': medium_match,
                'low_match_candidates': low_match,
                'average_match_score': round(avg_score, 2),
                'recent_uploads': recent_uploads
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
        finally:
            conn.close()

    def _row_to_dict(self, row):
        """Convert database row to dictionary"""
        data = dict(row)
        
        # Parse JSON fields
        for field in ['skills', 'experience', 'education', 'matched_skills', 'missing_skills', 'interview_recommendations']:
            if data.get(field):
                try:
                    data[field] = json.loads(data[field])
                except:
                    data[field] = []
            else:
                data[field] = []
        
        return data

    def search_candidates(self, query):
        """Search candidates by name, email, or skills"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            search_term = f"%{query}%"
            cursor.execute('''
                SELECT * FROM candidates 
                WHERE name LIKE ? OR email LIKE ? OR skills LIKE ?
                ORDER BY match_score DESC
            ''', (search_term, search_term, search_term))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error searching candidates: {e}")
            return []
        finally:
            conn.close()

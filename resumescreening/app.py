from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
from resume_parser import ResumeParser
from skill_matcher import SkillMatcher
from interview_recommender import InterviewRecommender
from database import Database

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'doc'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
db = Database()
resume_parser = ResumeParser()
skill_matcher = SkillMatcher()
interview_recommender = InterviewRecommender()

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('frontend/build', 'index.html')

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse resume
            resume_data = resume_parser.parse_resume(filepath)
            
            # Get job requirements from request
            job_requirements = request.form.get('job_requirements', '')
            
            # Match skills
            match_score, matched_skills, missing_skills = skill_matcher.match_skills(
                resume_data['skills'], job_requirements
            )
            
            # Generate interview recommendations
            interview_recommendations = interview_recommender.generate_recommendations(
                resume_data, match_score, matched_skills, missing_skills
            )
            
            # Save to database
            candidate_id = db.save_candidate({
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
                'resume_file': filename,
                'upload_date': datetime.now().isoformat()
            })
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'candidate_id': candidate_id,
                'resume_data': resume_data,
                'match_score': match_score,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'interview_recommendations': interview_recommendations
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = db.get_all_candidates()
        return jsonify({'candidates': candidates})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = db.get_candidate(candidate_id)
        if candidate:
            return jsonify({'candidate': candidate})
        return jsonify({'error': 'Candidate not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-job-requirements', methods=['POST'])
def update_job_requirements():
    try:
        data = request.get_json()
        requirements = data.get('requirements', '')
        
        # Update skill matcher with new requirements
        skill_matcher.update_requirements(requirements)
        
        # Recalculate scores for all candidates
        candidates = db.get_all_candidates()
        for candidate in candidates:
            match_score, matched_skills, missing_skills = skill_matcher.match_skills(
                candidate['skills'], requirements
            )
            db.update_candidate_score(candidate['id'], match_score, matched_skills, missing_skills)
        
        return jsonify({'success': True, 'message': 'Job requirements updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-candidate/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    try:
        success = db.delete_candidate(candidate_id)
        if success:
            return jsonify({'success': True, 'message': 'Candidate deleted'})
        return jsonify({'error': 'Candidate not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database
    db.init_database()
    print("Starting AI Resume Screening Server...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

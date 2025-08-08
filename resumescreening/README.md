# AI Resume Screening & Interview Suggestion System

A comprehensive AI-powered resume screening and interview recommendation platform that helps recruiters efficiently evaluate candidates and suggest optimal interview processes.

## Features

- **AI Resume Parsing**: Automatically extract skills, experience, and qualifications from resumes
- **Smart Skill Matching**: Match candidate skills against job requirements
- **Interview Recommendations**: AI-powered suggestions for interview questions and processes
- **Candidate Scoring**: Automated scoring system based on multiple criteria
- **Modern Web Interface**: Beautiful, responsive UI built with React
- **Real-time Processing**: Fast and efficient resume analysis

## Tech Stack

### Backend
- **Python Flask**: RESTful API server
- **SpaCy**: Natural language processing for resume parsing
- **Scikit-learn**: Machine learning for skill matching
- **Transformers**: Advanced text analysis
- **SQLite**: Lightweight database for candidate data

### Frontend
- **React**: Modern UI framework
- **Tailwind CSS**: Styling and responsive design
- **Axios**: HTTP client for API communication

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download SpaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Open the web application in your browser
2. Upload candidate resumes (PDF, DOCX, or TXT format)
3. View AI-generated analysis including:
   - Extracted skills and experience
   - Match score against job requirements
   - Interview recommendations
   - Candidate ranking

## API Endpoints

- `POST /api/upload-resume`: Upload and analyze resume
- `GET /api/candidates`: Get all candidates
- `GET /api/candidate/<id>`: Get specific candidate details
- `POST /api/update-job-requirements`: Update job requirements for matching

## Project Structure

```
resumescreening/
├── app.py                 # Main Flask application
├── resume_parser.py       # AI resume parsing logic
├── skill_matcher.py       # Skill matching algorithms
├── interview_recommender.py # Interview suggestion system
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── frontend/            # React frontend application
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

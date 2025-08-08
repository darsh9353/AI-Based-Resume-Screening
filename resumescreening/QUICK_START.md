# Quick Start Guide

## Prerequisites

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Node.js 16+** - Download from [nodejs.org](https://nodejs.org)
- **Git** - For cloning the repository

## Installation

### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd resumescreening
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

The setup script will automatically:
- Create a Python virtual environment
- Install all Python dependencies
- Download the SpaCy language model
- Install frontend dependencies
- Create sample data

### Option 2: Manual Setup

#### Backend Setup
1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download SpaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

#### Frontend Setup
1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

### 1. Start the Backend Server
```bash
# Activate virtual environment (if not already activated)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

python app.py
```

The backend will start on `http://localhost:5000`

### 2. Start the Frontend Development Server
```bash
# In a new terminal window
cd frontend
npm start
```

The frontend will start on `http://localhost:3000`

## First Steps

1. **Open your browser** and go to `http://localhost:3000`

2. **Configure job requirements:**
   - Go to Settings page
   - Enter your job requirements
   - Save the requirements

3. **Upload a resume:**
   - Go to Upload Resume page
   - Drag and drop a resume file (PDF, DOCX, DOC, TXT)
   - Enter job requirements if not already set
   - Click "Analyze Resume"

4. **View results:**
   - See the AI-generated analysis
   - Check match score and skills
   - Review interview recommendations

## Sample Data

The setup creates a sample job requirements file (`sample_requirements.txt`) that you can use as a starting point.

## Troubleshooting

### Common Issues

1. **"Module not found" errors:**
   - Make sure you're in the virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **SpaCy model not found:**
   - Run: `python -m spacy download en_core_web_sm`

3. **Frontend won't start:**
   - Make sure Node.js is installed
   - Delete `node_modules` and run `npm install` again

4. **Backend connection errors:**
   - Check if the backend is running on port 5000
   - Ensure no firewall is blocking the connection

### Getting Help

- Check the console for error messages
- Verify all prerequisites are installed
- Ensure ports 3000 and 5000 are available

## Features Overview

- **AI Resume Parsing:** Extracts skills, experience, and contact info
- **Smart Matching:** Compares candidate skills against job requirements
- **Interview Recommendations:** Suggests questions and interview format
- **Candidate Management:** View and manage all candidates
- **Dashboard Analytics:** See statistics and trends

## Next Steps

- Customize job requirements for your specific needs
- Upload multiple resumes to build your candidate database
- Use the interview recommendations to conduct better interviews
- Explore the dashboard for insights and analytics

Happy screening! 🎯

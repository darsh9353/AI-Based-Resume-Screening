#!/usr/bin/env python3
"""
Setup script for AI Resume Screening System
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_backend():
    """Setup the Python backend"""
    print("\n=== Setting up Backend ===")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Download SpaCy model
    if not run_command(f"{pip_cmd} install spacy", "Installing SpaCy"):
        return False
    
    if not run_command(f"{pip_cmd} -m spacy download en_core_web_sm", "Downloading SpaCy model"):
        return False
    
    return True

def setup_frontend():
    """Setup the React frontend"""
    print("\n=== Setting up Frontend ===")
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✓ Node.js found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is required but not found. Please install Node.js first.")
        return False
    
    # Install frontend dependencies
    os.chdir("frontend")
    if not run_command("npm install", "Installing frontend dependencies"):
        return False
    
    os.chdir("..")
    return True

def create_sample_data():
    """Create sample job requirements"""
    print("\n=== Creating Sample Data ===")
    
    sample_requirements = """
Senior Software Engineer Requirements:

Technical Skills:
- Python (3+ years experience)
- JavaScript/TypeScript
- React or Angular
- Node.js
- SQL databases (PostgreSQL, MySQL)
- AWS or Azure cloud platforms
- Docker and Kubernetes
- Git and CI/CD pipelines

Soft Skills:
- Strong communication skills
- Team collaboration
- Problem-solving abilities
- Leadership experience
- Agile methodology experience

Education:
- Bachelor's degree in Computer Science or related field
- Master's degree preferred

Experience:
- 5+ years of software development experience
- Experience with microservices architecture
- Experience with RESTful APIs
- Experience with testing frameworks (Jest, PyTest)
"""
    
    try:
        with open("sample_requirements.txt", "w") as f:
            f.write(sample_requirements.strip())
        print("✓ Sample job requirements created (sample_requirements.txt)")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 AI Resume Screening System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("1. Backend: python app.py")
    print("2. Frontend: cd frontend && npm start")
    print("\nThe application will be available at:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:5000")
    print("\nHappy screening! 🎯")

if __name__ == "__main__":
    main()

# SMARTCAREER AI - Resume Intelligence Platform

**An Intelligent Resume Analysis & Career Recommendation System**

Developed by **Sagar Singh**

## Overview

SMARTCAREER AI is a Python-based resume analysis application designed to help candidates understand their resumes, identify skill gaps, and explore suitable career opportunities.

The platform analyzes uploaded PDF resumes and generates useful insights through an interactive dashboard.

## Key Features

- PDF Resume Upload
- Candidate Name, Email and Phone Extraction
- Technical Skills Detection and Categorization
- Estimated ATS Resume Scoring
- Resume Score Breakdown
- Missing Skills Identification
- Job Role Recommendations
- Personalized Learning Roadmap
- PDF and TXT Report Generation
- Interactive Streamlit Dashboard

## Technology Stack

- Python
- Streamlit
- Pandas
- NLP-based Text Processing
- PyPDF
- ReportLab

## Project Structure

```text
AI_Resume_Analyzer/
â”‚
â”œâ”€â”€ app.py
â”œâ”€â”€ resume_upload_app.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ run_app.bat
â”‚
â”œâ”€â”€ data/
â”‚
â””â”€â”€ src/
    â”œâ”€â”€ __init__.py
    â”œâ”€â”€ pdf_reader.py
    â”œâ”€â”€ resume_parser.py
    â”œâ”€â”€ resume_scorer.py
    â”œâ”€â”€ skill_extractor.py
    â””â”€â”€ job_recommender.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd AI_Resume_Analyzer
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## How It Works

1. Upload a candidate's PDF resume.
2. Extract candidate information and resume text.
3. Detect technical skills.
4. Calculate an estimated ATS score.
5. Identify missing skills for selected job roles.
6. Generate job recommendations.
7. Explore the learning roadmap.
8. Download the analysis report in PDF or TXT format.

## Important Notes

- ATS scores are project-based estimates, not official employer ATS scores.
- Job recommendations are based on predefined skill databases and matching logic.
- This project does not currently fetch live job vacancies.
- Analysis accuracy may vary depending on PDF formatting and content.
- Uploaded resumes may contain personal information. Handle them responsibly.

## Developer

**Sagar Singh**

Independent AI/ML Portfolio Project

**Technologies:** Python | Streamlit | NLP | Data Analysis

---

**SMARTCAREER AI - Analyze Your Resume. Discover Your Career Direction.**


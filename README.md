# SkillSynth — ATS Resume Analyzer & Career Copilot

SkillSynth is a student-focused web application that compares a resume PDF with a target job description and turns the comparison into practical career guidance.

## Problem

Students and freshers often do not know whether their resume is aligned with a particular job description or which skills they should strengthen before applying.

## Solution

SkillSynth extracts readable text from a resume PDF, identifies technical skills required by the target job, compares those skills with the resume, and presents an actionable analysis.

## Features

- Resume PDF upload and text extraction
- Job-description based skill detection
- ATS/job-match score
- Matched skills
- Missing skills
- Smart resume feedback
- Skill-gap learning roadmap
- Readiness priority: Low / Medium / High
- Resume improvement suggestions
- Responsive student/fresher-friendly interface

## Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- Flask
- Flask-CORS
- pypdf

## How It Works

1. Upload a text-based PDF resume.
2. Paste the target job description.
3. SkillSynth extracts readable resume text.
4. It detects supported technical skills in the job description.
5. It compares those requirements against the resume.
6. It calculates the current skill-alignment score.
7. It displays matched skills, missing skills and an actionable learning roadmap.

## Important Scope Note

The current version uses a transparent rule-based skill matching engine. The score should therefore be understood as a **skill-alignment indicator**, not a guarantee of how a particular company's ATS will score a resume.

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
skillsynth-ats-resume-analyzer/
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Future Scope

- Semantic skill matching using an embedding/LLM layer
- Section-level resume quality analysis
- Role-specific interview preparation
- Personalized career recommendations

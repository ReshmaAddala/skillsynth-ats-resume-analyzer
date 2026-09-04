from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pypdf import PdfReader
import re

app = Flask(__name__)
CORS(app)

SKILLS = [
    "python", "java", "sql", "flask", "api", "html", "css",
    "javascript", "react", "git", "github", "docker", "aws",
    "machine learning", "data structures", "kotlin", "android",
    "c", "dbms", "linux", "oop"
]

ROADMAP = {
    "python": "Strengthen Python fundamentals, OOP, modules, file handling and problem solving.",
    "java": "Practice Java OOP, collections, exception handling and DSA.",
    "sql": "Learn SELECT, JOIN, GROUP BY, subqueries, indexes and database design.",
    "flask": "Build REST APIs with Flask, routing, request handling and JSON responses.",
    "api": "Learn REST, HTTP methods, JSON, authentication and API integration.",
    "html": "Improve semantic HTML, forms, accessibility and page structure.",
    "css": "Practice responsive design, Flexbox, Grid and modern UI techniques.",
    "javascript": "Strengthen JavaScript, DOM manipulation, asynchronous programming and APIs.",
    "react": "Learn components, props, state, hooks and API integration.",
    "git": "Practice branching, merging, pull requests and clean commit workflows.",
    "github": "Learn repositories, branches, pull requests, issues and collaboration.",
    "docker": "Learn images, containers, Dockerfiles and basic deployment.",
    "aws": "Learn EC2, S3, IAM and basic cloud deployment.",
    "machine learning": "Study preprocessing, supervised learning, model evaluation and common algorithms.",
    "data structures": "Practice arrays, strings, linked lists, stacks, queues, trees and graphs.",
    "kotlin": "Practice Kotlin syntax, OOP, collections and Android development patterns.",
    "android": "Build Android apps with activities, layouts, navigation and data handling.",
    "c": "Strengthen C fundamentals, pointers, arrays, functions and memory concepts.",
    "dbms": "Review relational databases, normalization, transactions and SQL.",
    "linux": "Practice Linux commands, permissions, processes and basic shell usage.",
    "oop": "Review encapsulation, inheritance, polymorphism and abstraction."
}

def contains_skill(text, skill):
    # Match phrases/words without accidental substring matches.
    if " " in skill:
        return skill in text
    return re.search(r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])", text) is not None

def analyze_text(resume_text, job_desc):
    resume_lower = resume_text.lower()
    jd_lower = job_desc.lower()

    required_skills = [skill for skill in SKILLS if contains_skill(jd_lower, skill)]
    matched_skills = [skill for skill in required_skills if contains_skill(resume_lower, skill)]
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]

    match_percentage = round(len(matched_skills) / len(required_skills) * 100) if required_skills else 0

    # Transparent MVP score: current score is skill alignment.
    ats_score = match_percentage

    if match_percentage >= 80:
        priority = "Low"
        priority_message = "Strong alignment. Focus on polishing projects, measurable achievements and interview preparation."
        feedback_title = "Excellent match"
    elif match_percentage >= 60:
        priority = "Medium"
        priority_message = "Good foundation. Strengthen the missing skills and show evidence of them through projects or coursework."
        feedback_title = "Good match"
    elif match_percentage >= 40:
        priority = "High"
        priority_message = "Several job requirements are missing. Tailor the resume and build small projects around the highest-priority gaps."
        feedback_title = "Needs improvement"
    else:
        priority = "High"
        priority_message = "The resume currently has limited overlap with this role. Focus on the core missing skills before applying."
        feedback_title = "Low match"

    roadmap = [
        {"skill": skill, "recommendation": ROADMAP.get(skill, f"Build practical experience with {skill}.")}
        for skill in missing_skills
    ]

    return {
        "ats_score": ats_score,
        "match_percentage": match_percentage,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_keywords": missing_skills,
        "skill_gap_count": len(missing_skills),
        "roadmap": roadmap,
        "priority": priority,
        "priority_message": priority_message,
        "feedback_title": feedback_title
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    job_desc = request.form.get("job_desc", "")

    if not resume_file:
        return jsonify({"error": "Please upload a resume PDF."}), 400

    if not resume_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Please upload a PDF resume."}), 400

    if not job_desc.strip():
        return jsonify({"error": "Please enter a job description."}), 400

    try:
        reader = PdfReader(resume_file)
        resume_text = "\n".join(
            (page.extract_text() or "") for page in reader.pages
        )
    except Exception:
        return jsonify({"error": "Could not read the uploaded PDF."}), 400

    if not resume_text.strip():
        return jsonify({
            "error": "No readable text was found in this PDF. Please upload a text-based resume PDF."
        }), 400

    return jsonify(analyze_text(resume_text, job_desc))

if __name__ == "__main__":
    app.run(debug=True)

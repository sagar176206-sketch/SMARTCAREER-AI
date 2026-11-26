
# ==========================================================
# SMARTCAREER AI
# ADVANCED RESUME SCORING SYSTEM
# ==========================================================

def calculate_resume_score(resume_data):

    breakdown = {}

    full_text = str(
        resume_data.get("full_text", "")
    ).strip()

    lower_text = full_text.lower()

    # --------------------------------------------------
    # 1. SKILL PROCESSING
    # --------------------------------------------------

    skills = resume_data.get("skills", [])

    if isinstance(skills, str):
        skills = skills.split(",")

    if isinstance(skills, dict):
        skills = [
            skill
            for values in skills.values()
            for skill in (
                values if isinstance(values, (list, tuple, set))
                else [values]
            )
        ]

    if not isinstance(skills, (list, tuple, set)):
        skills = [skills]

    skills = {
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    }

    # --------------------------------------------------
    # 2. TECHNICAL SKILLS - 30 MARKS
    # --------------------------------------------------

    skill_count = len(skills)

    skill_score = min(
        30,
        skill_count * 3
    )

    breakdown["Technical Skills"] = skill_score

    # --------------------------------------------------
    # 3. EDUCATION - 20 MARKS
    # --------------------------------------------------

    education = str(
        resume_data.get("education", "")
    ).strip()

    education_keywords = [
        "bachelor", "master", "degree",
        "b.a", "b.sc", "b.com", "b.tech",
        "m.tech", "m.sc", "m.com",
        "diploma", "graduation", "university",
        "college", "school", "phd"
    ]

    if education:
        education_score = 20

    elif any(word in lower_text for word in education_keywords):
        education_score = 20

    else:
        education_score = 0

    breakdown["Education"] = education_score

    # --------------------------------------------------
    # 4. PROJECTS - 20 MARKS
    # --------------------------------------------------

    project_text = str(
        resume_data.get("projects", "")
    ).strip()

    project_source = (
        project_text if project_text
        else full_text
    )

    project_keywords = [
        "project",
        "developed",
        "created",
        "built",
        "implemented",
        "designed",
        "application",
        "dashboard",
        "system",
        "model",
        "prediction",
        "analysis"
    ]

    project_count = sum(
        1
        for keyword in project_keywords
        if keyword in project_source.lower()
    )

    project_score = min(
        20,
        project_count * 3
    )

    breakdown["Projects"] = project_score

    # --------------------------------------------------
    # 5. EXPERIENCE - 15 MARKS
    # --------------------------------------------------

    experience = str(
        resume_data.get("experience", "")
    ).strip()

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "worked",
        "employment",
        "company",
        "professional"
    ]

    experience_source = (
        experience if experience
        else lower_text
    )

    has_experience = any(
        keyword in experience_source.lower()
        for keyword in experience_keywords
    )

    if experience:
        experience_score = 15

    elif has_experience:
        experience_score = 15

    else:
        # Fresher-friendly baseline
        experience_score = 10

    breakdown["Experience"] = experience_score

    # --------------------------------------------------
    # 6. CONTACT INFORMATION - 10 MARKS
    # --------------------------------------------------

    contact_score = 0

    if resume_data.get("name"):
        contact_score += 3

    if resume_data.get("email"):
        contact_score += 4

    if resume_data.get("phone"):
        contact_score += 3

    breakdown["Contact Information"] = contact_score

    # --------------------------------------------------
    # 7. RESUME CONTENT - 5 MARKS
    # --------------------------------------------------

    word_count = len(full_text.split())

    if word_count >= 300:
        content_score = 5

    elif word_count >= 150:
        content_score = 4

    elif word_count >= 75:
        content_score = 3

    elif word_count >= 30:
        content_score = 2

    else:
        content_score = 0

    breakdown["Resume Content"] = content_score

    # --------------------------------------------------
    # 8. FINAL SCORE
    # --------------------------------------------------

    score = sum(breakdown.values())

    score = max(0, min(100, score))

    # --------------------------------------------------
    # 9. RESUME RATING
    # --------------------------------------------------

    if score >= 85:
        rating = "Excellent"

    elif score >= 70:
        rating = "Strong"

    elif score >= 55:
        rating = "Good"

    elif score >= 40:
        rating = "Needs Improvement"

    else:
        rating = "Weak"

    # --------------------------------------------------
    # 10. STRENGTHS ANALYSIS
    # --------------------------------------------------

    strengths = []

    if skill_score >= 18:
        strengths.append(
            "Good technical skill coverage"
        )

    if education_score >= 15:
        strengths.append(
            "Education information is available"
        )

    if project_score >= 12:
        strengths.append(
            "Projects and practical work are mentioned"
        )

    if contact_score == 10:
        strengths.append(
            "Complete contact information"
        )

    if content_score >= 4:
        strengths.append(
            "Resume contains sufficient information"
        )

    # --------------------------------------------------
    # 11. WEAK AREAS
    # --------------------------------------------------

    weak_areas = []

    for category, marks in breakdown.items():

        maximum_marks = {
            "Technical Skills": 30,
            "Education": 20,
            "Projects": 20,
            "Experience": 15,
            "Contact Information": 10,
            "Resume Content": 5
        }

        if marks < maximum_marks[category] * 0.6:
            weak_areas.append(category)

    # --------------------------------------------------
    # 12. IMPROVEMENT SUGGESTIONS
    # --------------------------------------------------

    suggestions = []

    if skill_score < 18:
        suggestions.append(
            "Add relevant technical skills according to your target job."
        )

    if education_score == 0:
        suggestions.append(
            "Include your degree, college and education details."
        )

    if project_score < 12:
        suggestions.append(
            "Add practical projects with technologies and outcomes."
        )

    if experience_score < 15:
        suggestions.append(
            "As a fresher, highlight academic projects, internships and practical work."
        )

    if contact_score < 10:
        suggestions.append(
            "Add complete and correct contact information."
        )

    if content_score < 4:
        suggestions.append(
            "Improve resume content with relevant descriptions and achievements."
        )

    if not suggestions:
        suggestions.append(
            "Keep your resume updated with relevant skills and projects."
        )

    # --------------------------------------------------
    # 13. FINAL RESULT
    # --------------------------------------------------

    return {

        "score": score,

        "rating": rating,

        "breakdown": breakdown,

        "strengths": strengths,

        "weak_areas": weak_areas,

        "suggestions": suggestions,

        "skill_count": skill_count,

        "word_count": word_count

    }


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    sample_resume = {

        "name": "Test Candidate",

        "email": "test@example.com",

        "phone": "9876543210",

        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Pandas",
            "NumPy"
        ],

        "education": "Bachelor Degree",

        "experience": "",

        "projects": "Developed a Python project",

        "full_text": (
            "Bachelor Degree in Computer Science. "
            "Developed a Python project using "
            "Machine Learning and SQL. "
        ) * 15

    }

    result = calculate_resume_score(
        sample_resume
    )

    print("\nSMARTCAREER AI RESUME REPORT")

    print("\nOverall Score:", result["score"])

    print("Rating:", result["rating"])

    print("\nScore Breakdown:")

    for category, marks in result["breakdown"].items():
        print(category, ":", marks)

    print("\nStrengths:")
    for item in result["strengths"]:
        print("-", item)

    print("\nWeak Areas:")
    for item in result["weak_areas"]:
        print("-", item)

    print("\nSuggestions:")
    for item in result["suggestions"]:
        print("-", item)

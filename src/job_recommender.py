
# ==========================================================
# SMARTCAREER AI
# INTELLIGENT JOB RECOMMENDATION SYSTEM
# ==========================================================

JOB_DATABASE = {

    "Python Developer": [
        "Python", "SQL", "OOP", "DSA", "Git", "API"
    ],

    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Pandas", "NumPy", "Statistics"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NumPy", "Pandas", "Scikit-learn", "PyTorch"
    ],

    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning",
        "Deep Learning", "Pandas", "NumPy"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "Python", "API", "Git"
    ],

    "Data Engineer": [
        "Python", "SQL", "ETL", "Data Engineering",
        "Pandas", "Database", "Apache Spark"
    ],

    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NLP", "PyTorch", "TensorFlow", "API"
    ],

    "Business Analyst": [
        "Excel", "SQL", "Power BI",
        "Statistics", "Communication"
    ]
}


# ----------------------------------------------------------
# SKILL NORMALIZATION
# ----------------------------------------------------------

SKILL_ALIASES = {

    "ml": "machine learning",
    "machinelearning": "machine learning",

    "dl": "deep learning",
    "deeplearning": "deep learning",

    "js": "javascript",

    "powerbi": "power bi",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    "np": "numpy",
    "pd": "pandas",

    "postgres": "postgresql",

    "py torch": "pytorch",

    "tf": "tensorflow",

    "natural language processing": "nlp"
}


def normalize_skill(skill):

    skill = str(skill).strip().lower()

    skill = " ".join(skill.split())

    compact = skill.replace(" ", "")

    if compact in SKILL_ALIASES:
        return SKILL_ALIASES[compact]

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    return skill


# ----------------------------------------------------------
# CANDIDATE SKILL PROCESSING
# ----------------------------------------------------------

def process_candidate_skills(candidate_skills):

    if candidate_skills is None:
        return set()

    if isinstance(candidate_skills, str):
        candidate_skills = candidate_skills.split(",")

    elif isinstance(candidate_skills, dict):
        candidate_skills = [
            skill
            for skills in candidate_skills.values()
            for skill in (
                skills if isinstance(skills, (list, tuple, set))
                else [skills]
            )
        ]

    elif not isinstance(candidate_skills, (list, tuple, set)):
        candidate_skills = [candidate_skills]

    processed = set()

    for skill in candidate_skills:

        normalized = normalize_skill(skill)

        if normalized:
            processed.add(normalized)

    return processed


# ----------------------------------------------------------
# JOB RECOMMENDATION ENGINE
# ----------------------------------------------------------

def recommend_jobs(candidate_skills):

    candidate_skills = process_candidate_skills(
        candidate_skills
    )

    recommendations = []

    # No skills found
    if not candidate_skills:
        return recommendations

    for job, required_skills in JOB_DATABASE.items():

        matched = []
        missing = []

        for skill in required_skills:

            normalized = normalize_skill(skill)

            if normalized in candidate_skills:
                matched.append(skill)

            else:
                missing.append(skill)

        total_skills = len(required_skills)

        if total_skills == 0:
            continue

        percentage = (
            len(matched) / total_skills
        ) * 100

        recommendations.append({

            "job": job,

            "match_percentage": round(
                percentage, 2
            ),

            "matched_skills": matched,

            "missing_skills": missing

        })

    # Highest matching jobs first
    recommendations.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return recommendations


# ----------------------------------------------------------
# GET REQUIREMENTS FOR A PARTICULAR JOB
# ----------------------------------------------------------

def get_job_requirements(job_name):

    for job, skills in JOB_DATABASE.items():

        if job.lower() == str(job_name).strip().lower():
            return skills.copy()

    return []


# ----------------------------------------------------------
# SKILL GAP ANALYSIS
# ----------------------------------------------------------

def analyze_skill_gap(candidate_skills, job_name):

    candidate_skills = process_candidate_skills(
        candidate_skills
    )

    required_skills = get_job_requirements(job_name)

    if not required_skills:
        return {
            "job": job_name,
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0
        }

    matched = [
        skill for skill in required_skills
        if normalize_skill(skill) in candidate_skills
    ]

    missing = [
        skill for skill in required_skills
        if normalize_skill(skill) not in candidate_skills
    ]

    percentage = (
        len(matched) / len(required_skills)
    ) * 100

    return {

        "job": job_name,

        "matched_skills": matched,

        "missing_skills": missing,

        "match_percentage": round(
            percentage, 2
        )

    }


import re


# ==================================================
# SMARTCAREER AI - ADVANCED SKILL DATABASE
# ==================================================

SKILL_DATABASE = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript",
        "TypeScript", "R", "PHP", "Ruby", "Go", "Rust",
        "Kotlin", "Swift", "Dart", "Scala", "Perl"
    ],

    "Data Science & Analytics": [
        "Machine Learning", "Deep Learning", "Data Science",
        "Data Analysis", "Data Analytics", "Statistics",
        "Pandas", "NumPy", "SciPy", "Matplotlib",
        "Seaborn", "Plotly", "Exploratory Data Analysis",
        "Feature Engineering", "Time Series Analysis"
    ],

    "AI & ML Frameworks": [
        "PyTorch", "TensorFlow", "Scikit-learn", "Keras",
        "OpenCV", "XGBoost", "LightGBM", "CatBoost",
        "Hugging Face", "Transformers", "NLTK", "spaCy"
    ],

    "Generative AI & NLP": [
        "Natural Language Processing", "NLP",
        "Generative AI", "Large Language Models", "LLM",
        "Retrieval Augmented Generation", "RAG",
        "Prompt Engineering", "LangChain", "LlamaIndex",
        "Computer Vision", "Neural Networks",
        "Reinforcement Learning"
    ],

    "Database & Big Data": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "SQLite", "Oracle", "Redis", "Microsoft SQL Server",
        "Apache Spark", "Hadoop", "Apache Kafka",
        "Data Warehousing", "ETL"
    ],

    "Web Development": [
        "HTML", "CSS", "JavaScript", "TypeScript",
        "React", "Angular", "Vue.js", "Node.js",
        "Express.js", "Django", "Flask", "FastAPI",
        "Bootstrap", "Tailwind CSS", "REST API",
        "GraphQL"
    ],

    "Cloud & DevOps": [
        "AWS", "Microsoft Azure", "Google Cloud",
        "Docker", "Kubernetes", "Jenkins",
        "GitHub Actions", "CI/CD", "Linux",
        "Shell Scripting", "Terraform"
    ],

    "Tools & Platforms": [
        "Git", "GitHub", "GitLab", "Jupyter Notebook",
        "Google Colab", "VS Code", "Visual Studio",
        "PyCharm", "Streamlit", "Power BI",
        "Tableau", "Microsoft Excel", "Excel",
        "Apache Airflow", "Postman"
    ],

    "Computer Science": [
        "DSA", "Data Structures", "Algorithms",
        "Object Oriented Programming", "OOP",
        "Operating Systems", "Computer Networks",
        "Database Management Systems", "DBMS",
        "Software Engineering", "Problem Solving"
    ],

    "Other Technical Skills": [
        "API Development", "Software Testing",
        "Unit Testing", "Automation Testing",
        "Agile", "Scrum", "Cybersecurity",
        "Data Visualization", "Model Deployment",
        "MLOps", "Version Control"
    ]
}


# ==================================================
# SKILL ALIASES
# ==================================================

SKILL_ALIASES = {
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "tf": "TensorFlow",
    "pytorch": "PyTorch",
    "np": "NumPy",
    "pd": "Pandas",
    "js": "JavaScript",
    "ts": "TypeScript",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "llms": "Large Language Models",
    "llm": "LLM",
    "rag": "RAG",
    "eda": "Exploratory Data Analysis",
    "oop": "OOP",
    "dsa": "DSA",
    "dbms": "DBMS",
    "ms excel": "Microsoft Excel",
    "powerbi": "Power BI",
    "nodejs": "Node.js"
}


# ==================================================
# TEXT PREPARATION
# ==================================================

def prepare_text(text):
    """Convert input into searchable lowercase text."""

    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text.lower()).strip()


# ==================================================
# SKILL MATCHING
# ==================================================

def skill_exists(text, skill):
    """Check whether a skill exists as a separate term."""

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(skill.lower())
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, text, re.IGNORECASE) is not None


# ==================================================
# EXTRACT SKILLS BY CATEGORY
# ==================================================

def extract_skills_by_category(text):

    text_lower = prepare_text(text)

    result = {}

    for category, skills in SKILL_DATABASE.items():

        matched = []

        for skill in skills:

            if skill_exists(text_lower, skill):
                matched.append(skill)

        # Check common aliases
        for alias, canonical_skill in SKILL_ALIASES.items():

            if (
                canonical_skill in skills
                and skill_exists(text_lower, alias)
                and canonical_skill not in matched
            ):
                matched.append(canonical_skill)

        result[category] = sorted(set(matched))

    return result


# ==================================================
# EXTRACT ALL SKILLS
# ==================================================

def extract_skills(text):

    categorized = extract_skills_by_category(text)

    detected_skills = []

    for skills in categorized.values():
        detected_skills.extend(skills)

    return sorted(set(detected_skills))


# ==================================================
# SKILL SUMMARY
# ==================================================

def get_skill_summary(text):

    categorized = extract_skills_by_category(text)

    total_skills = sum(
        len(skills)
        for skills in categorized.values()
    )

    categories_with_skills = {
        category: skills
        for category, skills in categorized.items()
        if skills
    }

    return {
        "total_skills": total_skills,
        "categories": categorized,
        "categories_found": len(categories_with_skills),
        "detected_categories": categories_with_skills
    }


# ==================================================
# GET AVAILABLE SKILL DATABASE
# ==================================================

def get_all_skills():

    return {
        category: skills.copy()
        for category, skills in SKILL_DATABASE.items()
    }


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample_text = """
    I know Python, SQL, Machine Learning,
    Deep Learning, PyTorch, NumPy and Pandas.

    I have worked with Git, Streamlit, Scikit-learn,
    TensorFlow, Power BI, Django and Docker.
    """

    print("=" * 50)
    print("SMARTCAREER AI - SKILL EXTRACTION REPORT")
    print("=" * 50)

    print("\nDETECTED SKILLS:")
    print(extract_skills(sample_text))

    print("\nSKILLS BY CATEGORY:")

    for category, skills in extract_skills_by_category(
        sample_text
    ).items():

        if skills:
            print(f"\n{category}: {', '.join(skills)}")

    print("\nSKILL SUMMARY:")
    print(get_skill_summary(sample_text))

    print("\nTOTAL SKILLS IN DATABASE:")

    total_database_skills = sum(
        len(skills)
        for skills in SKILL_DATABASE.values()
    )

    print(total_database_skills)

    print("\nSKILL EXTRACTION TEST COMPLETED")

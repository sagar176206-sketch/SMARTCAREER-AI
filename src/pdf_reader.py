
import re
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


# ==================================================
# SKILL DATABASE
# ==================================================

SKILL_TERMS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "Power BI",
    "Excel",
    "Statistics",
    "DSA",
    "Data Structures",
    "Algorithms",
    "OOP",
    "Git",
    "GitHub",
    "Flask",
    "Django",
    "Streamlit",
    "React",
    "Node.js",
    "API",
    "MySQL",
    "MongoDB",
    "PostgreSQL",
    "R",
    "Tableau",
    "NLP",
    "Computer Vision",
    "CNN",
    "RNN"
]


# ==================================================
# PDF TEXT EXTRACTION
# ==================================================

def extract_resume_pdf_text(source):

    try:

        if isinstance(source, (str, Path)):

            reader = PdfReader(str(source))

        else:

            if hasattr(source, "seek"):
                source.seek(0)

            reader = PdfReader(source)

        if reader.is_encrypted:

            try:
                reader.decrypt("")
            except Exception:
                raise ValueError(
                    "Password-protected PDF is not supported."
                )

        pages_text = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages_text.append(text)

        full_text = "\n".join(pages_text)

        if not full_text.strip():

            raise ValueError(
                "No readable text found. "
                "This may be a scanned PDF."
            )

        return full_text

    except Exception as error:

        raise ValueError(
            f"PDF reading failed: {error}"
        )


# ==================================================
# EMAIL EXTRACTION
# ==================================================

def extract_email(text):

    pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    match = re.search(pattern, text)

    return match.group(0) if match else None


# ==================================================
# PHONE EXTRACTION
# ==================================================

def extract_phone(text):

    pattern = (
        r"(?<!\w)(?:\+91[\s-]?)?"
        r"[6-9]\d{9}(?!\w)"
    )

    match = re.search(pattern, text)

    return match.group(0) if match else None


# ==================================================
# NAME EXTRACTION
# ==================================================

def extract_candidate_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = [
        "resume",
        "curriculum vitae",
        "email",
        "phone",
        "mobile",
        "address",
        "career objective",
        "professional summary"
    ]

    for line in lines[:10]:

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line
        ).strip()

        if not cleaned:
            continue

        if any(
            word in cleaned.lower()
            for word in ignored_words
        ):
            continue

        if len(cleaned.split()) > 4:
            continue

        if len(cleaned) < 3:
            continue

        return cleaned

    return None


# ==================================================
# SECTION EXTRACTION
# ==================================================

def extract_section(text, headings):

    lines = text.splitlines()

    capture = False

    collected = []

    heading_pattern = re.compile(
        r"^(education|academic qualifications?|"
        r"experience|work experience|employment history|"
        r"projects?|technical skills|skills|"
        r"certifications?|achievements?)\s*[:\-]?$",
        re.IGNORECASE
    )

    target_headings = [
        heading.lower() for heading in headings
    ]

    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        if clean.lower().rstrip(":") in target_headings:

            capture = True
            continue

        if capture and heading_pattern.match(clean):

            if clean.lower().rstrip(":") not in target_headings:
                break

        if capture:
            collected.append(clean)

    return "\n".join(collected).strip()


# ==================================================
# SKILL EXTRACTION
# ==================================================

def extract_skills_from_text(text):

    text_lower = text.lower()

    detected = []

    for skill in SKILL_TERMS:

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text_lower):

            detected.append(skill)

    return sorted(set(detected))


# ==================================================
# COMPLETE RESUME ANALYSIS
# ==================================================

def analyze_resume_pdf(source):

    full_text = extract_resume_pdf_text(source)

    name = extract_candidate_name(full_text)

    email = extract_email(full_text)

    phone = extract_phone(full_text)

    skills = extract_skills_from_text(full_text)

    education = extract_section(
        full_text,
        [
            "education",
            "academic qualifications",
            "educational qualifications"
        ]
    )

    experience = extract_section(
        full_text,
        [
            "experience",
            "work experience",
            "employment history"
        ]
    )

    projects = extract_section(
        full_text,
        [
            "projects",
            "academic projects",
            "personal projects"
        ]
    )

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "full_text": full_text
    }


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    print("PDF READER MODULE")
    print("Module loaded successfully.")


import re


# ==========================================
# NAME EXTRACTION
# ==========================================

def extract_name(text):

    if not isinstance(text, str) or not text.strip():
        return None

    ignored_headings = {
        "website profile", "profile", "resume", "cv",
        "contact", "portfolio", "linkedin", "github",
        "objective", "summary", "professional summary",
        "profile summary", "career summary", "career objective",
        "education", "experience", "work experience",
        "skills", "projects", "certifications",
        "achievements", "personal details"
    }

    def valid_name(candidate):
        candidate = candidate.strip().strip(": ")

        if candidate.lower() in ignored_headings:
            return False

        if any(char in candidate for char in "@:/\\"):
            return False

        words = candidate.split()

        if not 2 <= len(words) <= 4:
            return False

        return bool(re.fullmatch(
            r"[A-Za-z][A-Za-z.'-]*(?:\s+[A-Za-z][A-Za-z.'-]*){1,3}",
            candidate
        ))

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Explicitly labelled candidate name
    for line in lines[:30]:
        match = re.match(
            r"^(?:candidate\s+)?name\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match and valid_name(match.group(1)):
            return match.group(1).strip()

    # Name immediately before summary
    summary_headings = {
        "summary", "professional summary",
        "profile summary", "career summary"
    }

    for index, line in enumerate(lines):
        if line.lower().strip(": ") in summary_headings:
            for previous in range(index - 1, max(-1, index - 4), -1):
                if valid_name(lines[previous]):
                    return lines[previous]

    # First likely candidate name
    for line in lines[:15]:
        if valid_name(line):
            return line

    return None


# ==========================================
# EMAIL EXTRACTION
# ==========================================

def extract_email(text):

    if not isinstance(text, str):
        return None

    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    return match.group(0) if match else None


# ==========================================
# PHONE EXTRACTION
# ==========================================

def extract_phone(text):

    if not isinstance(text, str):
        return None

    matches = re.findall(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,18}\d)(?!\w)",
        text
    )

    for phone in matches:
        digits = re.sub(r"\D", "", phone)

        if 10 <= len(digits) <= 13:
            return phone.strip()

    return None


# ==========================================
# COMPLETE RESUME PARSER
# ==========================================

def parse_resume(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }


import streamlit as st
import pandas as pd
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from src.pdf_reader import extract_resume_pdf_text
from src.skill_extractor import extract_skills
from src.resume_parser import (
    extract_name,
    extract_email,
    extract_phone
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SMARTCAREER AI | Resume Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# JOB DATABASE
# ==========================================

JOB_SKILLS = {
    "Python Developer": [
        "Python", "SQL", "Git", "OOP", "Django"
    ],
    "Data Analyst": [
        "Python", "SQL", "Pandas", "NumPy",
        "Excel", "Statistics"
    ],
    "Machine Learning Engineer": [
        "Python", "SQL", "Machine Learning",
        "Deep Learning", "PyTorch", "NumPy"
    ],
    "Data Scientist": [
        "Python", "SQL", "Machine Learning",
        "Statistics", "Pandas", "Deep Learning"
    ],
    "AI Engineer": [
        "Python", "Machine Learning",
        "Deep Learning", "PyTorch", "NLP"
    ]
}


LEARNING_RESOURCES = {
    "Python": "Learn Python basics, functions, OOP and build practical projects.",
    "SQL": "Learn SELECT, JOIN, GROUP BY, subqueries and database design.",
    "Git": "Learn Git commands, branches and GitHub version control.",
    "OOP": "Study classes, objects, inheritance and polymorphism.",
    "Django": "Learn Django models, views, APIs and web applications.",
    "Pandas": "Learn DataFrames, data cleaning and data analysis.",
    "NumPy": "Learn arrays, indexing and numerical operations.",
    "Excel": "Learn formulas, charts, pivot tables and data analysis.",
    "Statistics": "Study probability, mean, variance and standard deviation.",
    "Machine Learning": "Study regression, classification and model evaluation.",
    "Deep Learning": "Study neural networks, CNN and RNN fundamentals.",
    "PyTorch": "Learn tensors, neural networks and model training.",
    "NLP": "Study text processing and natural language processing."
}


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg, #080D1A 0%, #101A30 55%, #111827 100%
    );
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background: #0B1220;
    border-right: 1px solid #25334D;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

.hero {
    background: linear-gradient(
        115deg, #172554, #312E81, #164E63
    );
    border: 1px solid #475569;
    border-radius: 22px;
    padding: 32px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
}

.hero p {
    color: #DCEAFE;
    font-size: 15px;
}

.metric-card {
    background: linear-gradient(145deg, #17243B, #111C30);
    border: 1px solid #334765;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    margin-bottom: 12px;
}

.metric-title {
    color: #94A3B8;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #F8FAFC;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-sub {
    color: #38BDF8;
    font-size: 12px;
    margin-top: 5px;
}

.section-card {
    background: #111D31;
    border: 1px solid #2D405E;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 18px;
}

.skill-card {
    background: #17243B;
    border: 1px solid #334765;
    border-radius: 12px;
    padding: 13px;
    margin-bottom: 9px;
}

.job-card {
    background: linear-gradient(120deg, #17243B, #172554);
    border: 1px solid #3B4D70;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 15px;
}

.tag {
    display: inline-block;
    background: #123B35;
    color: #6EE7B7;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px;
}

.missing-tag {
    display: inline-block;
    background: #47232B;
    color: #FDA4AF;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px;
}

.small-muted {
    color: #94A3B8;
    font-size: 13px;
}

div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: #17243B;
    border: 1px solid #334765;
    padding: 16px;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def metric_card(title, value, subtitle):
    title = escape(str(title))
    value = escape(str(value))
    subtitle = escape(str(subtitle))

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def analyze_skill_gap(detected_skills, required_skills):

    detected = {
        str(skill).lower().strip()
        for skill in detected_skills
    }

    available = []
    missing = []

    for skill in required_skills:
        if skill.lower().strip() in detected:
            available.append(skill)
        else:
            missing.append(skill)

    return available, missing


def calculate_ats_score(
    resume_text,
    email,
    phone,
    detected_skills
):

    score = 0

    if email:
        score += 10

    if phone:
        score += 10

    headings = [
        "education",
        "experience",
        "skills",
        "projects"
    ]

    text_lower = resume_text.lower()

    found = sum(
        1 for heading in headings
        if heading in text_lower
    )

    score += min(found * 5, 20)
    score += min(len(detected_skills) * 5, 40)

    word_count = len(resume_text.split())

    if word_count >= 100:
        score += 10

    if word_count >= 200:
        score += 10

    return min(score, 100)


def recommend_jobs(detected_skills):

    recommendations = []

    for role, required in JOB_SKILLS.items():

        available, missing = analyze_skill_gap(
            detected_skills,
            required
        )

        percentage = (
            len(available) / len(required) * 100
            if required else 0
        )

        recommendations.append({
            "role": role,
            "match": round(percentage, 1),
            "available": available,
            "missing": missing
        })

    return sorted(
        recommendations,
        key=lambda item: item["match"],
        reverse=True
    )


def generate_learning_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        task = LEARNING_RESOURCES.get(
            skill,
            f"Study {skill} fundamentals and build a practical project."
        )

        roadmap.append({
            "skill": skill,
            "task": task
        })

    return roadmap


def generate_pdf_report(report_text):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=24,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=15
    )

    elements = [
        Paragraph(
            "SMARTCAREER AI - Resume Intelligence Report",
            title_style
        )
    ]

    for line in report_text.split("\n"):

        safe_line = escape(line) if line.strip() else " "

        elements.append(
            Paragraph(safe_line, body_style)
        )

        elements.append(Spacer(1, 6))

    document.build(elements)

    buffer.seek(0)

    return buffer


def create_report(
    candidate_name,
    email,
    phone,
    ats_score,
    detected_skills,
    selected_role,
    available,
    missing,
    recommendations,
    roadmap
):

    lines = [
        "SMARTCAREER AI - RESUME ANALYSIS REPORT",
        "",
        f"Candidate: {candidate_name or 'Not Found'}",
        f"Email: {email or 'Not Found'}",
        f"Phone: {phone or 'Not Found'}",
        f"Estimated ATS Score: {ats_score}/100",
        "",
        "DETECTED SKILLS",
        ", ".join(detected_skills) or "None",
        "",
        f"TARGET ROLE: {selected_role}",
        "",
        "AVAILABLE SKILLS",
        ", ".join(available) or "None",
        "",
        "MISSING SKILLS",
        ", ".join(missing) or "None",
        "",
        "JOB RECOMMENDATIONS"
    ]

    for job in recommendations:
        lines.append(
            f"{job['role']}: {job['match']}% match"
        )

    lines.extend([
        "",
        "PERSONALIZED LEARNING ROADMAP"
    ])

    for item in roadmap:
        lines.append(
            f"{item['skill']}: {item['task']}"
        )

    lines.extend([
        "",
        "NOTE:",
        "ATS score is a project-based estimate.",
        "Job matches use a static skill database.",
        "This report is not an official employer ATS result."
    ])

    return "\n".join(lines)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🚀 SMARTCAREER AI")
    st.caption("RESUME INTELLIGENCE PLATFORM")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📄 Resume Analysis",
            "🎯 Skill Gap",
            "💼 Job Matches",
            "📚 Learning Roadmap",
            "📥 Reports"
        ]
    )

    st.divider()

    st.markdown("### ⚙️ Analysis Settings")

    selected_role = st.selectbox(
        "Target Job Role",
        list(JOB_SKILLS.keys())
    )

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
        help="Upload a text-based PDF resume."
    )

    st.divider()

    st.markdown("### PROJECT STATUS")

    st.markdown(
        '<span class="tag">ANALYSIS ENGINE READY</span>',
        unsafe_allow_html=True
    )

    st.caption("SMARTCAREER AI | Resume Analyzer v2.0")


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🚀 SMARTCAREER AI</h1>
    <p>Intelligent Resume Analysis & Career Recommendation System</p>
    <p>Analyze your resume. Discover skill gaps. Find your career direction.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# LANDING PAGE
# ==========================================

if uploaded_file is None:

    st.markdown("## Welcome to your Career Intelligence Dashboard")

    st.info(
        "Upload your resume PDF using the left sidebar "
        "to unlock your personalized analysis."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "RESUME ANALYSIS",
            "PDF",
            "Extract skills and candidate details"
        )

    with col2:
        metric_card(
            "JOB MATCHING",
            "5+",
            "Compare skills with career roles"
        )

    with col3:
        metric_card(
            "LEARNING ROADMAP",
            "PLAN",
            "Discover skills you need to learn"
        )

    st.markdown("## ✨ Platform Features")

    feature_cols = st.columns(2)

    features = [
        ("📊 ATS Score", "Estimate resume quality using project-based rules."),
        ("🧠 Skill Extraction", "Identify supported technical skills."),
        ("💼 Job Recommendations", "Compare skills with career roles."),
        ("🎯 Skill Gap Analysis", "See available and missing skills."),
        ("📚 Learning Roadmap", "Get learning suggestions for missing skills."),
        ("📥 PDF Reports", "Export your resume analysis.")
    ]

    for index, (title, description) in enumerate(features):

        with feature_cols[index % 2]:

            st.markdown(f"""
            <div class="section-card">
                <h3>{escape(title)}</h3>
                <p class="small-muted">{escape(description)}</p>
            </div>
            """, unsafe_allow_html=True)

    st.info(
        "Developer: Sagar Singh | Independent Portfolio Project"
    )

    st.stop()


# ==========================================
# RESUME PROCESSING
# ==========================================

try:

    with st.spinner("SMARTCAREER AI is analyzing your resume..."):

        uploaded_file.seek(0)

        resume_text = extract_resume_pdf_text(uploaded_file)

        if not resume_text or not resume_text.strip():
            st.error(
                "No readable text found. Please upload a text-based PDF."
            )
            st.stop()

        candidate_name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)

        detected_skills = extract_skills(resume_text)

        if detected_skills is None:
            detected_skills = []

        required_skills = JOB_SKILLS[selected_role]

        available, missing = analyze_skill_gap(
            detected_skills,
            required_skills
        )

        ats_score = calculate_ats_score(
            resume_text,
            email,
            phone,
            detected_skills
        )

        recommendations = recommend_jobs(detected_skills)

        roadmap = generate_learning_roadmap(missing)

        match_percentage = (
            len(available) / len(required_skills) * 100
            if required_skills else 0
        )

        report_text = create_report(
            candidate_name,
            email,
            phone,
            ats_score,
            detected_skills,
            selected_role,
            available,
            missing,
            recommendations,
            roadmap
        )

except Exception as error:

    st.error(f"Resume analysis failed: {error}")

    st.info(
        "Check the PDF file and the functions inside your src folder."
    )

    st.stop()


# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "🏠 Dashboard":

    st.markdown("## 📊 Executive Overview")

    st.markdown(
        f"Welcome, **{escape(str(candidate_name or 'Candidate'))}**. "
        "Here is your resume intelligence summary."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "ATS SCORE",
            f"{ats_score}/100",
            "Estimated score"
        )

    with c2:
        metric_card(
            "DETECTED SKILLS",
            len(detected_skills),
            "Skills identified"
        )

    with c3:
        metric_card(
            "SKILL MATCH",
            f"{match_percentage:.0f}%",
            selected_role
        )

    with c4:
        metric_card(
            "MISSING SKILLS",
            len(missing),
            "Skills to improve"
        )

    st.markdown("## 👤 Candidate Profile")

    a, b, c = st.columns(3)

    with a:
        st.markdown("**Candidate Name**")
        st.write(candidate_name or "Not Found")

    with b:
        st.markdown("**Email Address**")
        st.write(email or "Not Found")

    with c:
        st.markdown("**Phone Number**")
        st.write(phone or "Not Found")

    st.divider()

    st.markdown("## 📈 Resume Performance")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown("### ATS Score")
        st.progress(ats_score / 100)

        st.metric(
            "Estimated Score",
            f"{ats_score}%"
        )

        st.caption(
            "Heuristic estimate, not a real ATS vendor score."
        )

    with chart2:

        st.markdown("### Skill Distribution")

        chart_data = pd.DataFrame({
            "Category": ["Available", "Missing"],
            "Skills": [len(available), len(missing)]
        })

        st.bar_chart(
            chart_data,
            x="Category",
            y="Skills"
        )

    st.divider()

    st.markdown("## 🏆 Top Job Matches")

    for job in recommendations[:3]:

        st.markdown(f"""
        <div class="job-card">
            <h3>💼 {escape(job['role'])}</h3>
            <h2>{job['match']}% Match</h2>
            <p class="small-muted">
                {len(job['available'])} matching skills
                | {len(job['missing'])} missing skills
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "Job matches are based on the project's static skill database."
    )


# ==========================================
# RESUME ANALYSIS PAGE
# ==========================================

elif page == "📄 Resume Analysis":

    st.markdown("## 📄 Detailed Resume Analysis")

    st.markdown("### Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Candidate Name",
            value=candidate_name or "",
            disabled=True
        )

        st.text_input(
            "Email",
            value=email or "",
            disabled=True
        )

    with col2:

        st.text_input(
            "Phone",
            value=phone or "",
            disabled=True
        )

        st.text_input(
            "Selected Job Role",
            value=selected_role,
            disabled=True
        )

    st.divider()

    st.markdown("### 🧠 Detected Technical Skills")

    if detected_skills:

        for skill in detected_skills:

            st.markdown(
                f'<span class="tag">{escape(str(skill))}</span>',
                unsafe_allow_html=True
            )

    else:

        st.warning("No supported skills were detected.")

    st.divider()

    st.markdown("### 📃 Extracted Resume Text")

    with st.expander("View complete extracted text"):
        st.text(resume_text)


# ==========================================
# SKILL GAP PAGE
# ==========================================

elif page == "🎯 Skill Gap":

    st.markdown("## 🎯 Skill Gap Intelligence")

    st.write(f"Target role: **{selected_role}**")

    left, right = st.columns(2)

    with left:

        st.markdown("### ✅ Available Skills")

        if available:

            for skill in available:

                st.markdown(
                    f'<div class="skill-card">✅ {escape(skill)}</div>',
                    unsafe_allow_html=True
                )

        else:

            st.warning("No matching skills found.")

    with right:

        st.markdown("### ❌ Missing Skills")

        if missing:

            for skill in missing:

                st.markdown(
                    f'<div class="skill-card">📌 {escape(skill)}</div>',
                    unsafe_allow_html=True
                )

        else:

            st.success("All required skills detected!")

    st.divider()

    st.markdown("### Skill Match Percentage")

    st.progress(match_percentage / 100)

    st.metric(
        "Role Skill Match",
        f"{match_percentage:.1f}%"
    )

    st.caption(
        "Matching uses exact skill-name comparison, not semantic understanding."
    )


# ==========================================
# JOB MATCHES PAGE
# ==========================================

elif page == "💼 Job Matches":

    st.markdown("## 💼 Career Opportunities")

    st.write(
        "Compare your detected skills against the project's job-role database."
    )

    for index, job in enumerate(recommendations, start=1):

        st.markdown(f"""
        <div class="job-card">
            <p class="small-muted">JOB MATCH #{index}</p>
            <h2>{escape(job['role'])}</h2>
            <h1>{job['match']}%</h1>
            <p>Skill Compatibility</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(job["match"] / 100)

        st.write(
            "**Matching Skills:** "
            + (", ".join(job["available"]) or "None")
        )

        st.write(
            "**Missing Skills:** "
            + (", ".join(job["missing"]) or "None")
        )

        st.divider()


# ==========================================
# LEARNING ROADMAP PAGE
# ==========================================

elif page == "📚 Learning Roadmap":

    st.markdown("## 📚 Your Personalized Learning Roadmap")

    st.write(
        "Use this roadmap to plan your learning based on missing skills."
    )

    if roadmap:

        for index, item in enumerate(roadmap, start=1):

            st.markdown(f"""
            <div class="section-card">
                <p class="small-muted">LEARNING MODULE {index}</p>
                <h3>📘 {escape(item['skill'])}</h3>
                <p>{escape(item['task'])}</p>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.success(
            "No missing skills for this selected job role!"
        )

    st.info(
        "These are learning suggestions, not outputs from a trained AI model."
    )


# ==========================================
# REPORTS PAGE
# ==========================================

elif page == "📥 Reports":

    st.markdown("## 📥 Download Analysis Reports")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="section-card">
            <h3>📄 TXT Report</h3>
            <p class="small-muted">
                Download a text summary of your analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "⬇ Download TXT",
            data=report_text,
            file_name="smartcareer_resume_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.markdown("""
        <div class="section-card">
            <h3>📕 PDF Report</h3>
            <p class="small-muted">
                Download a formatted PDF report.
            </p>
        </div>
        """, unsafe_allow_html=True)

        pdf_buffer = generate_pdf_report(report_text)

        st.download_button(
            "⬇ Download PDF",
            data=pdf_buffer,
            file_name="smartcareer_resume_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.divider()

    st.markdown("### Report Preview")

    st.text(report_text)


# ==========================================
# FOOTER AND DEVELOPER PROFILE
# ==========================================

st.divider()

st.markdown("""
<div style="
    background:#14243b;
    padding:25px;
    border-radius:15px;
    text-align:center;
    border:1px solid #294361;
">
    <h2>SMARTCAREER AI</h2>
    <h3>Developed by Sagar Singh</h3>
    <p>Independent AI/ML Portfolio Project</p>
    <p>Python | Streamlit | NLP | Machine Learning</p>
    <p style="color:#94A3B8;">
        Resume Intelligence & Career Recommendation System
    </p>
</div>
""", unsafe_allow_html=True)

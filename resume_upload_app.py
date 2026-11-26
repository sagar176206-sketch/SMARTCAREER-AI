
import streamlit as st
import json
from datetime import datetime

from src.pdf_reader import analyze_resume_pdf
from src.resume_scorer import calculate_resume_score
from src.job_recommender import recommend_jobs
from src.skill_extractor import extract_skills


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "resume_result" not in st.session_state:
    st.session_state.resume_result = None

if "score_data" not in st.session_state:
    st.session_state.score_data = None


# -----------------------------------
# HEADER
# -----------------------------------

st.title("🎯 Career Intelligence Platform")

st.markdown(
    "### AI-Powered Resume Analysis & Job Matching"
)

st.caption(
    "Analyze resumes, identify skill gaps and explore career opportunities."
)

st.divider()


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("⚙️ Control Panel")

target_role = st.sidebar.selectbox(
    "Select Target Job Role",
    [
        "Python Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Data Scientist",
        "Web Developer"
    ]
)

st.sidebar.info(
    "Upload a PDF resume and compare it with a job description."
)


# -----------------------------------
# RESUME UPLOAD
# -----------------------------------

st.subheader("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("🚀 Analyze Resume", type="primary"):

        try:
            with st.spinner("Analyzing your resume..."):

                resume_data = analyze_resume_pdf(uploaded_file)

                score_data = calculate_resume_score(
                    resume_data
                )

                st.session_state.resume_result = resume_data
                st.session_state.score_data = score_data

            st.success("Resume analyzed successfully!")

        except Exception as e:
            st.error(f"Resume analysis failed: {e}")


# -----------------------------------
# MAIN DASHBOARD
# -----------------------------------

resume = st.session_state.resume_result
score_data = st.session_state.score_data

if resume is None:

    st.info(
        "Upload a PDF resume and click Analyze Resume to see your dashboard."
    )

    st.markdown("### What this platform can do")

    col1, col2, col3 = st.columns(3)

    col1.markdown("#### 📊 Resume Score")
    col1.write("Evaluate resume sections using a transparent rule-based score.")

    col2.markdown("#### 🎯 Job Matching")
    col2.write("Compare candidate skills with a company's job requirements.")

    col3.markdown("#### 📚 Skill Gap")
    col3.write("Identify missing skills and plan what to learn next.")

else:

    # -----------------------------------
    # CANDIDATE INFORMATION
    # -----------------------------------

    st.divider()
    st.header("📊 Candidate Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Resume Score",
        f"{score_data['score']}/100"
    )

    col2.metric(
        "Skills Detected",
        len(resume.get("skills", []))
    )

    col3.metric(
        "Target Role",
        target_role
    )

    st.markdown("### 👤 Candidate Information")

    info1, info2, info3 = st.columns(3)

    info1.write("**Name**")
    info1.write(resume.get("name") or "Not detected")

    info2.write("**Email**")
    info2.write(resume.get("email") or "Not detected")

    info3.write("**Phone**")
    info3.write(resume.get("phone") or "Not detected")

    # -----------------------------------
    # TABS
    # -----------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Resume Analysis",
        "🎯 Job Matcher",
        "🧠 Skill Gap",
        "🎤 Interview Prep",
        "📥 Reports"
    ])

    # -----------------------------------
    # TAB 1: RESUME ANALYSIS
    # -----------------------------------

    with tab1:

        st.subheader("Resume Score Analysis")

        st.metric(
            "Overall Resume Rating",
            score_data["rating"]
        )

        breakdown = score_data.get("breakdown", {})

        if breakdown:

            st.write("### Score Breakdown")

            st.bar_chart(breakdown)

            for category, points in breakdown.items():
                st.write(f"**{category}:** {points} points")

        st.write("### Technical Skills")

        skills = resume.get("skills", [])

        if skills:
            st.write(", ".join(skills))
        else:
            st.warning("No technical skills detected.")

        st.write("### Education")
        st.write(resume.get("education") or "Not detected")

        st.write("### Experience")
        st.write(resume.get("experience") or "Not detected")

        st.write("### Projects")
        st.write(resume.get("projects") or "Not detected")

    # -----------------------------------
    # TAB 2: JOB DESCRIPTION MATCHER
    # -----------------------------------

    with tab2:

        st.subheader("🎯 Job Description Matcher")

        st.write(
            "Paste a company's job description below."
        )

        job_description = st.text_area(
            "Company Job Description",
            height=180,
            placeholder=(
                "Example: We are looking for a Python Developer "
                "with Python, SQL, Django and Machine Learning skills."
            )
        )

        if st.button("Compare Resume With Job"):

            if not job_description.strip():

                st.warning("Please enter a job description.")

            else:

                required_skills = extract_skills(
                    job_description
                )

                candidate_skills = resume.get("skills", [])

                candidate_set = {
                    skill.lower() for skill in candidate_skills
                }

                required_set = {
                    skill.lower() for skill in required_skills
                }

                matched = sorted(
                    candidate_set.intersection(required_set)
                )

                missing = sorted(
                    required_set.difference(candidate_set)
                )

                if not required_set:

                    st.warning(
                        "No supported technical skills were detected in this job description."
                    )

                else:

                    match_percentage = round(
                        len(matched) / len(required_set) * 100,
                        2
                    )

                    st.session_state.job_match = {
                        "role": target_role,
                        "match_percentage": match_percentage,
                        "matched_skills": matched,
                        "missing_skills": missing,
                        "required_skills": required_skills
                    }

        if st.session_state.get("job_match"):

            result = st.session_state.job_match

            st.divider()

            st.metric(
                "Job Description Match",
                f"{result['match_percentage']}%"
            )

            st.progress(
                int(result["match_percentage"])
            )

            col1, col2 = st.columns(2)

            with col1:
                st.success("Matched Skills")

                if result["matched_skills"]:
                    for skill in result["matched_skills"]:
                        st.write("✅ " + skill)
                else:
                    st.write("No matching skills found.")

            with col2:
                st.error("Missing Skills")

                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.write("❌ " + skill)
                else:
                    st.write("No missing skills detected.")

            st.caption(
                "This percentage measures detected skill overlap only. "
                "It is not a hiring probability or official ATS score."
            )

    # -----------------------------------
    # TAB 3: SKILL GAP ANALYSIS
    # -----------------------------------

    with tab3:

        st.subheader("🧠 Career Skill Gap Analysis")

        candidate_skills = resume.get("skills", [])

        recommendations = recommend_jobs(
            candidate_skills
        )

        st.write("### Recommended Job Roles")

        if recommendations:

            for job in recommendations:

                with st.expander(
                    f"{job['job']} — {job['match_percentage']}% skill match"
                ):

                    st.write("**Matched Skills**")

                    st.write(
                        ", ".join(job["matched_skills"])
                        or "None"
                    )

                    st.write("**Skills to Learn**")

                    st.write(
                        ", ".join(job["missing_skills"])
                        or "No missing skills in this checklist"
                    )

        else:
            st.info("No job recommendations available.")

        st.divider()

        st.write("### Suggested Learning Actions")

        if candidate_skills:

            st.write(
                "1. Strengthen your existing technical skills."
            )

            st.write(
                "2. Build practical projects related to your target role."
            )

            st.write(
                "3. Practice SQL, Python and problem-solving questions."
            )

            st.write(
                "4. Add measurable project results to your resume."
            )

        else:

            st.warning(
                "Add technical skills to your resume to receive better suggestions."
            )

    # -----------------------------------
    # TAB 4: INTERVIEW PREPARATION
    # -----------------------------------

    with tab4:

        st.subheader("🎤 Interview Preparation")

        interview_questions = {

            "Python Developer": [
                "What is the difference between a list and tuple?",
                "Explain Python decorators.",
                "What is exception handling?",
                "Explain OOP concepts in Python.",
                "What is the difference between == and is?"
            ],

            "Data Analyst": [
                "What is the difference between SQL WHERE and HAVING?",
                "Explain GROUP BY.",
                "What is data cleaning?",
                "What is the difference between mean and median?",
                "What is a data visualization?"
            ],

            "Machine Learning Engineer": [
                "What is supervised learning?",
                "Explain overfitting and underfitting.",
                "What is feature scaling?",
                "What is the purpose of train-test split?",
                "Explain Random Forest."
            ],

            "Data Scientist": [
                "What is hypothesis testing?",
                "Explain linear regression.",
                "What is feature engineering?",
                "What is a confusion matrix?",
                "Explain precision and recall."
            ],

            "Web Developer": [
                "What is HTML?",
                "What is CSS Flexbox?",
                "Explain JavaScript functions.",
                "What is an API?",
                "What is HTTP?"
            ]
        }

        st.write(
            f"### Questions for {target_role}"
        )

        for index, question in enumerate(
            interview_questions[target_role],
            start=1
        ):

            st.write(f"**Q{index}. {question}**")

    # -----------------------------------
    # TAB 5: DOWNLOAD REPORT
    # -----------------------------------

    with tab5:

        st.subheader("📥 Download Career Report")

        report = {
            "generated_at": datetime.now().isoformat(),
            "candidate": {
                "name": resume.get("name"),
                "email": resume.get("email"),
                "phone": resume.get("phone")
            },
            "resume_score": score_data,
            "skills": resume.get("skills", []),
            "education": resume.get("education"),
            "experience": resume.get("experience"),
            "projects": resume.get("projects"),
            "job_recommendations": recommend_jobs(
                resume.get("skills", [])
            )
        }

        st.download_button(
            label="📄 Download JSON Career Report",
            data=json.dumps(
                report,
                indent=4,
                ensure_ascii=False
            ),
            file_name="career_analysis_report.json",
            mime="application/json"
        )

        text_report = f"""
CAREER INTELLIGENCE REPORT

Candidate: {resume.get('name') or 'Not detected'}
Email: {resume.get('email') or 'Not detected'}

RESUME SCORE:
{score_data['score']}/100

RATING:
{score_data['rating']}

TECHNICAL SKILLS:
{', '.join(resume.get('skills', []))}

EDUCATION:
{resume.get('education') or 'Not detected'}

EXPERIENCE:
{resume.get('experience') or 'Not detected'}

PROJECTS:
{resume.get('projects') or 'Not detected'}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

        st.download_button(
            label="📃 Download Text Report",
            data=text_report,
            file_name="career_analysis_report.txt",
            mime="text/plain"
        )

st.divider()

st.caption(
    "Career Intelligence Platform | Resume analysis is informational "
    "and does not guarantee job selection."
)

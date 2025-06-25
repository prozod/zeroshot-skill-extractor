import streamlit as st
from lib.config.model_config import ModelConfig
from script import ResumeSkillExtractor
import tempfile
import os
import json
import base64
import subprocess


from dotenv import load_dotenv
load_dotenv()


def load_local_scraped_jobs(json_path="scraped_jobs.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load job listings: {e}")
        return []


def display_jobs(jobs):
    if not jobs:
        st.warning("No jobs found.")
        return

    for job in jobs:
        col1, col2 = st.columns([1, 5])

        with col1:
            logo = job.get("company_img_link")
            if logo:
                st.image(logo, width=80)

        with col2:
            title = job.get("title", "Untitled")
            company = job.get("company", "Unknown Company")
            location = job.get("place", "N/A")
            url = job.get("link", "#")
            description = job.get("description", "")[:300] + "..."  # preview

            st.markdown(f"### [{title}]({url})")
            st.markdown(f"**Company:** {company}")
            st.markdown(f"**Location:** {location}")
            st.markdown(f"**Description:** {description}")
            st.markdown("---")


def run_script_and_get_results(pdf_path: str):
    try:
        subprocess.run(["python3", "src/script.py", pdf_path], check=True)

        jobs = []
        resume_data = {}

        if os.path.exists("linkedin_jobs.json"):
            jobs = load_local_scraped_jobs("linkedin_jobs.json")
        else:
            st.warning("LinkedIn jobs file not found.")

        if os.path.exists("resume_analysis_zsl_results.json"):
            with open("resume_analysis_zsl_results.json", "r", encoding="utf-8") as f:
                resume_data = json.load(f)
        else:
            st.warning("Resume analysis result file not found.")

        return jobs, resume_data

    except subprocess.CalledProcessError as e:
        st.error(f"Error running script.py: {e}")
        return [], {}


@st.cache_resource
def load_extractor():
    config = ModelConfig.get_accurate_config()
    return ResumeSkillExtractor(config=config)


extractor = load_extractor()

st.title("CV Skill Extractor")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_pdf_path = tmp_file.name

    # PDF preview
    with open(temp_pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'''
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="700px"
            style="border: none;"
            type="application/pdf">
        </iframe>
        '''
    st.sidebar.markdown("### Uploaded resume (preview)")
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

    st.info("Running full pipeline...")

    job_data, resume_data = run_script_and_get_results(temp_pdf_path)

    # display results
    if resume_data:
        st.subheader("Predicted role: ")
        predicted_role = resume_data.get(
            "predicted_role", {}).get("predicted_role")
        confidence = resume_data.get(
            "predicted_role", {}).get("confidence", 0.0)
        st.write(f"**{predicted_role}** (confidence: {confidence:.2f})")

        st.subheader("Skills found:")
        for skill_info in resume_data.get("skills", {}).get("detailed_skills", []):
            skill = skill_info.get("skill", "UNKNOWN")
            conf = skill_info.get("confidence", 0.0)
            method = skill_info.get("method", "N/A")
            matches = skill_info.get("matches", 0)
            st.markdown(
                f"- **{skill}** (confidence: {conf:.2f}, method: {method}, matches: {matches})")

        st.subheader("Extraction stats")
        stats = resume_data.get("skills", {}).get("extraction_stats", {})
        st.write({
            "Total skills found": stats.get("total_found", 0),
            "Zero-shot matched": stats.get("zsl_count", 0),
            "Rule-based detected": stats.get("rule_based_count", 0),
        })

    st.subheader("Matching jobs based off of predicted role: ")
    display_jobs(job_data)

import streamlit as st
from lib.config.model_config import ModelConfig
from script import ResumeSkillExtractor
import tempfile
import os
import base64
import requests


from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("RAPIDAPI_KEY")


def query_jobs_by_role(title="backend engineer", limit=10, offset=0):
    url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"

    querystring = {
        "limit": str(limit),
        "offset": str(offset),
        "title_filter": title
    }

    headers = {
        "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("Status Code:", response.status_code)
    print("Raw Text:", response.text)

    try:
        return response.json()
    except Exception as e:
        print("JSON Decode Error:", e)
        return None


def display_jobs(jobs):
    if not jobs:
        st.warning("No jobs found.")
        return

    for job in jobs:
        col1, col2 = st.columns([1, 5])

        with col1:
            logo = job.get("organization_logo")
            if logo:
                st.image(logo, width=80)

        locations = job.get("locations_derived")
        with col2:
            title = job.get("title", "Untitled")
            company = job.get("organization", "Unknown Company")
            if isinstance(locations, list):
                location = ", ".join(locations)
            else:
                location = "N/A"
            url = job.get("url", "#")
            recruiter = job.get("recruiter_name")

            st.markdown(f"### [{title}]({url})")
            st.markdown(f"**Company:** {company}")
            if recruiter:
                st.markdown(f"**Recruiter:** {recruiter}")
            if location:
                st.markdown(f"📍 {location}")
            st.markdown("---")


# Initialize model and extractor once


@st.cache_resource
def load_extractor():
    config = ModelConfig.get_accurate_config()
    return ResumeSkillExtractor(config=config)


extractor = load_extractor()

st.title("CV Skill Extractor")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_pdf_path = tmp_file.name

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

    st.info("Processing your resume...")

    # Process resume
    results = extractor.process_resume(temp_pdf_path)

    # Clean up temporary file
    os.remove(temp_pdf_path)

    st.subheader("Predicted role")
    st.write(f"**{results['predicted_role']['predicted_role']}**")
    st.caption(f"Confidence: {results['predicted_role']['confidence']:.2f}")

    st.subheader("Extracted skills")
    for skill_info in results["skills"]["detailed_skills"]:
        st.markdown(
            f"- **{skill_info['skill']}** (confidence: {skill_info.get('confidence', 0):.2f}, method: {
                skill_info.get('method')}, matches: {skill_info.get('matches', 0)})"
        )

    st.subheader("Extraction statistics")
    stats = results["skills"]["extraction_stats"]
    st.write({
        "Total skills found": stats["total_found"],
        "Zero-shot matched": stats["zsl_count"],
        "Rule-based detected": stats["rule_based_count"],
    })

    # st.subheader("Experience info")
    # for exp in results["experience"]:
    #     st.write(f"{exp['context']} (Years: {exp['years']})")

    role = results['predicted_role']['predicted_role']

    st.subheader(f"Jobs matching: {role}")
    job_data = query_jobs_by_role(role)

    if isinstance(job_data, list):
        display_jobs(job_data)
    else:
        st.error("Unexpected API format.")

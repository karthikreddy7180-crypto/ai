
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Cover Letter Generator",
    page_icon="✉️",
    layout="centered"
)

# Custom design
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
.main-title {
    text-align: center;
    color: #17365d;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}
.stButton button {
    background-color: #17365d;
    color: white;
    border-radius: 8px;
    width: 100%;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# Application heading
st.markdown(
    '<div class="main-title">AI Cover Letter Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create professional job application letters using AI</div>',
    unsafe_allow_html=True
)

st.divider()

# Input form
st.subheader("Personal Information")

name = st.text_input("Full Name")
degree = st.text_input("Degree / Qualification")
skills = st.text_area("Technical Skills")
experience = st.text_area("Projects / Internship Experience")

st.subheader("Job Information")

company = st.text_input("Company Name")
role = st.text_input("Job Role")

job_description = st.text_area(
    "Job Description",
    height=150
)

# Generate button
if st.button("Generate Cover Letter"):

    if not API_KEY:
        st.error("API key not found. Please check your .env file.")

    elif not all([
        name, degree, skills, company,
        role, job_description
    ]):
        st.warning("Please fill in all required fields.")

    else:
        try:
            with st.spinner("Gemini AI is writing your cover letter..."):

                client = genai.Client(api_key=API_KEY)

                prompt = f"""
                Act as a professional career advisor.

                Write a personalized professional cover letter
                in less than 300 words.

                Applicant Name: {name}
                Degree: {degree}
                Skills: {skills}
                Projects and Internship: {experience}

                Company: {company}
                Job Role: {role}
                Job Description: {job_description}

                Instructions:
                1. Use professional language.
                2. Connect the applicant's skills to the job.
                3. Highlight relevant projects and experience.
                4. Do not invent qualifications or experience.
                5. Use a proper cover letter format.
                6. Keep it under 300 words.
                7. Do not add unsupported claims.
                """

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                cover_letter = response.text

                if not cover_letter:
                    st.error("AI did not return text. Please try again.")
                else:
                    st.session_state["cover_letter"] = cover_letter

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Display generated result
if "cover_letter" in st.session_state:

    st.divider()
    st.subheader("Your Generated Cover Letter")

    st.text_area(
        "AI Generated Result",
        value=st.session_state["cover_letter"],
        height=350
    )

    st.download_button(
        label="Download Cover Letter",
        data=st.session_state["cover_letter"],
        file_name="My_Cover_Letter.txt",
        mime="text/plain"
    )

st.divider()

st.caption("Powered by Google Gemini AI | Student AI Project")

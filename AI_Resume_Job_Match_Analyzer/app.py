import streamlit as st

from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, calculate_match
from ai_feedback import generate_ai_feedback


st.set_page_config(
    page_title="AI Resume Match Analyzer",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Resume–Job Match Analyzer")

st.write(
    """
    Upload your resume and paste a job description to understand
    how your current skills align with the opportunity.
    """
)

st.info(
    "The match score represents detected technical-skill overlap. "
    "It is not an employer hiring score."
)


# -----------------------------
# INPUT SECTION
# -----------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description",
        height=300,
        placeholder="Paste the complete job description here..."
    )


# -----------------------------
# ANALYSIS
# -----------------------------

if st.button(
    "Analyze Match",
    type="primary",
    use_container_width=True
):

    if uploaded_resume is None:

        st.warning("Please upload a resume.")

    elif not job_description.strip():

        st.warning("Please paste a job description.")

    else:

        try:

            with st.spinner("Analyzing resume..."):

                # STEP 1
                # Extract text from resume

                resume_text = extract_text_from_pdf(
                    uploaded_resume
                )


                if not resume_text:

                    st.error(
                        "No readable text was found in the PDF."
                    )

                    st.stop()


                # STEP 2
                # Detect technical skills

                resume_skills = extract_skills(
                    resume_text
                )

                job_skills = extract_skills(
                    job_description
                )


                # STEP 3
                # Calculate deterministic match

                (
                    match_percentage,
                    matched_skills,
                    missing_skills

                ) = calculate_match(
                    resume_skills,
                    job_skills
                )


                # -----------------------------
                # RESULTS
                # -----------------------------

                st.divider()

                st.header("Analysis Results")


                # MATCH SCORE

                st.metric(
                    "Technical Skill Match",
                    f"{match_percentage}%"
                )

                st.progress(
                    match_percentage / 100
                )


                # SKILLS

                result_col1, result_col2 = st.columns(2)


                with result_col1:

                    st.subheader("✅ Matched Skills")

                    if matched_skills:

                        for skill in matched_skills:

                            st.write(
                                f"✓ {skill.title()}"
                            )

                    else:

                        st.write(
                            "No matching skills detected."
                        )


                with result_col2:

                    st.subheader("🎯 Missing Skills")

                    if missing_skills:

                        for skill in missing_skills:

                            st.write(
                                f"• {skill.title()}"
                            )

                    else:

                        st.write(
                            "No missing skills detected from our skill list."
                        )


                # -----------------------------
                # AI FEEDBACK
                # -----------------------------

                st.divider()

                st.header("🧠 AI Career Feedback")


                with st.spinner(
                    "Generating personalized recommendations..."
                ):

                    feedback = generate_ai_feedback(
                        resume_text,
                        job_description,
                        match_percentage,
                        matched_skills,
                        missing_skills
                    )


                st.markdown(feedback)


                # DEBUG / LEARNING SECTION

                with st.expander(
                    "🔍 See what the system detected"
                ):

                    st.write(
                        "**Resume Skills:**",
                        resume_skills
                    )

                    st.write(
                        "**Job Description Skills:**",
                        job_skills
                    )


        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Built with Python + Streamlit + Gemini | "
    "Educational project"
)
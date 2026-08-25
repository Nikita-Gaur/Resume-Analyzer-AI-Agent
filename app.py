import os
import re
import json
import tempfile
import streamlit as st
from pypdf import PdfReader

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

st.set_page_config(page_title="Resume Analyzer AI Agent", page_icon="🤖", layout="wide")

st.title("🤖 Resume Analyzer AI Agent")
st.caption("Upload a resume and job description to analyze skills, gaps and job-match score.")

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def basic_keyword_analysis(resume, jd):
    common = {
        "python","sql","pandas","numpy","scikit-learn","tensorflow","pytorch",
        "machine learning","deep learning","nlp","computer vision","aws","azure",
        "docker","git","github","streamlit","fastapi","langchain","llm"
    }
    r = resume.lower()
    j = jd.lower()
    jd_skills = [s for s in common if s in j]
    matched = [s for s in jd_skills if s in r]
    missing = [s for s in jd_skills if s not in r]
    score = round(len(matched) / len(jd_skills) * 100) if jd_skills else 0
    return matched, missing, score

def ai_analysis(resume, jd):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    client = OpenAI(api_key=api_key)
    prompt = f"""
You are a Resume Analyzer AI Agent.
Analyze the resume against the job description.
Return ONLY valid JSON with keys:
match_score (number 0-100), matched_skills (array), missing_skills (array),
strengths (array), gaps (array), recommendations (array).

RESUME:
{resume[:12000]}

JOB DESCRIPTION:
{jd[:10000]}
"""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = response.choices[0].message.content.strip()
    text = re.sub(r"^```json\s*|\s*```$", "", text)
    return json.loads(text)

resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
jd = st.text_area("Paste Job Description", height=220, placeholder="Paste the complete job description here...")

if st.button("Analyze Resume", type="primary"):
    if not resume_file or not jd.strip():
        st.warning("Please upload a resume PDF and paste the job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_pdf_text(resume_file)
            result = ai_analysis(resume_text, jd) or None

            if result is None:
                matched, missing, score = basic_keyword_analysis(resume_text, jd)
                result = {
                    "match_score": score,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "strengths": ["Resume text was successfully extracted.", "Several job-related skills were identified."],
                    "gaps": missing,
                    "recommendations": [
                        "Add missing technical skills when you genuinely have them.",
                        "Quantify project impact using numbers.",
                        "Tailor project and experience bullets to the job description."
                    ]
                }

        score = int(result.get("match_score", 0))
        st.subheader("📊 Job Match Score")
        st.progress(max(0, min(score, 100)) / 100)
        st.metric("Match Score", f"{score}%")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("✅ Matched Skills")
            for x in result.get("matched_skills", []):
                st.write(f"• {x}")
        with c2:
            st.subheader("❌ Missing Skills")
            for x in result.get("missing_skills", []):
                st.write(f"• {x}")

        st.subheader("💪 Strengths")
        for x in result.get("strengths", []):
            st.write(f"• {x}")

        st.subheader("⚠️ Skill Gaps")
        for x in result.get("gaps", []):
            st.write(f"• {x}")

        st.subheader("🚀 Recommendations")
        for x in result.get("recommendations", []):
            st.write(f"• {x}")

        with st.expander("View extracted resume text"):
            st.text(resume_text[:15000])

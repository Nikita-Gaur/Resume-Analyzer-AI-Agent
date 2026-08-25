# Resume Analyzer AI Agent

An AI-powered resume analysis project that compares a resume with a job description.

## Features
- Upload Resume PDF
- Extract resume text
- Analyze required and matched skills
- Identify missing skills / skill gaps
- Generate Job Match Score
- Provide resume improvement recommendations
- Optional LLM analysis using OpenAI API
- Works in fallback keyword-analysis mode without an API key

## Tech Stack
Python, Streamlit, PyPDF, OpenAI API, NLP/LLM concepts

## Run in VS Code

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Optional: create `.env` manually or set the environment variable:
```text
OPENAI_API_KEY=your_api_key_here
```

Run:
```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Interview Explanation

"I built a Resume Analyzer AI Agent that extracts text from a PDF resume and compares it with a job description. It identifies matched skills, missing skills and skill gaps, calculates a job-match score, and provides recommendations. I used Python and Streamlit for the application, PyPDF for PDF extraction, and an LLM for semantic analysis. I also added a keyword-based fallback so the application can still demonstrate the core workflow without an API key."

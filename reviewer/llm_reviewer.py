# llm_reviewer.py
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

REVIEW_PROMPT = """You are a senior software engineer reviewing a pull request.

File: {filename}

Static analysis findings:
{static_findings}

Code diff:
{diff_chunk}

Review this change for:
1. Bugs or logical errors introduced
2. Security issues (e.g., injection, hardcoded secrets, unsafe deserialization)
3. Code quality / readability issues NOT already caught by static analysis
4. Whether the change matches good practice for this language

Respond in this exact format:
SEVERITY: <low/medium/high/none>
COMMENT: <your review comment, max 3 sentences. If no issues, say "No issues found.">
"""

def review_chunk(filename, diff_chunk, static_findings):
    prompt = REVIEW_PROMPT.format(
        filename=filename,
        static_findings=static_findings or "None",
        diff_chunk=diff_chunk
    )
    response = model.generate_content(prompt)
    return parse_review_response(response.text)

def parse_review_response(text):
    severity = "none"
    comment = text
    for line in text.splitlines():
        if line.startswith("SEVERITY:"):
            severity = line.replace("SEVERITY:", "").strip().lower()
        if line.startswith("COMMENT:"):
            comment = line.replace("COMMENT:", "").strip()
    return {"severity": severity, "comment": comment}
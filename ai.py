from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's career goal.

User goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills for this goal.
- Remove irrelevant tools and skills.
- Identify genuine skill gaps.
- Generate a roadmap only for missing skills.
- Make the analysis different depending on the user's goal.
- Give practical interview questions.
- Return ONLY valid JSON.

JSON format:
{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

Resume:
{resume_text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        content = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        return json.loads(content)

    except Exception as e:

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }
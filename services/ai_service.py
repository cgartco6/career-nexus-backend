import os
from openai import OpenAI

class AIService:
    def __init__(self):
        # Initialized with enterprise configurations
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key-for-compilation"))

    def rewrite_cv_ats_compliant(self, raw_cv_text: str, target_industry: str) -> str:
        """Injects explicit action verbs, industry-specific taxonomy, and clean parsable structuring."""
        prompt = f"""
        You are an expert executive CV editor specialized in global Applicant Tracking Systems (ATS) layout rules.
        Rewrite the following user CV text. Ensure you:
        1. Eliminate non-standard bullet characters.
        2. Infuse core algorithmic keyphrases tied closely to the industry: '{target_industry}'.
        3. Use the STAR methodology (Situation, Task, Action, Result) for professional records.
        4. Output everything cleanly inside structured Markdown layout. Avoid arbitrary tables or sidebars.
        
        Raw CV Payload:
        {raw_cv_text}
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content

    def generate_cover_letter(self, rewritten_cv: str, job_description: str) -> str:
        """Generates tailored cover letters aligning specific career highlights to company needs."""
        prompt = f"""
        Generate a highly professional, striking, and targeted Cover Letter based on the CV and Target Job Description.
        Maintain an assertive, value-driven tone. Do not use generic boilerplate placeholders.

        CV Data:
        {rewritten_cv}

        Target Job Specification:
        {job_description}
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content

    def run_ai_tutor_session(self, cv_context: str, user_response: str, stage: str) -> dict:
        """Simulates interactive technical/behavioral screening, scoring and guiding inputs live."""
        prompt = f"""
        You are a tough executive coach preparing a high-ticket candidate. 
        Current Stage: {stage}
        Candidate Profile Background: {cv_context}
        Candidate Answer: {user_response}

        Analyze the answer. Provide:
        1. Critiques of weaknesses (gaps in logic, lack of business metrics).
        2. A polished, ideal way to answer the question.
        3. The next logical, challenging interview question.
        
        Format output as explicit JSON with keys: 'critique', 'better_alternative', 'next_question'.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return response.choices[0].message.content

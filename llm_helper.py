import google.generativeai as genai
import os

# Why Option A over Option B: Option A gives immediate actionable value
# to developers by explaining failures in plain English with suggested fixes,
# reducing debugging time on every test failure.

def explain_failure(test_name, error_message, context=""):
    prompt = "You are a QA engineer assistant. A test has failed.\n\n"
    prompt += "Test Name: " + test_name + "\n\n"
    prompt += "Error Message:\n" + error_message + "\n\n"
    prompt += "Context:\n" + (context if context else "None") + "\n\n"
    prompt += "Respond in this exact format:\n"
    prompt += "WHAT BROKE: ...\n"
    prompt += "ROOT CAUSE: ...\n"
    prompt += "SUGGESTED FIX: ...\n"

    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "LLM ERROR: " + str(e)

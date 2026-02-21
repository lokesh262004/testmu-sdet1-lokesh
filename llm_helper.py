import anthropic
import os


def explain_failure(test_name, error_message, context=""):

    prompt = "You are a QA engineer assistant. A test has failed.\n\n"
    prompt += "Test Name: " + test_name + "\n\n"
    prompt += "Error Message:\n" + error_message + "\n\n"
    prompt += "Context:\n" + context + "\n\n"
    prompt += "Please explain in this format:\n"
    prompt += "WHAT BROKE: ...\n"
    prompt += "ROOT CAUSE: ...\n"
    prompt += "SUGGESTED FIX: ...\n"

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    except anthropic.AuthenticationError:
        return "LLM ERROR: Invalid API key."
    except anthropic.RateLimitError:
        return "LLM ERROR: Rate limit hit."
    except Exception as e:
        return "LLM ERROR: " + str(e)
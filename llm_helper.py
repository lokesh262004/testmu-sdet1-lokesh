"""
llm_helper.py

This module handles all communication with the Claude AI API.
When a test fails, we call explain_failure() with the error details
and Claude returns a plain English explanation + suggested fix.

Why Option A (Failure Explainer) over Option B (Flaky Test Classifier)?
Option A gives immediate, actionable value to any developer reading the report.
Instead of just seeing a stack trace, they get a human-readable explanation
of what broke and exactly how to fix it — saving debugging time on every failure.
"""

import anthropic
import os


def explain_failure(test_name: str, error_message: str, context: str = "") -> str:
    """
    Sends a test failure to Claude AI and returns a plain English explanation.

    Args:
        test_name:     The name of the test that failed (e.g. test_valid_login)
        error_message: The raw error/exception message from pytest
        context:       Optional extra context (e.g. URL, page title, response body)

    Returns:
        A plain English string with: what broke + why + suggested fix
    """

    # Build the prompt we send to Claude
    prompt = f"""You are a QA engineer assistant. A test has failed during an automated test run.

Test Name: {test_name}

Error Message:
{error_message}

Additional Context:
{context if context else "No additional context provided."}

Please explain:
1. What likely broke (in plain English, 2-3 sentences max)
2. The most likely root cause
3. A suggested fix or next debugging step

Keep your response concise and practical. Format it as:
WHAT BROKE: ...
ROOT CAUSE: ...
SUGGESTED FIX: ...
"""

    try:
        # Create the Anthropic client
        # It automatically reads ANTHROPIC_API_KEY from environment variables
        client = anthropic.Anthropic()

        # Make the real API call to Claude
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Fast and cost-efficient for this task
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    except anthropic.AuthenticationError:
        return "LLM ERROR: Invalid API key. Please check your ANTHROPIC_API_KEY environment variable."
    except anthropic.RateLimitError:
        return "LLM ERROR: Rate limit hit. Too many requests to Claude API."
    except Exception as e:
        return f"LLM ERROR: Could not get AI explanation. Reason: {str(e)}"

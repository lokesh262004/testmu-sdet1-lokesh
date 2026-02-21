"""
test_llm_demo.py

A simple demo test to show the LLM Failure Explainer working.
This test is DESIGNED to fail so you can see Claude AI explain the failure.

Run with: pytest tests/test_llm_demo.py -v
Then check: reports/failure_report.txt
"""
import pytest
import requests


def test_intentional_failure_demo():
    """
    This test intentionally fails to demonstrate the LLM Failure Explainer.
    When it fails, conftest.py catches the error and sends it to Claude AI.
    Claude will explain what broke and suggest a fix in the report.
    """
    # This will fail because 2 + 2 does not equal 5
    # You'll see Claude explain this in plain English in the report
    result = 2 + 2
    assert result == 5, f"Expected 5 but got {result}"


def test_api_failure_demo():
    """
    Simulates an API test failure by hitting a fake endpoint.
    Claude will explain the connection error in the failure report.
    """
    response = requests.get("https://api.testmu.ai/v1/tests",
                            headers={"Authorization": "Bearer fake_token"},
                            timeout=5)
    assert response.status_code == 200, \
        f"Expected 200 OK but got {response.status_code}"


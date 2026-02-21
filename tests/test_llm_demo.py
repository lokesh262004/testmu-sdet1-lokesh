"""
test_llm_demo.py
Demo test to show the LLM Failure Explainer working.
These tests are DESIGNED to fail so Claude AI explains the failure.
Run with: pytest tests/test_llm_demo.py -v
Then check: reports/failure_report.txt
"""
import pytest
import requests


def test_intentional_failure_demo():
    """
    This test intentionally fails to demonstrate the LLM Failure Explainer.
    When it fails, conftest.py catches the error and sends it to Claude AI.
    """
    result = 2 + 2
    assert result == 5, f"Expected 5 but got {result}"


def test_api_failure_demo():
    """
    Simulates an API test failure by hitting a fake endpoint.
    Claude will explain the connection error in the failure report.
    """
    response = requests.get(
        "https://httpbin.org/status/401",
        headers={"Authorization": "Bearer fake_token"},
        timeout=5
    )
    assert response.status_code == 200, \
        f"Expected 200 OK but got {response.status_code}"
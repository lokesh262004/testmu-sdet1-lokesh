"""
conftest.py

This is pytest's special configuration file.
It runs automatically before/after every test.

What it does here:
- After each test, checks if it failed
- If failed, sends the error to Claude AI via llm_helper
- Saves the AI explanation into a report file (reports/failure_report.txt)
- Also prints the explanation in the terminal
"""

import pytest
import os
from datetime import datetime
from llm_helper import explain_failure


# This list collects all failure explanations during the test run
failure_report = []


def pytest_runtest_makereport(item, call):
    """
    pytest hook: runs after each test phase (setup / call / teardown).
    We check the 'call' phase — that's when the actual test body runs.
    """
    if call.when == "call" and call.excinfo is not None:
        # A test has failed — extract the details
        test_name = item.nodeid
        error_message = str(call.excinfo.value)
        error_type = call.excinfo.type.__name__

        full_error = f"{error_type}: {error_message}"

        # Get page context if it's a Playwright test
        context = ""
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            try:
                page = item.funcargs["page"]
                context = f"Page URL at failure: {page.url}\nPage Title: {page.title()}"
            except Exception:
                context = "Could not retrieve page context."

        print(f"\n🔍 Sending failure to Claude AI for analysis: {test_name}")

        # Call Claude AI to explain the failure
        ai_explanation = explain_failure(
            test_name=test_name,
            error_message=full_error,
            context=context
        )

        print(f"\n🤖 Claude AI says:\n{ai_explanation}\n")

        # Store for the final report
        failure_report.append({
            "test": test_name,
            "error": full_error,
            "ai_explanation": ai_explanation,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


def pytest_sessionfinish(session, exitstatus):
    """
    pytest hook: runs once after ALL tests have finished.
    We write the full failure report to reports/failure_report.txt
    """
    if not failure_report:
        return  # No failures — no report needed

    # Make sure reports directory exists
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/failure_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("       TESTMU AI — AUTOMATED FAILURE ANALYSIS REPORT\n")
        f.write(f"       Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        for i, entry in enumerate(failure_report, 1):
            f.write(f"FAILURE #{i}\n")
            f.write(f"{'─' * 40}\n")
            f.write(f"Test:      {entry['test']}\n")
            f.write(f"Time:      {entry['timestamp']}\n")
            f.write(f"Error:     {entry['error']}\n\n")
            f.write(f"🤖 Claude AI Explanation:\n{entry['ai_explanation']}\n")
            f.write("\n" + "=" * 60 + "\n\n")

    print(f"\n📄 Failure report saved to: {report_path}")


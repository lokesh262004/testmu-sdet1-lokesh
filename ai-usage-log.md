# AI Usage Log

This file documents every AI tool used during this assessment, what task it helped with, and what it produced.

---

## Tool: Claude AI (claude.ai)

| Task | What I used it for | What it produced |
|------|-------------------|-----------------|
| Task 1 — Setup | Asked Claude to recommend the best stack and generate the folder structure for a Python Playwright project | Recommended Python + Playwright, generated the complete folder structure and setup commands |
| Task 1 — First Commit | Used Claude to draft the first commit message that mentions AI usage | Commit message: "Initial project setup using Claude AI to scaffold folder structure and install Playwright" |
| Task 2 — Login Tests | Prompted Claude with specific login scenarios to generate pytest + Playwright test cases | 7 test functions covering valid login, invalid credentials, empty fields, forgot password, session expiry, brute-force lockout |
| Task 2 — Dashboard Tests | Prompted Claude to generate dashboard test cases with a logged-in fixture | 8 test functions covering widget loading, data accuracy, filters, sorting, responsive layout, permission-based visibility |
| Task 2 — API Tests | Prompted Claude to generate REST API tests using the requests library | 10 test functions covering auth, CRUD, error handling, rate limiting, schema validation |
| Task 3 — LLM Integration | Used Claude to help design and write the llm_helper.py and conftest.py integration | Working Claude API integration that captures test failures and returns plain English explanations with root cause and fix suggestions |
| Task 3 — Prompts | Iteratively refined prompts for each module when first outputs were too generic | Final structured prompts that produce consistent, realistic test cases |

---

## Tool: Anthropic Claude API (claude-haiku-4-5-20251001)

| Task | What I used it for | What it produced |
|------|-------------------|-----------------|
| Task 3 — Runtime | Called programmatically inside conftest.py when a test fails | Plain English failure explanation with WHAT BROKE / ROOT CAUSE / SUGGESTED FIX format, saved to reports/failure_report.txt |

---

## Reflection

AI was used for **scaffolding, code generation, and runtime test analysis** — not for copying answers. Every prompt was iterated on based on what the first output got wrong. The LLM integration in Task 3 is a real API call (not mocked) and adds genuine value to the test report by making failures readable by anyone on the team, not just the developer who wrote the test.

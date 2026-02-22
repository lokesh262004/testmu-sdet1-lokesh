# Prompts Used for Test Case Generation

## Module 1 — Login

### Prompt Used:
```
You are a senior QA engineer. Generate detailed test cases for a Login module of a web-based 
test management platform. Use Python pytest + Playwright format.

Cover these scenarios:
1. Valid login with correct username and password
2. Invalid login with wrong password
3. Invalid login with wrong username
4. Empty username and password fields
5. Forgot password flow
6. Session expiry after inactivity
7. Brute-force lockout after 5 failed attempts

For each test:
- Use descriptive function names (test_<scenario>)
- Add a comment explaining what the test validates
- Use assert statements
- Use realistic fake data (e.g. testuser@testmu.ai)
- Target URL: https://app.testmu.ai/login

Output only the Python code. No explanation needed.
```

### What didn't work first time:
First attempt used a vague prompt ("write login tests in playwright python") and got generic tests 
with no real assertions, just page.goto() calls. Added specific scenario list, realistic data, 
and target URL on second attempt. Also had to explicitly ask for pytest format — first output 
was a standalone script with no test functions.

---

## Module 2 — Dashboard

### Prompt Used:
```
You are a senior QA engineer. Generate detailed test cases for a Dashboard module of a 
web-based test management platform built for QA teams. Use Python pytest + Playwright format.

Cover these scenarios:
1. Verify all dashboard widgets load within 3 seconds
2. Verify test run data displayed matches expected values
3. Verify filter by date range works correctly
4. Verify sort by status (pass/fail) works
5. Verify layout is responsive on 1280x720 and 375x812 (mobile)
6. Verify admin sees all widgets but viewer role sees limited widgets

For each test:
- Use descriptive function names
- Add inline comments
- Use page.wait_for_selector() for loading checks
- Assume user is already logged in (use a fixture)
- Target URL: https://app.testmu.ai/dashboard

Output only the Python code.
```

### What didn't work first time:
First prompt didn't mention the role-based visibility scenario — had to add it in a follow-up. 
Also the first output didn't use any fixtures for login state, so tests were not independent. 
Explicitly asking for a logged-in fixture fixed this. Responsive test needed viewport size 
added manually after first generation missed it.

---

## Module 3 — REST API

### Prompt Used:
```
You are a senior QA engineer. Generate REST API test cases for a test management platform API. 
Use Python pytest + requests library (not Playwright).

Base URL: https://api.testmu.ai/v1
Auth: Bearer token in Authorization header

Cover these scenarios:
1. Valid auth token returns 200
2. Invalid/expired token returns 401
3. GET /tests returns list of tests (schema validation)
4. POST /tests creates a new test (201 response)
5. PUT /tests/{id} updates an existing test
6. DELETE /tests/{id} deletes a test (204 response)
7. GET /tests with invalid ID returns 404
8. Simulate 500 server error handling
9. Rate limiting — send 100 requests rapidly and expect 429
10. Schema validation — response body has required fields: id, name, status, created_at

For each test:
- Use descriptive names
- Assert status codes AND response body fields
- Use a pytest fixture for the auth token and base URL
- Add a comment per test explaining the validation goal

Output only the Python code.
```

### What didn't work first time:
First attempt mixed Playwright and requests in the same file which caused import errors. 
Had to explicitly state "use requests library only, not Playwright". Also the schema validation 
test was missing — added scenario 10 in the second prompt iteration. Rate limiting test 
initially had no loop, just one request — fixed by specifying "send 100 requests rapidly".



---

## Per-Module Prompt Iteration Notes

### Login Module
First prompt was too vague — just asked for "login test cases." The LLM returned
generic scenarios without covering security edge cases. Added explicit instructions
to include brute-force lockout and SQL injection. Also specified Gherkin format
in the second attempt, which produced properly structured Given/When/Then steps.

### Dashboard Module
Initial prompt didn't mention roles or permissions, so all generated cases assumed
admin access. Revised prompt to specify "viewer" and "admin" roles explicitly.
Also had to add "responsive layout" as a keyword — the first output only covered
desktop scenarios and missed mobile entirely.

### API Module
First attempt generated only happy-path GET/POST tests. Had to re-prompt with
"include 4xx and 5xx error handling, rate limiting with 429 response, and schema
validation" to get full coverage. Also specified that auth token tests should cover
valid, invalid, missing, and expired token scenarios separately.
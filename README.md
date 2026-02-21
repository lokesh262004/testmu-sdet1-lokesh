# TestMu SDET-1 Assessment — AI-Native Quality Engineering

## Stack
- **Language:** Python 3
- **Test Framework:** pytest + Playwright
- **API Testing:** requests
- **LLM Integration:** Google Gemini API (gemini-1.5-flash)

---

## Project Structure

```
testmu-sdet1-lokesh/
├── tests/
│   ├── login/
│   │   └── test_login.py        # 7 login test cases
│   ├── dashboard/
│   │   └── test_dashboard.py    # 8 dashboard test cases
│   ├── api/
│   │   └── test_api.py          # 10 REST API test cases
│   └── test_llm_demo.py         # Demo test to show LLM integration
├── reports/
│   └── failure_report.txt       # Auto-generated AI failure analysis
├── prompts/
│   └── prompts.md               # All prompts used for test generation
├── llm_helper.py                # Claude AI API integration
├── conftest.py                  # pytest hooks for failure capture
├── ai-usage-log.md              # Log of every AI tool used
└── README.md
```

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/testmu-sdet1-lokesh.git
cd testmu-sdet1-lokesh
```

### 2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install playwright pytest pytest-playwright requests anthropic pytest-html
playwright install
```

### 4. Set your Claude API key
```bash
# Windows
set GEMINI_API_KEY=sk-ant-your-key-here

# Mac/Linux
export GEMINI_API_KEY=sk-ant-your-key-here
```

### 5. Run the LLM demo (shows AI failure explanation)
```bash
pytest tests/test_llm_demo.py -v
```
Then open `reports/failure_report.txt` to see Claude's explanation.

### 6. Run all tests
```bash
pytest tests/ -v
```

---

## Task 3 — LLM Integration (Option A: Failure Explainer)

When any test fails, the framework automatically:
1. Captures the test name, error message, and page URL (for Playwright tests)
2. Sends it to Claude AI via the Anthropic API
3. Gets back a plain English explanation: **what broke**, **root cause**, **suggested fix**
4. Saves everything to `reports/failure_report.txt`

### Sample Output (`reports/failure_report.txt`):
```
============================================================
       TESTMU AI — AUTOMATED FAILURE ANALYSIS REPORT
       Generated: 2025-01-15 14:32:01
============================================================

FAILURE #1
────────────────────────────────────────
Test:      tests/test_llm_demo.py::test_intentional_failure_demo
Time:      2025-01-15 14:32:01
Error:     AssertionError: Expected 5 but got 4

🤖 Claude AI Explanation:
WHAT BROKE: The assertion expected the sum of 2+2 to equal 5, but Python 
correctly computed 4. The test has an incorrect expected value.

ROOT CAUSE: The expected value in the assert statement is wrong. 
2 + 2 = 4, not 5.

SUGGESTED FIX: Change `assert result == 5` to `assert result == 4`, 
or update the test logic to match the actual expected business outcome.
```

---

## What I'd Build Next (With More Time)
- **CI/CD pipeline** — GitHub Actions to run tests on every pull request
- **HTML test report** — using pytest-html for a visual dashboard of results
- **Option B (Flaky Classifier)** — feed 5-run history to Claude to detect flaky patterns
- **Screenshot on failure** — attach Playwright screenshots to the AI explanation
- **Slack notification** — post the AI failure summary to a Slack channel automatically

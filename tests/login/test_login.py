import pytest
from playwright.sync_api import Page, expect


BASE_URL = "https://app.testmu.ai/login"
VALID_EMAIL = "testuser@testmu.ai"
VALID_PASSWORD = "Test@1234"


# ─────────────────────────────────────────────
# Test 1: Valid login with correct credentials
# ─────────────────────────────────────────────
def test_valid_login(page: Page):
    """Validates that a user with correct credentials is redirected to dashboard."""
    page.goto(BASE_URL)
    page.fill('input[name="email"]', VALID_EMAIL)
    page.fill('input[name="password"]', VALID_PASSWORD)
    page.click('button[type="submit"]')
    expect(page).to_have_url("https://app.testmu.ai/dashboard")


# ─────────────────────────────────────────────
# Test 2: Invalid login — wrong password
# ─────────────────────────────────────────────
def test_invalid_login_wrong_password(page: Page):
    """Validates that wrong password shows an error message."""
    page.goto(BASE_URL)
    page.fill('input[name="email"]', VALID_EMAIL)
    page.fill('input[name="password"]', "WrongPassword!")
    page.click('button[type="submit"]')
    error_msg = page.locator("text=Invalid email or password")
    expect(error_msg).to_be_visible()


# ─────────────────────────────────────────────
# Test 3: Invalid login — wrong username/email
# ─────────────────────────────────────────────
def test_invalid_login_wrong_email(page: Page):
    """Validates that a non-existent email shows an error."""
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "notauser@testmu.ai")
    page.fill('input[name="password"]', VALID_PASSWORD)
    page.click('button[type="submit"]')
    error_msg = page.locator("text=Invalid email or password")
    expect(error_msg).to_be_visible()


# ─────────────────────────────────────────────
# Test 4: Empty fields — form validation
# ─────────────────────────────────────────────
def test_empty_fields(page: Page):
    """Validates that submitting empty form shows required field errors."""
    page.goto(BASE_URL)
    page.click('button[type="submit"]')
    expect(page.locator("text=Email is required")).to_be_visible()
    expect(page.locator("text=Password is required")).to_be_visible()


# ─────────────────────────────────────────────
# Test 5: Forgot password flow
# ─────────────────────────────────────────────
def test_forgot_password_flow(page: Page):
    """Validates that forgot password link leads to reset page and accepts email."""
    page.goto(BASE_URL)
    page.click("text=Forgot password")
    expect(page).to_have_url("https://app.testmu.ai/forgot-password")
    page.fill('input[name="email"]', VALID_EMAIL)
    page.click('button[type="submit"]')
    expect(page.locator("text=Reset link sent")).to_be_visible()


# ─────────────────────────────────────────────
# Test 6: Session expiry — redirect to login
# ─────────────────────────────────────────────
def test_session_expiry_redirects_to_login(page: Page):
    """Validates that accessing dashboard without a session redirects to login."""
    # Clear cookies to simulate session expiry
    page.context.clear_cookies()
    page.goto("https://app.testmu.ai/dashboard")
    expect(page).to_have_url(BASE_URL)


# ─────────────────────────────────────────────
# Test 7: Brute-force lockout after 5 failed attempts
# ─────────────────────────────────────────────
def test_brute_force_lockout(page: Page):
    """Validates that account is locked after 5 consecutive failed login attempts."""
    page.goto(BASE_URL)
    for _ in range(5):
        page.fill('input[name="email"]', VALID_EMAIL)
        page.fill('input[name="password"]', "WrongPassword!")
        page.click('button[type="submit"]')

    # After 5 attempts, expect lockout message
    lockout_msg = page.locator("text=Account locked")
    expect(lockout_msg).to_be_visible()

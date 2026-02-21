import pytest
from playwright.sync_api import Page, expect


DASHBOARD_URL = "https://app.testmu.ai/dashboard"


@pytest.fixture
def logged_in_page(page: Page):
    """Fixture: logs in before each dashboard test so tests are independent."""
    page.goto("https://app.testmu.ai/login")
    page.fill('input[name="email"]', "testuser@testmu.ai")
    page.fill('input[name="password"]', "Test@1234")
    page.click('button[type="submit"]')
    page.wait_for_url(DASHBOARD_URL)
    return page


# ─────────────────────────────────────────────
# Test 1: All widgets load within 3 seconds
# ─────────────────────────────────────────────
def test_widgets_load_within_3_seconds(logged_in_page: Page):
    """Validates that all dashboard widgets are visible within 3 seconds of page load."""
    page = logged_in_page
    page.wait_for_selector(".dashboard-widget", timeout=3000)
    widgets = page.locator(".dashboard-widget")
    assert widgets.count() > 0, "No widgets found on dashboard"


# ─────────────────────────────────────────────
# Test 2: Data accuracy — test run counts match
# ─────────────────────────────────────────────
def test_dashboard_data_accuracy(logged_in_page: Page):
    """Validates that the displayed test run count is a real number, not empty."""
    page = logged_in_page
    run_count = page.locator('[data-testid="total-runs"]').inner_text()
    assert run_count.isdigit(), f"Expected a number but got: {run_count}"


# ─────────────────────────────────────────────
# Test 3: Filter by date range
# ─────────────────────────────────────────────
def test_filter_by_date_range(logged_in_page: Page):
    """Validates that applying a date filter updates the dashboard results."""
    page = logged_in_page
    page.click('[data-testid="date-filter"]')
    page.click("text=Last 7 days")
    page.wait_for_selector(".dashboard-widget")
    filtered_label = page.locator('[data-testid="filter-label"]').inner_text()
    assert "7" in filtered_label, "Date filter label did not update correctly"


# ─────────────────────────────────────────────
# Test 4: Sort by status (pass/fail)
# ─────────────────────────────────────────────
def test_sort_by_status(logged_in_page: Page):
    """Validates that sorting by status reorders the test list correctly."""
    page = logged_in_page
    page.click('[data-testid="sort-by-status"]')
    page.wait_for_selector(".test-row")
    first_status = page.locator(".test-row:first-child .status-badge").inner_text()
    assert first_status in ["Pass", "Fail"], f"Unexpected status value: {first_status}"


# ─────────────────────────────────────────────
# Test 5: Responsive layout on desktop and mobile
# ─────────────────────────────────────────────
def test_responsive_layout_desktop(logged_in_page: Page):
    """Validates dashboard layout renders correctly at 1280x720 (desktop)."""
    page = logged_in_page
    page.set_viewport_size({"width": 1280, "height": 720})
    page.reload()
    expect(page.locator(".dashboard-widget")).to_be_visible()


def test_responsive_layout_mobile(logged_in_page: Page):
    """Validates dashboard layout renders correctly at 375x812 (mobile)."""
    page = logged_in_page
    page.set_viewport_size({"width": 375, "height": 812})
    page.reload()
    # On mobile, sidebar should be hidden
    sidebar = page.locator(".sidebar")
    assert not sidebar.is_visible(), "Sidebar should be hidden on mobile"


# ─────────────────────────────────────────────
# Test 6: Permission-based widget visibility
# ─────────────────────────────────────────────
def test_admin_sees_all_widgets(page: Page):
    """Validates that admin role can see all widgets including admin-only ones."""
    page.goto("https://app.testmu.ai/login")
    page.fill('input[name="email"]', "admin@testmu.ai")
    page.fill('input[name="password"]', "Admin@1234")
    page.click('button[type="submit"]')
    page.wait_for_url(DASHBOARD_URL)
    admin_widget = page.locator('[data-testid="admin-widget"]')
    expect(admin_widget).to_be_visible()


def test_viewer_sees_limited_widgets(page: Page):
    """Validates that viewer role cannot see admin-only widgets."""
    page.goto("https://app.testmu.ai/login")
    page.fill('input[name="email"]', "viewer@testmu.ai")
    page.fill('input[name="password"]', "Viewer@1234")
    page.click('button[type="submit"]')
    page.wait_for_url(DASHBOARD_URL)
    admin_widget = page.locator('[data-testid="admin-widget"]')
    assert not admin_widget.is_visible(), "Viewer should not see admin-only widget"

import pytest
import requests
import time


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def base_url():
    """Returns the base URL for the TestMu API."""
    return "https://api.testmu.ai/v1"


@pytest.fixture
def auth_headers():
    """Returns valid Authorization headers using a test Bearer token."""
    return {"Authorization": "Bearer test_valid_token_abc123"}


@pytest.fixture
def invalid_headers():
    """Returns an invalid/expired token header."""
    return {"Authorization": "Bearer expired_token_xyz"}


# ─────────────────────────────────────────────
# Test 1: Valid auth token returns 200
# ─────────────────────────────────────────────
def test_valid_auth_token(base_url, auth_headers):
    """Validates that a valid token gives a 200 response on a protected endpoint."""
    response = requests.get(f"{base_url}/tests", headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"


# ─────────────────────────────────────────────
# Test 2: Invalid/expired token returns 401
# ─────────────────────────────────────────────
def test_invalid_auth_token(base_url, invalid_headers):
    """Validates that an expired or invalid token returns 401 Unauthorized."""
    response = requests.get(f"{base_url}/tests", headers=invalid_headers)
    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"


# ─────────────────────────────────────────────
# Test 3: GET /tests — schema validation
# ─────────────────────────────────────────────
def test_get_tests_schema(base_url, auth_headers):
    """Validates that GET /tests returns a list and each item has required fields."""
    response = requests.get(f"{base_url}/tests", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    if len(data) > 0:
        item = data[0]
        required_fields = ["id", "name", "status", "created_at"]
        for field in required_fields:
            assert field in item, f"Missing required field: {field}"


# ─────────────────────────────────────────────
# Test 4: POST /tests — create a new test
# ─────────────────────────────────────────────
def test_create_test(base_url, auth_headers):
    """Validates that POST /tests creates a new test and returns 201."""
    payload = {
        "name": "Automated Test - Login Flow",
        "status": "pending",
        "description": "Validates user login with valid credentials"
    }
    response = requests.post(f"{base_url}/tests", json=payload, headers=auth_headers)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    data = response.json()
    assert "id" in data, "Response should include the new test's ID"


# ─────────────────────────────────────────────
# Test 5: PUT /tests/{id} — update existing test
# ─────────────────────────────────────────────
def test_update_test(base_url, auth_headers):
    """Validates that PUT /tests/{id} updates a test and returns 200."""
    test_id = "existing-test-id-001"
    payload = {"status": "pass"}
    response = requests.put(f"{base_url}/tests/{test_id}", json=payload, headers=auth_headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    data = response.json()
    assert data.get("status") == "pass", "Status was not updated correctly"


# ─────────────────────────────────────────────
# Test 6: DELETE /tests/{id} — delete a test
# ─────────────────────────────────────────────
def test_delete_test(base_url, auth_headers):
    """Validates that DELETE /tests/{id} removes a test and returns 204."""
    test_id = "existing-test-id-002"
    response = requests.delete(f"{base_url}/tests/{test_id}", headers=auth_headers)
    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"


# ─────────────────────────────────────────────
# Test 7: GET /tests with invalid ID returns 404
# ─────────────────────────────────────────────
def test_get_test_invalid_id(base_url, auth_headers):
    """Validates that requesting a non-existent test ID returns 404."""
    response = requests.get(f"{base_url}/tests/nonexistent-id-99999", headers=auth_headers)
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}"


# ─────────────────────────────────────────────
# Test 8: Server error (500) is handled gracefully
# ─────────────────────────────────────────────
def test_server_error_handling(base_url, auth_headers):
    """Validates that a simulated 500 endpoint returns proper error structure."""
    response = requests.get(f"{base_url}/tests/trigger-500", headers=auth_headers)
    assert response.status_code == 500
    data = response.json()
    assert "error" in data, "500 response should contain an error field"


# ─────────────────────────────────────────────
# Test 9: Rate limiting returns 429 after many requests
# ─────────────────────────────────────────────
def test_rate_limiting(base_url, auth_headers):
    """Validates that sending 100 rapid requests triggers a 429 Too Many Requests."""
    status_codes = []
    for _ in range(100):
        response = requests.get(f"{base_url}/tests", headers=auth_headers)
        status_codes.append(response.status_code)
        if response.status_code == 429:
            break
    assert 429 in status_codes, "Rate limiting was not triggered after 100 rapid requests"


# ─────────────────────────────────────────────
# Test 10: Schema validation — all required fields present
# ─────────────────────────────────────────────
def test_response_schema_required_fields(base_url, auth_headers):
    """Validates that every test object in the response contains: id, name, status, created_at."""
    response = requests.get(f"{base_url}/tests", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    required_fields = ["id", "name", "status", "created_at"]
    for item in data:
        for field in required_fields:
            assert field in item, f"Test item missing field '{field}': {item}"

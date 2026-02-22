\# Generated Test Cases (LLM Output)



Generated using Claude AI (claude-3-5-haiku) via prompt engineering.

See `prompts.md` for the exact prompts used.



---



\## Login Tests (8 scenarios)



Feature: User Login

&nbsp; As a registered user

&nbsp; I want to log in to the TestMu platform

&nbsp; So that I can access my test dashboard



&nbsp; Scenario: Valid credentials login

&nbsp;   Given I am on the login page

&nbsp;   When I enter valid email "testuser@testmu.ai" and password "ValidPass@123"

&nbsp;   And I click the login button

&nbsp;   Then I should be redirected to the dashboard

&nbsp;   And I should see a welcome message



&nbsp; Scenario: Invalid password login

&nbsp;   Given I am on the login page

&nbsp;   When I enter valid email "testuser@testmu.ai" and wrong password "WrongPass"

&nbsp;   And I click the login button

&nbsp;   Then I should see an error message "Invalid credentials"

&nbsp;   And I should remain on the login page



&nbsp; Scenario: Empty email field

&nbsp;   Given I am on the login page

&nbsp;   When I leave the email field empty

&nbsp;   And I enter password "ValidPass@123"

&nbsp;   And I click the login button

&nbsp;   Then I should see a validation error "Email is required"



&nbsp; Scenario: Empty password field

&nbsp;   Given I am on the login page

&nbsp;   When I enter email "testuser@testmu.ai"

&nbsp;   And I leave the password field empty

&nbsp;   And I click the login button

&nbsp;   Then I should see a validation error "Password is required"



&nbsp; Scenario: Forgot password link

&nbsp;   Given I am on the login page

&nbsp;   When I click the "Forgot Password" link

&nbsp;   Then I should be redirected to the password reset page

&nbsp;   And I should see a field to enter my email



&nbsp; Scenario: Session expiry redirect

&nbsp;   Given I am logged in

&nbsp;   When my session token expires

&nbsp;   And I try to access a protected page

&nbsp;   Then I should be redirected to the login page

&nbsp;   And I should see "Session expired, please log in again"



&nbsp; Scenario: Brute force lockout

&nbsp;   Given I am on the login page

&nbsp;   When I enter wrong credentials 5 times in a row

&nbsp;   Then my account should be temporarily locked

&nbsp;   And I should see "Too many failed attempts. Try again later."



&nbsp; Scenario: SQL injection attempt

&nbsp;   Given I am on the login page

&nbsp;   When I enter "' OR 1=1 --" in the email field

&nbsp;   And I enter any value in the password field

&nbsp;   And I click the login button

&nbsp;   Then I should see an error "Invalid credentials"

&nbsp;   And the system should not be compromised



---



\## Dashboard Tests (8 scenarios)



Feature: Dashboard Functionality

&nbsp; As a logged-in user

&nbsp; I want to view my test dashboard

&nbsp; So that I can monitor my test runs and results



&nbsp; Scenario: Dashboard widgets load

&nbsp;   Given I am logged in

&nbsp;   When I navigate to the dashboard

&nbsp;   Then all widgets should load within 3 seconds

&nbsp;   And I should see the test run summary widget

&nbsp;   And I should see the pass/fail ratio chart



&nbsp; Scenario: Data accuracy on dashboard

&nbsp;   Given I have 10 test runs with 8 passing and 2 failing

&nbsp;   When I view the dashboard

&nbsp;   Then the pass rate should display as "80%"

&nbsp;   And the total runs should display as "10"



&nbsp; Scenario: Filter tests by date range

&nbsp;   Given I am on the dashboard

&nbsp;   When I set the date filter to "Last 7 days"

&nbsp;   Then only test runs from the last 7 days should be shown

&nbsp;   And the summary metrics should update accordingly



&nbsp; Scenario: Sort test runs by status

&nbsp;   Given I am on the dashboard with multiple test runs

&nbsp;   When I click the "Status" column header to sort

&nbsp;   Then failing tests should appear at the top

&nbsp;   And passing tests should appear below



&nbsp; Scenario: Responsive layout on mobile

&nbsp;   Given I am logged in on a mobile device (375px width)

&nbsp;   When I navigate to the dashboard

&nbsp;   Then the layout should adapt to mobile screen

&nbsp;   And all widgets should be visible without horizontal scrolling



&nbsp; Scenario: Permission-based widget visibility

&nbsp;   Given I am logged in as a "viewer" role user

&nbsp;   When I navigate to the dashboard

&nbsp;   Then I should not see the "Admin Settings" widget

&nbsp;   And I should see the "My Test Runs" widget



&nbsp; Scenario: Empty state dashboard

&nbsp;   Given I am a new user with no test runs

&nbsp;   When I navigate to the dashboard

&nbsp;   Then I should see an empty state message "No test runs yet"

&nbsp;   And I should see a "Create your first test" button



&nbsp; Scenario: Dashboard refresh

&nbsp;   Given I am on the dashboard

&nbsp;   When I click the refresh button

&nbsp;   Then the data should reload

&nbsp;   And the "Last updated" timestamp should update



---



\## API Tests (13 scenarios)



Feature: REST API Testing

&nbsp; As an API consumer

&nbsp; I want to interact with the TestMu REST API

&nbsp; So that I can manage test runs programmatically



&nbsp; Scenario: Valid token returns 200

&nbsp;   Given I have a valid JWT auth token

&nbsp;   When I send a GET request to "/api/v1/user/profile"

&nbsp;   Then the response status should be 200

&nbsp;   And the response body should contain user profile data



&nbsp; Scenario: Missing token returns 401

&nbsp;   Given I have no auth token

&nbsp;   When I send a GET request to "/api/v1/user/profile"

&nbsp;   Then the response status should be 401

&nbsp;   And the response body should contain "Unauthorized"



&nbsp; Scenario: Invalid token returns 401

&nbsp;   Given I have an invalid token "Bearer this.is.fake"

&nbsp;   When I send a GET request to "/api/v1/user/profile"

&nbsp;   Then the response status should be 401



&nbsp; Scenario: Expired token returns 401

&nbsp;   Given I have an expired JWT token

&nbsp;   When I send a GET request to "/api/v1/user/profile"

&nbsp;   Then the response status should be 401

&nbsp;   And the error should indicate token expiry



&nbsp; Scenario: Create test run (POST)

&nbsp;   Given I have a valid auth token

&nbsp;   When I POST to "/api/v1/runs" with valid run data

&nbsp;   Then the response status should be 201

&nbsp;   And the response should contain a new run ID



&nbsp; Scenario: Read test run (GET)

&nbsp;   Given a test run with ID "run-001" exists

&nbsp;   When I GET "/api/v1/runs/run-001" with a valid token

&nbsp;   Then the response status should be 200

&nbsp;   And the response body should contain run details



&nbsp; Scenario: Update test run (PUT)

&nbsp;   Given a test run with ID "run-001" exists

&nbsp;   When I PUT "/api/v1/runs/run-001" with updated status "passed"

&nbsp;   Then the response status should be 200

&nbsp;   And the run status should be updated to "passed"



&nbsp; Scenario: Delete test run (DELETE)

&nbsp;   Given a test run with ID "run-001" exists

&nbsp;   When I DELETE "/api/v1/runs/run-001" with a valid token

&nbsp;   Then the response status should be 204



&nbsp; Scenario: Read deleted run returns 404

&nbsp;   Given test run "run-001" has been deleted

&nbsp;   When I GET "/api/v1/runs/run-001"

&nbsp;   Then the response status should be 404



&nbsp; Scenario: 404 for nonexistent resource

&nbsp;   Given I have a valid auth token

&nbsp;   When I GET "/api/v1/runs/nonexistent-id-99999"

&nbsp;   Then the response status should be 404

&nbsp;   And the body should contain "Not found"



&nbsp; Scenario: 400 for invalid payload

&nbsp;   Given I have a valid auth token

&nbsp;   When I POST to "/api/v1/runs" with missing required fields

&nbsp;   Then the response status should be 400

&nbsp;   And the body should contain validation error details



&nbsp; Scenario: Rate limit triggers after burst

&nbsp;   Given I have a valid auth token

&nbsp;   When I send 100 requests within 10 seconds

&nbsp;   Then at least one response should have status 429

&nbsp;   And the response should contain "Too Many Requests"



&nbsp; Scenario: Rate limit response has Retry-After header

&nbsp;   Given the rate limit has been triggered

&nbsp;   When I receive a 429 response

&nbsp;   Then the response headers should contain "Retry-After"

&nbsp;   And the value should indicate seconds to wait


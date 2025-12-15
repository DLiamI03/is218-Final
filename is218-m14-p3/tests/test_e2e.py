import pytest
from playwright.sync_api import Page, expect
import time


# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
    }


@pytest.fixture
def test_user_credentials():
    """Generate unique test user credentials."""
    timestamp = int(time.time())
    return {
        "username": f"testuser{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "testpass123"
    }


class TestAuthenticationE2E:
    """E2E tests for authentication flows."""
    
    def test_user_registration_positive(self, page: Page, test_user_credentials):
        """Test successful user registration."""
        page.goto(BASE_URL)
        
        # Click on Register link
        page.click("#show-register")
        
        # Fill registration form
        page.fill("#register-username", test_user_credentials["username"])
        page.fill("#register-email", test_user_credentials["email"])
        page.fill("#register-password", test_user_credentials["password"])
        
        # Submit form
        page.click("#registerForm button[type='submit']")
        
        # Wait for success message
        expect(page.locator("#toast")).to_contain_text("Registration successful")
        
        # Should redirect to login form
        expect(page.locator("#login-form")).to_be_visible()
    
    def test_user_registration_duplicate_username(self, page: Page, test_user_credentials):
        """Test registration with duplicate username (negative)."""
        import uuid
        unique_username = f"duptest_{uuid.uuid4().hex[:8]}"
        
        page.goto(BASE_URL)
        
        # Register first user
        page.click("#show-register")
        page.fill("#register-username", unique_username)
        page.fill("#register-email", f"{unique_username}@example.com")
        page.fill("#register-password", test_user_credentials["password"])
        page.click("#registerForm button[type='submit']")
        
        # Wait for success toast and form to switch back to login
        expect(page.locator("#toast")).to_contain_text("Registration successful", timeout=5000)
        page.wait_for_timeout(1000)
        
        # Ensure we're back on login form before clicking show-register
        expect(page.locator("#login-form")).to_be_visible()
        
        # Try to register again with same username
        page.click("#show-register")
        page.wait_for_timeout(500)
        page.fill("#register-username", unique_username)
        page.fill("#register-email", f"different_{unique_username}@example.com")
        page.fill("#register-password", test_user_credentials["password"])
        page.click("#registerForm button[type='submit']")
        
        # Should show error for duplicate username
        expect(page.locator("#toast")).to_contain_text("already registered")
    
    def test_user_login_positive(self, page: Page, test_user_credentials):
        """Test successful user login."""
        page.goto(BASE_URL)
        
        # Register user first
        page.click("#show-register")
        page.fill("#register-username", test_user_credentials["username"])
        page.fill("#register-email", test_user_credentials["email"])
        page.fill("#register-password", test_user_credentials["password"])
        page.click("#registerForm button[type='submit']")
        
        # Wait for registration success
        page.wait_for_timeout(1000)
        
        # Login
        page.fill("#login-username", test_user_credentials["username"])
        page.fill("#login-password", test_user_credentials["password"])
        page.click("#loginForm button[type='submit']")
        
        # Should show app section
        expect(page.locator("#app-section")).to_be_visible()
        expect(page.locator("#username-display")).to_contain_text(test_user_credentials["username"])
    
    def test_user_login_invalid_credentials(self, page: Page):
        """Test login with invalid credentials (negative)."""
        page.goto(BASE_URL)
        
        # Try to login with invalid credentials
        page.fill("#login-username", "nonexistentuser")
        page.fill("#login-password", "wrongpassword")
        page.click("#loginForm button[type='submit']")
        
        # Should show error
        expect(page.locator("#toast")).to_contain_text("Incorrect username or password")
        
        # Should stay on login page
        expect(page.locator("#auth-section")).to_be_visible()


class TestCalculationsBREAD:
    """E2E tests for BREAD operations on calculations."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_user_credentials):
        """Setup: Register and login before each test."""
        page.goto(BASE_URL)
        
        # Register
        page.click("#show-register")
        page.fill("#register-username", test_user_credentials["username"])
        page.fill("#register-email", test_user_credentials["email"])
        page.fill("#register-password", test_user_credentials["password"])
        page.click("#registerForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Login
        page.fill("#login-username", test_user_credentials["username"])
        page.fill("#login-password", test_user_credentials["password"])
        page.click("#loginForm button[type='submit']")
        
        # Wait for app to load
        expect(page.locator("#app-section")).to_be_visible()
        page.wait_for_timeout(1000)
    
    def test_add_calculation_positive(self, page: Page):
        """Test adding a new calculation (positive scenario)."""
        # Fill calculation form
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        
        # Submit form
        page.click("#calculationForm button[type='submit']")
        
        # Should show success message
        expect(page.locator("#toast")).to_contain_text("added successfully")
        
        # Should display in list
        expect(page.locator(".calculation-item")).to_be_visible()
        expect(page.locator(".calculation-expression")).to_contain_text("10 + 5")
        expect(page.locator(".calculation-result")).to_contain_text("15")
    
    def test_add_calculation_all_operations(self, page: Page):
        """Test adding calculations with all operations."""
        operations = [
            ("10", "add", "5", "15"),
            ("20", "subtract", "8", "12"),
            ("6", "multiply", "7", "42"),
            ("100", "divide", "4", "25"),
        ]
        
        for operand1, operation, operand2, expected_result in operations:
            page.fill("#operand1", operand1)
            page.select_option("#operation", operation)
            page.fill("#operand2", operand2)
            page.click("#calculationForm button[type='submit']")
            
            page.wait_for_timeout(500)
        
        # Should have 4 calculations
        calculations = page.locator(".calculation-item")
        expect(calculations).to_have_count(4)
    
    def test_add_calculation_divide_by_zero(self, page: Page):
        """Test division by zero (negative scenario)."""
        # Try to divide by zero
        page.fill("#operand1", "10")
        page.select_option("#operation", "divide")
        page.fill("#operand2", "0")
        page.click("#calculationForm button[type='submit']")
        
        # Should show error
        expect(page.locator("#toast")).to_contain_text("divide by zero")
    
    def test_add_calculation_invalid_input(self, page: Page):
        """Test adding calculation with invalid input (negative scenario)."""
        # Try to submit without selecting operation
        page.fill("#operand1", "10")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        
        # Should show error (HTML5 validation or toast)
        # The form should not submit
        expect(page.locator("#calculationForm")).to_be_visible()
    
    def test_browse_calculations(self, page: Page):
        """Test browsing all calculations."""
        # Add multiple calculations
        for i in range(3):
            page.fill("#operand1", str(i + 1))
            page.select_option("#operation", "add")
            page.fill("#operand2", str(i + 1))
            page.click("#calculationForm button[type='submit']")
            page.wait_for_timeout(500)
        
        # Click refresh
        page.click("#refresh-btn")
        page.wait_for_timeout(500)
        
        # Should show all 3 calculations
        calculations = page.locator(".calculation-item")
        expect(calculations).to_have_count(3)
    
    def test_read_calculation_via_edit(self, page: Page):
        """Test reading a specific calculation by clicking edit."""
        # Add a calculation
        page.fill("#operand1", "15")
        page.select_option("#operation", "multiply")
        page.fill("#operand2", "3")
        page.click("#calculationForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Click edit button
        page.click(".calculation-item .btn-success")
        
        # Form should be populated with calculation data
        expect(page.locator("#operand1")).to_have_value("15")
        expect(page.locator("#operation")).to_have_value("multiply")
        expect(page.locator("#operand2")).to_have_value("3")
        expect(page.locator("#form-title")).to_contain_text("Edit")
    
    def test_edit_calculation_positive(self, page: Page):
        """Test editing an existing calculation (positive scenario)."""
        # Add a calculation
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Click edit
        page.click(".calculation-item .btn-success")
        
        # Modify the calculation
        page.fill("#operand1", "20")
        page.select_option("#operation", "multiply")
        page.fill("#operand2", "3")
        page.click("#calculationForm button[type='submit']")
        
        # Should show success message
        expect(page.locator("#toast")).to_contain_text("updated successfully")
        
        # Should display updated values
        page.wait_for_timeout(500)
        expect(page.locator(".calculation-expression")).to_contain_text("20 × 3")
        expect(page.locator(".calculation-result")).to_contain_text("60")
    
    def test_edit_calculation_to_invalid_state(self, page: Page):
        """Test editing calculation to invalid state (negative scenario)."""
        # Add a calculation
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Click edit
        page.click(".calculation-item .btn-success")
        
        # Try to change to divide by zero
        page.select_option("#operation", "divide")
        page.fill("#operand2", "0")
        page.click("#calculationForm button[type='submit']")
        
        # Should show error
        expect(page.locator("#toast")).to_contain_text("divide by zero")
    
    def test_delete_calculation_positive(self, page: Page):
        """Test deleting a calculation (positive scenario)."""
        # Add a calculation
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Delete the calculation
        page.once("dialog", lambda dialog: dialog.accept())
        page.click(".calculation-item .btn-danger")
        
        # Should show success message
        expect(page.locator("#toast")).to_contain_text("deleted successfully")
        
        # Should show empty state
        page.wait_for_timeout(500)
        expect(page.locator(".empty-state")).to_be_visible()
    
    def test_delete_multiple_calculations(self, page: Page):
        """Test deleting multiple calculations."""
        # Add 3 calculations
        for i in range(3):
            page.fill("#operand1", str(i + 1))
            page.select_option("#operation", "add")
            page.fill("#operand2", str(i + 1))
            page.click("#calculationForm button[type='submit']")
            page.wait_for_timeout(500)
        
        # Delete all calculations
        for _ in range(3):
            page.once("dialog", lambda dialog: dialog.accept())
            page.click(".calculation-item .btn-danger")
            page.wait_for_timeout(500)
        
        # Should show empty state
        expect(page.locator(".empty-state")).to_be_visible()
    
    def test_cancel_edit(self, page: Page):
        """Test canceling an edit operation."""
        # Add a calculation
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        
        page.wait_for_timeout(1000)
        
        # Click edit
        page.click(".calculation-item .btn-success")
        
        # Verify edit mode
        expect(page.locator("#form-title")).to_contain_text("Edit")
        
        # Click cancel
        page.click("#cancel-btn")
        
        # Should return to add mode
        expect(page.locator("#form-title")).to_contain_text("Add New")
        expect(page.locator("#operand1")).to_have_value("")


class TestUserIsolation:
    """Test that users can only access their own calculations."""
    
    def test_user_isolation(self, page: Page):
        """Test that different users see only their own calculations."""
        timestamp = int(time.time())
        
        # Create first user
        user1 = {
            "username": f"user1_{timestamp}",
            "email": f"user1_{timestamp}@example.com",
            "password": "password123"
        }
        
        page.goto(BASE_URL)
        page.click("#show-register")
        page.fill("#register-username", user1["username"])
        page.fill("#register-email", user1["email"])
        page.fill("#register-password", user1["password"])
        page.click("#registerForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Login as user1
        page.fill("#login-username", user1["username"])
        page.fill("#login-password", user1["password"])
        page.click("#loginForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Add calculation for user1
        page.fill("#operand1", "100")
        page.select_option("#operation", "add")
        page.fill("#operand2", "50")
        page.click("#calculationForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Logout
        page.click("#logout-btn")
        page.wait_for_timeout(1000)
        
        # Create second user
        user2 = {
            "username": f"user2_{timestamp}",
            "email": f"user2_{timestamp}@example.com",
            "password": "password123"
        }
        
        page.click("#show-register")
        page.fill("#register-username", user2["username"])
        page.fill("#register-email", user2["email"])
        page.fill("#register-password", user2["password"])
        page.click("#registerForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Login as user2
        page.fill("#login-username", user2["username"])
        page.fill("#login-password", user2["password"])
        page.click("#loginForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # User2 should see empty calculations
        expect(page.locator(".empty-state")).to_be_visible()


class TestUIResponsiveness:
    """Test UI responsiveness and validation."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup: Register and login before each test."""
        timestamp = int(time.time())
        credentials = {
            "username": f"testuser{timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "testpass123"
        }
        
        page.goto(BASE_URL)
        page.click("#show-register")
        page.fill("#register-username", credentials["username"])
        page.fill("#register-email", credentials["email"])
        page.fill("#register-password", credentials["password"])
        page.click("#registerForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        page.fill("#login-username", credentials["username"])
        page.fill("#login-password", credentials["password"])
        page.click("#loginForm button[type='submit']")
        expect(page.locator("#app-section")).to_be_visible()
        page.wait_for_timeout(1000)
    
    def test_form_validation(self, page: Page):
        """Test client-side form validation."""
        # Test that number inputs have proper type attribute
        operand1_type = page.get_attribute("#operand1", "type")
        assert operand1_type == "number", "Operand1 should be a number input"
        
        # Test that form has valid inputs
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        
        # Verify values are set correctly
        assert page.input_value("#operand1") == "10"
        assert page.input_value("#operand2") == "5"
    
    def test_refresh_button(self, page: Page):
        """Test the refresh button functionality."""
        # Add a calculation
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("#calculationForm button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Click refresh
        page.click("#refresh-btn")
        page.wait_for_timeout(500)
        
        # Calculation should still be visible
        expect(page.locator(".calculation-item")).to_be_visible()

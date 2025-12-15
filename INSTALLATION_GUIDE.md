# Installation and Testing Guide

## Complete Setup Instructions

Follow these steps to get the project running and tested.

---

## Option 1: Docker Compose (Easiest & Recommended)

This method handles everything automatically - database, application, and dependencies.

### Prerequisites
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Make sure Docker Desktop is running

### Steps

1. **Navigate to project directory:**
```powershell
cd c:\Users\Dogukan\Documents\VSC\IS218_M14
```

2. **Start everything:**
```powershell
docker-compose up --build
```

This command will:
- Build the Docker image
- Start PostgreSQL database
- Start the FastAPI application
- Set up all dependencies automatically

3. **Access the application:**
- Open browser: http://localhost:8000
- API docs: http://localhost:8000/docs

4. **Stop the application:**
Press `Ctrl+C` in the terminal, then:
```powershell
docker-compose down
```

---

## Option 2: Local Development (For Testing)

This method is useful for running tests locally.

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15 (or use Docker for just the database)

### Steps

1. **Start PostgreSQL (using Docker):**
```powershell
docker run -d --name postgres-calc \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=calculations_db \
  -p 5432:5432 \
  postgres:15
```

2. **Set up Python environment:**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium
```

3. **Create .env file:**
```powershell
copy .env.example .env
```

4. **Start the application:**
```powershell
uvicorn app.main:app --reload
```

5. **Access the application:**
- Open browser: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## Running Tests

### Setup for Tests

Make sure you have installed the dependencies:
```powershell
pip install -r requirements.txt
playwright install --with-deps chromium
```

### Run All Tests
```powershell
pytest -v
```

### Run E2E Tests Only
```powershell
pytest tests/test_e2e.py -v
```

### Run Tests with Browser Visible
```powershell
pytest tests/test_e2e.py -v --headed --slowmo 100
```

### Run Specific Test
```powershell
pytest tests/test_e2e.py::TestCalculationsBREAD::test_add_calculation_positive -v
```

### Expected Output
You should see tests passing like:
```
tests/test_e2e.py::TestAuthenticationE2E::test_user_registration_positive PASSED
tests/test_e2e.py::TestAuthenticationE2E::test_user_login_positive PASSED
tests/test_e2e.py::TestCalculationsBREAD::test_add_calculation_positive PASSED
tests/test_e2e.py::TestCalculationsBREAD::test_browse_calculations PASSED
tests/test_e2e.py::TestCalculationsBREAD::test_edit_calculation_positive PASSED
tests/test_e2e.py::TestCalculationsBREAD::test_delete_calculation_positive PASSED
...
```

---

## Testing the Application Manually

### 1. Register a New User
1. Go to http://localhost:8000
2. Click "Register"
3. Enter:
   - Username: `testuser` (min 3 characters)
   - Email: `test@example.com`
   - Password: `testpass123` (min 6 characters)
4. Click "Register" button
5. You should see "Registration successful!" message

### 2. Login
1. Enter your username and password
2. Click "Login"
3. You should be redirected to the main application

### 3. Add a Calculation (CREATE)
1. Fill in the form:
   - First Operand: `10`
   - Operation: Select "Addition (+)"
   - Second Operand: `5`
2. Click "Add Calculation"
3. You should see the calculation appear in the list showing `10 + 5 = 15`

### 4. Browse Calculations (READ ALL)
- All your calculations are displayed automatically
- Click "Refresh" button to reload the list
- You should see all your calculations with timestamps

### 5. View Calculation Details (READ ONE)
- Each calculation shows:
  - Expression (e.g., "10 + 5")
  - Result (e.g., "= 15")
  - Created and updated timestamps

### 6. Edit a Calculation (UPDATE)
1. Click the "Edit" button on any calculation
2. The form will populate with the calculation's values
3. Change any values (e.g., change 5 to 8)
4. Click "Update Calculation"
5. You should see the result update (e.g., "10 + 8 = 18")

### 7. Delete a Calculation (DELETE)
1. Click the "Delete" button on any calculation
2. Confirm the deletion in the popup dialog
3. The calculation should disappear from the list

### 8. Test Validation
Try these to test error handling:
- **Division by zero**: Enter `10 ÷ 0` → Should show error
- **Invalid operation**: Don't select an operation → Should prevent submission
- **Empty fields**: Leave fields empty → Should prevent submission

### 9. Test All Operations
Create calculations with:
- Addition: `15 + 7 = 22`
- Subtraction: `20 - 8 = 12`
- Multiplication: `6 × 7 = 42`
- Division: `100 ÷ 4 = 25`

### 10. Test User Isolation
1. Logout (click "Logout" button)
2. Register a new user with different credentials
3. Login with new user
4. You should see NO calculations (empty state)
5. Add a calculation for this user
6. Logout and login with first user
7. You should only see the first user's calculations

---

## API Testing with cURL or Postman

### 1. Register User
```powershell
curl -X POST http://localhost:8000/register `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"testpass123\"}'
```

### 2. Login
```powershell
curl -X POST http://localhost:8000/token `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=testuser&password=testpass123"
```

Save the `access_token` from the response.

### 3. Add Calculation
```powershell
curl -X POST http://localhost:8000/calculations `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -d '{\"operation\":\"add\",\"operand1\":10,\"operand2\":5}'
```

### 4. Browse Calculations
```powershell
curl -X GET http://localhost:8000/calculations `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Get Specific Calculation
```powershell
curl -X GET http://localhost:8000/calculations/1 `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 6. Update Calculation
```powershell
curl -X PUT http://localhost:8000/calculations/1 `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -d '{\"operation\":\"multiply\",\"operand1\":20,\"operand2\":3}'
```

### 7. Delete Calculation
```powershell
curl -X DELETE http://localhost:8000/calculations/1 `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

### Swagger UI
- URL: http://localhost:8000/docs
- Features:
  - Try out all endpoints directly in browser
  - See request/response schemas
  - Test authentication
  - View all available operations

### ReDoc
- URL: http://localhost:8000/redoc
- Features:
  - Alternative documentation view
  - Better for reading/reference
  - Cleaner layout

---

## Troubleshooting

### Problem: Port 8000 already in use
**Solution:**
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
uvicorn app.main:app --port 8001
```

### Problem: Database connection error
**Solution:**
```powershell
# Check if PostgreSQL is running
docker ps

# Restart Docker Compose
docker-compose down -v
docker-compose up --build
```

### Problem: Tests failing
**Solution:**
```powershell
# Make sure app is running
docker-compose up

# Wait for app to start (check http://localhost:8000)

# Run tests in new terminal
pytest tests/test_e2e.py -v
```

### Problem: Playwright browser issues
**Solution:**
```powershell
# Reinstall Playwright browsers
playwright install --with-deps chromium

# If that fails, try
pip uninstall playwright
pip install playwright
playwright install --with-deps chromium
```

### Problem: ModuleNotFoundError
**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Docker container won't start
**Solution:**
```powershell
# Clean everything
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

---

## Verifying Everything Works

Run this checklist to verify complete functionality:

### Backend Tests
- [ ] App starts without errors
- [ ] Can access http://localhost:8000
- [ ] API docs load at http://localhost:8000/docs
- [ ] Health check works: http://localhost:8000/health

### Frontend Tests
- [ ] Main page loads
- [ ] Can switch between login and register
- [ ] Form validation works
- [ ] No console errors (F12 Developer Tools)

### BREAD Operations
- [ ] **Browse**: GET /calculations returns list
- [ ] **Read**: GET /calculations/{id} returns specific calculation
- [ ] **Edit**: PUT /calculations/{id} updates calculation
- [ ] **Add**: POST /calculations creates calculation
- [ ] **Delete**: DELETE /calculations/{id} removes calculation

### Authentication
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Token is stored and used
- [ ] Can logout
- [ ] Protected endpoints require authentication

### Validation
- [ ] Division by zero is prevented
- [ ] Invalid operations are rejected
- [ ] Empty fields are validated
- [ ] User can only see own calculations

### Test Suite
- [ ] All unit tests pass
- [ ] All E2E tests pass
- [ ] Tests cover positive scenarios
- [ ] Tests cover negative scenarios

---

## Next Steps

Once everything is working locally:

1. **Initialize Git:**
```powershell
git init
git add .
git commit -m "Initial commit: BREAD operations for calculations"
```

2. **Push to GitHub:**
```powershell
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

3. **Set up CI/CD:**
- Add GitHub secrets (DOCKER_USERNAME, DOCKER_PASSWORD)
- Push code triggers GitHub Actions
- Verify workflow passes

4. **Take Screenshots:**
- GitHub Actions success
- Docker Hub image
- Application BREAD operations

5. **Complete Documentation:**
- Fill out REFLECTION.md
- Update README.md with your URLs
- Review SUBMISSION_CHECKLIST.md

6. **Submit:**
- GitHub repository URL
- Docker Hub image URL
- Screenshots
- Completed reflection

---

**You're all set! Good luck! 🚀**

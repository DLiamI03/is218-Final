# Submission Checklist - IS218 Module 14

## Student Information
- **Name**: ___________________
- **Date**: ___________________
- **GitHub Repository**: ___________________
- **Docker Hub Repository**: ___________________

---

## 1. Submission Completeness (50 Points)

### GitHub Repository Link (10 Points)
- [ ] Repository link provided
- [ ] Repository is public and accessible
- [ ] All code is committed and pushed
- [ ] Repository has a clear structure

**Notes**: ___________________

---

### Required Files in Repository (15 Points)

#### Backend Files
- [ ] `app/main.py` - BREAD endpoints implemented
- [ ] `app/database.py` - Database models (User, Calculation)
- [ ] `app/schemas.py` - Pydantic schemas
- [ ] `app/auth.py` - Authentication logic

#### Frontend Files
- [ ] `static/index.html` - Main HTML page
- [ ] `static/style.css` - Styling
- [ ] `static/script.js` - Frontend JavaScript

#### Test Files
- [ ] `tests/conftest.py` - Test configuration
- [ ] `tests/test_e2e.py` - Playwright E2E tests

#### Configuration Files
- [ ] `Dockerfile` - Docker image definition
- [ ] `docker-compose.yml` - Docker Compose configuration
- [ ] `requirements.txt` - Python dependencies
- [ ] `.github/workflows/ci-cd.yml` - GitHub Actions workflow
- [ ] `pytest.ini` - Pytest configuration

**Notes**: ___________________

---

### Screenshots (15 Points)

#### Required Screenshots (5 points each)

**1. GitHub Actions Workflow Success**
- [ ] Screenshot shows successful workflow run
- [ ] All stages passed (test, build, push)
- [ ] Timestamp visible
- [ ] File name: `screenshot_github_actions.png`

**2. Docker Hub Deployment**
- [ ] Screenshot shows Docker Hub repository
- [ ] Image is successfully pushed
- [ ] Latest tag visible
- [ ] File name: `screenshot_docker_hub.png`

**3. Application Functionality**
- [ ] Screenshots show all BREAD operations working
  - [ ] Browse: List of calculations
  - [ ] Read: Viewing a calculation
  - [ ] Edit: Editing a calculation
  - [ ] Add: Creating a new calculation
  - [ ] Delete: Deleting a calculation
- [ ] File names: `screenshot_browse.png`, `screenshot_add.png`, `screenshot_edit.png`, `screenshot_delete.png`

**Notes**: ___________________

---

### Documentation (10 Points)

#### README.md (5 Points)
- [ ] Clear project description
- [ ] Installation instructions
- [ ] How to run the application
- [ ] How to run tests locally
- [ ] API documentation or link to docs
- [ ] Docker Hub repository link
- [ ] Environment variables explained
- [ ] Troubleshooting section

#### REFLECTION.md (5 Points)
- [ ] Completed reflection document
- [ ] Addresses key experiences
- [ ] Discusses challenges faced
- [ ] Explains technical decisions
- [ ] Describes learning outcomes
- [ ] Professional and thoughtful responses

**Notes**: ___________________

---

## 2. Functionality of BREAD Operations (50 Points)

### Browse - GET /calculations (10 Points)
- [ ] Endpoint returns all user-specific calculations
- [ ] Calculations are properly formatted
- [ ] Pagination support (skip, limit)
- [ ] Only returns logged-in user's calculations
- [ ] Handles empty state gracefully
- [ ] Frontend displays all calculations correctly

**Test Results**: ___________________

---

### Read - GET /calculations/{id} (10 Points)
- [ ] Endpoint retrieves specific calculation by ID
- [ ] Returns 404 if calculation not found
- [ ] Returns 404 if calculation belongs to another user
- [ ] Returns correct calculation details
- [ ] All fields present and accurate
- [ ] Frontend can view calculation details

**Test Results**: ___________________

---

### Edit - PUT/PATCH /calculations/{id} (10 Points)
- [ ] Endpoint updates existing calculation
- [ ] Validates input data
- [ ] Recalculates result correctly
- [ ] Prevents division by zero
- [ ] Returns 404 if calculation not found
- [ ] Returns 400 for invalid input
- [ ] Changes persist in database
- [ ] Frontend edit form works correctly
- [ ] Updated timestamp is updated

**Test Results**: ___________________

---

### Add - POST /calculations (10 Points)
- [ ] Endpoint creates new calculation
- [ ] Validates input (operation, operands)
- [ ] Calculates result correctly for all operations:
  - [ ] Addition
  - [ ] Subtraction
  - [ ] Multiplication
  - [ ] Division
- [ ] Prevents division by zero
- [ ] Associates calculation with logged-in user
- [ ] Returns 400 for invalid input
- [ ] Frontend form works correctly

**Test Results**: ___________________

---

### Delete - DELETE /calculations/{id} (10 Points)
- [ ] Endpoint deletes calculation by ID
- [ ] Returns 404 if calculation not found
- [ ] Returns 404 if calculation belongs to another user
- [ ] Returns 204 on successful deletion
- [ ] Calculation is removed from database
- [ ] Doesn't affect other calculations
- [ ] Frontend delete confirmation works
- [ ] List updates after deletion

**Test Results**: ___________________

---

## 3. Testing Quality (Bonus Points Consideration)

### Positive Scenarios Coverage
- [ ] User registration and login
- [ ] Adding calculations (all operations)
- [ ] Browsing all calculations
- [ ] Reading specific calculation
- [ ] Editing calculations
- [ ] Deleting calculations
- [ ] Form validation working

**Test Count**: _____ positive tests

---

### Negative Scenarios Coverage
- [ ] Registration with duplicate username
- [ ] Login with invalid credentials
- [ ] Division by zero prevented
- [ ] Invalid operation type
- [ ] Unauthorized access attempts
- [ ] Editing to invalid state
- [ ] Invalid input handling

**Test Count**: _____ negative tests

---

### Test Execution
- [ ] All tests pass locally
- [ ] Tests pass in CI/CD pipeline
- [ ] Tests are well-organized
- [ ] Tests have clear descriptions
- [ ] Tests cover edge cases

**Notes**: ___________________

---

## 4. Code Quality (Bonus Points Consideration)

### Backend Code Quality
- [ ] Clean, readable code
- [ ] Proper error handling
- [ ] Input validation
- [ ] Security best practices
- [ ] RESTful API design
- [ ] Appropriate HTTP status codes
- [ ] Database transactions handled correctly

**Notes**: ___________________

---

### Frontend Code Quality
- [ ] Clean, organized JavaScript
- [ ] Proper error handling
- [ ] Client-side validation
- [ ] Good user experience
- [ ] Responsive design
- [ ] Accessibility considerations
- [ ] No console errors

**Notes**: ___________________

---

## 5. CI/CD Implementation (Bonus Points Consideration)

### GitHub Actions Workflow
- [ ] Workflow file is properly configured
- [ ] Tests run automatically on push/PR
- [ ] Docker image builds on success
- [ ] Image pushes to Docker Hub (on main branch)
- [ ] Proper secret management
- [ ] Clear stage separation
- [ ] Error handling and notifications

**Notes**: ___________________

---

## 6. Additional Features (Bonus Points)

List any additional features implemented:
- [ ] ___________________
- [ ] ___________________
- [ ] ___________________

---

## 7. Final Verification

### Local Testing
- [ ] Application runs locally with Docker Compose
- [ ] All features work as expected
- [ ] No errors in console/logs
- [ ] Database operations work correctly

### Repository Check
- [ ] All files committed
- [ ] No sensitive data in repository
- [ ] .gitignore properly configured
- [ ] README is up to date

### Submission Package
- [ ] GitHub repository link
- [ ] Docker Hub link
- [ ] Screenshots folder/files
- [ ] README.md complete
- [ ] REFLECTION.md complete
- [ ] All tests passing

---

## Grading Summary

| Category | Points Possible | Points Earned | Notes |
|----------|----------------|---------------|-------|
| GitHub Repository | 10 | | |
| Required Files | 15 | | |
| Screenshots | 15 | | |
| Documentation | 10 | | |
| Browse Operation | 10 | | |
| Read Operation | 10 | | |
| Edit Operation | 10 | | |
| Add Operation | 10 | | |
| Delete Operation | 10 | | |
| **Total** | **100** | | |

---

## Submission Declaration

I declare that this submission is my own work and that I have properly cited all sources used in this project.

**Student Signature**: ___________________  
**Date**: ___________________

---

## Instructor Use Only

**Graded By**: ___________________  
**Date Graded**: ___________________  
**Total Score**: _____ / 100  
**Comments**:

___________________
___________________
___________________
___________________

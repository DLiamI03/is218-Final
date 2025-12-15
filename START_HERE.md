# START HERE - IS218 Module 14 Project

Welcome! This document will guide you through getting started with your BREAD operations project.

## 🎯 What You Have

A complete FastAPI application with:
- ✅ User authentication (register/login)
- ✅ BREAD operations for calculations (Browse, Read, Edit, Add, Delete)
- ✅ Responsive web interface
- ✅ Comprehensive E2E tests
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Docker containerization

## 🚀 Quick Start (3 Steps)

### Step 1: Test Locally with Docker

Open PowerShell in this directory and run:

```powershell
docker-compose up --build
```

Then open your browser to: **http://localhost:8000**

**Try it out:**
1. Register a new account
2. Login with your credentials
3. Add a calculation (e.g., 10 + 5)
4. See the result (15)
5. Edit or delete the calculation

Press `Ctrl+C` to stop the server when done.

---

### Step 2: Run Tests

In a new PowerShell window:

```powershell
# Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# Run tests
pytest tests/test_e2e.py -v
```

You should see all tests passing! ✅

---

### Step 3: Push to GitHub

1. **Create a GitHub repository:**
   - Go to https://github.com/new
   - Name it: `IS218_M14` or `calculations-bread-api`
   - Make it public
   - Don't initialize with README (we already have one)

2. **Initialize and push:**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: BREAD operations for calculations"
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

3. **Set up GitHub secrets for CI/CD:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add two secrets:
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub token

4. **Watch the magic:**
   - GitHub Actions will automatically run tests
   - If tests pass, it builds and pushes Docker image
   - Check the "Actions" tab to see the workflow

---

## 📋 What to Submit

1. **GitHub Repository URL**
   - Your repository with all code

2. **Docker Hub URL**
   - Your Docker image (e.g., `https://hub.docker.com/r/yourusername/calculations-app`)

3. **Screenshots** (save in `screenshots/` folder):
   - ✅ GitHub Actions workflow showing successful run
   - ✅ Docker Hub showing pushed image
   - ✅ Application functionality:
     - Browse: List of calculations
     - Add: Creating a new calculation
     - Edit: Editing a calculation
     - Delete: Deleting a calculation

4. **Completed Documentation**:
   - ✅ [REFLECTION.md](REFLECTION.md) - Your thoughts and learnings
   - ✅ [README.md](README.md) - Already complete, just add your URLs

---

## 📚 Documentation Guide

### Read These Files:

1. **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Setup completion guide
2. **[QUICK_START.md](QUICK_START.md)** - Quick reference
3. **[README.md](README.md)** - Comprehensive documentation
4. **[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)** - Grading rubric

### Complete This File:

- **[REFLECTION.md](REFLECTION.md)** - Answer all questions about your experience

---

## 🔍 Understanding the Code

### Backend Structure

**[app/main.py](app/main.py)** - Main FastAPI application
- Lines 71-90: User registration and login
- Lines 104-120: **Browse** - Get all calculations
- Lines 123-143: **Read** - Get specific calculation
- Lines 146-180: **Add** - Create new calculation
- Lines 183-229: **Edit** - Update calculation
- Lines 232-254: **Delete** - Remove calculation

**[app/database.py](app/database.py)** - Database models
- Lines 17-26: User model
- Lines 29-42: Calculation model

**[app/schemas.py](app/schemas.py)** - Validation schemas
- Lines 27-47: CalculationBase with validation
- Lines 50-52: CalculationCreate
- Lines 55-67: CalculationUpdate
- Lines 70-78: CalculationResponse

**[app/auth.py](app/auth.py)** - Authentication
- Lines 28-31: Password hashing/verification
- Lines 34-43: JWT token creation
- Lines 58-77: Get current user from token

### Frontend Structure

**[static/index.html](static/index.html)** - HTML structure
- Lines 10-35: Login form
- Lines 38-55: Register form
- Lines 63-97: Calculation form and list

**[static/script.js](static/script.js)** - JavaScript logic
- Lines 85-115: Register handler
- Lines 118-150: Login handler
- Lines 188-217: Load calculations (Browse)
- Lines 220-257: Add/Update calculation
- Lines 260-283: Edit calculation (Read)
- Lines 295-309: Delete calculation

**[static/style.css](static/style.css)** - Styling
- Modern, responsive design with gradient background
- Card-based layout
- Toast notifications for feedback

### Tests

**[tests/test_e2e.py](tests/test_e2e.py)** - E2E tests
- Lines 36-114: Authentication tests (positive & negative)
- Lines 140-171: Add calculation tests
- Lines 190-209: Browse tests
- Lines 211-226: Read tests
- Lines 228-255: Edit tests
- Lines 257-289: Delete tests
- Lines 292-351: User isolation tests

---

## 🎓 Key Features to Demonstrate

### 1. User Authentication
- Secure registration with validation
- JWT-based login
- Password hashing with bcrypt
- Protected endpoints

### 2. BREAD Operations
- **Browse**: Pagination support, user-specific data
- **Read**: Detailed calculation view
- **Edit**: Full validation, recalculation of results
- **Add**: Four operations, division by zero prevention
- **Delete**: Confirmation dialog, cascade handling

### 3. Validation
- Client-side: HTML5 form validation, JavaScript checks
- Server-side: Pydantic schemas, custom validators
- Business logic: Division by zero, operation types

### 4. Testing
- Positive scenarios: Happy path testing
- Negative scenarios: Error handling, edge cases
- User isolation: Security testing

### 5. CI/CD
- Automated testing on every push
- Docker image building
- Deployment to Docker Hub

---

## 🐛 Common Issues & Solutions

### Issue 1: Docker container won't start
**Solution:**
```powershell
docker-compose down -v
docker-compose up --build
```

### Issue 2: Tests fail locally
**Solution:**
```powershell
# Make sure app is running
docker-compose up

# In new terminal
pytest tests/test_e2e.py -v
```

### Issue 3: GitHub Actions failing
**Check:**
- Are Docker Hub secrets set correctly?
- Are tests passing locally?
- Check Actions tab for error logs

### Issue 4: Can't connect to database
**Solution:**
- Check `.env` file has correct DATABASE_URL
- Ensure PostgreSQL is running (Docker Compose handles this)

---

## ✅ Pre-Submission Checklist

Before submitting, verify:

**Functionality:**
- [ ] Application runs locally
- [ ] Can register new user
- [ ] Can login
- [ ] Can add calculation
- [ ] Can view all calculations (Browse)
- [ ] Can edit calculation
- [ ] Can delete calculation
- [ ] Division by zero is prevented
- [ ] Invalid inputs are rejected

**Testing:**
- [ ] All tests pass locally: `pytest -v`
- [ ] E2E tests cover all BREAD operations
- [ ] Tests include positive and negative scenarios

**GitHub:**
- [ ] Code pushed to GitHub
- [ ] Repository is public
- [ ] README has project description
- [ ] REFLECTION.md is completed

**CI/CD:**
- [ ] GitHub Actions workflow exists
- [ ] Docker Hub secrets configured
- [ ] Workflow runs successfully
- [ ] Docker image pushed to Docker Hub

**Documentation:**
- [ ] All screenshots taken
- [ ] REFLECTION.md completed
- [ ] README has repository URLs
- [ ] SUBMISSION_CHECKLIST.md reviewed

---

## 🎯 Grading Breakdown

**Submission Completeness (50 points):**
- GitHub repository link: 10 pts
- Screenshots: 15 pts
- Documentation: 10 pts
- CI/CD working: 15 pts

**BREAD Functionality (50 points):**
- Browse: 10 pts
- Read: 10 pts
- Edit: 10 pts
- Add: 10 pts
- Delete: 10 pts

**Total: 100 points**

---

## 🎉 You're Ready!

Everything is set up and ready to go. Just follow the steps above and you'll have a complete, working project!

**Need help?** Check these files:
- [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) - Detailed setup guide
- [README.md](README.md) - Full documentation
- [QUICK_START.md](QUICK_START.md) - Quick reference

**Good luck! 🚀**

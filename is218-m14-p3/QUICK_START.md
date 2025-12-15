# Quick Start Guide - IS218 Module 14

## Get Started in 5 Minutes! 🚀

### Option 1: Using Docker Compose (Easiest)

1. **Prerequisites**
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Ensure Docker is running

2. **Clone and Start**
   ```bash
   git clone <your-repo-url>
   cd IS218_M14
   docker-compose up --build
   ```

3. **Access the Application**
   - Open browser: `http://localhost:8000`
   - Register a new account
   - Start creating calculations!

### Option 2: Local Development

1. **Prerequisites**
   - Python 3.11+
   - PostgreSQL 15+

2. **Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your database credentials
   
   # Start the application
   uvicorn app.main:app --reload
   ```

3. **Access**
   - Open browser: `http://localhost:8000`

## First Steps

### 1. Register
- Click "Register" on the login page
- Enter username, email, and password
- Click "Register"

### 2. Login
- Enter your credentials
- Click "Login"

### 3. Create Your First Calculation
- Enter first number
- Select operation (add, subtract, multiply, divide)
- Enter second number
- Click "Add Calculation"

### 4. Manage Calculations
- **View**: All calculations displayed automatically
- **Edit**: Click "Edit" button, modify values, click "Update"
- **Delete**: Click "Delete" button, confirm deletion

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# Run all tests
pytest -v

# Run E2E tests
pytest tests/test_e2e.py -v
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Common Issues

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Database Connection Error
- Check if PostgreSQL is running
- Verify DATABASE_URL in .env file

### Docker Issues
```bash
# Clean and rebuild
docker-compose down -v
docker-compose up --build
```

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review the [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- See [REFLECTION.md](REFLECTION.md) for insights

## What's Next?

1. ✅ Complete all BREAD operations
2. ✅ Run and pass all tests
3. ✅ Set up CI/CD pipeline
4. ✅ Push Docker image to Docker Hub
5. ✅ Complete reflection document
6. ✅ Take screenshots
7. ✅ Submit project!

**Happy Coding! 💻**

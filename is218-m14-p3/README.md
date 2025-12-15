# Calculation Manager - BREAD Operations

A full-stack web application built with FastAPI and vanilla JavaScript that implements BREAD (Browse, Read, Edit, Add, Delete) operations for mathematical calculations.

## Features

- ✅ **User Authentication**: Secure registration and login with JWT tokens
- ✅ **BREAD Operations**: Complete CRUD functionality for calculations
  - **Browse**: View all your calculations with pagination
  - **Read**: View detailed information about specific calculations
  - **Edit**: Update existing calculations
  - **Add**: Create new calculations with four operations (add, subtract, multiply, divide)
  - **Delete**: Remove calculations
- ✅ **Real-time Validation**: Client-side and server-side input validation
- ✅ **User Isolation**: Each user can only access their own calculations
- ✅ **Responsive UI**: Modern, clean interface that works on all devices
- ✅ **Comprehensive Testing**: E2E tests with Playwright covering positive and negative scenarios
- ✅ **CI/CD Pipeline**: Automated testing and Docker image deployment

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Authentication**: JWT with OAuth2
- **Testing**: Pytest, Playwright
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js (for Playwright tests)

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd IS218_M14
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application at `http://localhost:8000`

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database and update the `.env` file:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the application at `http://localhost:8000`

## API Documentation

Once the application is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user information

#### Calculations (BREAD)
- `GET /calculations` - Browse all calculations (with pagination)
- `GET /calculations/{id}` - Read a specific calculation
- `POST /calculations` - Add a new calculation
- `PUT /calculations/{id}` - Edit/Update a calculation
- `PATCH /calculations/{id}` - Partially update a calculation
- `DELETE /calculations/{id}` - Delete a calculation

## Running Tests

### Install test dependencies:
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
```

### Run all tests:
```bash
pytest -v
```

### Run E2E tests only:
```bash
pytest tests/test_e2e.py -v
```

### Run tests with headed browser:
```bash
pytest tests/test_e2e.py -v --headed --slowmo 100
```

## Test Coverage

The test suite includes:

### Positive Scenarios ✅
- User registration and login
- Adding calculations with all operations
- Browsing all calculations
- Reading specific calculation details
- Editing calculations
- Deleting calculations
- User isolation (users can only access their own data)

### Negative Scenarios ❌
- Registration with duplicate username/email
- Login with invalid credentials
- Division by zero prevention
- Invalid operation types
- Editing calculations to invalid states
- Unauthorized access attempts

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Test Stage**: Runs all tests including E2E tests
2. **Build Stage**: Builds Docker image if tests pass
3. **Push Stage**: Pushes image to Docker Hub (on main branch)

### Setting up CI/CD

Add these secrets to your GitHub repository:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

## Docker Hub

The Docker image is automatically pushed to Docker Hub on successful builds:
```bash
docker pull <your-dockerhub-username>/calculations-app:latest
```

Run the pulled image:
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  <your-dockerhub-username>/calculations-app:latest
```

## Project Structure

```
IS218_M14/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and BREAD endpoints
│   ├── database.py       # Database models and configuration
│   ├── schemas.py        # Pydantic schemas for validation
│   └── auth.py           # Authentication logic
├── static/
│   ├── index.html        # Main HTML page
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── tests/
│   ├── conftest.py       # Test configuration
│   └── test_e2e.py       # Playwright E2E tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions workflow
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
├── pytest.ini            # Pytest configuration
└── README.md            # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/calculations_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

## Usage Guide

### 1. Register a New Account
- Click "Register" on the login page
- Enter username (min 3 characters), email, and password (min 6 characters)
- Click "Register" button

### 2. Login
- Enter your username and password
- Click "Login" button

### 3. Add a Calculation
- Fill in the first operand
- Select an operation (add, subtract, multiply, divide)
- Fill in the second operand
- Click "Add Calculation"

### 4. View Your Calculations
- All your calculations are displayed in the list
- Shows the expression, result, and timestamps
- Click "Refresh" to reload the list

### 5. Edit a Calculation
- Click the "Edit" button on any calculation
- Modify the values in the form
- Click "Update Calculation"
- Click "Cancel" to abort the edit

### 6. Delete a Calculation
- Click the "Delete" button on any calculation
- Confirm the deletion in the dialog

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL environment variable
- Verify database credentials

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # On Unix/Mac
netstat -ano | findstr :8000  # On Windows

# Kill the process or use a different port
uvicorn app.main:app --port 8001
```

### Docker Issues
```bash
# Clean up Docker
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- FastAPI documentation
- Playwright testing framework
- SQLAlchemy ORM
- Docker containerization platform

## Contact

For questions or support, please open an issue on GitHub.

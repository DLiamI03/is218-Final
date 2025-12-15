# IS218_Last Project Setup

This project was created as a clean starter template based on IS218_M14, with all calculator-specific functionality removed.

## What Was Done

### 1. Copied Base Structure
- Entire IS218_M14 project copied to IS218_Last
- All git repositories removed (no GitHub repo included)

### 2. Calculator Code Removed
The following calculator-specific elements were gutted out:

#### Backend Changes:
- **database.py**: Removed Calculation model and its relationship to User
- **schemas.py**: Removed all calculation-related schemas (CalculationBase, CalculationCreate, CalculationUpdate, CalculationResponse)
- **main.py**: Removed all BREAD endpoints for calculations, left authentication endpoints intact

#### Frontend Changes:
- **index.html**: Replaced calculator form/list with placeholder content
- **script.js**: Removed all calculation-related JavaScript functions, kept authentication

#### Tests:
- **test_e2e.py**: Removed all calculator tests, kept only authentication tests as examples

### 3. Configuration Updates
- **docker-compose.yml**: Changed database name from calculations_db to pp_db
- **database.py**: Updated default DATABASE_URL to use pp_db
- **README.md**: Completely rewritten as a starter template guide

### 4. What Remains Intact
 User authentication system (register/login with JWT)
 Database setup with User model
 Docker & Docker Compose configuration
 Testing framework (Playwright)
 All infrastructure and deployment files
 Static file serving
 Frontend styling (CSS)

## Next Steps

This template is ready for your new project. Add your custom:
1. Database models in pp/database.py
2. API endpoints in pp/main.py
3. Pydantic schemas in pp/schemas.py
4. Frontend UI in static/ directory
5. Tests in 	ests/test_e2e.py

## Files Ready for Customization

- pp/main.py - Line with TODO comment for your endpoints
- pp/database.py - Clean User model ready to extend
- pp/schemas.py - Basic user schemas, add your own
- static/index.html - Placeholder content area
- static/script.js - TODO comments for your JavaScript
- 	ests/test_e2e.py - Authentication tests as examples

## Running the Project

`ash
cd IS218_Last
docker-compose up --build
`

Visit http://localhost:8000 to see the starter template.

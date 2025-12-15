# CI/CD Setup Guide

## GitHub Actions - Required Secrets

To enable the CI/CD pipeline, add these secrets to your GitHub repository:

### How to Add Secrets:
1. Go to your repository: https://github.com/DLiamI03/is218-Final
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each secret below

### Required Secrets:

#### 1. Docker Hub Integration
```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token
```

**How to get Docker Hub credentials:**
- Sign up at https://hub.docker.com
- Username: Your Docker Hub username
- Password: Use an Access Token (recommended over password)
  - Go to Account Settings → Security → New Access Token
  - Name it "GitHub Actions"
  - Copy the token and use as `DOCKER_PASSWORD`

#### 2. OpenAI API Key (Optional but recommended)
```
OPENAI_API_KEY=sk-proj-your-openai-api-key
```

**Why needed:**
- Enables AI features during tests
- Tests will still pass without it (graceful fallback)
- Get from: https://platform.openai.com/api-keys

### Environment Variables in .env (Local Development)

Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Email (Optional - defaults to mock mode)
EMAIL_ENABLED=false
EMAIL_PROVIDER=mock
FROM_EMAIL=noreply@fittrack.app
FRONTEND_URL=http://localhost:8000
```

## CI/CD Pipeline Overview

The pipeline runs automatically on:
- **Push** to `main` or `develop` branches
- **Pull requests** to `main` branch

### Pipeline Stages:

1. **Code Quality** ✅
   - Black (code formatting)
   - isort (import sorting)
   - Flake8 (style guide)
   - Pylint (code analysis)

2. **Automated Tests** ✅
   - Unit tests with pytest
   - Code coverage reporting
   - Minimum 50% coverage required

3. **Security Scan** 🔒
   - Safety (dependency vulnerabilities)
   - Bandit (security issues)

4. **Docker Build & Push** 🐳
   - Builds Docker image
   - Pushes to Docker Hub
   - Tagged with branch name and SHA
   - Only on `main` branch

5. **Integration Tests** 🔗
   - End-to-end tests
   - Browser automation tests
   - Only after Docker build

6. **Deployment Notification** 🚀
   - Success confirmation
   - Docker image location

## Viewing CI/CD Results

1. Go to **Actions** tab in your GitHub repository
2. Click on any workflow run to see details
3. Each job shows pass/fail status
4. Click on individual jobs to see logs

### Quality Gates

The pipeline enforces these quality standards:
- ✅ All tests must pass
- ✅ Code coverage ≥ 50%
- ✅ Pylint score ≥ 7.0/10
- ✅ No critical security issues
- ✅ Docker build succeeds

## Troubleshooting

### Pipeline Fails on Tests
```bash
# Run tests locally first
pytest tests/ -v --cov=app

# Fix any failing tests before pushing
```

### Docker Build Fails
```bash
# Test Docker build locally
docker build -t fittrack:test .
docker run -p 8000:8000 fittrack:test
```

### Missing Secrets Error
- Check all required secrets are added in GitHub
- Secret names must match exactly (case-sensitive)
- Regenerate tokens if expired

### OpenAI Tests Fail
- This is OK if you don't have API key
- Tests have fallback behavior
- Add `OPENAI_API_KEY` secret to enable AI tests

## Email Verification Setup (Optional)

The app includes email verification for new users:

### Mock Mode (Default - for development)
```env
EMAIL_ENABLED=false
EMAIL_PROVIDER=mock
```
- Emails are logged to console
- Verification links printed in logs
- Perfect for testing/demo

### Production Email (Optional)

**SendGrid Setup:**
```env
EMAIL_ENABLED=true
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
```

**Mailgun Setup:**
```env
EMAIL_ENABLED=true
EMAIL_PROVIDER=mailgun
MAILGUN_DOMAIN=yourdomain.com
MAILGUN_API_KEY=your-mailgun-api-key
FROM_EMAIL=noreply@yourdomain.com
```

## Production Deployment

Once CI/CD passes, deploy your Docker image:

```bash
# On your server
docker pull your-dockerhub-username/fittrack:latest
docker-compose up -d
```

## Badge for README

Add this to your README.md to show CI/CD status:

```markdown
![CI/CD Pipeline](https://github.com/DLiamI03/is218-Final/actions/workflows/ci-cd.yml/badge.svg)
![Tests](https://github.com/DLiamI03/is218-Final/actions/workflows/tests.yml/badge.svg)
```

## Demo Tips for Final Presentation

1. **Show GitHub Actions Tab**
   - Display green checkmarks for passing tests
   - Show Docker image was built and pushed
   - Demonstrate automated quality gates

2. **Show Email Verification**
   - Register new user
   - Show verification email in logs
   - Click verification link
   - User is now verified

3. **Show Docker Hub**
   - Display your images at https://hub.docker.com
   - Show tags (latest, main, SHA)
   - Demonstrate CI/CD pushed the image

4. **Highlight Quality Standards**
   - 50%+ test coverage
   - Pylint score ≥ 7.0
   - Automated security scanning
   - All requirements from module14 met

Good luck with your presentation! 🎉

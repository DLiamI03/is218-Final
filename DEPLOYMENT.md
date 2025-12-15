# 🚀 Deployment Guide - Fitness Tracker

Deploy your AI-powered fitness tracker to production using the same DigitalOcean setup from IS218_M14.

## Prerequisites

✅ **From IS218_M14, you should already have:**
- Ubuntu 24.04 VPS (DigitalOcean droplet)
- Docker & Docker Compose installed
- Caddy reverse proxy running
- Domain configured with DNS
- Firewall & security configured
- SSH access set up

## Deployment Steps

### 1. Prepare Environment File

On your server, create `.env.production`:

```bash
# SSH into your server
ssh your-user@your-server-ip

# Navigate to your projects directory
cd ~/projects

# Create project directory
mkdir fittrack
cd fittrack

# Create production environment file
nano .env.production
```

Add these variables (fill in your actual values):

```env
POSTGRES_PASSWORD=your-secure-postgres-password
SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=sk-proj-your-openai-api-key
DOMAIN=fittrack.yourdomain.com
```

Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

### 2. Upload Your Code

**Option A: Using Git (Recommended)**

```bash
# On server
cd ~/projects/fittrack
git clone https://github.com/yourusername/fittrack.git .

# Or if you already have it cloned
git pull origin main
```

**Option B: Using SCP (Direct Upload)**

```powershell
# From your local machine (in IS218_Last directory)
scp -r * your-user@your-server-ip:~/projects/fittrack/
```

### 3. Deploy with Docker Compose

```bash
# On server
cd ~/projects/fittrack

# Build and start containers
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --build

# Check containers are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f web
```

### 4. Update DNS & Caddy

**Add DNS Record (in DigitalOcean or your DNS provider):**
- Type: A
- Name: fittrack (or your subdomain)
- Value: Your server IP
- TTL: 300

**Caddy automatically handles HTTPS** thanks to the labels in docker-compose.prod.yml!

The app will be available at: `https://fittrack.yourdomain.com`

### 5. Initialize Database

```bash
# Run seed data (optional - adds common foods/exercises)
docker-compose -f docker-compose.prod.yml exec web python seed_data.py
```

### 6. Test Your Deployment

1. Visit `https://fittrack.yourdomain.com`
2. Create an account
3. Test AI food parsing
4. Test AI workout parsing
5. Test meal suggestions in Insights tab

## 🔧 Maintenance Commands

### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
```

### Restart Application
```bash
docker-compose -f docker-compose.prod.yml restart web
```

### Update Application
```bash
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

### Database Backup
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres fittrack_db > backup_$(date +%Y%m%d).sql
```

### Database Restore
```bash
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres fittrack_db < backup_20241214.sql
```

## 🛡️ Security Checklist

- ✅ Strong POSTGRES_PASSWORD (not 'postgres')
- ✅ Unique SECRET_KEY generated
- ✅ OpenAI API key kept secure
- ✅ Firewall allows only 22, 80, 443
- ✅ SSH key-based authentication only
- ✅ Regular security updates
- ✅ Fail2ban monitoring SSH
- ✅ HTTPS enabled via Caddy

## 📊 Monitoring

### Check Application Health
```bash
# Check if containers are running
docker-compose -f docker-compose.prod.yml ps

# Check resource usage
docker stats
```

### Check Logs for Errors
```bash
# Web application logs
docker-compose -f docker-compose.prod.yml logs --tail=100 web

# Database logs
docker-compose -f docker-compose.prod.yml logs --tail=100 db
```

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Rebuild
docker-compose -f docker-compose.prod.yml up -d --build --force-recreate
```

### Can't connect to database
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Test connection
docker-compose -f docker-compose.prod.yml exec web python -c "from app.database import engine; print('DB OK')"
```

### AI features not working
```bash
# Check OpenAI API key is set
docker-compose -f docker-compose.prod.yml exec web printenv OPENAI_API_KEY

# Check logs for API errors
docker-compose -f docker-compose.prod.yml logs web | grep -i openai
```

### HTTPS not working
```bash
# Check Caddy logs
docker logs caddy

# Verify DNS points to server
dig fittrack.yourdomain.com

# Restart Caddy
docker restart caddy
```

## 💰 Cost Breakdown

- **DigitalOcean Droplet**: $6-12/month (Basic/Regular)
- **Domain Name**: ~$12/year
- **OpenAI API Usage**: ~$1-5/month (depends on usage)
- **Total**: ~$8-20/month for unlimited users

## 🎯 Production Tips

1. **Monitor OpenAI costs** in their dashboard
2. **Set up daily backups** (cron job)
3. **Monitor disk space** (`df -h`)
4. **Keep Docker images updated** regularly
5. **Review logs weekly** for errors/attacks
6. **Test backups** - restore to staging server

## ✅ You're Live!

Your fitness tracker is now running in production with:
- ✅ Automatic HTTPS
- ✅ AI-powered features
- ✅ Professional domain
- ✅ Secure authentication
- ✅ Production database
- ✅ Docker containerization

Share your deployed app: `https://fittrack.yourdomain.com` 🎉

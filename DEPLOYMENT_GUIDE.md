# Deployment Guide - Making Your Project Live

**Goal:** Share your Investment Diligence Engine with the world  
**Options:** Local sharing, Cloud deployment, Enterprise hosting

---

## 🎯 Choose Your Deployment Strategy

| Option | Best For | Time | Cost | Access |
|--------|----------|------|------|--------|
| **Local Demo** | Reviewers, testing | 0 min | FREE | On your machine |
| **Streamlit Cloud** | Public demo, portfolio | 10 min | FREE | Public URL |
| **Heroku** | Production prototype | 20 min | FREE-$7/mo | Public URL |
| **AWS/Azure** | Enterprise deployment | 2-4 hrs | $20-100/mo | Custom domain |

---

## ✅ PRE-DEPLOYMENT CHECKLIST

Before deploying anywhere, verify:

```powershell
# 1. Test locally first
streamlit run app.py
# Should open at http://localhost:8501

# 2. Run test suite
python test_system.py
# Should show: 8/8 tests passing

# 3. Try analyzing a stock
python analyze.py AAPL
# Should complete in 15-30 seconds

# 4. Check API keys work
python test_claude_api.py
# Should connect successfully
```

**✅ All working?** Proceed to deployment!

---

## 🚀 OPTION 1: Local Demo (Immediate)

**Best for:** Showing to reviewers, internal testing

### **Share Project Folder**

**Steps:**
1. **Create clean copy:**
```powershell
# Remove cache and temporary files
Remove-Item -Recurse -Force .tmp\*

# Remove sensitive data
Remove-Item .env

# Create zip file
Compress-Archive -Path * -DestinationPath Investment_Engine.zip
```

2. **Send to reviewer with instructions:**
```
Subject: Investment Diligence Engine - Ready for Review

Attached: Investment_Engine.zip

Setup (5 minutes):
1. Extract zip file
2. Install Python dependencies: pip install -r requirements.txt
3. Create .env file with your API keys:
   ANTHROPIC_API_KEY=sk-ant-xxx
   NEWSAPI_KEY=xxx
4. Run: streamlit run app.py
5. Open: http://localhost:8501

Test:
- Select AAPL from dropdown
- Click "Analyze AAPL"
- Wait 30 seconds
- Review results

Questions? Reply to this email.
```

**Pros:**
- ✅ Immediate (no deployment needed)
- ✅ Full control
- ✅ No hosting costs

**Cons:**
- ❌ Requires Python on their machine
- ❌ They need API keys
- ❌ Not accessible 24/7

---

## 🌐 OPTION 2: Streamlit Cloud (10 Minutes)

**Best for:** Public portfolio, demo for interviews, sharing with anyone

### **Step-by-Step Deployment**

#### **Step 1: Create GitHub Repository**

```powershell
# 1. Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - Investment Diligence Engine"

# 2. Create repo on GitHub
# Go to: https://github.com/new
# Name: investment-diligence-engine
# Visibility: Public (or Private)

# 3. Push code
git remote add origin https://github.com/YOUR_USERNAME/investment-diligence-engine.git
git branch -M main
git push -u origin main
```

#### **Step 2: Deploy to Streamlit Cloud**

1. **Go to:** https://streamlit.io/cloud
2. **Sign in** with GitHub account
3. **Click:** "New app"
4. **Configure:**
   - Repository: `YOUR_USERNAME/investment-diligence-engine`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `investment-engine` (or your choice)

5. **Add secrets** (API keys):
   - Click "Advanced settings"
   - Paste in secrets box:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-xxx"
   NEWSAPI_KEY = "xxx"
   ```

6. **Click:** "Deploy!"

#### **Step 3: Wait for Deployment** (2-3 minutes)

You'll see:
```
🚀 Building app...
📦 Installing dependencies...
✅ App deployed successfully!
```

#### **Step 4: Get Your Public URL**

```
Your app is live at:
https://investment-engine.streamlit.app

Share this URL with anyone!
```

### **Streamlit Cloud Features**

✅ **FREE tier includes:**
- 1 GB storage
- Unlimited viewers
- Auto-deploy on git push
- HTTPS encryption
- Custom subdomain

✅ **Automatic updates:**
```powershell
# Make changes locally
git add .
git commit -m "Updated stock list"
git push

# Streamlit Cloud auto-deploys in ~2 minutes!
```

### **Troubleshooting**

**Issue: App keeps crashing**
```toml
# Add to .streamlit/config.toml (create if missing)
[server]
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

**Issue: Secrets not loading**
```python
# In app.py, add at top:
import os
from dotenv import load_dotenv

# Try environment variables if secrets.toml fails
if "ANTHROPIC_API_KEY" not in os.environ:
    load_dotenv()
```

---

## ⚙️ OPTION 3: Heroku (20 Minutes)

**Best for:** Production prototype with custom domain

### **Prerequisites**

```powershell
# Install Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
choco install heroku-cli

# Verify installation
heroku --version
```

### **Deployment Steps**

#### **Step 1: Prepare Project**

**Create Procfile:**
```powershell
# Create Procfile (no extension!)
@"
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
"@ | Out-File -Encoding ASCII Procfile
```

**Create runtime.txt:**
```powershell
# Specify Python version
"python-3.11.0" | Out-File -Encoding ASCII runtime.txt
```

**Update requirements.txt:**
```powershell
# Ensure these are included
@"
streamlit>=1.28.0
yfinance>=0.2.28
anthropic>=0.25.0
requests>=2.31.0
python-dotenv>=1.0.0
"@ | Out-File -Encoding ASCII requirements.txt
```

#### **Step 2: Deploy to Heroku**

```powershell
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create investment-diligence-engine

# 3. Set API keys as environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxx
heroku config:set NEWSAPI_KEY=xxx
heroku config:set CACHE_TTL=3600

# 4. Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# 5. Open app
heroku open
```

#### **Step 3: Monitor & Scale**

```powershell
# View logs
heroku logs --tail

# Scale (if needed)
heroku ps:scale web=1

# Check status
heroku ps
```

### **Heroku Pricing**

| Tier | Cost | Features |
|------|------|----------|
| Free | $0 | 550 dyno hours/month, sleeps after 30min idle |
| Hobby | $7/mo | Always-on, custom domain |
| Basic | $25/mo | More memory, better performance |

### **Custom Domain**

```powershell
# Add your domain
heroku domains:add www.yourcompany.com

# Get DNS target
heroku domains

# Update DNS:
# CNAME: www → shiny-grass-123.herokudns.com
```

---

## ☁️ OPTION 4: AWS/Azure (Enterprise)

**Best for:** Production deployment with full control

### **AWS Elastic Beanstalk**

**Quick setup:**
```powershell
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize
eb init -p python-3.11 investment-engine

# 3. Create environment
eb create investment-engine-prod

# 4. Set environment variables
eb setenv ANTHROPIC_API_KEY=xxx NEWSAPI_KEY=xxx

# 5. Deploy
eb deploy

# 6. Open
eb open
```

**Cost:** ~$20-50/month (t3.medium instance)

### **Azure App Service**

**Quick setup:**
```powershell
# 1. Install Azure CLI
# Windows: https://aka.ms/installazurecliwindows

# 2. Login
az login

# 3. Create resource group
az group create --name InvestmentEngine --location eastus

# 4. Create app service plan
az appservice plan create --name InvestmentEnginePlan --resource-group InvestmentEngine --sku B1

# 5. Create web app
az webapp create --name investment-engine-app --resource-group InvestmentEngine --plan InvestmentEnginePlan --runtime "PYTHON|3.11"

# 6. Set environment variables
az webapp config appsettings set --name investment-engine-app --resource-group InvestmentEngine --settings ANTHROPIC_API_KEY=xxx NEWSAPI_KEY=xxx

# 7. Deploy from GitHub
az webapp deployment source config --name investment-engine-app --resource-group InvestmentEngine --repo-url https://github.com/YOUR_USERNAME/investment-diligence-engine --branch main

# 8. Open
az webapp browse --name investment-engine-app --resource-group InvestmentEngine
```

**Cost:** ~$13-55/month (B1-S1 tier)

---

## 🐳 OPTION 5: Docker (Advanced)

**Best for:** Containerized deployment anywhere

### **Create Dockerfile**

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Build & Run**

```powershell
# Build image
docker build -t investment-engine .

# Run locally
docker run -p 8501:8501 `
  -e ANTHROPIC_API_KEY=xxx `
  -e NEWSAPI_KEY=xxx `
  investment-engine

# Push to Docker Hub
docker tag investment-engine YOUR_USERNAME/investment-engine
docker push YOUR_USERNAME/investment-engine

# Deploy anywhere (AWS ECS, Azure ACI, etc.)
```

---

## 📊 POST-DEPLOYMENT CHECKLIST

After deployment, verify:

### **Functionality Test**

```
✅ App loads without errors
✅ Stock dropdown appears
✅ Can select a stock (e.g., AAPL)
✅ "Analyze" button works
✅ Analysis completes in 15-30 seconds
✅ Results display correctly
✅ Color coding works (green/yellow/red)
✅ Multiple stocks can be analyzed
```

### **Performance Test**

```
✅ Page load time < 3 seconds
✅ Analysis time < 30 seconds
✅ No memory leaks (check after 10+ analyses)
✅ Handles concurrent users (if applicable)
```

### **Security Test**

```
✅ API keys not exposed in client
✅ HTTPS enabled (Streamlit Cloud auto)
✅ No sensitive data in logs
✅ .env file not committed to git
```

---

## 🎯 RECOMMENDED APPROACH

**For this project, I recommend:**

### **Phase 1: Local Demo (Now)**
- Share zip file with reviewers
- Quick feedback loop
- No deployment complexity

### **Phase 2: Streamlit Cloud (Week 1)**
- Deploy to public URL
- Add to portfolio/resume
- Show in interviews
- **TIME: 10 minutes**
- **COST: FREE**

### **Phase 3: Production (If adopted)**
- Move to AWS/Azure
- Add monitoring, analytics
- Scale as needed

---

## 🔗 SHAREABLE LINKS

After deploying to Streamlit Cloud, create a landing page:

**Example README for GitHub:**
```markdown
# Investment Diligence Engine

🚀 **Live Demo:** https://investment-engine.streamlit.app

AI-powered stock analysis in 30 seconds.

### Features
- Financial health (Altman Z-Score)
- News sentiment (100 articles)
- AI recommendation (Claude)

### Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Tech Stack
- Python 3.11
- Streamlit
- Claude AI
- yfinance, NewsAPI
```

**Share on LinkedIn:**
```
🚀 Excited to share my latest project: Investment Diligence Engine

Compresses stock research from days to 30 seconds using:
✅ Real-time financial data
✅ AI-powered risk analysis
✅ Automated report generation

Try it live: https://investment-engine.streamlit.app

Built with: Python, Streamlit, Claude AI, WAT Framework

#AI #FinTech #Python #DataScience
```

---

## 📞 SUPPORT

### **If deployment fails:**

1. **Check logs:**
```powershell
# Streamlit Cloud: View "Logs" tab in dashboard
# Heroku: heroku logs --tail
# AWS: eb logs
```

2. **Common issues:**
- Missing dependencies → Update requirements.txt
- API key errors → Check environment variables
- Port conflicts → Use $PORT variable
- Memory limits → Upgrade plan or optimize code

3. **Get help:**
- Streamlit Community: https://discuss.streamlit.io
- Heroku Support: https://help.heroku.com
- AWS Support: https://console.aws.amazon.com/support

---

## 🎓 BEST PRACTICES

### **Before Going Live**

```
✅ Test with 10+ stocks
✅ Add error handling for API failures
✅ Set up monitoring/alerts
✅ Document known limitations
✅ Add usage analytics (optional)
✅ Create backup/restore plan
```

### **After Going Live**

```
✅ Monitor daily for errors
✅ Check API usage/costs
✅ Gather user feedback
✅ Update documentation
✅ Plan feature roadmap
```

---

## 🏆 SUCCESS CRITERIA

**You'll know deployment succeeded when:**

1. ✅ Public URL loads instantly
2. ✅ Anyone can analyze stocks (no setup required)
3. ✅ Results appear in <30 seconds
4. ✅ No errors in production logs
5. ✅ Users give positive feedback

**Example success:**
- 100+ unique visitors in Week 1
- 500+ stock analyses run
- Added to 10+ portfolios
- Positive comments on LinkedIn

---

## 🚀 GO LIVE NOW!

**Fastest path to production:**

```powershell
# 1. Push to GitHub (5 min)
git init
git add .
git commit -m "Initial commit"
gh repo create investment-diligence-engine --public --push

# 2. Deploy to Streamlit Cloud (5 min)
# Visit: https://streamlit.io/cloud
# Connect repo, add secrets, deploy

# 3. Share! (1 min)
# Post on LinkedIn with live URL
```

**Total time: 11 minutes to go live! 🎉**

---

**Ready to deploy?** Choose your option above and follow the steps!

**Questions?** Check troubleshooting section or contact support.

**Good luck! 🚀**

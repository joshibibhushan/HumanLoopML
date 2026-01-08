# Deploy Backend to Render - Step by Step Guide

This guide will walk you through deploying the HumanLoopML FastAPI backend to Render.

## Prerequisites

✅ Render account created  
✅ GitHub repository with your code pushed  
✅ Baseline model trained (`models/model_v1.joblib` exists)

---

## Step 1: Prepare Your Repository

### 1.1 Push Code to GitHub

Make sure all your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 1.2 Verify Model Files

Your `models/` folder should contain:
- `model_v1.joblib`
- `vectorizer_v1.joblib`
- `label_names.json`

**Important**: These files need to be in your repository for Render to access them. If they're in `.gitignore`, temporarily remove them from gitignore or commit them.

---

## Step 2: Create Web Service on Render

### 2.1 Navigate to Render Dashboard

1. Go to [render.com](https://render.com) and log in
2. Click **"+ New"** button (top right)
3. Select **"Web Service"** from the service types

### 2.2 Connect GitHub Repository

1. **Connect Repository**:
   - If first time: Click "Connect GitHub" and authorize Render
   - Select your repository: `HumanLoopML` (or your repo name)
   - Click **"Connect"**

### 2.3 Configure Service Settings

Fill in the following:

**Basic Settings:**
- **Name**: `humanloopml-api` (or any name you prefer)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master`)
- **Root Directory**: Leave empty (or set to `.` if needed)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r api/requirements.txt
  ```
- **Start Command**: 
  ```
  cd api && uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Environment Variables:**
Click **"Add Environment Variable"**:
- **Key**: `PORT`
- **Value**: `10000`

**Plan:**
- Select **"Free"** plan (or upgrade if needed)

### 2.4 Create Service

Click **"Create Web Service"** at the bottom.

---

## Step 3: Wait for Deployment

Render will:
1. Clone your repository
2. Install dependencies (`pip install -r api/requirements.txt`)
3. Start the service
4. Provide a URL like: `https://humanloopml-api.onrender.com`

⏱️ **First deployment takes 5-10 minutes**

You can watch the logs in real-time on the Render dashboard.

---

## Step 4: Verify Deployment

### 4.1 Check Service Status

Once deployed, you should see:
- ✅ Status: **"Live"**
- 🌐 URL: `https://your-service-name.onrender.com`

### 4.2 Test the API

Open these URLs in your browser:

1. **API Root**: `https://your-service-name.onrender.com/`
   - Should show API info

2. **Health Check**: `https://your-service-name.onrender.com/health`
   - Should return: `{"status":"healthy","model_loaded":true,...}`

3. **API Docs**: `https://your-service-name.onrender.com/docs`
   - Should show Swagger UI with all endpoints

4. **Test Prediction** (using curl or browser):
   ```
   https://your-service-name.onrender.com/predict
   ```
   Use the Swagger UI at `/docs` to test the `/predict` endpoint.

---

## Step 5: Update Frontend

### 5.1 Update API URL

Edit `frontend/app.js`:

```javascript
// Change this line:
const API_BASE_URL = 'http://localhost:8000';

// To your Render URL:
const API_BASE_URL = 'https://your-service-name.onrender.com';
```

### 5.2 Test Locally

1. Open `frontend/index.html` in your browser
2. Make a prediction
3. It should connect to your Render backend!

---

## Step 6: Deploy Frontend (GitHub Pages)

### Option A: Use frontend folder directly

1. Push updated `frontend/app.js` to GitHub
2. Go to GitHub repo → **Settings** → **Pages**
3. **Source**: Deploy from a branch
4. **Branch**: `main` (or `master`)
5. **Folder**: `/frontend`
6. Your site: `https://username.github.io/humanloopml/`

### Option B: Copy to docs folder

1. Copy `frontend/` contents to `docs/`
2. Push to GitHub
3. In GitHub Pages settings, select folder: `/docs`

---

## Troubleshooting

### ❌ Build Fails: "No module named 'fastapi'"

**Solution**: Check that `api/requirements.txt` exists and has all dependencies.

### ❌ Service Crashes: "Model not found"

**Solution**: 
1. Make sure model files are committed to Git
2. Check that `models/model_v1.joblib` exists in your repo
3. Verify the path in `api/main.py` is correct

### ❌ Service Crashes: "Port already in use"

**Solution**: The `$PORT` environment variable should be set. Make sure you added:
- Key: `PORT`
- Value: `10000`

### ❌ Cold Start Delay

**Issue**: First request after inactivity takes 30-60 seconds.

**Solution**: 
- This is normal on Render free tier (spins down after 15 min)
- Consider upgrading to paid plan for always-on
- Or use a service like UptimeRobot to ping your service every 5 minutes

### ❌ CORS Errors

**Solution**: The backend is configured to allow all origins. If you see CORS errors:
1. Check backend is running
2. Verify frontend URL is correct
3. Check browser console for exact error

### ❌ Model Files Too Large for Git

**Solution**: 
1. Use Git LFS: `git lfs track "*.joblib"`
2. Or upload models to cloud storage and download on startup
3. Or include models in deployment (they're ~50MB, usually fine)

---

## Advanced: Using render.yaml

You can also use the `render.yaml` file for infrastructure-as-code:

1. The `render.yaml` file is already in your repo
2. In Render dashboard, go to **"Infrastructure as Code"**
3. Select your repository
4. Render will read `render.yaml` and create services automatically

---

## Monitoring & Logs

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. See real-time logs and errors

### Monitor Performance

- **Metrics** tab shows:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

---

## Updating Your Deployment

### After Code Changes

1. Push changes to GitHub
2. Render automatically detects changes
3. Triggers new deployment
4. Usually takes 2-5 minutes

### After Model Retraining

1. Retrain locally: `py training/retrain_with_feedback.py`
2. Commit new model files: `git add models/ && git commit -m "Updated model"`
3. Push to GitHub: `git push`
4. Render will redeploy automatically

---

## Cost

**Free Tier Includes:**
- 750 hours/month (enough for 24/7)
- 512MB RAM
- Spins down after 15 min inactivity (cold start ~30s)

**Upgrade If:**
- You need always-on (no cold starts)
- More RAM for larger models
- Higher request limits

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Update frontend `API_BASE_URL`
3. ✅ Deploy frontend to GitHub Pages
4. ✅ Test end-to-end
5. 🎉 Share your demo!

---

## Quick Reference

**Backend URL**: `https://your-service-name.onrender.com`  
**Frontend URL**: `https://username.github.io/humanloopml/`  
**API Docs**: `https://your-service-name.onrender.com/docs`  
**Health Check**: `https://your-service-name.onrender.com/health`

---

**Need Help?** Check the main [README.md](README.md) or [docs/architecture.md](docs/architecture.md) for more details.

# Connecting Frontend (GitHub Pages) to Backend (Render)

## Quick Setup

### Step 1: Get Your Render Backend URL

1. Go to your Render dashboard
2. Find your web service (e.g., `humanloopml-api`)
3. Copy the URL (e.g., `https://humanloopml-api.onrender.com`)

### Step 2: Update Frontend Configuration

Edit `docs/app.js` and change line 4:

```javascript
// Change from:
const API_BASE_URL = 'http://localhost:8000';

// To your Render URL:
const API_BASE_URL = 'https://your-render-app.onrender.com';
```

### Step 3: Commit and Push

```bash
git add docs/app.js
git commit -m "Update API URL to Render backend"
git push origin main
```

GitHub Pages will automatically update in 1-2 minutes.

---

## Security Considerations

### ✅ Current Setup (Safe for Demo)

**What's Public:**
- Frontend code (HTML/CSS/JS) - ✅ Normal for public demos
- Backend API URL - ✅ Normal for public APIs
- API endpoints - ✅ Designed to be public

**What's Protected:**
- ✅ CORS restricts which domains can call your API
- ✅ Backend validates all inputs
- ✅ No sensitive data exposed

### 🔒 For Production (If Needed)

If you want additional security:

1. **Add API Key Authentication:**
   - Generate API keys
   - Store in environment variables on Render
   - Validate keys in FastAPI middleware

2. **Rate Limiting:**
   - Add rate limiting to prevent abuse
   - Use `slowapi` or similar

3. **Restrict CORS Further:**
   - Only allow your specific GitHub Pages domain
   - Remove localhost in production

---

## Testing the Connection

1. Open: https://joshibibhushan.github.io/HumanLoopML/
2. Open browser console (F12)
3. Enter text and click "Predict"
4. Check console for any errors
5. If you see CORS errors, verify your Render URL is correct

---

## Troubleshooting

### ❌ CORS Error

**Error**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution**: 
1. Verify Render backend is running
2. Check CORS settings in `api/main.py`
3. Make sure your GitHub Pages URL is in `allow_origins`

### ❌ Connection Refused

**Error**: `Failed to fetch` or `Network error`

**Solution**:
1. Check Render service is "Live"
2. Test backend directly: `https://your-app.onrender.com/health`
3. Verify API_BASE_URL in `docs/app.js` is correct

### ❌ Cold Start Delay

**Issue**: First request takes 30-60 seconds

**Solution**: 
- Normal on Render free tier (spins down after 15 min)
- Subsequent requests are fast
- Consider upgrading for always-on

---

## Current Configuration

**Frontend**: https://joshibibhushan.github.io/HumanLoopML/  
**Backend**: `https://your-render-app.onrender.com` (update this!)  
**CORS**: Allows requests from `joshibibhushan.github.io`

---

## Next Steps

1. ✅ Update `API_BASE_URL` in `docs/app.js`
2. ✅ Commit and push to GitHub
3. ✅ Wait for GitHub Pages to rebuild (1-2 min)
4. ✅ Test the connection
5. 🎉 Your demo is live!

# 🚀 Deployment Guide: Render + Vercel

This guide walks you through deploying your Customer Support application to production.

## 📋 Prerequisites

1. **GitHub Account** - Your repo is already at: https://github.com/Atharvasayyyy/Chat_bot-of-CS
2. **Render Account** - Sign up at https://render.com (free tier available)
3. **Vercel Account** - Sign up at https://vercel.com (free tier available)
4. **SendGrid Account** - Already configured (API key needed for Render)
5. **PostgreSQL Database** - Render will provide this automatically

---

## 🔧 Step 1: Deploy Backend to Render

### 1.1 Create a PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **New +** → **PostgreSQL**
3. Fill in:
   - **Name:** `customer-support-db`
   - **Database:** `customer_support_db`
   - **User:** `postgres` (or your preferred name)
   - Leave **Region** as default
   - **Datadog API Key:** Skip (optional)
4. Click **Create Database**
5. ⏳ Wait 2-3 minutes for the database to be ready
6. Copy the **Internal Database URL** (you'll need this)

### 1.2 Deploy FastAPI Backend

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Select **Deploy existing code from a Git repository**
4. Authorize GitHub and select: `Atharvasayyyy/Chat_bot-of-CS`
5. Fill in the form:
   - **Name:** `customer-support-api`
   - **Region:** Choose closest to you (or default)
   - **Branch:** `main`
   - **Runtime:** `Docker`
   - **Dockerfile Path:** `Backend/Dockerfile`
   - **Plan:** Free (or Pro for better performance)

6. Click **Advanced** to add **Environment Variables:**

   ```
   DB_HOST=        → From Database Internal URL (host part)
   DB_PORT=5432    → PostgreSQL default port
   DB_NAME=customer_support_db
   DB_USER=postgres
   DB_PASSWORD=    → From Database Internal URL (password part)
   SENDGRID_API_KEY=SG.xxxxxxxxx  → Your SendGrid API key
   FRONTEND_URL=   → Leave blank for now, update after Vercel deployment
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ENVIRONMENT=production
   ```

7. Click **Create Web Service**
8. ⏳ Wait for deployment (5-10 minutes)
9. 📝 **Copy your backend URL** - Will look like: `https://customer-support-api.onrender.com`

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Project

1. Go to https://vercel.com/dashboard
2. Click **Add New** → **Project**
3. Click **Import Git Repository**
4. Select: `Atharvasayyyy/Chat_bot-of-CS`
5. Fill in:
   - **Project Name:** `customer-support-ui`
   - **Framework Preset:** `Vite`
   - **Root Directory:** `./Frontend/support-ui`

6. Click **Environment Variables** and add:

   ```
   VITE_API_BASE_URL = https://your-backend-render.onrender.com
   ```

   (Replace with your actual backend URL from Step 1.2)

7. Click **Deploy**
8. ⏳ Wait for deployment (2-3 minutes)
9. 📝 **Copy your frontend URL** - Will look like: `https://customer-support-ui.vercel.app`

---

## 🔗 Step 3: Connect Backend ↔ Frontend

### 3.1 Update Render Backend with Frontend URL

1. Go back to Render dashboard
2. Click on your `customer-support-api` service
3. Go to **Environment** tab
4. Edit the `FRONTEND_URL` variable:
   ```
   FRONTEND_URL=https://your-frontend-url.vercel.app
   ```
5. Click **Save Changes**
6. Your backend will auto-redeploy ✅

### 3.2 Verify CORS Configuration

Test that your frontend can reach the backend:

1. Open your Vercel frontend URL
2. Fill in the chat form and test the API call
3. Check Render logs for any errors: Dashboard → Your Service → Logs

---

## 📊 Step 4: Database Connection String

To extract database credentials from Render:

1. Go to Render Dashboard → **PostgreSQL** service
2. Find the **Internal Database URL**:
   ```
   postgresql://user:password@hostname:5432/dbname
   ```
3. Extract each part:
   - `DB_HOST` = `hostname`
   - `DB_USER` = `user`
   - `DB_PASSWORD` = `password`
   - `DB_NAME` = `dbname`
   - `DB_PORT` = `5432`

---

## 🔑 Step 5: Environment Variables Summary

### Backend (Render):

```
DB_HOST=<database-host>
DB_PORT=5432
DB_NAME=customer_support_db
DB_USER=postgres
DB_PASSWORD=<database-password>
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
FRONTEND_URL=https://your-frontend-url.vercel.app
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://your-frontend-url.vercel.app
ENVIRONMENT=production
```

### Frontend (Vercel):

```
VITE_API_BASE_URL=https://your-backend-render.onrender.com
```

---

## 🧪 Testing Your Deployment

1. **Frontend URL:** Open https://your-frontend-url.vercel.app
2. **Landing Page:** You should see the landing page with logo, Request Demo button
3. **Request Demo:** Click button → Should show chat interface
4. **Test Chat:** Enter a user ID and try to submit a message
5. **Check Backend Logs:** Render Dashboard → Your Service → Logs (should show activity)

---

## 🚨 Troubleshooting

### Frontend shows "Cannot reach backend"

- ✅ Check `VITE_API_BASE_URL` in Vercel environment variables
- ✅ Verify Render backend is running (check Render logs)
- ✅ Ensure CORS is configured correctly in `Backend/main.py`

### Database connection errors

- ✅ Verify `DB_HOST`, `DB_USER`, `DB_PASSWORD` are correct
- ✅ Check database is still running on Render
- ✅ Make sure port `5432` is open (Render handles this automatically)

### "SENDGRID_API_KEY" not found

- ✅ Go to Render → Your Service → Environment
- ✅ Add/update the `SENDGRID_API_KEY` variable
- ✅ Redeploy the service

### Build fails on Vercel

- ✅ Check Vercel build logs for details
- ✅ Verify `vite.config.js` is present in `Frontend/support-ui/`
- ✅ Ensure all npm dependencies are installed locally first

---

## 📝 Files Created for Deployment

- **Backend:**
  - `Backend/requirements.txt` - Python dependencies
   - `Backend/render.yaml` - Render configuration
   - `Backend/Dockerfile` - Forces Python 3.11 for a wheel-based build
  - `Backend/.env.example` - Environment variables template
  - Updated `Backend/main.py` - CORS configuration

- **Frontend:**
  - `Frontend/support-ui/vercel.json` - Vercel configuration
  - `Frontend/support-ui/.env.example` - Already exists

---

## ✅ Checklist

- [ ] Render PostgreSQL database created
- [ ] Render backend deployed with all env vars
- [ ] Backend URL copied
- [ ] Vercel frontend deployed with backend URL
- [ ] Frontend URL copied
- [ ] Render backend updated with frontend URL
- [ ] CORS test passed
- [ ] Landing page loads
- [ ] Chat form functional
- [ ] Backend receives requests (check logs)

---

## 🎉 Success!

Your application is now live!

- **Frontend:** https://your-frontend-url.vercel.app
- **Backend API:** https://your-backend-api.onrender.com
- **Database:** Managed by Render PostgreSQL

Happy coding! 🚀

# 🚀 PATH B: Netlify + Railway Deployment Guide

## Overview

This guide deploys your multiplayer game across **two services**:

| Service | What It Does | Cost |
|---------|------------|------|
| **Netlify** | Hosts your static game files (HTML/CSS/JS) | Free |
| **Railway** | Runs your Python WebSocket server 24/7 | Free tier available |

Result: **Multiplayer works from anywhere on the internet!** 🌍

---

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Browser 1  │────────>│   Netlify    │<────────│  Browser 2  │
│  (Player 1) │ HTTPS   │ (Static Site)│ HTTPS   │  (Player 2) │
│             │<────────│              │────────>│             │
└─────────────┘         └──────────────┘         └─────────────┘
      ↓                         ↓                       ↓
      └─────────────────┬───────┴───────┬───────────────┘
                        │               │
                  [Both connect via WebSocket]
                        ↓               ↓
                  ┌──────────────────────────┐
                  │  Railway (Python Server) │
                  │  wss://yourapp.railway   │
                  └──────────────────────────┘
```

---

## Part A: Deploy Static Site to Netlify

### Step 1: Push Code to GitHub

```bash
# Navigate to your project folder
cd /path/to/csgame2-ready

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "CS Game 2 - Ready for deployment"

# Add GitHub remote (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/csgame2.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Netlify

1. **Go to netlify.com**
   - Sign up (use GitHub login)

2. **Click "Add new site"**
   - Click "Import an existing project"

3. **Select GitHub**
   - Click "Authorize Netlify"
   - Authorize and log in

4. **Select Your Repository**
   - Search for "csgame2"
   - Click to select it

5. **Configure Build Settings**
   - **Build command:** `npm run build`
   - **Publish directory:** (leave blank or `.`)
   - Click **"Deploy site"**

6. **Wait for Deploy**
   - Should complete in 2-3 minutes
   - You'll get a URL like: `https://yoursite.netlify.app`

7. **Test Static Site**
   - Visit your Netlify URL
   - Game should load (but multiplayer won't work yet - need Railway server)

✅ **Static site is now live!**

---

## Part B: Deploy Python Server to Railway

### Step 1: Create Railway Account

1. **Go to railway.app**
   - Click "Sign up"
   - Use GitHub login (easier)
   - Authorize Railway

2. **Create New Project**
   - Click "New Project"
   - Click "Deploy from GitHub"

### Step 2: Connect Your GitHub Repository

1. **Select Your Repository**
   - Search for "csgame2"
   - Click to select

2. **Authorize Railway**
   - Click "Authorize Railway-App"
   - Confirm

### Step 3: Configure Railway

1. **Railway Auto-Detects Python**
   - It should detect `requirements.txt`
   - Click "Deploy"

2. **Wait for Deployment**
   - Watch the build logs
   - Should complete in 1-2 minutes

3. **Get Your Railway URL**
   - Go to "Settings"
   - Find "Domain"
   - Copy the domain (looks like `yourapp-production.up.railway.app`)

✅ **Python server is now running in cloud!**

---

## Part C: Connect Game to Railway Server

### Step 1: Update network.js

In your local copy of `js/network.js`, find this function:

```javascript
function getWebSocketUrl() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  
  // Check if running locally
  if (location.hostname === '127.0.0.1' || 
      location.hostname === 'localhost' || 
      location.hostname === '') {
    return proto + '://localhost:8081/ws';
  }
  
  // For Netlify deployment, use the same domain
  return proto + '://' + location.host + '/.netlify/functions/index/ws';
}
```

**Replace with:**

```javascript
function getWebSocketUrl() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  
  // Check if running locally
  if (location.hostname === '127.0.0.1' || 
      location.hostname === 'localhost' || 
      location.hostname === '') {
    return proto + '://localhost:8081/ws';
  }
  
  // For production, connect to Railway server
  // Replace YOUR-APP-NAME with your actual Railway app name
  return 'wss://YOUR-APP-NAME-production.up.railway.app/ws';
}
```

### Step 2: Get Your Railway App Name

1. **Go to Railway dashboard**
2. **Click your project**
3. **Look for the domain** (example: `awesome-game-production.up.railway.app`)
4. **Replace `YOUR-APP-NAME`** with your actual name

**Example:**
```javascript
return 'wss://awesome-game-production.up.railway.app/ws';
```

### Step 3: Push Updated Code

```bash
git add js/network.js
git commit -m "Connect to Railway WebSocket server"
git push origin main
```

### Step 4: Redeploy on Netlify

1. **Go to netlify.com**
2. **Click your site**
3. **Click "Deploys"**
4. **Click "Trigger deploy"**
5. Wait for ✅ **Deploy complete**

---

## ✅ Testing Your Game

### Local Testing (Before Deployment)

```bash
# Terminal 1: Run Python server
python api/index.py

# Terminal 2: Run HTTP server
python -m http.server 8000

# Browser: http://localhost:8000
```

Open 2 browser windows:
- Window 1: Click "Online" (becomes Player 1)
- Window 2: Click "Online" (becomes Player 2)
- Should auto-connect and game starts! ✓

### Live Testing (After Deployment)

1. **Visit your Netlify URL**
   - Example: `https://yoursite.netlify.app`

2. **Open in 2 Browser Windows/Tabs**
   - Window 1: Click "Online"
   - Window 2: Click "Online"
   - Should see connection status and game syncing

3. **Test on Different Devices**
   - Desktop + Mobile
   - Different networks
   - Should all work! 🎉

---

## 🎯 Your URLs

After deployment, you'll have:

**Frontend (Netlify):**
```
https://yoursite.netlify.app
```

**Backend (Railway):**
```
wss://yourapp-production.up.railway.app/ws
```

**Share with Friends:**
Just share the Netlify URL! They can:
1. Open the URL
2. Click "Online"
3. You open same URL in another window
4. Click "Online"
5. Game syncs automatically! 🎮

---

## 🔍 Troubleshooting

### "Cannot reach game server"

**Check #1: Is Railway server running?**
1. Go to railway.app
2. Click your project
3. Look for green "Active" status
4. If red, click to see error logs

**Check #2: Correct domain in network.js?**
1. Open `js/network.js`
2. Verify the Railway URL is correct
3. Make sure it's `wss://` (secure WebSocket)
4. No trailing slash

**Check #3: Netlify deployed latest code?**
1. Go to netlify.com
2. Check "Deploys" tab
3. Latest deploy should show ✅
4. If not, click "Trigger deploy"

### "Connected but no sync"

**Check:**
1. Open browser console (F12)
2. Look for error messages
3. Check both players are connected
4. Try refreshing both pages

### "Connection works locally but not on cloud"

**Common issue:** Forgot to update `network.js` with Railway URL

**Fix:**
1. Update `js/network.js` with your Railway domain
2. Commit and push: `git push origin main`
3. Trigger Netlify redeploy
4. Wait 2-3 minutes for deploy to finish

---

## 📋 Deployment Checklist

### Netlify Setup
- [ ] Code pushed to GitHub
- [ ] Netlify connected to GitHub repo
- [ ] Deploy completed (green checkmark)
- [ ] Netlify URL works in browser

### Railway Setup
- [ ] Railway account created
- [ ] Repository connected to Railway
- [ ] Deploy completed in Railway
- [ ] Got Railway domain/URL

### Code Updates
- [ ] Updated `js/network.js` with Railway URL
- [ ] Code committed and pushed
- [ ] Netlify redeployed with new code

### Testing
- [ ] Local testing works (2 browser windows)
- [ ] Can open Netlify URL
- [ ] Can connect to Railway server
- [ ] Multiplayer works on live URLs

### Share
- [ ] Copy Netlify URL
- [ ] Share with friends
- [ ] Friends can join and play! 🎮

---

## 🚨 Common Issues & Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| "Cannot reach game server" | Railway server not running | Check Railway dashboard for green "Active" status |
| "WebSocket error" | Wrong URL in network.js | Update with correct Railway domain |
| "Connection works locally not cloud" | Forgot to update network.js | Update js/network.js and redeploy Netlify |
| "Works once then crashes" | Server timeout | Railway keeps running, should auto-restart |
| "Players see different game state" | Network lag | This is normal - latency is shown in game |

---

## 💡 Next Steps

1. ✅ Download the zip file
2. ✅ Extract it
3. ✅ Follow Part A (Deploy to Netlify)
4. ✅ Follow Part B (Deploy to Railway)
5. ✅ Follow Part C (Connect them)
6. ✅ Test and share!

---

## 🎉 You're Done!

Your multiplayer game is now:
- ✅ Live on the internet
- ✅ Works from anywhere
- ✅ Free to host
- ✅ Can share with anyone

**Share your Netlify URL with friends and play together!** 🚀

---

## 📞 Need Help?

**Netlify Issues?**
- Check netlify.com dashboard
- Look at "Deploy log" for errors
- Make sure all files were pushed to GitHub

**Railway Issues?**
- Check railway.app dashboard
- Look for red "Failed" status
- Click to see error logs

**Connection Issues?**
- Verify Railway URL in network.js
- Make sure it's `wss://` not `ws://`
- Try both browsers in incognito mode

---

Good luck! Happy multiplayer gaming! 🎮

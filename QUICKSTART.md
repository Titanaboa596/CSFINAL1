# 🎮 CS Game 2 - Quick Start Guide

## What You Have

✅ **Frontend**: Complete multiplayer tank game (HTML/CSS/JS)  
✅ **Backend**: Pure Python WebSocket server (no external dependencies)  
✅ **Configuration**: Ready for Netlify deployment  

## Running Locally

### Option 1: Simple Test (Fastest)

```bash
# Terminal 1: Start WebSocket server
python api/index.py

# Terminal 2: Start HTTP server
cd /home/claude
python -m http.server 8000

# Browser: Visit http://localhost:8000
# Click "Online" mode to test multiplayer!
```

### Option 2: With Netlify CLI (Recommended)

```bash
# Install Netlify CLI (one-time)
npm install -g netlify-cli

# Run with Netlify environment
netlify dev

# Browser: Visit http://localhost:8888
```

## Deploying to Netlify

### Step 1: Prepare GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit: CS Game 2"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/csgame2.git
git push -u origin main
```

### Step 2: Deploy

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Select GitHub and authorize
4. Choose your `csgame2` repository
5. Click "Deploy site"

**Netlify will automatically:**
- Build your site
- Deploy the WebSocket server as a Function
- Assign you a free domain (e.g., `yoursite.netlify.app`)

### Step 3: Test

Open your site URL in two browser tabs/windows:
- First tab: becomes Player 1 (Host)
- Second tab: becomes Player 2 (Joiner)
- Game starts automatically! 🎮

## Project Structure

```
.
├── api/
│   └── index.py              # WebSocket server
├── js/
│   ├── network.js            # (Updated for Netlify)
│   ├── gameloop.js
│   ├── gamestate.js
│   ├── tank.js
│   └── ... other game files
├── css/
│   └── style.css
├── index.html                # Lobby page
├── game.html                 # Game page
├── netlify.toml              # Netlify config
├── package.json              # Build config
├── requirements.txt          # Python dependencies
└── DEPLOYMENT_GUIDE.md       # Detailed guide
```

## Key Changes from Original

1. **network.js** - Updated WebSocket URL detection:
   - Local: `ws://localhost:8081/ws`
   - Netlify: `wss://yoursite.netlify.app/.netlify/functions/index/ws`

2. **api/index.py** - Standalone WebSocket server:
   - No external dependencies (uses Python stdlib)
   - Broadcasts game messages to all connected clients
   - Works with Netlify Functions

3. **netlify.toml** - Deployment configuration:
   - Tells Netlify where your files are
   - Configures the serverless function

## Troubleshooting

### "WebSocket connection failed"
- Check if server is running: `python api/index.py`
- Check browser console for error details
- Verify the WebSocket URL in network.js

### "Game won't start in multiplayer"
- Open 2 browser windows (or incognito tabs)
- First window: Click "Online" → becomes Host (P1)
- Second window: Click "Online" → should detect host and join
- If not detecting, refresh second window

### Netlify deployment issues
- Check Function logs in Netlify dashboard
- Verify `netlify.toml` is in root directory
- Make sure `api/index.py` exists in `api/` folder

## Next Steps

1. **Test locally** - Run the server and game
2. **Push to GitHub** - Create a repository
3. **Connect to Netlify** - Import from GitHub
4. **Play multiplayer!** - Share your URL with friends

## Files You Need to Modify (None!)

Your game files are already updated:
- ✅ `js/network.js` - Ready for Netlify
- ✅ `api/index.py` - WebSocket server
- ✅ `netlify.toml` - Configuration
- ✅ `package.json` - Build config

## Support Resources

- [Netlify Functions Docs](https://docs.netlify.com/functions/overview/)
- [WebSocket Protocol](https://tools.ietf.org/html/rfc6455)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

---

**Happy Gaming! 🚀**

Questions? Check `DEPLOYMENT_GUIDE.md` for detailed information.

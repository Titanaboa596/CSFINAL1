# CS Game 2 - Netlify Deployment Guide

## Overview
This guide shows how to deploy your multiplayer tank game with a FastAPI WebSocket backend to Netlify.

## Project Structure
```
your-project/
├── api/
│   └── index.py           # FastAPI app (Netlify Function)
├── csgame2-main/          # Your game files
│   ├── index.html
│   ├── game.html
│   ├── css/
│   ├── js/
│   │   └── network.js     # (UPDATED for Netlify)
│   └── ...
├── netlify.toml           # Netlify configuration
├── package.json
├── requirements.txt       # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Prepare Your Repository

```bash
# Create a new directory for your project
mkdir csgame2-netlify
cd csgame2-netlify

# Copy your game files
cp -r csgame2-main/* ./

# Create the api directory (for serverless functions)
mkdir api

# Copy the provided files:
# - api/index.py (provided)
# - network.js (replace your current one with the updated version)
# - netlify.toml
# - package.json
# - requirements.txt
```

### 2. Local Testing

#### Option A: Test with Local FastAPI Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python api/index.py
```

The server will start at `http://localhost:8081`

Then open your game:
```bash
# In another terminal, start a simple HTTP server
cd csgame2-netlify
python -m http.server 8000
```

Visit: `http://localhost:8000`

#### Option B: Test with Netlify CLI (recommended)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Run locally with Netlify environment
netlify dev
```

This starts both the frontend and backend functions at `http://localhost:8888`

### 3. Deploy to Netlify

#### Step 1: Connect Your Repository

1. Go to [netlify.com](https://netlify.com)
2. Sign in (or create a free account)
3. Click "Add new site" → "Import an existing project"
4. Select GitHub (or GitLab/Bitbucket)
5. Authorize Netlify to access your repositories
6. Select your `csgame2-netlify` repository

#### Step 2: Configure Build Settings

Netlify should auto-detect from `netlify.toml`, but verify:

- **Build command**: `npm run build`
- **Publish directory**: `public` (or root if your HTML files are in root)
- **Functions directory**: `api`

#### Step 3: Set Environment Variables (if needed)

In Netlify dashboard:
1. Go to your site settings
2. Click "Build & deploy" → "Environment"
3. Add any environment variables your app needs

#### Step 4: Deploy

```bash
# Option 1: Push to GitHub
git add .
git commit -m "Deploy to Netlify"
git push origin main
```

Netlify will automatically build and deploy!

Or:

```bash
# Option 2: Use Netlify CLI
netlify deploy --prod
```

### 4. Verify Your Deployment

After deployment:

1. Visit your Netlify site URL (e.g., `https://yoursite.netlify.app`)
2. Try the online multiplayer mode
3. Check the browser console for any errors
4. Monitor Netlify Function logs if you have issues

## Important Notes

### WebSocket Configuration

The `network.js` file has been updated to handle both:
- **Local development**: Connects to `localhost:8081/ws`
- **Netlify deployment**: Connects to `/.netlify/functions/index/ws`

### File Structure for Netlify

Make sure your HTML files are in the **root directory** or configure `publish` in `netlify.toml`:

```toml
[build]
  publish = "."        # if HTML in root
  # OR
  publish = "public"   # if HTML in public/
```

### Common Issues

#### Issue: WebSocket connection fails after deployment
- Check that `network.js` has the correct WebSocket URL
- Verify Function logs in Netlify dashboard
- Ensure no CORS errors in browser console

#### Issue: Frontend loads but game won't connect
- Check browser console for errors
- Verify the WebSocket URL is correct
- Check Netlify Function status in dashboard

#### Issue: 404 errors for game files
- Verify `publish` directory in `netlify.toml` matches your file structure
- Ensure `[[redirects]]` is set up to route to `index.html`

## Performance Tips

1. **Local vs Remote**: During matchmaking, players don't need the FastAPI server - it only syncs state
2. **Optimize images/assets**: Use modern formats (WebP) to reduce bandwidth
3. **Monitor Function execution**: Check Netlify logs for slow endpoints
4. **Enable edge functions**: For ultra-low latency, consider Netlify Edge Functions

## Testing Multiplayer

1. Open your game in two different browsers (or incognito windows)
2. Click "Online" in the lobby
3. One player becomes Host (P1)
4. Open the same game in another browser window
5. Second player joins as P2
6. Game starts automatically!

## Additional Resources

- [Netlify Functions Documentation](https://docs.netlify.com/functions/overview/)
- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Netlify CLI Guide](https://cli.netlify.com/)

## Support

If you encounter issues:

1. Check Netlify Function logs
2. Open browser DevTools → Console tab
3. Check for CORS errors
4. Verify your `netlify.toml` configuration
5. Try local testing with `netlify dev` first

Good luck deploying your game! 🚀

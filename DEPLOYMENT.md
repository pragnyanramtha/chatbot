# 🚀 Deployment Guide

This guide walks you through deploying your Programmable Chatbot to production.

## 📋 Prerequisites

- GitHub account
- Vercel account (for frontend)
- Railway/Render account (for backend)
- Google Gemini API key

## 🎯 Deployment Strategy

We'll deploy:
- **Frontend** → Vercel (static hosting)
- **Backend** → Railway (Python hosting)

## 🔧 Step 1: Prepare Your Repository

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Run deployment script**:
```bash
./deploy.sh
```
Choose option 3 for full deployment guide.

## 🖥️ Step 2: Deploy Backend (Railway)

1. **Visit [Railway](https://railway.app)**
2. **Connect GitHub**: Link your repository
3. **Create New Project**: Select your chatbot repo
4. **Configure Environment**:
   - Add `GEMINI_API_KEY` with your API key
   - Railway auto-detects Python and installs dependencies
5. **Deploy**: Railway automatically builds and deploys
6. **Get URL**: Copy your Railway app URL (e.g., `https://your-app.railway.app`)

### Alternative: Render Deployment

1. **Visit [Render](https://render.com)**
2. **Create Web Service**: Connect your GitHub repo
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment: Add `GEMINI_API_KEY`
4. **Deploy**: Render builds and deploys automatically

## 🌐 Step 3: Deploy Frontend (Vercel)

1. **Install Vercel CLI** (if not already installed):
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
vercel --prod
```

3. **Configure Environment Variables** in Vercel dashboard:
   - `VITE_API_URL` = Your Railway/Render backend URL

4. **Redeploy** after adding environment variables:
```bash
vercel --prod
```

## ✅ Step 4: Verify Deployment

1. **Test Frontend**: Visit your Vercel URL
2. **Check Backend**: Visit `your-backend-url/health`
3. **Test Chat**: Send a message through the UI

## 🔧 Environment Variables Summary

### Backend (Railway/Render)
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend-url.railway.app
```

## 🐛 Troubleshooting

### Frontend Issues
- **Blank page**: Check browser console for errors
- **API errors**: Verify `VITE_API_URL` is correct
- **Build fails**: Check Node.js version compatibility

### Backend Issues
- **500 errors**: Check backend logs for Python errors
- **CORS errors**: Ensure CORS is properly configured
- **Gemini errors**: Verify API key is valid and has quota

### Common Solutions
1. **Clear browser cache** after deployment
2. **Check environment variables** are set correctly
3. **Verify API endpoints** are accessible
4. **Review deployment logs** for specific errors

## 📊 Monitoring

### Backend Monitoring
- Railway: Built-in metrics and logs
- Render: Application logs and metrics
- Health check: `GET /health` endpoint

### Frontend Monitoring
- Vercel: Built-in analytics and performance metrics
- Browser DevTools: Network and console monitoring

## 🔄 Updates and Maintenance

### Updating Knowledge Base
1. Edit `config.json` in your repository
2. Push changes to GitHub
3. Backend automatically redeploys with new knowledge

### Code Updates
1. Make changes locally
2. Test with `./start.sh`
3. Push to GitHub
4. Both frontend and backend auto-deploy

## 💰 Cost Considerations

### Free Tiers
- **Vercel**: Generous free tier for personal projects
- **Railway**: $5/month after free trial
- **Render**: Free tier with limitations
- **Gemini API**: Pay-per-use pricing

### Optimization Tips
- Use `gemini-2.5-flash-lite` for lower costs
- Implement rate limiting for production
- Monitor API usage in Google Cloud Console

## 🔒 Security Best Practices

1. **Never commit API keys** to repository
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (automatic with Vercel/Railway)
4. **Implement rate limiting** for production use
5. **Monitor API usage** to prevent abuse

## 📈 Scaling

### High Traffic
- Consider upgrading to paid hosting tiers
- Implement caching for knowledge base queries
- Use CDN for static assets

### Multiple Environments
- Create separate deployments for staging/production
- Use different API keys for different environments
- Implement proper CI/CD pipelines

---

🎉 **Congratulations!** Your chatbot is now live and ready to help users!
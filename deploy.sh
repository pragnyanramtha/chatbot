#!/bin/bash

# Deployment script for Programmable Chatbot
# This script helps deploy the frontend to Vercel and provides backend deployment options

set -e

echo "🚀 Programmable Chatbot Deployment Script"
echo "=========================================="

# Check if required tools are installed
check_requirements() {
    echo "📋 Checking requirements..."
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is required but not installed."
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        echo "❌ git is required but not installed."
        exit 1
    fi
    
    echo "✅ Requirements check passed"
}

# Build the frontend
build_frontend() {
    echo "🔨 Building frontend..."
    npm install
    npm run build
    echo "✅ Frontend built successfully"
}

# Deploy to Vercel
deploy_vercel() {
    echo "🌐 Deploying to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        echo "📦 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    echo "🔧 Setting up Vercel project..."
    echo "Please follow the prompts to configure your Vercel project."
    echo "When asked for the build command, use: npm run build"
    echo "When asked for the output directory, use: dist"
    
    vercel --prod
    
    echo "✅ Frontend deployed to Vercel!"
}

# Backend deployment options
show_backend_options() {
    echo ""
    echo "🖥️  Backend Deployment Options"
    echo "=============================="
    echo ""
    echo "Your FastAPI backend needs to be deployed separately. Here are recommended options:"
    echo ""
    echo "1. 🐍 Railway (Recommended for Python)"
    echo "   - Visit: https://railway.app"
    echo "   - Connect your GitHub repo"
    echo "   - Railway will auto-detect your Python app"
    echo "   - Add your GEMINI_API_KEY environment variable"
    echo ""
    echo "2. 🚀 Render"
    echo "   - Visit: https://render.com"
    echo "   - Create a new Web Service"
    echo "   - Connect your GitHub repo"
    echo "   - Build command: pip install -r requirements.txt"
    echo "   - Start command: python main.py"
    echo "   - Add GEMINI_API_KEY environment variable"
    echo ""
    echo "3. ☁️  Google Cloud Run"
    echo "   - Use the provided Dockerfile"
    echo "   - Deploy with: gcloud run deploy"
    echo ""
    echo "4. 🔵 Heroku"
    echo "   - Create a Procfile: web: python main.py"
    echo "   - Deploy with Heroku CLI"
    echo ""
    echo "After deploying your backend, update your Vercel environment variables:"
    echo "VITE_API_URL=https://your-backend-url.com"
}

# Create Dockerfile for backend
create_dockerfile() {
    echo "🐳 Creating Dockerfile for backend deployment..."
    
    cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
EOF

    echo "✅ Dockerfile created"
}

# Create .dockerignore
create_dockerignore() {
    echo "📝 Creating .dockerignore..."
    
    cat > .dockerignore << 'EOF'
node_modules
dist
.git
.env
venv
__pycache__
*.pyc
.vscode
.DS_Store
EOF

    echo "✅ .dockerignore created"
}

# Create Procfile for Heroku
create_procfile() {
    echo "📝 Creating Procfile for Heroku..."
    
    cat > Procfile << 'EOF'
web: python main.py
EOF

    echo "✅ Procfile created"
}

# Main deployment flow
main() {
    echo "What would you like to deploy?"
    echo "1) Frontend only (Vercel)"
    echo "2) Create backend deployment files"
    echo "3) Full deployment guide"
    echo "4) Exit"
    
    read -p "Choose an option (1-4): " choice
    
    case $choice in
        1)
            check_requirements
            build_frontend
            deploy_vercel
            echo ""
            echo "🎉 Frontend deployed! Don't forget to deploy your backend and update VITE_API_URL"
            ;;
        2)
            create_dockerfile
            create_dockerignore
            create_procfile
            echo ""
            echo "✅ Backend deployment files created!"
            echo "You can now deploy to Railway, Render, Google Cloud Run, or Heroku"
            ;;
        3)
            check_requirements
            build_frontend
            create_dockerfile
            create_dockerignore
            create_procfile
            deploy_vercel
            show_backend_options
            ;;
        4)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option"
            exit 1
            ;;
    esac
}

# Run main function
main
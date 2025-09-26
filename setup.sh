#!/bin/bash

echo "Setting up Chatbot Application..."

# Create Python virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Make sure you have your Gemini API key in .env file"
echo "2. Run: ./start.sh"
echo ""
echo "Or run manually:"
echo "Backend: source venv/bin/activate && python main.py"
echo "Frontend: npm run dev"
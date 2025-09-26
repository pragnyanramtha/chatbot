# 🤖 Programmable Chatbot with Gemini AI

A powerful, customizable chatbot built with FastAPI backend and React frontend, featuring Google's Gemini AI integration and a programmable knowledge base system.

## ✨ Features

### 🧠 AI & Intelligence
- **Google Gemini AI Integration** - Uses latest Gemini 2.5 models (Flash, Flash-Lite, Pro)
- **Conversation Memory** - Maintains chat history and context across messages
- **Multiple Chat Sessions** - Support for independent conversation threads
- **Programmable Knowledge Base** - JSON-based knowledge system for domain-specific responses

### 🎨 Frontend
- **Modern React UI** - Clean, responsive chat interface
- **Real-time Messaging** - Smooth chat experience with loading indicators
- **Session Management** - Visual session indicators and management
- **Customizable Branding** - Configure title and description via JSON

### 🔧 Backend
- **FastAPI Framework** - High-performance async Python backend
- **RESTful APIs** - Well-documented endpoints for all functionality
- **Session Storage** - In-memory chat history with database-ready architecture
- **CORS Support** - Ready for cross-origin frontend integration

### 🚀 Deployment Ready
- **Vercel Frontend** - One-click frontend deployment
- **Multiple Backend Options** - Railway, Render, Google Cloud Run, Heroku
- **Docker Support** - Containerized deployment ready
- **Environment Configuration** - Secure API key management

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   Gemini AI     │
│                 │◄──►│                 │◄──►│                 │
│  - Chat UI      │    │  - Session Mgmt │    │  - Text Gen     │
│  - Session Mgmt │    │  - Knowledge DB │    │  - Context      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Knowledge Base │
                       │   (config.json) │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone and Setup
```bash
git clone <your-repo>
cd programmable-chatbot
./setup.sh  # Installs all dependencies
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run Development Servers
```bash
./start.sh  # Starts both frontend and backend
```

Visit `http://localhost:3000` to use your chatbot!

## 📖 Configuration

### Knowledge Base (`config.json`)
Customize your chatbot's knowledge by editing the JSON configuration:

```json
{
  "title": "Your Company Name",
  "description": "Your chatbot description",
  "entries": [
    {
      "id": "unique-id",
      "key": "Topic Name",
      "value": "Detailed information about the topic...",
      "tags": ["tag1", "tag2"],
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Environment Variables
- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `VITE_API_URL` - Backend URL for production deployment

## 🔌 API Reference

### Chat Endpoints
- `POST /chat` - Send message and get AI response
- `GET /sessions` - List all active chat sessions
- `GET /sessions/{id}/history` - Get chat history for session
- `DELETE /sessions/{id}` - Clear session history

### Configuration Endpoints
- `GET /config` - Get app title and description
- `GET /knowledge` - Get all knowledge base entries
- `GET /health` - Health check

### Example Usage
```bash
# Send a chat message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your services?",
    "session_id": "user-123"
  }'

# Get session history
curl "http://localhost:8000/sessions/user-123/history"
```

## 🌐 Deployment

### Frontend (Vercel)
```bash
./deploy.sh  # Choose option 1 for frontend only
```

### Backend Options

#### 1. Railway (Recommended)
1. Connect your GitHub repo to [Railway](https://railway.app)
2. Add `GEMINI_API_KEY` environment variable
3. Deploy automatically

#### 2. Render
1. Create new Web Service on [Render](https://render.com)
2. Build command: `pip install -r requirements.txt`
3. Start command: `python main.py`
4. Add `GEMINI_API_KEY` environment variable

#### 3. Docker Deployment
```bash
./deploy.sh  # Choose option 2 to create Docker files
docker build -t chatbot-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key chatbot-backend
```

## 🛠️ Development

### Project Structure
```
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── services/          # API services
│   └── styles/            # CSS styles
├── config.json            # Knowledge base
├── main.py               # FastAPI backend
├── models.py             # Data models
├── gemini_service.py     # AI integration
├── knowledge_service.py  # Knowledge management
└── deploy.sh            # Deployment script
```

### Adding Knowledge Entries
1. Edit `config.json`
2. Add new entries with unique IDs
3. Use descriptive tags for better search
4. Restart backend to load changes

### Customizing UI
- Update `config.json` for title/description
- Modify React components in `src/components/`
- Customize styles in `src/styles/`

## 🔧 Advanced Features

### Multiple Chat Sessions
Each user can have independent conversations:
```javascript
// Frontend: Create new session
const sessionId = `user-${Date.now()}`;
await apiService.sendMessage("Hello", sessionId);
```

### Knowledge Base Search
The system automatically searches knowledge base and provides context to AI:
- Fuzzy text matching on titles and content
- Tag-based filtering
- Relevance scoring

### Session Management
- Automatic conversation history
- Memory limits to prevent token overflow
- Session cleanup and management APIs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- Check the [Issues](../../issues) page for common problems
- Review API documentation at `http://localhost:8000/docs`
- Ensure your Gemini API key is valid and has sufficient quota

## 🎯 Use Cases

- **Customer Support** - Automated help desk with company knowledge
- **Documentation Assistant** - Interactive documentation chatbot  
- **Educational Tool** - Subject-specific learning assistant
- **Internal FAQ** - Company internal knowledge sharing
- **Product Guide** - Interactive product information system

---

Built with ❤️ using FastAPI, React, and Google Gemini AI
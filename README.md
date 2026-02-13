# 🚀 NASA Space Explorer

An interactive chatbot powered by NASA APIs that lets you explore space through natural conversation. Built with LangGraph, FastMCP, and real-time NASA data.

![NASA Space Explorer](https://img.shields.io/badge/NASA-API-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![Next.js](https://img.shields.io/badge/Next.js-14-black)

## ✨ Features

- 🌌 **Astronomy Picture of the Day (APOD)**: Get NASA's stunning daily space images with descriptions
- 🔴 **Mars Rover Photos**: Access photos from Curiosity, Opportunity, and Spirit rovers
- ☄️ **Near Earth Objects (NEO)**: Track asteroids and potentially hazardous objects near Earth
- 🔍 **NASA Media Library**: Search through NASA's vast collection of images and videos
- 💬 **Natural Language Interface**: Chat naturally about space topics and get real-time data

## 🏗️ Architecture

This application consists of three main components:

1. **Frontend (Next.js)**: Modern chat interface with space-themed UI
2. **Backend (FastAPI + LangGraph)**: Orchestrates LLM and tool calls using LangGraph
3. **Tools (FastMCP)**: MCP server providing NASA API tools

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│   Tools    │
│  (Next.js)  │      │  (FastAPI)   │      │  (FastMCP) │
│             │◀─────│ (LangGraph)  │◀─────│ NASA APIs  │
└─────────────┘      └──────────────┘      └────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- NASA API key (optional - defaults to DEMO_KEY)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NikhilBaravkarDataScientist/agui-langgraph-fastmcp-demo.git
   cd agui-langgraph-fastmcp-demo
   ```

2. **Get your NASA API key** (optional but recommended)
   - Visit [https://api.nasa.gov/](https://api.nasa.gov/)
   - Sign up for a free API key (takes 30 seconds)
   - Free tier: 1,000 requests per hour
   - Demo key (DEMO_KEY): 30 requests per hour per IP

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   NASA_API_KEY=your_nasa_api_key_here  # or use DEMO_KEY
   ```

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Tools MCP Server: [http://localhost:9000](http://localhost:9000)

## 💡 Usage Examples

Once the application is running, try these queries:

- **"Show me today's astronomy picture"** - Get APOD
- **"Get photos from Mars Curiosity rover sol 1000"** - Mars rover images
- **"Are there any asteroids near Earth right now?"** - NEO data
- **"Search for images of the Hubble Space Telescope"** - NASA media search
- **"Show me pictures from Mars rover's NAVCAM camera"** - Specific camera photos
- **"What near earth objects were detected this week?"** - Recent NEO activity

## 🛠️ NASA API Tools

The chatbot has access to these NASA API tools:

### 1. APOD (Astronomy Picture of the Day)
Get NASA's daily featured space image with explanation.

**Parameters:**
- `date` (optional): Date in YYYY-MM-DD format

### 2. Mars Rover Photos
Fetch photos from Mars rovers.

**Parameters:**
- `sol`: Martian sol (day) number (default: 1000)
- `camera`: Camera name - FHAZ, RHAZ, MAST, NAVCAM, etc. (default: "all")
- `rover`: Rover name - curiosity, opportunity, spirit (default: "curiosity")

### 3. Near Earth Objects (NEO)
Get data about asteroids near Earth.

**Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format (max 7 days)

### 4. NASA Image Search
Search NASA's media library.

**Parameters:**
- `query`: Search keywords
- `media_type`: image, video, or audio (default: "image")

## 🏃 Development

### Running Individual Components

**Backend only:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Tools server only:**
```bash
cd tools
pip install -r requirements.txt
python server.py
```

**Frontend only:**
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

**Backend:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `NASA_API_KEY`: Your NASA API key (optional, defaults to DEMO_KEY)

**Tools:**
- `NASA_API_KEY`: Your NASA API key (optional, defaults to DEMO_KEY)

**Frontend:**
- `NEXT_PUBLIC_WS_URL`: WebSocket URL for backend (default: ws://localhost:8000/ws/chat)

## 📁 Project Structure

```
.
├── backend/              # FastAPI backend with LangGraph
│   ├── app/
│   │   ├── graph/       # LangGraph nodes, edges, state
│   │   ├── llm/         # OpenAI LLM configuration
│   │   ├── mcp/         # MCP client for tool calls
│   │   └── utils/       # Utilities (memory, streaming)
│   └── requirements.txt
│
├── tools/               # FastMCP server with NASA tools
│   ├── server.py        # MCP server setup
│   ├── tools.py         # NASA API tool implementations
│   └── requirements.txt
│
├── frontend/            # Next.js frontend
│   ├── app/             # Next.js app directory
│   ├── components/      # React components
│   └── lib/             # WebSocket utilities
│
└── docker-compose.yml   # Docker orchestration
```

## 🔒 Security

- Never commit API keys to the repository
- Use environment variables for sensitive data
- The `.env` file is gitignored by default
- NASA's DEMO_KEY is rate-limited and should only be used for testing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [NASA Open APIs](https://api.nasa.gov/) for providing free access to space data
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) for LLM integration

## 📚 Resources

- [NASA API Documentation](https://api.nasa.gov/)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Next.js Documentation](https://nextjs.org/docs)

---

**Made with ❤️ and ☕ for space exploration enthusiasts**

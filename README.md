# 📺 Live News Video Hub

A YouTube-style live news video aggregator that auto-aggregates the newest video posts from major news channels and displays them in a responsive feed with real-time updates.

## ✨ Features

- **Real-time Video Feed**: Auto-updates with newest videos from major news channels
- **YouTube-style Interface**: Clean, responsive design with video thumbnails and metadata
- **Live Streaming Support**: Special indicators for live broadcasts
- **Category Filtering**: Filter videos by World, Politics, Business, Technology, Health, Entertainment, Science, etc.
- **External Video Sources**: Integration with YouTube API, Vimeo API, and demo content for missing categories
- **Search Functionality**: Search across video titles and channel names
- **WebSocket Updates**: Real-time notifications when new videos are added
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Dark/Light Mode**: Toggle between themes
- **Video Player**: Full YouTube embed player with related videos

## 🚀 Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Socket.io Client** - Real-time WebSocket communication

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database (can be upgraded to PostgreSQL)
- **WebSockets** - Real-time communication
- **Feedparser** - RSS feed parsing
- **HTTPX** - Async HTTP client

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd live-news-video-hub
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend API will be available at `http://localhost:8000`

## 🎯 Usage

1. **Start both servers** (frontend and backend)
2. **Open your browser** to `http://localhost:3000`
3. **Browse videos** by category or search for specific content
4. **Click on videos** to watch them in the full player
5. **Watch for real-time updates** as new videos appear automatically

## 📊 Supported News Channels

The application currently aggregates videos from:

### RSS Feed Sources
- **BBC News** - World news and current events
- **CNN** - Breaking news and analysis
- **Al Jazeera English** - International news coverage
- **Sky News** - UK and world news
- **Reuters** - Business and world news
- **Fox News** - US politics and news
- **MSNBC** - US politics and analysis
- **CNBC** - Business and financial news
- **Bloomberg Television** - Business and financial news
- **TEDx Talks** - Technology and ideas
- **MKBHD** - Technology reviews and news
- **Verge Science** - Technology and science

### External API Sources
- **Health**: SciShow, Healthcare Triage, Mayo Clinic
- **Entertainment**: PewDiePie, MrBeast, Entertainment Tonight
- **Science**: Kurzgesagt, TED-Ed, SmarterEveryDay, Mark Rober

### Demo Content
- Fallback demo videos for categories with limited content

## 🔧 Configuration

### Adding New Channels

To add new YouTube channels, edit the `_get_default_channels()` method in `backend/rss_fetcher.py`:

```python
{
    "id": "CHANNEL_ID",  # YouTube channel ID
    "name": "Channel Name",
    "category": "category_id",  # Must match existing category
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID"
}
```

### RSS Feed Format

The application uses YouTube's RSS feeds in the format:
```
https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./news_videos.db

# External API Keys (Optional)
YOUTUBE_API_KEY=your_youtube_api_key_here
VIMEO_ACCESS_TOKEN=your_vimeo_access_token_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

For detailed API setup instructions, see [API_SETUP.md](API_SETUP.md).

## 🏗️ Project Structure

```
live-news-video-hub/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── watch/[id]/        # Video watch page
├── components/            # React components
│   ├── Header.tsx         # Navigation header
│   ├── VideoCard.tsx      # Individual video card
│   ├── VideoGrid.tsx      # Video grid layout
│   ├── VideoPlayer.tsx    # YouTube embed player
│   ├── SearchBar.tsx      # Search functionality
│   ├── CategoryTabs.tsx   # Category filtering
│   └── RelatedVideos.tsx  # Related videos sidebar
├── hooks/                 # Custom React hooks
│   └── useWebSocket.ts    # WebSocket connection
├── lib/                   # Utility libraries
│   └── api.ts            # API client
├── types/                 # TypeScript type definitions
│   └── index.ts          # Shared types
├── backend/               # FastAPI backend
│   ├── main.py           # FastAPI application
│   ├── models.py         # Database models
│   ├── database.py       # Database configuration
│   ├── rss_fetcher.py    # RSS feed processing
│   ├── video_apis.py     # External video APIs
│   ├── websocket_manager.py # WebSocket management
│   ├── test_apis.py      # API testing script
│   └── requirements.txt  # Python dependencies
└── README.md             # This file
```

## 🔄 How It Works

1. **RSS Polling**: The backend polls YouTube RSS feeds every 5 minutes
2. **External APIs**: Fetches videos from YouTube API, Vimeo API, and other sources
3. **Video Processing**: New videos are parsed and stored in the database
4. **Real-time Updates**: WebSocket broadcasts new videos to connected clients
5. **Frontend Display**: Videos are displayed in a responsive grid with filtering
6. **YouTube Embed**: Videos are played using legal YouTube embeds

## 🚀 Deployment

### Frontend (Vercel)
```bash
npm run build
# Deploy to Vercel or your preferred platform
```

### Backend (Railway/Render/Fly.io)
```bash
# Update DATABASE_URL to PostgreSQL
# Deploy using your preferred platform
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- YouTube RSS feeds for providing video data
- FastAPI for the excellent Python web framework
- Next.js team for the amazing React framework
- All the news channels for their content

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Note**: This application uses YouTube RSS feeds which are publicly available and legal to use. No YouTube API key is required for basic functionality. External APIs (YouTube API, Vimeo API) are optional and provide additional content for categories with limited RSS feed coverage.

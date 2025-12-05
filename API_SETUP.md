# API Setup Guide

This guide will help you set up the external video APIs to fetch videos for health, entertainment, and science categories.

## YouTube API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click on it and press "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key
5. Set the environment variable:
   ```bash
   export YOUTUBE_API_KEY=your_api_key_here
   ```

## Vimeo API Setup (Optional)

1. Go to [Vimeo Developer](https://developer.vimeo.com/)
2. Create a new app
3. Generate an access token
4. Set the environment variable:
   ```bash
   export VIMEO_ACCESS_TOKEN=your_access_token_here
   ```

## Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here

# Vimeo API Configuration (Optional)
VIMEO_ACCESS_TOKEN=your_vimeo_access_token_here

# Database Configuration
DATABASE_URL=sqlite:///./news_videos.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Running the Application

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Start the backend server:
   ```bash
   python main.py
   ```

3. In another terminal, start the frontend:
   ```bash
   npm run dev
   ```

## API Endpoints

The following new endpoints are available:

- `GET /api/videos/health` - Get health-related videos
- `GET /api/videos/entertainment` - Get entertainment videos
- `GET /api/videos/science` - Get science videos
- `GET /api/videos/external/{category}` - Get videos from external sources for any category

## Fallback Content

If no API keys are configured, the system will use demo videos for the missing categories. These demo videos provide sample content to demonstrate the functionality.

## Troubleshooting

- If you see "YouTube API key not configured" warnings, make sure you've set the `YOUTUBE_API_KEY` environment variable
- If videos aren't loading, check the browser console and server logs for error messages
- Make sure your API keys have the necessary permissions and quotas

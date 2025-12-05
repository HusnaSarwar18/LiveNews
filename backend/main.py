from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import asyncio
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import Video, Channel, Category
from database import engine, SessionLocal
from rss_fetcher import RSSFetcher
from websocket_manager import WebSocketManager
from video_apis import VideoAPIs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Live News Video Hub API",
    description="YouTube-style live news video aggregator with real-time updates",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager
websocket_manager = WebSocketManager()

# RSS fetcher
rss_fetcher = RSSFetcher()

# Video APIs
video_apis = VideoAPIs()

@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    # Create database tables
    from models import Base
    Base.metadata.create_all(bind=engine)
    
    # Start RSS fetching task
    asyncio.create_task(rss_fetcher.start_fetching())

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await rss_fetcher.stop_fetching()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Live News Video Hub API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/videos")
async def get_videos(
    category: Optional[str] = Query(None, description="Filter by category"),
    channel: Optional[str] = Query(None, description="Filter by channel ID"),
    is_live: Optional[bool] = Query(None, description="Filter by live status"),
    search: Optional[str] = Query(None, description="Search in titles and descriptions"),
    limit: int = Query(20, ge=1, le=100, description="Number of videos to return"),
    offset: int = Query(0, ge=0, description="Number of videos to skip")
):
    """Get videos with optional filtering"""
    try:
        db = SessionLocal()
        
        # Build query
        query = db.query(Video)
        
        if category and category != "all":
            query = query.filter(Video.category == category)
        
        if channel:
            query = query.filter(Video.channel_id == channel)
        
        if is_live is not None:
            query = query.filter(Video.is_live == is_live)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Video.title.ilike(search_term)) |
                (Video.description.ilike(search_term))
            )
        
        # Order by published date (newest first)
        query = query.order_by(Video.published.desc())
        
        # Apply pagination
        total = query.count()
        videos = query.offset(offset).limit(limit).all()
        
        # Convert to response format
        video_list = []
        for video in videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description
            }
            video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Error fetching videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/videos/{video_id}")
async def get_video(video_id: str):
    """Get a specific video by ID"""
    try:
        db = SessionLocal()
        video = db.query(Video).filter(Video.id == video_id).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_data = {
            "id": video.id,
            "title": video.title,
            "channel": {
                "id": video.channel_id,
                "name": video.channel_name
            },
            "published": int(video.published.timestamp() * 1000),
            "url": video.url,
            "embedUrl": video.embed_url,
            "thumbnail": video.thumbnail,
            "category": video.category,
            "isLive": video.is_live,
            "duration": video.duration,
            "viewCount": video.view_count,
            "description": video.description
        }
        
        return {
            "success": True,
            "data": video_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching video {video_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/videos/live")
async def get_live_videos():
    """Get all currently live videos"""
    try:
        db = SessionLocal()
        videos = db.query(Video).filter(Video.is_live == True).order_by(Video.published.desc()).all()
        
        video_list = []
        for video in videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description
            }
            video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list
        }
        
    except Exception as e:
        logger.error(f"Error fetching live videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/search")
async def search_videos(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """Search videos by title and description"""
    try:
        db = SessionLocal()
        search_term = f"%{q}%"
        
        videos = db.query(Video).filter(
            (Video.title.ilike(search_term)) |
            (Video.description.ilike(search_term)) |
            (Video.channel_name.ilike(search_term))
        ).order_by(Video.published.desc()).limit(limit).all()
        
        video_list = []
        for video in videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description
            }
            video_list.append(video_data)
        
        return {
            "success": True,
            "data": {
                "videos": video_list,
                "total": len(video_list),
                "query": q
            }
        }
        
    except Exception as e:
        logger.error(f"Error searching videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/channels")
async def get_channels():
    """Get all channels"""
    try:
        db = SessionLocal()
        channels = db.query(Channel).all()
        
        channel_list = []
        for channel in channels:
            channel_data = {
                "id": channel.id,
                "name": channel.name,
                "category": channel.category,
                "rssUrl": channel.rss_url,
                "thumbnail": channel.thumbnail,
                "subscriberCount": channel.subscriber_count
            }
            channel_list.append(channel_data)
        
        return {
            "success": True,
            "data": channel_list
        }
        
    except Exception as e:
        logger.error(f"Error fetching channels: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/categories")
async def get_categories():
    """Get all categories"""
    try:
        db = SessionLocal()
        categories = db.query(Category).all()
        
        category_list = []
        for category in categories:
            category_data = {
                "id": category.id,
                "name": category.name,
                "color": category.color,
                "channels": category.channels.split(',') if category.channels else []
            }
            category_list.append(category_data)
        
        return {
            "success": True,
            "data": category_list
        }
        
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/videos/external/{category}")
async def get_external_videos(
    category: str,
    limit: int = Query(20, ge=1, le=50, description="Number of videos to return")
):
    """Get videos from external sources (YouTube, Vimeo, etc.) for a specific category"""
    try:
        # Fetch videos from external sources
        videos = await video_apis.fetch_all_sources(category, limit)
        
        # Convert to response format
        video_list = []
        for video in videos:
            video_data = {
                "id": video['id'],
                "title": video['title'],
                "channel": {
                    "id": video['channel_id'],
                    "name": video['channel_name']
                },
                "published": int(video['published'].timestamp() * 1000),
                "url": video['url'],
                "embedUrl": video['embed_url'],
                "thumbnail": video['thumbnail'],
                "category": video['category'],
                "isLive": video['is_live'],
                "duration": video['duration'],
                "viewCount": video.get('view_count', 0),
                "description": video['description'],
                "source": "external"
            }
            video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list,
            "total": len(video_list),
            "category": category
        }
        
    except Exception as e:
        logger.error(f"Error fetching external videos for category {category}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/videos/health")
async def get_health_videos(
    limit: int = Query(20, ge=1, le=50, description="Number of videos to return")
):
    """Get health-related videos from all sources"""
    try:
        # First try to get from database
        db = SessionLocal()
        db_videos = db.query(Video).filter(Video.category == "health").order_by(Video.published.desc()).limit(limit).all()
        
        # Convert database videos to response format
        video_list = []
        for video in db_videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description,
                "source": "database"
            }
            video_list.append(video_data)
        
        # If we don't have enough videos, fetch from external sources
        if len(video_list) < limit:
            external_videos = await video_apis.fetch_all_sources("health", limit - len(video_list))
            
            for video in external_videos:
                video_data = {
                    "id": video['id'],
                    "title": video['title'],
                    "channel": {
                        "id": video['channel_id'],
                        "name": video['channel_name']
                    },
                    "published": int(video['published'].timestamp() * 1000),
                    "url": video['url'],
                    "embedUrl": video['embed_url'],
                    "thumbnail": video['thumbnail'],
                    "category": video['category'],
                    "isLive": video['is_live'],
                    "duration": video['duration'],
                    "viewCount": video.get('view_count', 0),
                    "description": video['description'],
                    "source": "external"
                }
                video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list,
            "total": len(video_list),
            "category": "health"
        }
        
    except Exception as e:
        logger.error(f"Error fetching health videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/videos/entertainment")
async def get_entertainment_videos(
    limit: int = Query(20, ge=1, le=50, description="Number of videos to return")
):
    """Get entertainment-related videos from all sources"""
    try:
        # First try to get from database
        db = SessionLocal()
        db_videos = db.query(Video).filter(Video.category == "entertainment").order_by(Video.published.desc()).limit(limit).all()
        
        # Convert database videos to response format
        video_list = []
        for video in db_videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description,
                "source": "database"
            }
            video_list.append(video_data)
        
        # If we don't have enough videos, fetch from external sources
        if len(video_list) < limit:
            external_videos = await video_apis.fetch_all_sources("entertainment", limit - len(video_list))
            
            for video in external_videos:
                video_data = {
                    "id": video['id'],
                    "title": video['title'],
                    "channel": {
                        "id": video['channel_id'],
                        "name": video['channel_name']
                    },
                    "published": int(video['published'].timestamp() * 1000),
                    "url": video['url'],
                    "embedUrl": video['embed_url'],
                    "thumbnail": video['thumbnail'],
                    "category": video['category'],
                    "isLive": video['is_live'],
                    "duration": video['duration'],
                    "viewCount": video.get('view_count', 0),
                    "description": video['description'],
                    "source": "external"
                }
                video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list,
            "total": len(video_list),
            "category": "entertainment"
        }
        
    except Exception as e:
        logger.error(f"Error fetching entertainment videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/videos/science")
async def get_science_videos(
    limit: int = Query(20, ge=1, le=50, description="Number of videos to return")
):
    """Get science-related videos from all sources"""
    try:
        # First try to get from database
        db = SessionLocal()
        db_videos = db.query(Video).filter(Video.category == "science").order_by(Video.published.desc()).limit(limit).all()
        
        # Convert database videos to response format
        video_list = []
        for video in db_videos:
            video_data = {
                "id": video.id,
                "title": video.title,
                "channel": {
                    "id": video.channel_id,
                    "name": video.channel_name
                },
                "published": int(video.published.timestamp() * 1000),
                "url": video.url,
                "embedUrl": video.embed_url,
                "thumbnail": video.thumbnail,
                "category": video.category,
                "isLive": video.is_live,
                "duration": video.duration,
                "viewCount": video.view_count,
                "description": video.description,
                "source": "database"
            }
            video_list.append(video_data)
        
        # If we don't have enough videos, fetch from external sources
        if len(video_list) < limit:
            external_videos = await video_apis.fetch_all_sources("science", limit - len(video_list))
            
            for video in external_videos:
                video_data = {
                    "id": video['id'],
                    "title": video['title'],
                    "channel": {
                        "id": video['channel_id'],
                        "name": video['channel_name']
                    },
                    "published": int(video['published'].timestamp() * 1000),
                    "url": video['url'],
                    "embedUrl": video['embed_url'],
                    "thumbnail": video['thumbnail'],
                    "category": video['category'],
                    "isLive": video['is_live'],
                    "duration": video['duration'],
                    "viewCount": video.get('view_count', 0),
                    "description": video['description'],
                    "source": "external"
                }
                video_list.append(video_data)
        
        return {
            "success": True,
            "data": video_list,
            "total": len(video_list),
            "category": "science"
        }
        
    except Exception as e:
        logger.error(f"Error fetching science videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

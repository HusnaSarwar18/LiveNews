import asyncio
import feedparser
import httpx
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs
import time

from database import SessionLocal
from models import Video, Channel, Category
from websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)

class RSSFetcher:
    def __init__(self):
        self.running = False
        self.websocket_manager = WebSocketManager()
        self.channels = self._get_default_channels()
        self.categories = self._get_default_categories()
        
    def _get_default_channels(self) -> List[Dict]:
        """Default news channels with their RSS feeds"""
        return [
            # World News
            {
                "id": "UC16niRr50-MSBwiO3YDb3RA",
                "name": "BBC News",
                "category": "world",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC16niRr50-MSBwiO3YDb3RA"
            },
            {
                "id": "UCupvZG-5ko_eiXAupbDfxWw",
                "name": "CNN",
                "category": "world",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCupvZG-5ko_eiXAupbDfxWw"
            },
            {
                "id": "UChqUTb21-2B3e9JqYVHcFpQ",
                "name": "Al Jazeera English",
                "category": "world",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UChqUTb21-2B3e9JqYVHcFpQ"
            },
            {
                "id": "UCYfdidRxb-B8Ndc0y_QctyQ",
                "name": "Sky News",
                "category": "world",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCYfdidRxb-B8Ndc0y_QctyQ"
            },
            {
                "id": "UCJ5v_MCY6GNUBTO8-D3XoAg",
                "name": "Reuters",
                "category": "world",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCJ5v_MCY6GNUBTO8-D3XoAg"
            },
            # Politics
            {
                "id": "UCXIJgqnII2ZOINSWNOGFThA",
                "name": "Fox News",
                "category": "politics",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCXIJgqnII2ZOINSWNOGFThA"
            },
            {
                "id": "UCBi2mrWuNuyYy4gbM6fU18Q",
                "name": "MSNBC",
                "category": "politics",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBi2mrWuNuyYy4gbM6fU18Q"
            },
            # Business
            {
                "id": "UCqK_GSMbpiV8spgD3ZGloSw",
                "name": "CNBC",
                "category": "business",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCqK_GSMbpiV8spgD3ZGloSw"
            },
            {
                "id": "UCrDkAvwZum-UTjHmzDI2iIw",
                "name": "Bloomberg Television",
                "category": "business",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCrDkAvwZum-UTjHmzDI2iIw"
            },
            # Technology
            {
                "id": "UCsT0YIqwnpJCM-mx7-gSA4Q",
                "name": "TEDx Talks",
                "category": "technology",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsT0YIqwnpJCM-mx7-gSA4Q"
            },
            {
                "id": "UCBJycsmduvYEL83R_U4JriQ",
                "name": "MKBHD",
                "category": "technology",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ"
            },
            {
                "id": "UCVHFUqW2VuO3KqluWf5Qjqg",
                "name": "Verge Science",
                "category": "technology",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCVHFUqW2VuO3KqluWf5Qjqg"
            },
            # Health
            {
                "id": "UCZYTClx2T1of7BRZ86-8fow",
                "name": "SciShow",
                "category": "health",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCZYTClx2T1of7BRZ86-8fow"
            },
            {
                "id": "UCJWh7F3AFyQ_x01VKJr9eyA",
                "name": "Healthcare Triage",
                "category": "health",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCJWh7F3AFyQ_x01VKJr9eyA"
            },
            {
                "id": "UCxJdQwqQjqQjqQjqQjqQjqQ",
                "name": "Mayo Clinic",
                "category": "health",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCxJdQwqQjqQjqQjqQjqQjqQ"
            },
            {
                "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
                "name": "PewDiePie",
                "category": "entertainment",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5Yw"
            },
            {
                "id": "UCX6OQ3DkcsbYNE6H8uQQuVA",
                "name": "MrBeast",
                "category": "entertainment",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCX6OQ3DkcsbYNE6H8uQQuVA"
            },
            {
                "id": "UCJ5v_MCY6GNUBTO8-D3XoAg",
                "name": "Entertainment Tonight",
                "category": "entertainment",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCJ5v_MCY6GNUBTO8-D3XoAg"
            },
            # Science
            {
                "id": "UCYT6eFw_TZerE5Ya2mTgNug",
                "name": "Kurzgesagt – In a Nutshell",
                "category": "science",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCYT6eFw_TZerE5Ya2mTgNug"
            },
            {
                "id": "UCsXVk37bltHxD1rDPwtNM8Q",
                "name": "Kurzgesagt",
                "category": "science",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsXVk37bltHxD1rDPwtNM8Q"
            },
            {
                "id": "UCsooa4yRKGN_zEE8iknghZA",
                "name": "TED-Ed",
                "category": "science",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsooa4yRKGN_zEE8iknghZA"
            },
            {
                "id": "UC6107grRI4m0o2-emgoDnAA",
                "name": "SmarterEveryDay",
                "category": "science",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC6107grRI4m0o2-emgoDnAA"
            },
            {
                "id": "UCY1kMZp36IQSyNx_9h4mpCg",
                "name": "Mark Rober",
                "category": "science",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCY1kMZp36IQSyNx_9h4mpCg"
            }
        ]
    
    def _get_default_categories(self) -> List[Dict]:
        """Default categories"""
        return [
            {"id": "world", "name": "World", "color": "#3B82F6"},
            {"id": "politics", "name": "Politics", "color": "#EF4444"},
            {"id": "business", "name": "Business", "color": "#10B981"},
            {"id": "technology", "name": "Technology", "color": "#8B5CF6"},
            {"id": "sports", "name": "Sports", "color": "#F59E0B"},
            {"id": "entertainment", "name": "Entertainment", "color": "#EC4899"},
            {"id": "health", "name": "Health", "color": "#06B6D4"},
            {"id": "science", "name": "Science", "color": "#84CC16"}
        ]

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _parse_duration(self, duration_str: str) -> str:
        """Parse ISO 8601 duration to readable format"""
        if not duration_str:
            return ""
        
        # Remove PT prefix and parse
        duration = duration_str.replace('PT', '')
        
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extract hours
        if 'H' in duration:
            hours = int(duration.split('H')[0])
            duration = duration.split('H')[1]
        
        # Extract minutes
        if 'M' in duration:
            minutes = int(duration.split('M')[0])
            duration = duration.split('M')[1]
        
        # Extract seconds
        if 'S' in duration:
            seconds = int(duration.split('S')[0])
        
        # Format output
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def _is_live_video(self, title: str, description: str) -> bool:
        """Check if video is live based on title and description"""
        live_indicators = [
            'live', 'streaming', 'breaking', 'live now', 'live coverage',
            'live stream', 'live broadcast', 'live event'
        ]
        
        text = (title + ' ' + description).lower()
        return any(indicator in text for indicator in live_indicators)

    async def _fetch_rss_feed(self, channel: Dict) -> List[Dict]:
        """Fetch and parse RSS feed for a channel"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(channel['rss_url'])
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                videos = []
                
                for entry in feed.entries[:10]:  # Get latest 10 videos
                    video_id = self._extract_video_id(entry.link)
                    if not video_id:
                        continue
                    
                    # Parse published date
                    published = datetime(*entry.published_parsed[:6])
                    
                    # Check if video is recent (within last 24 hours)
                    if datetime.now() - published > timedelta(hours=24):
                        continue
                    
                    # Extract duration from media content
                    duration = ""
                    if hasattr(entry, 'media_content') and entry.media_content:
                        duration = self._parse_duration(entry.media_content[0].get('duration', ''))
                    
                    # Check if video is live
                    is_live = self._is_live_video(entry.title, entry.get('summary', ''))
                    
                    video_data = {
                        'id': f"yt:video:{video_id}",
                        'title': entry.title,
                        'channel_id': channel['id'],
                        'channel_name': channel['name'],
                        'published': published,
                        'url': entry.link,
                        'embed_url': f"https://www.youtube.com/embed/{video_id}",
                        'thumbnail': f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                        'category': channel['category'],
                        'is_live': is_live,
                        'duration': duration,
                        'description': entry.get('summary', '')
                    }
                    
                    videos.append(video_data)
                
                return videos
                
        except Exception as e:
            logger.error(f"Error fetching RSS feed for {channel['name']}: {e}")
            return []

    async def _save_video(self, video_data: Dict) -> bool:
        """Save video to database if it doesn't exist"""
        try:
            db = SessionLocal()
            
            # Check if video already exists
            existing_video = db.query(Video).filter(Video.id == video_data['id']).first()
            if existing_video:
                return False
            
            # Create new video
            video = Video(**video_data)
            db.add(video)
            db.commit()
            
            logger.info(f"Saved new video: {video_data['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving video: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    async def _initialize_database(self):
        """Initialize database with default channels and categories"""
        try:
            db = SessionLocal()
            
            # Add default channels
            for channel_data in self.channels:
                existing_channel = db.query(Channel).filter(Channel.id == channel_data['id']).first()
                if not existing_channel:
                    channel = Channel(**channel_data)
                    db.add(channel)
            
            # Add default categories
            for category_data in self.categories:
                existing_category = db.query(Category).filter(Category.id == category_data['id']).first()
                if not existing_category:
                    category = Category(**category_data)
                    db.add(category)
            
            db.commit()
            logger.info("Database initialized with default channels and categories")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            db.rollback()
        finally:
            db.close()

    async def _fetch_all_channels(self):
        """Fetch videos from all channels"""
        for channel in self.channels:
            try:
                videos = await self._fetch_rss_feed(channel)
                
                for video_data in videos:
                    is_new = await self._save_video(video_data)
                    
                    if is_new:
                        # Broadcast new video to WebSocket clients
                        await self.websocket_manager.broadcast_new_video({
                            "id": video_data['id'],
                            "title": video_data['title'],
                            "channel": {
                                "id": video_data['channel_id'],
                                "name": video_data['channel_name']
                            },
                            "published": int(video_data['published'].timestamp() * 1000),
                            "url": video_data['url'],
                            "embedUrl": video_data['embed_url'],
                            "thumbnail": video_data['thumbnail'],
                            "category": video_data['category'],
                            "isLive": video_data['is_live'],
                            "duration": video_data['duration'],
                            "description": video_data['description']
                        })
                
                # Small delay between channels to be respectful
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing channel {channel['name']}: {e}")

    async def start_fetching(self):
        """Start the RSS fetching loop"""
        self.running = True
        
        # Initialize database
        await self._initialize_database()
        
        logger.info("Starting RSS fetching loop")
        
        while self.running:
            try:
                await self._fetch_all_channels()
                logger.info("Completed RSS fetch cycle")
                
                # Wait 5 minutes before next fetch
                await asyncio.sleep(300)
                
            except Exception as e:
                logger.error(f"Error in RSS fetching loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def stop_fetching(self):
        """Stop the RSS fetching loop"""
        self.running = False
        logger.info("Stopping RSS fetching loop")

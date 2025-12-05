import asyncio
import httpx
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from urllib.parse import urlparse, parse_qs
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class VideoAPIs:
    def __init__(self):
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')
        self.vimeo_access_token = os.getenv('VIMEO_ACCESS_TOKEN', '')
        
    async def fetch_youtube_videos(self, category: str, max_results: int = 20) -> List[Dict]:
        """Fetch videos from YouTube API for specific category"""
        if not self.youtube_api_key:
            logger.warning("YouTube API key not configured")
            return []
            
        try:
            # Map our categories to YouTube search terms
            category_mapping = {
                'health': ['health', 'medical', 'wellness', 'fitness'],
                'entertainment': ['entertainment', 'comedy', 'music', 'gaming'],
                'science': ['science', 'education', 'physics', 'chemistry', 'biology'],
                'technology': ['technology', 'tech', 'programming', 'AI'],
                'business': ['business', 'finance', 'economics'],
                'politics': ['politics', 'news', 'government'],
                'world': ['world news', 'international', 'global'],
                'sports': ['sports', 'athletics', 'fitness']
            }
            
            search_terms = category_mapping.get(category, [category])
            all_videos = []
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                for term in search_terms[:3]:  # Use first 3 terms to avoid rate limits
                    try:
                        # Search for recent videos
                        search_url = "https://www.googleapis.com/youtube/v3/search"
                        params = {
                            'part': 'snippet',
                            'q': term,
                            'type': 'video',
                            'order': 'date',
                            'maxResults': min(max_results, 10),
                            'key': self.youtube_api_key,
                            'publishedAfter': (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
                        }
                        
                        response = await client.get(search_url, params=params)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if 'items' in data:
                            # Get video details for each found video
                            video_ids = [item['id']['videoId'] for item in data['items']]
                            videos_detail = await self._get_youtube_video_details(client, video_ids)
                            
                            for item, video_detail in zip(data['items'], videos_detail):
                                if video_detail:
                                    video_data = {
                                        'id': f"yt:video:{item['id']['videoId']}",
                                        'title': item['snippet']['title'],
                                        'channel_id': item['snippet']['channelId'],
                                        'channel_name': item['snippet']['channelTitle'],
                                        'published': datetime.fromisoformat(item['snippet']['publishedAt'].replace('Z', '+00:00')),
                                        'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                                        'embed_url': f"https://www.youtube.com/embed/{item['id']['videoId']}",
                                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                                        'category': category,
                                        'is_live': False,  # Search API doesn't return live status
                                        'duration': video_detail.get('duration', ''),
                                        'view_count': video_detail.get('view_count', 0),
                                        'description': item['snippet']['description']
                                    }
                                    all_videos.append(video_data)
                    
                    except Exception as e:
                        logger.error(f"Error fetching YouTube videos for term '{term}': {e}")
                        continue
                        
            return all_videos[:max_results]
            
        except Exception as e:
            logger.error(f"Error in YouTube API fetch: {e}")
            return []
    
    async def _get_youtube_video_details(self, client: httpx.AsyncClient, video_ids: List[str]) -> List[Dict]:
        """Get detailed information for YouTube videos"""
        if not video_ids:
            return []
            
        try:
            # YouTube API allows up to 50 video IDs per request
            chunks = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]
            all_details = []
            
            for chunk in chunks:
                try:
                    url = "https://www.googleapis.com/youtube/v3/videos"
                    params = {
                        'part': 'contentDetails,statistics',
                        'id': ','.join(chunk),
                        'key': self.youtube_api_key
                    }
                    
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'items' in data:
                        for item in data['items']:
                            details = {
                                'duration': self._parse_youtube_duration(item['contentDetails']['duration']),
                                'view_count': int(item['statistics'].get('viewCount', 0))
                            }
                            all_details.append(details)
                    else:
                        # Add empty details for videos that couldn't be fetched
                        all_details.extend([{} for _ in chunk])
                        
                except Exception as e:
                    logger.error(f"Error fetching video details for chunk: {e}")
                    all_details.extend([{} for _ in chunk])
                    
            return all_details
            
        except Exception as e:
            logger.error(f"Error in video details fetch: {e}")
            return [{} for _ in video_ids]
    
    def _parse_youtube_duration(self, duration: str) -> str:
        """Parse YouTube ISO 8601 duration to readable format"""
        if not duration:
            return ""
        
        # Remove PT prefix and parse
        duration = duration.replace('PT', '')
        
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
    
    async def fetch_vimeo_videos(self, category: str, max_results: int = 20) -> List[Dict]:
        """Fetch videos from Vimeo API for specific category"""
        if not self.vimeo_access_token:
            logger.warning("Vimeo access token not configured")
            return []
            
        try:
            # Map our categories to Vimeo search terms
            category_mapping = {
                'health': ['health', 'medical', 'wellness'],
                'entertainment': ['entertainment', 'comedy', 'music'],
                'science': ['science', 'education', 'documentary'],
                'technology': ['technology', 'tech', 'innovation'],
                'business': ['business', 'finance'],
                'politics': ['politics', 'news'],
                'world': ['world', 'international'],
                'sports': ['sports', 'fitness']
            }
            
            search_terms = category_mapping.get(category, [category])
            all_videos = []
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    'Authorization': f'Bearer {self.vimeo_access_token}',
                    'Content-Type': 'application/json'
                }
                
                for term in search_terms[:2]:  # Use first 2 terms
                    try:
                        url = "https://api.vimeo.com/videos"
                        params = {
                            'query': term,
                            'per_page': min(max_results, 10),
                            'sort': 'date',
                            'filter': 'duration',
                            'filter_min': 60,  # Minimum 1 minute
                            'filter_max': 3600  # Maximum 1 hour
                        }
                        
                        response = await client.get(url, params=params, headers=headers)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if 'data' in data:
                            for item in data['data']:
                                video_data = {
                                    'id': f"vimeo:video:{item['uri'].split('/')[-1]}",
                                    'title': item['name'],
                                    'channel_id': item['user']['uri'].split('/')[-1],
                                    'channel_name': item['user']['name'],
                                    'published': datetime.fromisoformat(item['created_time'].replace('Z', '+00:00')),
                                    'url': item['link'],
                                    'embed_url': item['player_embed_url'],
                                    'thumbnail': item['pictures']['sizes'][-1]['link'],
                                    'category': category,
                                    'is_live': False,
                                    'duration': self._format_vimeo_duration(item['duration']),
                                    'view_count': item.get('stats', {}).get('plays', 0),
                                    'description': item.get('description', '')
                                }
                                all_videos.append(video_data)
                    
                    except Exception as e:
                        logger.error(f"Error fetching Vimeo videos for term '{term}': {e}")
                        continue
                        
            return all_videos[:max_results]
            
        except Exception as e:
            logger.error(f"Error in Vimeo API fetch: {e}")
            return []
    
    def _format_vimeo_duration(self, seconds: int) -> str:
        """Format Vimeo duration from seconds to readable format"""
        if not seconds:
            return ""
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    async def fetch_demo_videos(self, category: str, max_results: int = 20) -> List[Dict]:
        """Fetch demo videos for categories that don't have enough content"""
        # This is a fallback method that returns demo videos
        # In a real implementation, you might use other APIs or scrape content
        
        demo_videos = {
            'health': [
                {
                    'id': 'demo:health:1',
                    'title': 'Understanding Mental Health: A Comprehensive Guide',
                    'channel_id': 'demo_channel_1',
                    'channel_name': 'Health & Wellness Channel',
                    'published': datetime.now() - timedelta(hours=2),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'health',
                    'is_live': False,
                    'duration': '15:30',
                    'view_count': 125000,
                    'description': 'Learn about mental health awareness and wellness tips.'
                },
                {
                    'id': 'demo:health:2',
                    'title': 'Nutrition Basics: What Your Body Needs',
                    'channel_id': 'demo_channel_2',
                    'channel_name': 'Nutrition Experts',
                    'published': datetime.now() - timedelta(hours=4),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'health',
                    'is_live': False,
                    'duration': '12:45',
                    'view_count': 89000,
                    'description': 'Essential nutrition information for a healthy lifestyle.'
                }
            ],
            'entertainment': [
                {
                    'id': 'demo:entertainment:1',
                    'title': 'Latest Movie Reviews: Blockbuster Hits',
                    'channel_id': 'demo_channel_3',
                    'channel_name': 'Movie Critics',
                    'published': datetime.now() - timedelta(hours=1),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'entertainment',
                    'is_live': False,
                    'duration': '18:20',
                    'view_count': 250000,
                    'description': 'Reviews of the latest movies and entertainment news.'
                },
                {
                    'id': 'demo:entertainment:2',
                    'title': 'Gaming News: Latest Releases and Updates',
                    'channel_id': 'demo_channel_4',
                    'channel_name': 'Gaming Central',
                    'published': datetime.now() - timedelta(hours=3),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'entertainment',
                    'is_live': False,
                    'duration': '22:15',
                    'view_count': 180000,
                    'description': 'Latest gaming news, reviews, and updates.'
                }
            ],
            'science': [
                {
                    'id': 'demo:science:1',
                    'title': 'The Future of Space Exploration',
                    'channel_id': 'demo_channel_5',
                    'channel_name': 'Science Today',
                    'published': datetime.now() - timedelta(hours=2),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'science',
                    'is_live': False,
                    'duration': '25:40',
                    'view_count': 320000,
                    'description': 'Exploring the latest developments in space technology.'
                },
                {
                    'id': 'demo:science:2',
                    'title': 'Climate Change: Understanding the Science',
                    'channel_id': 'demo_channel_6',
                    'channel_name': 'Environmental Science',
                    'published': datetime.now() - timedelta(hours=5),
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                    'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg',
                    'category': 'science',
                    'is_live': False,
                    'duration': '19:30',
                    'view_count': 150000,
                    'description': 'Scientific analysis of climate change and its impacts.'
                }
            ]
        }
        
        return demo_videos.get(category, [])[:max_results]
    
    async def fetch_all_sources(self, category: str, max_results: int = 20) -> List[Dict]:
        """Fetch videos from all available sources for a category"""
        all_videos = []
        
        # Try YouTube API first
        youtube_videos = await self.fetch_youtube_videos(category, max_results // 2)
        all_videos.extend(youtube_videos)
        
        # Try Vimeo API
        vimeo_videos = await self.fetch_vimeo_videos(category, max_results // 4)
        all_videos.extend(vimeo_videos)
        
        # If we don't have enough videos, add demo videos
        if len(all_videos) < max_results:
            demo_videos = await self.fetch_demo_videos(category, max_results - len(all_videos))
            all_videos.extend(demo_videos)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_videos = []
        for video in all_videos:
            if video['title'] not in seen_titles:
                seen_titles.add(video['title'])
                unique_videos.append(video)
        
        return unique_videos[:max_results]

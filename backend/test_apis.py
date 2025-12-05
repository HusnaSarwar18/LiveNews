#!/usr/bin/env python3
"""
Test script for the new video APIs
"""

import asyncio
import json
from video_apis import VideoAPIs

async def test_video_apis():
    """Test the video APIs for different categories"""
    video_apis = VideoAPIs()
    
    categories = ['health', 'entertainment', 'science']
    
    for category in categories:
        print(f"\n{'='*50}")
        print(f"Testing {category.upper()} category")
        print(f"{'='*50}")
        
        try:
            # Test fetching from all sources
            videos = await video_apis.fetch_all_sources(category, 5)
            
            print(f"Found {len(videos)} videos for {category}")
            
            for i, video in enumerate(videos[:3], 1):
                print(f"\n{i}. {video['title']}")
                print(f"   Channel: {video['channel_name']}")
                print(f"   Duration: {video['duration']}")
                print(f"   Published: {video['published']}")
                print(f"   URL: {video['url']}")
                
        except Exception as e:
            print(f"Error testing {category}: {e}")
    
    print(f"\n{'='*50}")
    print("API Testing Complete")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(test_video_apis())

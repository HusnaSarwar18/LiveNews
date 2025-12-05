#!/usr/bin/env python3
"""
Demo data script for Live News Video Hub
This script populates the database with sample videos for testing.
"""

import asyncio
import random
from datetime import datetime, timedelta
from database import SessionLocal
from models import Video, Channel, Category

# Sample video data for testing
SAMPLE_VIDEOS = [
    {
        "id": "yt:video:dQw4w9WgXcQ",
        "title": "Breaking News: Major Economic Policy Changes Announced",
        "channel_id": "UC16niRr50-MSBwiO3YDb3RA",
        "channel_name": "BBC News",
        "published": datetime.now() - timedelta(hours=2),
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        "category": "world",
        "is_live": False,
        "duration": "5:23",
        "description": "Major economic policy changes have been announced that will affect millions of people worldwide."
    },
    {
        "id": "yt:video:9bZkp7q19f0",
        "title": "LIVE: Presidential Address on Climate Change",
        "channel_id": "UCupvZG-5ko_eiXAupbDfxWw",
        "channel_name": "CNN",
        "published": datetime.now() - timedelta(minutes=30),
        "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "embed_url": "https://www.youtube.com/embed/9bZkp7q19f0",
        "thumbnail": "https://i.ytimg.com/vi/9bZkp7q19f0/hqdefault.jpg",
        "category": "politics",
        "is_live": True,
        "duration": "",
        "description": "Watch live as the President addresses the nation on climate change policies."
    },
    {
        "id": "yt:video:kJQP7kiw5Fk",
        "title": "Tech Review: Latest Smartphone Innovations",
        "channel_id": "UCBJycsmduvYEL83R_U4JriQ",
        "channel_name": "MKBHD",
        "published": datetime.now() - timedelta(hours=4),
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "embed_url": "https://www.youtube.com/embed/kJQP7kiw5Fk",
        "thumbnail": "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
        "category": "technology",
        "is_live": False,
        "duration": "12:45",
        "description": "In-depth review of the latest smartphone innovations and what they mean for consumers."
    },
    {
        "id": "yt:video:ZZ5LpwO-An4",
        "title": "Stock Market Analysis: What's Next for Investors",
        "channel_id": "UCqK_GSMbpiV8spgD3ZGloSw",
        "channel_name": "CNBC",
        "published": datetime.now() - timedelta(hours=6),
        "url": "https://www.youtube.com/watch?v=ZZ5LpwO-An4",
        "embed_url": "https://www.youtube.com/embed/ZZ5LpwO-An4",
        "thumbnail": "https://i.ytimg.com/vi/ZZ5LpwO-An4/hqdefault.jpg",
        "category": "business",
        "is_live": False,
        "duration": "8:12",
        "description": "Expert analysis of current market trends and what investors should expect in the coming weeks."
    },
    {
        "id": "yt:video:OPf0YbXqDm0",
        "title": "Global Weather Update: Extreme Conditions Worldwide",
        "channel_id": "UChqUTb21-2B3e9JqYVHcFpQ",
        "channel_name": "Al Jazeera English",
        "published": datetime.now() - timedelta(hours=1),
        "url": "https://www.youtube.com/watch?v=OPf0YbXqDm0",
        "embed_url": "https://www.youtube.com/embed/OPf0YbXqDm0",
        "thumbnail": "https://i.ytimg.com/vi/OPf0YbXqDm0/hqdefault.jpg",
        "category": "world",
        "is_live": False,
        "duration": "4:56",
        "description": "Latest updates on extreme weather conditions affecting multiple regions around the world."
    },
    {
        "id": "yt:video:1Bix44H1qvY",
        "title": "LIVE: Breaking News Coverage",
        "channel_id": "UCYfdidRxb-B8Ndc0y_QctyQ",
        "channel_name": "Sky News",
        "published": datetime.now() - timedelta(minutes=15),
        "url": "https://www.youtube.com/watch?v=1Bix44H1qvY",
        "embed_url": "https://www.youtube.com/embed/1Bix44H1qvY",
        "thumbnail": "https://i.ytimg.com/vi/1Bix44H1qvY/hqdefault.jpg",
        "category": "world",
        "is_live": True,
        "duration": "",
        "description": "Live coverage of breaking news events as they unfold."
    },
    {
        "id": "yt:video:3YxaaGgTQYM",
        "title": "The Future of Artificial Intelligence",
        "channel_id": "UCsT0YIqwnpJCM-mx7-gSA4Q",
        "channel_name": "TEDx Talks",
        "published": datetime.now() - timedelta(hours=8),
        "url": "https://www.youtube.com/watch?v=3YxaaGgTQYM",
        "embed_url": "https://www.youtube.com/embed/3YxaaGgTQYM",
        "thumbnail": "https://i.ytimg.com/vi/3YxaaGgTQYM/hqdefault.jpg",
        "category": "technology",
        "is_live": False,
        "duration": "18:32",
        "description": "A fascinating talk about the future of AI and its impact on society."
    },
    {
        "id": "yt:video:jNQXAC9IVRw",
        "title": "Political Debate: Key Issues of the Day",
        "channel_id": "UCXIJgqnII2ZOINSWNOGFThA",
        "channel_name": "Fox News",
        "published": datetime.now() - timedelta(hours=3),
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "embed_url": "https://www.youtube.com/embed/jNQXAC9IVRw",
        "thumbnail": "https://i.ytimg.com/vi/jNQXAC9IVRw/hqdefault.jpg",
        "category": "politics",
        "is_live": False,
        "duration": "15:47",
        "description": "Heated debate on the key political issues facing the nation today."
    },
    {
        "id": "yt:video:kJQP7kiw5Fk",
        "title": "Market Watch: Daily Trading Analysis",
        "channel_id": "UCqK_GSMbpiV8spgD3ZGloSw",
        "channel_name": "CNBC",
        "published": datetime.now() - timedelta(hours=5),
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "embed_url": "https://www.youtube.com/embed/kJQP7kiw5Fk",
        "thumbnail": "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
        "category": "business",
        "is_live": False,
        "duration": "10:23",
        "description": "Daily analysis of market movements and trading opportunities."
    },
    {
        "id": "yt:video:ZZ5LpwO-An4",
        "title": "Health Update: Latest Medical Breakthroughs",
        "channel_id": "UCJ5v_MCY6GNUBTO8-D3XoAg",
        "channel_name": "Reuters",
        "published": datetime.now() - timedelta(hours=7),
        "url": "https://www.youtube.com/watch?v=ZZ5LpwO-An4",
        "embed_url": "https://www.youtube.com/embed/ZZ5LpwO-An4",
        "thumbnail": "https://i.ytimg.com/vi/ZZ5LpwO-An4/hqdefault.jpg",
        "category": "health",
        "is_live": False,
        "duration": "6:18",
        "description": "Latest medical breakthroughs and their potential impact on healthcare."
    }
]

def populate_demo_data():
    """Populate database with demo data"""
    try:
        db = SessionLocal()
        
        # Clear existing videos
        db.query(Video).delete()
        print("🗑️  Cleared existing videos")
        
        # Add sample videos
        for video_data in SAMPLE_VIDEOS:
            video = Video(**video_data)
            db.add(video)
        
        db.commit()
        print(f"✅ Added {len(SAMPLE_VIDEOS)} sample videos to database")
        
        # Print summary
        print("\n📊 Demo Data Summary:")
        print(f"Total videos: {db.query(Video).count()}")
        print(f"Live videos: {db.query(Video).filter(Video.is_live == True).count()}")
        print(f"Categories: {db.query(Video.category).distinct().count()}")
        
        # Show videos by category
        categories = db.query(Video.category).distinct().all()
        for category in categories:
            count = db.query(Video).filter(Video.category == category[0]).count()
            print(f"  - {category[0]}: {count} videos")
        
    except Exception as e:
        print(f"❌ Error populating demo data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🎬 Populating database with demo data...")
    populate_demo_data()
    print("\n🎉 Demo data population completed!")
    print("You can now start the application and see sample videos.")

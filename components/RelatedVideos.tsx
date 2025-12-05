'use client';

import { useState, useEffect } from 'react';
import { Video } from '@/types';
import { fetchVideos } from '@/lib/api';
import VideoCard from './VideoCard';
import { Loader2 } from 'lucide-react';

interface RelatedVideosProps {
  currentVideoId: string;
  category: string;
  channelId: string;
}

export default function RelatedVideos({ currentVideoId, category, channelId }: RelatedVideosProps) {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadRelatedVideos = async () => {
      try {
        setLoading(true);
        // Fetch videos from the same category and channel, excluding current video
        const response = await fetchVideos({
          category,
          limit: 10,
        });
        
        // Filter out the current video and limit to 8 videos
        const filteredVideos = response.data
          .filter(video => video.id !== currentVideoId)
          .slice(0, 8);
        
        setVideos(filteredVideos);
      } catch (error) {
        console.error('Failed to load related videos:', error);
      } finally {
        setLoading(false);
      }
    };

    loadRelatedVideos();
  }, [currentVideoId, category, channelId]);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
        Related Videos
      </h3>
      
      {loading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-5 h-5 animate-spin text-primary-500" />
        </div>
      ) : (
        <div className="space-y-3">
          {videos.map((video) => (
            <div key={video.id} className="transform scale-95">
              <VideoCard video={video} />
            </div>
          ))}
          
          {videos.length === 0 && (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              No related videos found
            </div>
          )}
        </div>
      )}
    </div>
  );
}

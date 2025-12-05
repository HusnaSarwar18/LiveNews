'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Video } from '@/types';
import { fetchVideo } from '@/lib/api';
import Header from '@/components/Header';
import VideoPlayer from '@/components/VideoPlayer';
import RelatedVideos from '@/components/RelatedVideos';
import { Loader2 } from 'lucide-react';

export default function WatchPage() {
  const params = useParams();
  const videoId = params.id as string;
  
  const [video, setVideo] = useState<Video | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadVideo = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetchVideo(videoId);
        setVideo(response.data);
      } catch (err) {
        setError('Failed to load video');
        console.error('Error loading video:', err);
      } finally {
        setLoading(false);
      }
    };

    if (videoId) {
      loadVideo();
    }
  }, [videoId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-dark-900">
        <Header />
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center gap-3">
            <Loader2 className="w-6 h-6 animate-spin text-primary-500" />
            <span className="text-gray-600 dark:text-gray-400">Loading video...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error || !video) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-dark-900">
        <Header />
        <div className="container mx-auto px-4 py-12">
          <div className="text-center">
            <div className="text-6xl mb-4">❌</div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Video Not Found
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mb-6">
              {error || 'The video you are looking for does not exist.'}
            </p>
            <a
              href="/"
              className="btn-primary"
            >
              Go Back Home
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-900">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Video Player */}
          <div className="lg:col-span-2">
            <VideoPlayer video={video} />
            
            {/* Video Info */}
            <div className="mt-6 bg-white dark:bg-dark-800 rounded-lg p-6">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                {video.title}
              </h1>
              
              <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                <div className="flex items-center gap-4">
                  <span className="font-medium text-gray-700 dark:text-gray-300">
                    {video.channel.name}
                  </span>
                  <span>
                    {new Date(video.published).toLocaleDateString()}
                  </span>
                </div>
                
                {video.viewCount && (
                  <span>{video.viewCount.toLocaleString()} views</span>
                )}
              </div>
              
              {video.description && (
                <div className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
                  {video.description}
                </div>
              )}
            </div>
          </div>
          
          {/* Related Videos Sidebar */}
          <div className="lg:col-span-1">
            <RelatedVideos 
              currentVideoId={video.id}
              category={video.category}
              channelId={video.channel.id}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

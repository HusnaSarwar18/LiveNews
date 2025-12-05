'use client';

import { Video } from '@/types';
import { useState, useEffect } from 'react';

interface VideoPlayerProps {
  video: Video;
}

export default function VideoPlayer({ video }: VideoPlayerProps) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
  }, [video.id]);

  return (
    <div className="bg-black rounded-lg overflow-hidden">
      <div className="relative w-full aspect-video">
        {isLoading && (
          <div className="absolute inset-0 bg-gray-900 flex items-center justify-center">
            <div className="text-white">Loading video...</div>
          </div>
        )}
        
        <iframe
          src={`${video.embedUrl}?autoplay=0&rel=0&modestbranding=1`}
          title={video.title}
          className="w-full h-full"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
          onLoad={() => setIsLoading(false)}
        />
      </div>
      
      {/* Live indicator overlay */}
      {video.isLive && (
        <div className="absolute top-4 left-4 bg-red-500 text-white text-sm font-semibold px-3 py-1 rounded-full flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse-slow"></div>
          LIVE
        </div>
      )}
    </div>
  );
}

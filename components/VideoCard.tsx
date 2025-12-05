'use client';

import { Video } from '@/types';
import { Clock, Eye, Play } from 'lucide-react';
import Link from 'next/link';

interface VideoCardProps {
  video: Video;
}

export default function VideoCard({ video }: VideoCardProps) {
  const formatTimeAgo = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const formatViewCount = (count?: number) => {
    if (!count) return '';
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
    return count.toString();
  };

  return (
    <Link href={`/watch/${video.id}`} className="block">
      <div className="video-card group cursor-pointer">
        {/* Thumbnail */}
        <div className="video-thumbnail">
          <img
            src={video.thumbnail}
            alt={video.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
          />
          
          {/* Live Badge */}
          {video.isLive && (
            <div className="live-badge">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse-slow"></div>
              <span>LIVE</span>
            </div>
          )}
          
          {/* Play Button Overlay */}
          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center">
            <div className="w-12 h-12 bg-white bg-opacity-90 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <Play className="w-6 h-6 text-gray-900 ml-1" fill="currentColor" />
            </div>
          </div>
          
          {/* Duration */}
          {video.duration && !video.isLive && (
            <div className="absolute bottom-2 right-2 bg-black bg-opacity-80 text-white text-xs px-1 py-0.5 rounded">
              {video.duration}
            </div>
          )}
        </div>

        {/* Video Info */}
        <div className="p-3">
          <h3 className="font-medium text-gray-900 dark:text-white text-sm line-clamp-2 mb-2 group-hover:text-primary-500 transition-colors">
            {video.title}
          </h3>
          
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <span className="font-medium text-gray-700 dark:text-gray-300">
              {video.channel.name}
            </span>
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>{formatTimeAgo(video.published)}</span>
            </div>
          </div>
          
          {video.viewCount && (
            <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400 mt-1">
              <Eye className="w-3 h-3" />
              <span>{formatViewCount(video.viewCount)} views</span>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}

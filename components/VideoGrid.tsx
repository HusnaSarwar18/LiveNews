'use client';

import { Video } from '@/types';
import VideoCard from './VideoCard';
import { Loader2 } from 'lucide-react';

interface VideoGridProps {
  videos: Video[];
  loading: boolean;
  onLoadMore?: () => void;
}

export default function VideoGrid({ videos, loading, onLoadMore }: VideoGridProps) {
  if (loading && videos.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex items-center gap-3">
          <Loader2 className="w-6 h-6 animate-spin text-primary-500" />
          <span className="text-gray-600 dark:text-gray-400">Loading videos...</span>
        </div>
      </div>
    );
  }

  if (!loading && videos.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📺</div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No videos found
        </h3>
        <p className="text-gray-500 dark:text-gray-400">
          Try adjusting your search or category filters
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Video Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
        {videos.map((video) => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>

      {/* Loading More Indicator */}
      {loading && videos.length > 0 && (
        <div className="flex items-center justify-center py-8">
          <div className="flex items-center gap-3">
            <Loader2 className="w-5 h-5 animate-spin text-primary-500" />
            <span className="text-gray-600 dark:text-gray-400">Loading more videos...</span>
          </div>
        </div>
      )}

      {/* Load More Button */}
      {!loading && onLoadMore && videos.length >= 20 && (
        <div className="flex items-center justify-center py-8">
          <button
            onClick={onLoadMore}
            className="btn-secondary flex items-center gap-2"
          >
            Load More Videos
          </button>
        </div>
      )}
    </div>
  );
}

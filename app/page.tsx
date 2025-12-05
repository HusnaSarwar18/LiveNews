'use client';

import { useState, useEffect } from 'react';
import { Video } from '@/types';
import VideoGrid from '@/components/VideoGrid';
import CategoryTabs from '@/components/CategoryTabs';
import SearchBar from '@/components/SearchBar';
import Header from '@/components/Header';
import { useWebSocket } from '@/hooks/useWebSocket';
import { fetchVideos, fetchHealthVideos, fetchEntertainmentVideos, fetchScienceVideos } from '@/lib/api';

export default function HomePage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  // WebSocket connection for real-time updates
  const { connected } = useWebSocket({
    onMessage: (message) => {
      if (message.type === 'new_video' && message.data) {
        setVideos(prev => [message.data, ...prev]);
      }
    },
  });

  useEffect(() => {
    const loadVideos = async () => {
      try {
        setLoading(true);
        let response;
        
        // Use specific API endpoints for categories that need external sources
        if (selectedCategory === 'health') {
          response = await fetchHealthVideos(50);
        } else if (selectedCategory === 'entertainment') {
          response = await fetchEntertainmentVideos(50);
        } else if (selectedCategory === 'science') {
          response = await fetchScienceVideos(50);
        } else {
          // Use the general API for other categories
          response = await fetchVideos({
            category: selectedCategory === 'all' ? undefined : selectedCategory,
            search: searchQuery || undefined,
            limit: 50,
          });
        }
        
        setVideos(response.data);
      } catch (error) {
        console.error('Failed to load videos:', error);
      } finally {
        setLoading(false);
      }
    };

    loadVideos();
  }, [selectedCategory, searchQuery]);

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-900">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        {/* Search and Filters */}
        <div className="mb-6 space-y-4">
          <SearchBar onSearch={handleSearch} />
          <CategoryTabs 
            selectedCategory={selectedCategory}
            onCategoryChange={handleCategoryChange}
          />
        </div>

        {/* Connection Status */}
        {!connected && (
          <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/20 border border-yellow-300 dark:border-yellow-700 rounded-lg">
            <p className="text-yellow-800 dark:text-yellow-200 text-sm">
              🔄 Connecting to live updates...
            </p>
          </div>
        )}

        {/* Video Grid */}
        <VideoGrid 
          videos={videos} 
          loading={loading}
          onLoadMore={() => {
            // Implement infinite scroll
          }}
        />
      </main>
    </div>
  );
}

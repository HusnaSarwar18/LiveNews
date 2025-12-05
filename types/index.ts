export interface Video {
  id: string;
  title: string;
  channel: {
    id: string;
    name: string;
  };
  published: number;
  url: string;
  embedUrl: string;
  thumbnail: string;
  category: string;
  isLive: boolean;
  duration?: string;
  viewCount?: number;
  description?: string;
}

export interface Channel {
  id: string;
  name: string;
  category: string;
  rssUrl: string;
  thumbnail?: string;
  subscriberCount?: number;
}

export interface Category {
  id: string;
  name: string;
  color: string;
  channels: string[];
}

export interface SearchResult {
  videos: Video[];
  total: number;
  query: string;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface WebSocketMessage {
  type: 'new_video' | 'update' | 'error';
  data?: Video | any;
  message?: string;
}

export interface VideoFilters {
  category?: string;
  channel?: string;
  isLive?: boolean;
  search?: string;
  limit?: number;
  offset?: number;
}

import axios from 'axios';
import { Video, VideoFilters, ApiResponse, SearchResult } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const fetchVideos = async (filters: VideoFilters = {}): Promise<ApiResponse<Video[]>> => {
  const params = new URLSearchParams();
  
  if (filters.category) params.append('category', filters.category);
  if (filters.channel) params.append('channel', filters.channel);
  if (filters.isLive !== undefined) params.append('is_live', filters.isLive.toString());
  if (filters.search) params.append('search', filters.search);
  if (filters.limit) params.append('limit', filters.limit.toString());
  if (filters.offset) params.append('offset', filters.offset.toString());

  const response = await api.get(`/api/videos?${params.toString()}`);
  return response.data;
};

export const fetchVideo = async (id: string): Promise<ApiResponse<Video>> => {
  const response = await api.get(`/api/videos/${id}`);
  return response.data;
};

export const searchVideos = async (query: string, limit: number = 20): Promise<ApiResponse<SearchResult>> => {
  const response = await api.get(`/api/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  return response.data;
};

export const fetchChannels = async (): Promise<ApiResponse<any[]>> => {
  const response = await api.get('/api/channels');
  return response.data;
};

export const fetchCategories = async (): Promise<ApiResponse<any[]>> => {
  const response = await api.get('/api/categories');
  return response.data;
};

export const fetchLiveVideos = async (): Promise<ApiResponse<Video[]>> => {
  const response = await api.get('/api/videos/live');
  return response.data;
};

export const fetchExternalVideos = async (category: string, limit: number = 20): Promise<ApiResponse<Video[]>> => {
  const response = await api.get(`/api/videos/external/${category}?limit=${limit}`);
  return response.data;
};

export const fetchHealthVideos = async (limit: number = 20): Promise<ApiResponse<Video[]>> => {
  const response = await api.get(`/api/videos/health?limit=${limit}`);
  return response.data;
};

export const fetchEntertainmentVideos = async (limit: number = 20): Promise<ApiResponse<Video[]>> => {
  const response = await api.get(`/api/videos/entertainment?limit=${limit}`);
  return response.data;
};

export const fetchScienceVideos = async (limit: number = 20): Promise<ApiResponse<Video[]>> => {
  const response = await api.get(`/api/videos/science?limit=${limit}`);
  return response.data;
};

export default api;

'use client';

import { useState } from 'react';

interface CategoryTabsProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const categories = [
  { id: 'all', name: 'All', icon: '📺' },
  { id: 'world', name: 'World', icon: '🌍' },
  { id: 'politics', name: 'Politics', icon: '🏛️' },
  { id: 'business', name: 'Business', icon: '💼' },
  { id: 'technology', name: 'Technology', icon: '💻' },
  { id: 'sports', name: 'Sports', icon: '⚽' },
  { id: 'entertainment', name: 'Entertainment', icon: '🎬' },
  { id: 'health', name: 'Health', icon: '🏥' },
  { id: 'science', name: 'Science', icon: '🔬' },
];

export default function CategoryTabs({ selectedCategory, onCategoryChange }: CategoryTabsProps) {
  const [showMore, setShowMore] = useState(false);

  const visibleCategories = showMore ? categories : categories.slice(0, 6);

  return (
    <div className="w-full">
      <div className="flex flex-wrap gap-2 items-center">
        {visibleCategories.map((category) => (
          <button
            key={category.id}
            onClick={() => onCategoryChange(category.id)}
            className={`category-tab flex items-center gap-2 ${
              selectedCategory === category.id ? 'active' : ''
            }`}
          >
            <span>{category.icon}</span>
            <span>{category.name}</span>
          </button>
        ))}
        
        {categories.length > 6 && (
          <button
            onClick={() => setShowMore(!showMore)}
            className="category-tab flex items-center gap-2"
          >
            <span>{showMore ? '👆' : '👇'}</span>
            <span>{showMore ? 'Less' : 'More'}</span>
          </button>
        )}
      </div>
    </div>
  );
}

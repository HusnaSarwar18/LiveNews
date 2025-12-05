import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Live News Video Hub',
  description: 'YouTube-style live news video aggregator with real-time updates from major news channels',
  keywords: 'news, videos, live, youtube, bbc, cnn, al jazeera, sky news',
  authors: [{ name: 'Live News Video Hub' }],
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        <div className="min-h-full bg-gray-50 dark:bg-dark-900">
          {children}
        </div>
      </body>
    </html>
  );
}

#!/usr/bin/env python3
# extract_news.py - Automated news extraction

import os
import json
import sqlite3
import requests
import feedparser
from datetime import datetime, timedelta
from collections import Counter

NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

RSS_FEEDS = [
    'https://techcrunch.com/category/artificial-intelligence/feed/',
    'https://www.marktechpost.com/feed/',
    'https://feeds.feedburner.com/venturebeat/SZYF',
]

def fetch_newsapi(days_back=7):
    if not NEWS_API_KEY:
        return []
    
    articles = []
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    try:
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': 'artificial intelligence OR machine learning',
            'from': from_date,
            'sortBy': 'publishedAt',
            'apiKey': NEWS_API_KEY,
            'pageSize': 100
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                })
    except Exception as e:
        print(f"NewsAPI error: {e}")
    
    return articles

def fetch_rss():
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:20]:
                articles.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', ''),
                    'url': entry.get('link', ''),
                    'published_at': entry.get('published', ''),
                    'source': feed.feed.get('title', 'RSS'),
                })
        except:
            pass
    return articles

def main():
    print("🔄 Extracting AI news...")
    
    # Fetch from all sources
    all_articles = []
    all_articles.extend(fetch_newsapi(days_back=7))
    all_articles.extend(fetch_rss())
    
    # Deduplicate
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    # Save to database
    conn = sqlite3.connect('ai_news.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT UNIQUE,
            published_at TEXT,
            source TEXT
        )
    ''')
    
    count = 0
    for article in unique_articles:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO articles (title, description, url, published_at, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (article['title'], article['description'], article['url'], 
                  article['published_at'], article['source']))
            count += 1
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print(f"✅ Extracted {count} articles")
    
    # Save summary
    with open('extraction_summary.json', 'w') as f:
        json.dump({
            'total_articles': count,
            'timestamp': datetime.now().isoformat()
        }, f)

if __name__ == '__main__':
    main()

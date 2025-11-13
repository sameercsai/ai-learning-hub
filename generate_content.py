#!/usr/bin/env python3
# generate_content.py - Generate website and newsletter

import os
import json
import sqlite3
from datetime import datetime
from collections import defaultdict

BRANDING = {
    'company_name': 'Cognitive Sprints',
    'tagline': 'AI Learning & Innovation Hub',
    'website': 'https://cognitive-sprints.in',
    'primary_color': '#667eea',
    'secondary_color': '#764ba2',
    'contact_email': 'sameer@cognitive-sprints.in',
}

PRODUCT_KEYWORDS = ['launch', 'release', 'announce', 'unveil', 'introduce']

INDUSTRIES = {
    'Healthcare': ['healthcare', 'medical', 'hospital'],
    'Finance': ['finance', 'banking', 'trading'],
    'Education': ['education', 'learning', 'student'],
    'Retail': ['retail', 'ecommerce', 'shopping'],
}

def classify_articles():
    conn = sqlite3.connect('ai_news.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, url, source FROM articles")
    articles = cursor.fetchall()
    
    products = []
    industry_use_cases = defaultdict(list)
    
    for article_id, title, description, url, source in articles:
        text = f"{title or ''} {description or ''}".lower()
        
        # Check if product
        if sum(1 for kw in PRODUCT_KEYWORDS if kw in text) >= 2:
            products.append({
                'title': title,
                'url': url,
                'source': source,
                'date': 'Recent'
            })
        
        # Classify by industry
        for industry, keywords in INDUSTRIES.items():
            if any(kw in text for kw in keywords):
                industry_use_cases[industry].append({
                    'title': title,
                    'url': url,
                    'description': description
                })
    
    conn.close()
    
    return products, dict(industry_use_cases)

def generate_website(products, industries):
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{BRANDING['company_name']} - AI Learning</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f7fa; }
        .header { background: linear-gradient(135deg, {BRANDING['primary_color']}, {BRANDING['secondary_color']}); 
                  color: white; padding: 3rem 2rem; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .section { margin: 3rem 0; }
        .section-title { font-size: 2rem; color: #333; margin-bottom: 1.5rem; 
                         border-bottom: 3px solid {BRANDING['primary_color']}; padding-bottom: 0.5rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card h3 { color: {BRANDING['primary_color']}; margin-bottom: 1rem; }
        .btn { display: inline-block; padding: 0.6rem 1.2rem; background: {BRANDING['primary_color']}; 
               color: white; text-decoration: none; border-radius: 20px; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 {BRANDING['company_name']}</h1>
        <p>{BRANDING['tagline']}</p>
        <p>Updated: {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    <div class="container">
        <div class="section">
            <h2 class="section-title">🚀 Latest AI Products</h2>
            <div class="grid">
'''
    
    for product in products[:12]:
        html += f'''
                <div class="card">
                    <h3>{product['title'][:80]}</h3>
                    <p><small>{product['source']}</small></p>
                    <a href="{product['url']}" class="btn" target="_blank">Read More →</a>
                </div>
'''
    
    html += '''
            </div>
        </div>
        <div class="section">
            <h2 class="section-title">🏭 AI by Industry</h2>
            <div class="grid">
'''
    
    for industry, items in list(industries.items())[:10]:
        html += f'''
                <div class="card">
                    <h3>{industry}</h3>
                    <p>{len(items)} use cases</p>
                </div>
'''
    
    html += f'''
            </div>
        </div>
    </div>
    <div style="background: #2c3e50; color: white; text-align: center; padding: 2rem;">
        <p>© {datetime.now().year} {BRANDING['company_name']}</p>
        <p><a href="mailto:{BRANDING['contact_email']}" style="color: {BRANDING['primary_color']};">
            {BRANDING['contact_email']}</a></p>
    </div>
</body>
</html>
'''
    
    return html

def generate_newsletter(products, industries):
    newsletter = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Newsletter</title>
</head>
<body style="font-family: Arial; max-width: 600px; margin: 0 auto; background: #f5f7fa;">
    <div style="background: linear-gradient(135deg, {BRANDING['primary_color']}, {BRANDING['secondary_color']}); 
                color: white; padding: 30px; text-align: center;">
        <h1>🤖 {BRANDING['company_name']}</h1>
        <p>{BRANDING['tagline']}</p>
        <p>{datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    <div style="background: white; padding: 30px;">
        <h2 style="color: {BRANDING['primary_color']};">🚀 This Week's Top AI Products</h2>
'''
    
    for i, product in enumerate(products[:5], 1):
        newsletter += f'''
        <div style="padding: 15px; margin: 10px 0; background: #f8f9fa; border-left: 4px solid {BRANDING['primary_color']};">
            <strong>{i}. {product['title'][:80]}</strong><br>
            <small>{product['source']}</small><br>
            <a href="{product['url']}" style="color: {BRANDING['primary_color']};">Read More →</a>
        </div>
'''
    
    newsletter += f'''
        <div style="text-align: center; margin: 30px 0;">
            <a href="https://sameer-ai-hub.netlify.app" 
               style="display: inline-block; padding: 12px 30px; background: {BRANDING['primary_color']}; 
                      color: white; text-decoration: none; border-radius: 25px;">
                Visit Full Hub →
            </a>
        </div>
    </div>
    <div style="background: #2c3e50; color: white; padding: 20px; text-align: center;">
        <p>{BRANDING['company_name']}</p>
        <p><a href="mailto:{BRANDING['contact_email']}" style="color: {BRANDING['primary_color']};">
            {BRANDING['contact_email']}</a></p>
    </div>
</body>
</html>
'''
    
    return newsletter

def main():
    print("🔄 Generating content...")
    
    # Classify articles
    products, industries = classify_articles()
    
    # Generate website
    os.makedirs('public', exist_ok=True)
    website_html = generate_website(products, industries)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(website_html)
    print("✅ Website generated")
    
    # Generate newsletter
    newsletter_html = generate_newsletter(products, industries)
    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(newsletter_html)
    print("✅ Newsletter generated")
    
    # Save metadata
    with open('content_metadata.json', 'w') as f:
        json.dump({
            'products_count': len(products),
            'industries_count': len(industries),
            'generated_at': datetime.now().isoformat()
        }, f)

if __name__ == '__main__':
    main()

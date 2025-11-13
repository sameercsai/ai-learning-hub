# AI Learning Hub - Automated System

## 🤖 Automated Updates

This repository automatically updates every Monday at 9 AM UTC with:
- Latest AI news from multiple sources
- Categorized by industry and technology
- Deployed to Netlify
- Newsletter sent via Mailchimp

## 🔧 Setup

### GitHub Secrets Required:

1. **NEWS_API_KEY**: Get from https://newsapi.org
2. **NETLIFY_AUTH_TOKEN**: Get from Netlify User Settings → Applications
3. **NETLIFY_SITE_ID**: Found in Site Settings → General → Site details
4. **MAILCHIMP_API_KEY**: Get from Mailchimp → Account → Extras → API keys
5. **MAILCHIMP_LIST_ID**: Found in Audience → Settings → Audience name and defaults

## 📁 Files

- `.github/workflows/update.yml` - Automation workflow
- `extract_news.py` - News extraction
- `generate_content.py` - Content generation
- `send_newsletter.py` - Newsletter distribution
- `public/` - Generated website files

## 🚀 Manual Trigger

Go to Actions tab → "Update AI Learning Hub" → "Run workflow"

## 📊 Statistics

- Company: Cognitive Sprints
- Website: https://sameer-ai-hub.netlify.app
- Contact: sameer@cognitive-sprints.in

---
Automated with ❤️ by GitHub Actions

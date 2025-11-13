#!/usr/bin/env python3
# send_newsletter.py - Send via Mailchimp API

import os
import json
import requests

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID', '')

def send_newsletter():
    if not MAILCHIMP_API_KEY or not MAILCHIMP_LIST_ID:
        print("⚠️  Mailchimp credentials not configured")
        return
    
    # Read newsletter
    with open('newsletter.html', 'r') as f:
        newsletter_html = f.read()
    
    # Extract datacenter from API key
    dc = MAILCHIMP_API_KEY.split('-')[-1]
    
    # Create campaign
    url = f'https://{dc}.api.mailchimp.com/3.0/campaigns'
    headers = {
        'Authorization': f'Bearer {MAILCHIMP_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    campaign_data = {
        'type': 'regular',
        'recipients': {'list_id': MAILCHIMP_LIST_ID},
        'settings': {
            'subject_line': f'🤖 Your Weekly AI Update',
            'from_name': 'Cognitive Sprints',
            'reply_to': 'sameer@cognitivesprints.com'
        }
    }
    
    try:
        response = requests.post(url, json=campaign_data, headers=headers)
        if response.status_code == 200:
            campaign = response.json()
            campaign_id = campaign['id']
            
            # Set content
            content_url = f'https://{dc}.api.mailchimp.com/3.0/campaigns/{campaign_id}/content'
            content_data = {'html': newsletter_html}
            requests.put(content_url, json=content_data, headers=headers)
            
            # Send campaign
            send_url = f'https://{dc}.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send'
            requests.post(send_url, headers=headers)
            
            print("✅ Newsletter sent via Mailchimp!")
        else:
            print(f"⚠️  Mailchimp API error: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Error sending newsletter: {e}")

if __name__ == '__main__':
    send_newsletter()

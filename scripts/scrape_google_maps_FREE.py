#!/usr/bin/env python3
"""
FREE Google Maps Scraper for Catio Builders
No API costs - uses Apify free tier ($5 credits/month)

Setup:
1. Create free account: https://apify.com/
2. Get API token: https://console.apify.com/account/integrations
3. Set environment variable: export APIFY_API_TOKEN="your_token"

Usage:
    python3 scrape_google_maps_FREE.py
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict
import requests

# Apify configuration
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
APIFY_ACTOR_ID = 'nwua9Gu5YrADL7ZDj'  # Google Maps Scraper actor

# Search configuration
CITIES = [
    "Portland, OR",
    "Seattle, WA",
    "Vancouver, BC",
    "Eugene, OR",
    "Spokane, WA",
    "Boise, ID",
    # Add more cities as budget allows
]

KEYWORDS = [
    "custom catio builders",
    "catio installation",
    "cat enclosure builders",
]

# Output configuration
OUTPUT_DIR = os.path.expanduser('~/catio-directory/data/raw')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_search_queries() -> List[str]:
    """Generate all search query combinations"""
    queries = []
    for city in CITIES:
        for keyword in KEYWORDS:
            queries.append(f"{keyword} in {city}")
    return queries


def run_apify_scraper(queries: List[str]) -> Dict:
    """
    Run Apify Google Maps Scraper
    
    Free tier: $5 credits/month = ~500-1000 results
    This should cost about $2-3 for 300-600 results
    """
    if not APIFY_API_TOKEN:
        raise ValueError(
            "APIFY_API_TOKEN not set. Get it from https://console.apify.com/account/integrations"
        )
    
    # Apify input configuration
    run_input = {
        "searchStringsArray": queries,
        "maxCrawledPlacesPerSearch": 100,  # Limit per search to stay in budget
        "language": "en",
        "maxReviews": 0,  # Skip reviews to save credits
        "maxImages": 0,  # Skip images to save credits
        "exportPlaceUrls": False,
        "scrapeReviewerName": False,
        "scrapeReviewerId": False,
        "scrapeReviewerUrl": False,
        "scrapeReviewId": False,
        "scrapeReviewUrl": False,
        "scrapeResponseFromOwnerText": False,
    }
    
    print(f"🚀 Starting Apify scraper with {len(queries)} queries...")
    print(f"📊 Expected results: {len(queries) * 50} businesses (estimate)")
    print(f"💰 Estimated cost: $2-3 from free $5 credits")
    print()
    
    # Start the actor run
    response = requests.post(
        f'https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/runs',
        params={'token': APIFY_API_TOKEN},
        json=run_input,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 201:
        raise Exception(f"Failed to start Apify run: {response.text}")
    
    run_data = response.json()['data']
    run_id = run_data['id']
    
    print(f"✅ Run started: {run_id}")
    print(f"🔗 Monitor at: https://console.apify.com/actors/runs/{run_id}")
    print()
    print("⏳ Waiting for scraper to finish (usually 2-5 minutes)...")
    
    # Poll for completion
    while True:
        time.sleep(10)  # Check every 10 seconds
        
        status_response = requests.get(
            f'https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/runs/{run_id}',
            params={'token': APIFY_API_TOKEN}
        )
        
        status_data = status_response.json()['data']
        status = status_data['status']
        
        if status == 'SUCCEEDED':
            print("✅ Scraping complete!")
            break
        elif status in ['FAILED', 'ABORTED', 'TIMED-OUT']:
            raise Exception(f"Scraper failed with status: {status}")
        else:
            print(f"   Status: {status} - still running...")
    
    # Get results
    dataset_id = status_data['defaultDatasetId']
    results_response = requests.get(
        f'https://api.apify.com/v2/datasets/{dataset_id}/items',
        params={'token': APIFY_API_TOKEN, 'format': 'json'}
    )
    
    results = results_response.json()
    
    # Show usage stats
    usage = status_data.get('stats', {})
    print()
    print(f"📊 Results: {len(results)} businesses found")
    print(f"💰 Credits used: ${usage.get('computeUnits', 0):.2f}")
    print()
    
    return results


def save_results(results: List[Dict]):
    """Save results to CSV"""
    import csv
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(OUTPUT_DIR, f'google_maps_scraped_{timestamp}.csv')
    
    if not results:
        print("⚠️ No results to save")
        return
    
    # Define CSV columns
    fieldnames = [
        'name', 'address', 'city', 'state', 'postalCode', 'countryCode',
        'latitude', 'longitude', 'phone', 'website', 'url',
        'categoryName', 'rating', 'reviewsCount', 'plusCode',
        'placeId', 'searchString'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for result in results:
            # Normalize field names
            row = {
                'name': result.get('title', ''),
                'address': result.get('address', ''),
                'city': result.get('city', ''),
                'state': result.get('state', result.get('province', '')),
                'postalCode': result.get('postalCode', ''),
                'countryCode': result.get('countryCode', ''),
                'latitude': result.get('location', {}).get('lat', ''),
                'longitude': result.get('location', {}).get('lng', ''),
                'phone': result.get('phone', ''),
                'website': result.get('website', ''),
                'url': result.get('url', ''),
                'categoryName': result.get('categoryName', ''),
                'rating': result.get('totalScore', ''),
                'reviewsCount': result.get('reviewsCount', 0),
                'plusCode': result.get('plusCode', ''),
                'placeId': result.get('placeId', ''),
                'searchString': result.get('searchString', ''),
            }
            writer.writerow(row)
    
    print(f"✅ Saved {len(results)} results to: {output_file}")
    print()
    print("📁 Next steps:")
    print(f"   1. Review the data: cat {output_file}")
    print(f"   2. Run cleaning script: See 02-claude-code-cleaning.md")
    
    return output_file


def main():
    """Main execution"""
    print("=" * 70)
    print("FREE GOOGLE MAPS SCRAPER - CATIO BUILDERS")
    print("Using Apify free tier ($5 credits/month)")
    print("=" * 70)
    print()
    
    if not APIFY_API_TOKEN:
        print("❌ ERROR: APIFY_API_TOKEN not set")
        print()
        print("Setup instructions:")
        print("1. Create free account: https://apify.com/")
        print("2. Get API token: https://console.apify.com/account/integrations")
        print("3. Run: export APIFY_API_TOKEN='your_token_here'")
        print("4. Re-run this script")
        return
    
    # Build search queries
    queries = build_search_queries()
    print(f"📋 Search queries ({len(queries)} total):")
    for i, query in enumerate(queries, 1):
        print(f"   {i}. {query}")
    print()
    
    # Confirm before scraping
    proceed = input("🚀 Proceed with scraping? This will use ~$2-3 of your free $5 credits. (y/n): ")
    if proceed.lower() != 'y':
        print("Cancelled.")
        return
    
    # Run scraper
    try:
        results = run_apify_scraper(queries)
        save_results(results)
        
        print("=" * 70)
        print("✅ SCRAPING COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print()
        print(f"❌ ERROR: {e}")
        print()
        print("Troubleshooting:")
        print("- Check your API token is correct")
        print("- Verify you have credits remaining: https://console.apify.com/billing")
        print("- Check run logs: https://console.apify.com/actors/runs")


if __name__ == '__main__':
    main()

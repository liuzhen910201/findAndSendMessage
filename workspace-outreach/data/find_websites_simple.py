#!/usr/bin/env python3
import csv
import requests
import time
from urllib.parse import urljoin
import sys

def try_common_urls(company_name):
    """Try common URL patterns for Japanese companies"""
    # Extract company name without corporate type
    name = company_name
    
    # Remove common corporate suffixes
    suffixes = ['株式会社', '合同会社', '有限会社', '合資会社', '合名会社']
    for suffix in suffixes:
        name = name.replace(suffix, '')
    
    # Remove parentheses and their contents
    import re
    name = re.sub(r'\(.*?\)', '', name)
    
    # Clean up whitespace
    name = name.strip()
    
    # Try different URL patterns
    patterns = []
    
    # For names with spaces or special characters
    base_name = name.replace(' ', '').replace('.', '').replace('-', '')
    
    # Common Japanese domains
    patterns.append(f"https://www.{base_name}.co.jp")
    patterns.append(f"https://{base_name}.co.jp")
    patterns.append(f"https://www.{base_name}.jp")
    patterns.append(f"https://{base_name}.jp")
    patterns.append(f"https://www.{base_name}.com")
    patterns.append(f"https://{base_name}.com")
    
    # For companies with "Japan" in name
    if 'Japan' in company_name or 'JAPAN' in company_name:
        jp_name = base_name.replace('Japan', '').replace('JAPAN', '')
        patterns.append(f"https://www.{jp_name}.co.jp")
        patterns.append(f"https://{jp_name}.co.jp")
        patterns.append(f"https://www.{jp_name}.jp")
        patterns.append(f"https://{jp_name}.jp")
    
    return patterns

def check_url(url):
    """Check if URL is accessible"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except:
        return False

def update_csv():
    """Read CSV, try to find websites, and update the file"""
    input_file = '/Users/zhenliu/.openclaw/workspace-outreach/data/input_companies_final.csv'
    
    # Read the CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    
    # Process each row (skip header)
    for i in range(1, len(rows)):
        company_name = rows[i][0]
        current_website = rows[i][1]
        
        print(f"\nProcessing {i}/{len(rows)-1}: {company_name}")
        
        # Skip if already has website URL
        if current_website and current_website.strip():
            print(f"  Already has website: {current_website}")
            continue
        
        # Try common URL patterns
        possible_urls = try_common_urls(company_name)
        print(f"  Trying {len(possible_urls)} URL patterns...")
        
        found_url = None
        for url in possible_urls:
            print(f"    Checking {url}...", end='')
            if check_url(url):
                print(" FOUND!")
                found_url = url
                break
            else:
                print(" not found")
        
        if found_url:
            rows[i][1] = found_url
            print(f"  Found website: {found_url}")
        else:
            print(f"  Could not find website for {company_name}")
        
        # Be polite to servers
        time.sleep(0.5)
    
    # Write back to CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\nUpdated {input_file}")

if __name__ == "__main__":
    update_csv()
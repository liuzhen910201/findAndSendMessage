#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re

def find_contact_page(url):
    """Try to find contact page on a website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for common contact page links (Japanese and English)
        contact_keywords = [
            # Japanese
            'お問い合わせ', '問い合わせ', 'お問合せ', '問合せ', 'お問い合わせフォーム',
            '問い合わせフォーム', 'お問い合わせはこちら', '問い合わせはこちら',
            'お問い合わせページ', '問い合わせページ', 'お問い合わせ先', '問い合わせ先',
            'ご質問・お問い合わせ', 'お問合わせ', '問合わせ',
            # English
            'contact', 'contact-us', 'contactus', 'inquiry', 'inquiries',
            'contact-form', 'contact us', 'get in touch', 'reach us',
            'contact page', 'contact information'
        ]
        
        # Check all links
        for link in soup.find_all('a', href=True):
            link_text = link.get_text().lower()
            href = link['href'].lower()
            
            # Check if link text or href contains contact keywords
            for keyword in contact_keywords:
                if keyword in link_text or keyword in href:
                    # Convert relative URL to absolute
                    contact_url = urljoin(url, link['href'])
                    return contact_url
        
        # Also check for common contact page paths
        common_paths = [
            # Japanese paths
            '/お問い合わせ', '/問い合わせ', '/お問合せ', '/問合せ',
            '/contact', '/contact/', '/contact-us', '/contactus',
            '/inquiry', '/inquiries', '/contact.html',
            '/お問い合わせフォーム', '/問い合わせフォーム'
        ]
        
        for path in common_paths:
            test_url = urljoin(url, path)
            try:
                test_response = requests.head(test_url, headers=headers, timeout=5)
                if test_response.status_code < 400:
                    return test_url
            except:
                continue
                
        # Check meta tags and page content for contact clues
        page_text = soup.get_text().lower()
        for keyword in contact_keywords:
            if keyword in page_text:
                # Try to find the actual link in context
                for link in soup.find_all('a'):
                    link_text = link.get_text().lower()
                    if keyword in link_text:
                        contact_url = urljoin(url, link['href'])
                        return contact_url
                
    except Exception as e:
        print(f"Error processing {url}: {e}")
    
    return None

def update_csv():
    """Read CSV, find contact URLs for websites we have, and update the file"""
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
        website_url = rows[i][1]
        contact_url = rows[i][2]
        
        print(f"\nProcessing {i}/{len(rows)-1}: {company_name}")
        
        # Skip if already has contact URL
        if contact_url and contact_url.strip():
            print(f"  Already has contact URL: {contact_url}")
            continue
        
        # Skip if no website URL
        if not website_url or not website_url.strip():
            print(f"  No website URL, skipping")
            continue
        
        print(f"  Checking website: {website_url}")
        
        # Try to find contact page
        found_contact_url = find_contact_page(website_url)
        
        if found_contact_url:
            rows[i][2] = found_contact_url
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 成功"  # URL备注
            print(f"  Found contact URL: {found_contact_url}")
        else:
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 未找到"  # URL备注
            print(f"  Could not find contact page")
        
        # Update search time
        rows[i][6] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Be polite to servers
        time.sleep(2)
    
    # Write back to CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\nUpdated {input_file}")

if __name__ == "__main__":
    update_csv()
#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re
import sys

def try_direct_access(url):
    """Try to access URL directly with better error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # Try with a longer timeout and allow redirects
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"  Direct access failed: {type(e).__name__}")
        return None

def find_contact_page_from_html(html, base_url):
    """Find contact page from HTML content"""
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for common contact page links (Japanese and English)
    contact_keywords = [
        # Japanese
        'お問い合わせ', '問い合わせ', 'お問合せ', '問合せ', 'お問い合わせフォーム',
        '問い合わせフォーム', 'お問い合わせはこちら', '問い合わせはこちら',
        'お問い合わせページ', '問い合わせページ', 'お問い合わせ先', '問い合わせ先',
        'ご質問・お問い合わせ', 'お問合わせ', '問合わせ', 'お問合せフォーム',
        # English
        'contact', 'contact-us', 'contactus', 'inquiry', 'inquiries',
        'contact-form', 'contact us', 'get in touch', 'reach us',
        'contact page', 'contact information', 'contact-us.html',
        'contact.html', 'inquiry.html', 'contact-form.html'
    ]
    
    # Check all links
    for link in soup.find_all('a', href=True):
        link_text = link.get_text().strip().lower()
        href = link['href'].lower()
        
        # Check if link text or href contains contact keywords
        for keyword in contact_keywords:
            if keyword in link_text or keyword in href:
                # Convert relative URL to absolute
                contact_url = urljoin(base_url, link['href'])
                return contact_url
    
    # Also check for common contact page paths
    common_paths = [
        # Japanese paths
        '/お問い合わせ', '/問い合わせ', '/お問合せ', '/問合せ',
        '/contact', '/contact/', '/contact-us', '/contactus',
        '/inquiry', '/inquiries', '/contact.html', '/contact-us.html',
        '/inquiry.html', '/contact-form.html',
        '/お問い合わせフォーム', '/問い合わせフォーム',
        # Common patterns
        '/company/contact', '/info/contact', '/support/contact',
        '/about/contact', '/services/contact'
    ]
    
    # Check if any of these paths exist in the HTML
    for link in soup.find_all('a', href=True):
        href = link['href']
        for path in common_paths:
            if path in href:
                contact_url = urljoin(base_url, href)
                return contact_url
    
    # Check meta tags and page content for contact clues
    page_text = soup.get_text().lower()
    for keyword in contact_keywords:
        if keyword in page_text:
            # Try to find the actual link in context
            for link in soup.find_all('a'):
                link_text = link.get_text().lower()
                if keyword in link_text:
                    contact_url = urljoin(base_url, link['href'])
                    return contact_url
    
    return None

def try_common_contact_paths(base_url):
    """Try common contact page paths directly"""
    common_paths = [
        '/contact', '/contact/', '/contact-us', '/contactus',
        '/inquiry', '/inquiries', '/contact.html', '/contact-us.html',
        '/inquiry.html', '/contact-form.html',
        # Japanese paths
        '/お問い合わせ', '/問い合わせ', '/お問合せ', '/問合せ',
        '/contact/ja', '/ja/contact', '/jp/contact',
        '/company/contact', '/info/contact', '/support/contact'
    ]
    
    for path in common_paths:
        test_url = urljoin(base_url, path)
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.head(test_url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                return test_url
        except:
            continue
    
    return None

def find_contact_page(url):
    """Main function to find contact page using multiple approaches"""
    print(f"  Finding contact page for: {url}")
    
    # Approach 1: Try direct access and parse HTML
    html = try_direct_access(url)
    if html:
        contact_url = find_contact_page_from_html(html, url)
        if contact_url:
            print(f"    Found via HTML parsing: {contact_url}")
            return contact_url
    
    # Approach 2: Try common contact paths
    contact_url = try_common_contact_paths(url)
    if contact_url:
        print(f"    Found via common paths: {contact_url}")
        return contact_url
    
    # Approach 3: Try to construct likely contact URLs
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Remove www. if present
    if domain.startswith('www.'):
        clean_domain = domain[4:]
    else:
        clean_domain = domain
    
    # Try common contact URL patterns
    patterns = [
        f"https://{domain}/contact",
        f"https://{domain}/contact/",
        f"https://{domain}/contact-us",
        f"https://{domain}/inquiry",
        f"https://www.{clean_domain}/contact",
        f"https://www.{clean_domain}/contact/",
        f"https://www.{clean_domain}/contact-us",
        f"https://www.{clean_domain}/inquiry",
    ]
    
    for pattern in patterns:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.head(pattern, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                print(f"    Found via pattern matching: {pattern}")
                return pattern
        except:
            continue
    
    print(f"    Could not find contact page")
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
        
        # Try to find contact page
        found_contact_url = find_contact_page(website_url)
        
        if found_contact_url:
            rows[i][2] = found_contact_url
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 成功"  # URL备注
            print(f"  ✓ Found contact URL: {found_contact_url}")
        else:
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 未找到"  # URL备注
            print(f"  ✗ Could not find contact page")
        
        # Update search time
        rows[i][6] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Be polite to servers
        time.sleep(3)
    
    # Write back to CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\n✓ Updated {input_file}")

if __name__ == "__main__":
    update_csv()
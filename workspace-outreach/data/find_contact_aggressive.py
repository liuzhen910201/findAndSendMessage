#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re

def find_contact_page_aggressive(url):
    """More aggressive approach to find contact pages"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # First try to get the main page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extended list of contact keywords
        contact_keywords = [
            # Japanese
            'お問い合わせ', '問い合わせ', 'お問合せ', '問合せ', 'お問い合わせフォーム',
            '問い合わせフォーム', 'お問い合わせはこちら', '問い合わせはこちら',
            'お問い合わせページ', '問い合わせページ', 'お問い合わせ先', '問い合わせ先',
            'ご質問・お問い合わせ', 'お問合わせ', '問合わせ', 'お問い合わせ・ご相談',
            '問い合わせ・ご相談', 'お問い合わせ窓口', '問い合わせ窓口',
            'お問い合わせ先・アクセス', '問い合わせ先・アクセス',
            'お問い合わせ/資料請求', '問い合わせ/資料請求',
            # English
            'contact', 'contact-us', 'contactus', 'inquiry', 'inquiries',
            'contact-form', 'contact us', 'get in touch', 'reach us',
            'contact page', 'contact information', 'contact details',
            'get in contact', 'write to us', 'email us', 'call us',
            'support', 'help', 'faq', 'feedback'
        ]
        
        # Strategy 1: Check all links on the page
        all_links = []
        for link in soup.find_all('a', href=True):
            link_text = link.get_text().strip().lower()
            href = link['href'].lower()
            full_url = urljoin(url, link['href'])
            all_links.append((link_text, href, full_url, link))
        
        # Check for exact matches first
        for link_text, href, full_url, link in all_links:
            for keyword in contact_keywords:
                if keyword in link_text or keyword in href:
                    # Verify the link is accessible
                    try:
                        test_response = requests.head(full_url, headers=headers, timeout=5)
                        if test_response.status_code < 400:
                            return full_url
                    except:
                        continue
        
        # Strategy 2: Look for contact information in page text
        page_text = soup.get_text().lower()
        contact_indicators = []
        
        for keyword in contact_keywords:
            if keyword in page_text:
                # Find the context around the keyword
                start = max(0, page_text.find(keyword) - 100)
                end = min(len(page_text), page_text.find(keyword) + 100)
                context = page_text[start:end]
                
                # Look for URLs in the context
                url_pattern = r'https?://[^\s<>"\']+'
                urls_in_context = re.findall(url_pattern, context)
                
                if urls_in_context:
                    for found_url in urls_in_context:
                        try:
                            test_response = requests.head(found_url, headers=headers, timeout=5)
                            if test_response.status_code < 400:
                                return found_url
                        except:
                            continue
        
        # Strategy 3: Check common contact page paths
        common_paths = [
            # Japanese paths
            '/お問い合わせ', '/問い合わせ', '/お問合せ', '/問合せ',
            '/contact', '/contact/', '/contact-us', '/contactus',
            '/inquiry', '/inquiries', '/contact.html',
            '/お問い合わせフォーム', '/問い合わせフォーム',
            '/contact/form', '/contactus/form', '/inquiry/form',
            '/support', '/help', '/faq', '/feedback'
        ]
        
        for path in common_paths:
            test_url = urljoin(url, path)
            try:
                test_response = requests.head(test_url, headers=headers, timeout=5)
                if test_response.status_code < 400:
                    return test_url
            except:
                continue
        
        # Strategy 4: Look for email addresses or phone numbers
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, response.text)
        
        if emails:
            # If we find emails but no contact page, check if there's a mailto: link
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('mailto:'):
                    # Return the page containing the email
                    return url
        
        # Strategy 5: Check sitemap or robots.txt
        try:
            robots_url = urljoin(url, '/robots.txt')
            robots_response = requests.get(robots_url, headers=headers, timeout=5)
            if robots_response.status_code == 200:
                # Look for sitemap in robots.txt
                sitemap_pattern = r'Sitemap:\s*(https?://[^\s]+)'
                sitemaps = re.findall(sitemap_pattern, robots_response.text)
                for sitemap_url in sitemaps:
                    try:
                        sitemap_response = requests.get(sitemap_url, headers=headers, timeout=5)
                        if sitemap_response.status_code == 200:
                            # Parse sitemap for contact pages
                            sitemap_soup = BeautifulSoup(sitemap_response.text, 'xml')
                            for loc in sitemap_soup.find_all('loc'):
                                loc_text = loc.get_text().lower()
                                for keyword in contact_keywords:
                                    if keyword in loc_text:
                                        return loc.get_text()
                    except:
                        continue
        except:
            pass
                
    except Exception as e:
        print(f"Error processing {url}: {e}")
    
    return None

def update_csv():
    """Update CSV with aggressive contact page search"""
    input_file = '/Users/zhenliu/.openclaw/workspace-outreach/data/input_companies_final.csv'
    
    # Read the CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    
    # Process rows that have website but no contact URL
    for i in range(1, len(rows)):
        company_name = rows[i][0]
        website_url = rows[i][1]
        contact_url = rows[i][2]
        
        # Skip if no website or already has contact URL
        if not website_url or not website_url.strip() or (contact_url and contact_url.strip()):
            continue
        
        print(f"\nAggressive search for: {company_name}")
        print(f"  Website: {website_url}")
        
        # Try aggressive search
        found_contact_url = find_contact_page_aggressive(website_url)
        
        if found_contact_url:
            rows[i][2] = found_contact_url
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 成功(深度搜索)"  # URL备注
            print(f"  Found contact URL: {found_contact_url}")
        else:
            rows[i][4] = "已检索"  # URL状态
            rows[i][5] = "检索状态: 深度搜索未找到"  # URL备注
            print(f"  Could not find contact page with aggressive search")
        
        # Update search time
        rows[i][6] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Be polite to servers
        time.sleep(3)
    
    # Write back to CSV
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\nUpdated {input_file}")

if __name__ == "__main__":
    update_csv()
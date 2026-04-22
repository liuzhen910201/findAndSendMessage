---
name: contact-page-search
description: Finds the inquiry/contact page URL for a given company name.
tags: [search, website, contact]
---

# Purpose

Given a company name, find the official inquiry/contact page.

# Steps

1. Search for the company official website
2. Confirm likely official domain
3. Search within the site for pages such as お問い合わせ, Contact, Inquiry
4. Return the best inquiry page URL

# Output

- company_name
- inquiry_page_url
- status
- reason

# Status Values

- FOUND
- NOT_FOUND
- MANUAL_CHECK
- BLOCKED

# Hard Rules

- Prefer official domains only
- Do not return third-party listing sites
- If uncertain, return MANUAL_CHECK

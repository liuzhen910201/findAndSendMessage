---
name: official-site-discovery
description: Identifies the official corporate website for a given company.
tags: [search, website, discovery, company]
---

# Purpose

Find the official corporate site of a company with high confidence.

# Inputs

- company_name
- website_hint (optional)
- industry (optional)

# Steps

1. Search for the company name and official website signals
2. Compare candidate domains
3. Open candidate pages
4. Check branding, corporate profile, legal information, and navigation
5. Select only high-confidence official domain
6. Return manual review when uncertain

# Output

- official_website
- confidence_level
- evidence
- validation_reason

# Do Not

- Do not return third-party directory pages
- Do not treat social media as the official site
- Do not guess when multiple candidates remain unresolved

---
name: contact-page-validation
description: Finds and evaluates the most appropriate inquiry page on an official website.
tags: [contact, inquiry, validation, website]
---

# Purpose

Locate and validate a business-relevant inquiry page on the verified corporate site.

# Inputs

- company_name
- official_website

# Steps

1. Search navigation and footer for contact-related links
2. Open candidate inquiry pages
3. Classify the page purpose
4. Determine whether business outreach is appropriate
5. Return page URL and suitability

# Allowed Page Types

- general_contact
- business_inquiry
- partnership_inquiry
- corporate_contact

# Disallowed Page Types

- customer_support_only
- recruitment_only
- investor_only
- privacy_request_only

# Output

- inquiry_page_url
- inquiry_page_type
- suitability
- validation_reason

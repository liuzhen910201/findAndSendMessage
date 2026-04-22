---
name: excel-intake
description: Validates and reads company outreach input rows from a spreadsheet.
tags: [excel, spreadsheet, intake, validation]
---

# Purpose

Read an outreach spreadsheet and validate required columns before orchestration begins.

# Required Columns

- company_id
- company_name
- partnership_theme
- message_language
- approval_status

# Optional Columns

- website_hint
- industry
- contact_person
- notes

# Steps

1. Open spreadsheet
2. Confirm required headers exist
3. Normalize empty cells
4. Validate company_name is present
5. Validate company_id uniqueness where possible
6. Return normalized row objects

# Output

For each row return:
- company_id
- company_name
- partnership_theme
- message_language
- approval_status
- website_hint
- notes

# Failure Rules

If required columns are missing, stop immediately.
If company_name is empty, mark the row invalid.

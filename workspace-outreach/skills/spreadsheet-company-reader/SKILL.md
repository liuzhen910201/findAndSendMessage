---
name: spreadsheet-company-reader
description: Reads input_companies.xlsx and extracts company names from the company_name column.
tags: [spreadsheet, excel, reader]
---

# Purpose

Read the spreadsheet and identify the company_name column.

# Steps

1. Open input_companies.xlsx
2. Detect header row
3. Find the company_name column
4. Return all non-empty company names with row numbers

# Output

- row_index
- company_name

# Failure Rules

If company_name column is missing, stop immediately and report an error.

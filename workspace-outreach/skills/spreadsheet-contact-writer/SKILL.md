---
name: spreadsheet-contact-writer
description: Writes inquiry page results into a new rightmost column in input_companies.xlsx.
tags: [spreadsheet, excel, writer]
---

# Purpose

Write inquiry page search results back into the spreadsheet.

# Target Column

Preferred new column name:
- inquiry_page_url

If inquiry_page_url already exists:
- update that column
Otherwise:
- append it as the rightmost column

# Steps

1. Open input_companies.xlsx
2. Check whether inquiry_page_url exists
3. If not, add it as the rightmost column
4. Write the URL or status for each row
5. Save the workbook

# Output

- updated_file_path
- updated_rows
- target_column_name

# Hard Rules

- Never modify company_name values
- Never reorder rows
- Never delete existing columns

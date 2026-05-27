---
name: outreach-message-drafting
description: Drafts concise business outreach messages for collaboration inquiries.
tags: [drafting, outreach, japanese, business]
---

# Purpose

Generate a clean and professional inquiry draft for business collaboration outreach.

# Inputs

- company_name
- partnership_theme
- message_language
- target_department (optional)
- notes (optional)

# Draft Rules

- Be polite and concise
- Explain the purpose early
- Mention collaboration or development interest clearly
- Do not overstate capabilities
- Do not mention confidential details not provided in input
- Avoid spam-like marketing language

# Outputs

- drafted_subject
- drafted_message
- draft_version
- language

# Variants

Provide:
- short version for short forms
- standard version for textarea forms


## Content Cleaning Rules

- Never copy raw scraped website text directly into messages.
- Ignore garbled text, mojibake, broken encoding, HTML fragments, CSS, or JavaScript snippets.
- Use only clearly readable Japanese company information.
- Summarize company business naturally before drafting outreach messages.
- If the business description cannot be verified clearly, write:
  「公式サイト上で事業内容を明確に確認できませんでした。」
- Draft messages must sound natural and professional Japanese.
- Do not include unreadable symbols or machine-decoded text in any output field.

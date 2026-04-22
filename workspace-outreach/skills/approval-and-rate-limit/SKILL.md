---
name: approval-and-rate-limit
description: Checks whether a record is approved and safe to send under campaign rules.
tags: [approval, compliance, sending, rate-limit]
---

# Purpose

Ensure that no outreach message is sent without explicit approval and send-safety checks.

# Inputs

- company_id
- approval_status
- campaign_id
- prior_send_history
- cooldown_policy

# Rules

Allow send only when:
- approval_status = approved_to_send
- no duplicate send exists
- cooldown rule is satisfied
- inquiry page suitability is suitable

# Default Cooldown

- Maximum 5 sends per batch
- Minimum 60 seconds between sends
- No resend within the same campaign

# Outputs

- send_eligibility
- denial_reason
- duplicate_status
- cooldown_status

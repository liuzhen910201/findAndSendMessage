# 🤖 AI Outreach System（客户官网 & お問い合わせ 自动化）

## 📌 项目简介

本项目基于 OpenClaw 构建一个 AI Agent 系统，实现：

公司名（Excel）
→ 搜索官网
→ 查找 お問い合わせ 页面
→ 写回 Excel

---

## 🧠 系统架构

main<br>
 ├─ main-orchestrator<br>
 │    ├─ company-researcher<br>
 │    ├─ contact-page-finder<br>
 │    ├─ outreach-drafter<br>
 │    └─ send-review-guard<br>
 │<br>
 └─ contact-url-updater<br>

---

## 📂 Workspace

~/.openclaw/workspace-outreach/

skills/
- spreadsheet-company-reader
- contact-page-search
- spreadsheet-contact-writer

data/
- input_companies.xlsx

---

## 🌐 Brave Search 配置

1. 获取 API Key  
https://api.search.brave.com/

2. 设置环境变量

export BRAVE_SEARCH_API_KEY=你的key

3. 重启

openclaw gateway restart

---

## 🚀 使用方法

输入：

请使用 contact-url-updater 读取 (例如)input_companies_final.csv，
为每个公司补全問い合わせ页面URL

---

## 💰 费用

免费：$5 / 月（≈1000次搜索）

建议：
不要勾选 Override Monthly Spend Limit

---

## ⚠️ 常见问题

- 不返回结果 → restart gateway
- URL 不准确 → 确认 web_search 已启用
- 卡住 → 新建 session

---

## 🎯 结果

Excel新增列：

inquiry_page_url

---

## 👨‍💻 Author

Zhen Liu

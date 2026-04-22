# 🤖 AIアウトリーチシステム（企業公式サイト & お問い合わせ自動取得）

## 📌 概要

本プロジェクトは OpenClaw をベースに構築された AI Agent システムであり、以下の処理を自動化します：

企業名（Excel）
→ 公式サイト検索
→ お問い合わせページ特定
→ Excelへ書き戻し

---

## 🧠 システム構成

main
 ├─ main-orchestrator
 │    ├─ company-researcher
 │    ├─ contact-page-finder
 │    ├─ outreach-drafter
 │    └─ send-review-guard
 │
 └─ contact-url-updater

---

## 📂 ワークスペース構成

~/.openclaw/workspace-outreach/

skills/
- spreadsheet-company-reader
- contact-page-search
- spreadsheet-contact-writer

data/
- input_companies.xlsx

---

## 🌐 Brave Search API 設定（必須）

### なぜ必要か

未設定の場合：
- AIが推測でURLを生成する
- 正確な検索ができない

---

### 設定手順

① APIキー取得  
https://api.search.brave.com/

② 環境変数設定

export BRAVE_SEARCH_API_KEY=あなたのAPIキー

③ 永続化（Mac）

echo 'export BRAVE_SEARCH_API_KEY=あなたのAPIキー' >> ~/.zshrc
source ~/.zshrc

④ Gateway再起動

openclaw gateway restart

---

## 💰 料金

無料枠：$5 / 月（約1000回検索）

※通常の利用では無料範囲内で十分です

---

## 🚀 使用方法

input_companies.xlsx を読み込み、
各企業の問い合わせページURLを検索し、
inquiry_page_url列に書き込みます

---

## 📊 出力結果

Excelに新規カラム追加：

inquiry_page_url

---

## ⚠️ よくある問題

- 応答がない → gateway再起動
- URLが不正確 → web_search確認
- セッションが重い → 新規session作成

---

## 🎯 まとめ

企業リストから自動的に公式サイトとお問い合わせページを取得し、Excelへ反映するAI自動化システム

---

## 👨‍💻 作成者

Zhen Liu

import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "input" / "companies.xlsx"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "companies.json"

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_excel(INPUT_FILE, header=None)

companies = []
for value in df.iloc[:, 0].dropna():
    name = str(value).strip()
    if name and name not in companies:
        companies.append(name)

result = [
    {
        "company_name": name,
        "official_website": "",
        "contact_url": "",
        "company_overview": "",
        "draft_message": "",
        "status": "pending"
    }
    for name in companies
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Loaded {len(result)} companies")
print(f"Output: {OUTPUT_FILE}")

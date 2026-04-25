import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path


BASE_URL = "https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx"
TARGET_CROPS = ["蘋果", "香蕉", "柳橙", "葡萄", "梨"]
OUT_PATH = Path("data/raw/taiwan_main_fruits_2017_to_present.csv")


def roc_date(gregorian_date: date) -> str:
    return f"{gregorian_date.year - 1911:03d}.{gregorian_date.month:02d}.{gregorian_date.day:02d}"


def month_ranges(start_roc_year: int = 106):
    today = date.today()
    current_roc_year = today.year - 1911
    ranges = []
    for year in range(start_roc_year, current_roc_year + 1):
        max_month = today.month if year == current_roc_year else 12
        for month in range(1, max_month + 1):
            start = date(year + 1911, month, 1)
            if year == current_roc_year and month == today.month:
                end = today
            else:
                if month == 12:
                    next_start = date(year + 1912, 1, 1)
                else:
                    next_start = date(year + 1911, month + 1, 1)
                end = next_start - timedelta(days=1)
            ranges.append((roc_date(start), roc_date(end)))
    return ranges


def fetch_rows(crop: str, start_date: str, end_date: str):
    all_rows = []
    skip = 0
    top = 1000
    while True:
        params = {
            "StartDate": start_date,
            "EndDate": end_date,
            "Crop": crop,
            "$top": str(top),
            "$skip": str(skip),
        }
        url = BASE_URL + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=60) as response:
            rows = json.load(response)
        if not rows:
            break
        all_rows.extend(rows)
        if len(rows) < top:
            break
        skip += top
        time.sleep(0.15)
    return all_rows


def main():
    fieldnames = [
        "query_crop",
        "交易日期",
        "種類代碼",
        "作物代號",
        "作物名稱",
        "市場代號",
        "市場名稱",
        "上價",
        "中價",
        "下價",
        "平均價",
        "交易量",
    ]

    collected = []
    for crop in TARGET_CROPS:
        for start_date, end_date in month_ranges():
            rows = fetch_rows(crop, start_date, end_date)
            for row in rows:
                row["query_crop"] = crop
                collected.append({key: row.get(key, "") for key in fieldnames})
            time.sleep(0.15)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(collected)

    print(f"wrote {len(collected)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()

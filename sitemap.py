import csv
import time
from bs4 import BeautifulSoup
import requests

url = "https://www.musashino-u.ac.jp/"

# { url: title }格納用辞書
site_urls = {url: None}

for current_url in list(site_urls.keys()):
    # すでに辞書に格納（タイトル取得済み）されていればスキップ
    if site_urls[current_url] is not None:
        continue

    time.sleep(1)

    try:
        # current_url をリクエスト
        res = requests.get(current_url, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")

        # タイトルを辞書に格納
        site_urls[current_url] = (
            soup.title.text.strip() if soup.title else "タイトルなし"
        )

        # ページ内のURLを辞書に格納
        for a in soup.find_all("a", href=True):
            href = a["href"].split("#")[0]

            if href.startswith("http") and href not in site_urls:
                site_urls[href] = None

    except Exception:
        site_urls[current_url] = "取得失敗"

# CSV出力
with open("result.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    for url_key, title in site_urls.items():
        writer.writerow([title, url_key])

print("保存が完了しました。")
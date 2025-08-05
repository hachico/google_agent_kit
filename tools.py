import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

API_KEY = 'AIzaSyDlpAVkHlV6QJse7fqwsSi78rvYB1n6VnY'  # ここにAPIキーを入力
CX = '87688d3c09a364791'            # ここにカスタム検索エンジンIDを入力

# Google検索ツール（ダミー）
# 実際にはGoogle Search APIを利用しますが、ここではシンプルな例として定義します。
def search_website(company_name: str) -> str:
    """会社の公式ウェブサイトURLをGoogle検索で探します。"""
    # 実際にはAPIを叩いてURLを取得するロジック
    # ここでは仮のURLを返します。
    results = google_search(company_name)
    for item in results:
        #print(f"タイトル: {item['title']}, リンク: {item['link']}")
        return item['link']
'''
    if "グーグル" in company_name:
        return "https://www.google.com/"
    return f"https://www.{company_name.lower().replace(' ', '')}.com/"
'''

# Google検索API
def google_search(query, api_key=API_KEY, cx=CX) -> list:
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
    }
    response = requests.get(url, params=params)
    results = response.json()
    return results.get('items', [])

# ウェブコンテンツ取得ツール
def get_web_content(url: str) -> str:
    """指定されたURLからコンテンツを取得します。JavaScriptでレンダリングされるページにも対応します。"""
    try:
        # Playwrightを使って動的コンテンツをレンダリング
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            content = page.content()
            browser.close()
        
        # BeautifulSoupでHTMLからテキストを抽出
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

    except Exception as e:
        return f"コンテンツ取得エラー: {e}"
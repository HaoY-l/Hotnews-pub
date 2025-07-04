from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from utils.savenews import save_feed_items 

ithome_bp = Blueprint("ithome", __name__, url_prefix="/api/ithome")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://m.ithome.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def get_time(text):
    try:
        # 格式例如：14:00
        today = datetime.today().strftime("%Y-%m-%d")
        dt = datetime.strptime(f"{today} {text.strip()}", "%Y-%m-%d %H:%M")
        return int(dt.timestamp())
    except Exception:
        return None


def replace_link(url, get_id=False):
    match = re.search(r"(?:html|live)/(\d+)\.htm", url)
    if match:
        post_id = match.group(1)
        if get_id:
            return post_id
        return f"https://www.ithome.com/0/{post_id[:3]}/{post_id[3:]}.htm"
    return url


@ithome_bp.route("/", methods=["GET"])
def ithome_main():
    try:
        data = get_list()
        response = {
            "name": "ithome",
            "title": "IT之家",
            "type": "热榜",
            "description": "爱科技，爱这里 - 前沿科技新闻网站",
            "link": "https://m.ithome.com/rankm/",
            "total": len(data),
            "data": data
        }
        # ✅ 存入数据库（hotnews）
        save_feed_items(data, source="ithome", category="热榜")
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": "请求失败", "message": str(e)}), 500


def get_list():
    url = "https://m.ithome.com/rankm/"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select(".rank-box .placeholder")

    data = []
    for item in items:
        a_tag = item.select_one("a")
        href = a_tag["href"] if a_tag and "href" in a_tag.attrs else ""
        post_id = int(replace_link(href, get_id=True)) if href else 100000
        title = item.select_one(".plc-title").get_text(strip=True)
        cover_img = item.select_one("img")
        cover = cover_img["data-original"] if cover_img and "data-original" in cover_img.attrs else ""
        post_time = item.select_one("span.post-time")
        timestamp = get_time(post_time.get_text()) if post_time else None
        hot_text = item.select_one(".review-num").get_text() if item.select_one(".review-num") else ""
        hot = int(re.sub(r"\D", "", hot_text)) if hot_text else 0

        full_url = replace_link(href)

        data.append({
            "id": post_id,
            "title": title,
            "cover": cover,
            "timestamp": timestamp,
            "hot": hot,
            "url": full_url,
            "mobileUrl": full_url
        })
    return data

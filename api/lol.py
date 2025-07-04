from flask import Blueprint, jsonify
import requests
from datetime import datetime
from utils.savenews import save_feed_items 

lol_bp = Blueprint("lol", __name__, url_prefix="/api/lol")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://lol.qq.com/",
    "Connection": "keep-alive",
}

def get_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except Exception:
        return None

@lol_bp.route("/", methods=["GET"])
def lol_main():
    try:
        data = get_list()
        # ✅ 存入数据库（hotnews）
        save_feed_items(data, source="lol", category="更新公告")
        return jsonify({
            "name": "lol",
            "title": "英雄联盟",
            "type": "更新公告",
            "link": "https://lol.qq.com/gicp/news/423/2/1334/1.html",
            "total": len(data),
            "data": data
        })
    except Exception as e:
        return jsonify({"error": "请求失败", "message": str(e)}), 500

def get_list():
    url = (
        "https://apps.game.qq.com/cmc/zmMcnTargetContentList"
        "?r0=json&page=1&num=30&target=24&source=web_pc"
    )
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    items = result.get("data", {}).get("result", [])

    data = []
    for v in items:
        docid = v.get("iDocID")
        data.append({
            "id": docid,
            "title": v.get("sTitle"),
            "cover": f"https:{v.get('sIMG')}",
            "author": v.get("sAuthor"),
            "hot": int(v.get("iTotalPlay", 0)),
            "timestamp": get_time(v.get("sCreated")),
            "url": f"https://lol.qq.com/news/detail.shtml?docid={docid}",
            "mobileUrl": f"https://lol.qq.com/news/detail.shtml?docid={docid}",
        })
    return data

from flask import Blueprint, request, jsonify
import requests
import time
from datetime import datetime
from utils.savenews import save_feed_items

v2ex_bp = Blueprint("v2ex", __name__, url_prefix="/api/v2ex")

TYPE_MAP = {
    "hot": "最热主题",
    "latest": "最新主题",
}

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/122.0.0.0 Safari/537.36"),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

def get_current_time_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

@v2ex_bp.route("/", methods=["GET"])
def get_topics():
    req_type = request.args.get("type", "hot")
    if req_type not in TYPE_MAP:
        req_type = "hot"
    url = f"https://www.v2ex.com/api/topics/{req_type}.json"

    params = {}
    no_cache = request.args.get("noCache", "false").lower() == "true"
    if no_cache:
        params["_"] = int(time.time() * 1000)

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        return jsonify({"error": "请求失败", "message": str(e)}), 500

    data_list = []
    for v in result:
        data_list.append({
            "id": v.get("id"),
            "title": v.get("title"),
            "desc": v.get("content", ""),
            "author": v.get("member", {}).get("username"),
            "timestamp": None,  # API未提供时间，置None
            "hot": v.get("replies", 0),
            "url": v.get("url"),
            "mobileUrl": v.get("url"),
        })

    # 持久化
    save_feed_items(data_list, source="v2ex", category=TYPE_MAP[req_type])

    return jsonify({
        "name": "v2ex",
        "title": "V2EX",
        "type": "主题榜",
        "params": {
            "type": {
                "name": "榜单分类",
                "type": TYPE_MAP,
            }
        },
        "link": "https://www.v2ex.com/",
        "total": len(data_list),
        "data": data_list,
    })

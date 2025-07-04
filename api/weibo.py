from flask import Blueprint, request, jsonify
import requests
import time
from datetime import datetime
from utils.savenews import save_feed_items

weibo_bp = Blueprint("weibo", __name__, url_prefix="/api/weibo")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://s.weibo.com/",
}

def get_time(ts):
    try:
        if ts:
            return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@weibo_bp.route("/", methods=["GET"])
def get_hot_list():
    no_cache = request.args.get("noCache", "false").lower() == "true"
    url = "https://weibo.com/ajax/side/hotSearch"
    if no_cache:
        url += f"?_={int(time.time() * 1000)}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        return jsonify({"error": "请求失败", "message": str(e)}), 500

    list_data = result.get("data", {}).get("realtime", [])
    data_list = []

    for v in list_data:
        word = v.get("word")
        word_scheme = v.get("word_scheme")
        key = word_scheme if word_scheme else f"#{word}"
        url = f"https://s.weibo.com/weibo?q={key}&t=31&band_rank=1&Refer=top"
        data_list.append({
            "id": v.get("mid") or word,
            "title": word,
            "desc": v.get("note") or key,
            "author": v.get("flag_desc"),
            "timestamp": get_time(v.get("onboard_time")),
            "hot": v.get("num"),
            "url": url,
            "mobileUrl": url,
        })

    save_feed_items(data_list, source="weibo", category="热搜榜")

    return jsonify({
        "name": "weibo",
        "title": "微博",
        "type": "热搜榜",
        "description": "实时热点，每分钟更新一次",
        "link": "https://s.weibo.com/top/summary/",
        "total": len(data_list),
        "data": data_list,
    })

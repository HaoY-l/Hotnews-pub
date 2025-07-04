from flask import Blueprint, jsonify
import requests
from utils.tools import get_time
from utils.savenews import save_feed_items  # ✅ 导入保存函数

csdn_bp = Blueprint("csdn", __name__, url_prefix="/api/csdn")

@csdn_bp.route("/", methods=["GET"])
def csdn_main():
    url = "https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=30"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        return jsonify({"error": "请求失败", "message": str(e)}), 500

    data_list = result.get("data", [])
    parsed_list = []
    for item in data_list:
        pic_list = item.get("picList", [])
        cover = pic_list[0] if pic_list else None
        parsed_list.append({
            "id": item.get("productId"),
            "title": item.get("articleTitle"),
            "cover": cover,
            "desc": None,
            "author": item.get("nickName"),
            "timestamp": get_time(item.get("period")),
            "hot": int(item.get("hotRankScore", 0)),
            "url": item.get("articleDetailUrl"),
            "mobileUrl": item.get("articleDetailUrl"),
        })

    # ✅ 保存数据到 SQLite 数据库
    save_feed_items(parsed_list, source="csdn", category="排行榜")

    return jsonify({
        "name": "csdn",
        "title": "CSDN",
        "type": "排行榜",
        "description": "专业开发者社区",
        "link": "https://www.csdn.net/",
        "total": len(parsed_list),
        "data": parsed_list,
    })

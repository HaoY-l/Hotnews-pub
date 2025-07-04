from flask import Blueprint, request, jsonify
from utils.tools import post_json, get_time

kr36_bp = Blueprint("kr36", __name__, url_prefix="/api/36kr")

# 类型映射
type_map = {
    "hot": "人气榜",
    "video": "视频榜",
    "comment": "热议榜",
    "collect": "收藏榜",
}

list_type_map = {
    "hot": "hotRankList",
    "video": "videoList",
    "comment": "remarkList",
    "collect": "collectList",
}


@kr36_bp.route("/hotlist", methods=["GET"])
def get_hotlist():
    req_type = request.args.get("type", "hot")
    no_cache = request.args.get("noCache", "false").lower() == "true"

    if req_type not in type_map:
        return jsonify({"error": "Invalid type"}), 400

    url = f"https://gateway.36kr.com/api/mis/nav/home/nav/rank/{req_type}"
    body = {
        "partner_id": "wap",
        "param": {
            "siteId": 1,
            "platformId": 2
        },
        "timestamp": int(get_time(timestamp=True))
    }

    response = post_json(url, body, no_cache=no_cache)
    if not response or "data" not in response.get("data", {}):
        return jsonify({"error": "Failed to fetch data"}), 500

    raw_list = response["data"]["data"].get(list_type_map[req_type], [])
    parsed_list = []

    for item in raw_list:
        material = item.get("templateMaterial", {})
        parsed_list.append({
            "id": item.get("itemId"),
            "title": material.get("widgetTitle"),
            "cover": material.get("widgetImage"),
            "author": material.get("authorName"),
            "timestamp": get_time(item.get("publishTime")),
            "hot": material.get("statCollect"),
            "url": f"https://www.36kr.com/p/{item.get('itemId')}",
            "mobileUrl": f"https://m.36kr.com/p/{item.get('itemId')}",
        })

    return jsonify({
        "name": "36kr",
        "title": "36氪",
        "type": type_map[req_type],
        "params": {
            "type": {
                "name": "热榜分类",
                "type": type_map
            }
        },
        "link": "https://m.36kr.com/hot-list-m",
        "total": len(parsed_list),
        "data": parsed_list
    })

from flask import Blueprint, jsonify
import requests
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed

refresh_bp = Blueprint("refresh", __name__, url_prefix="/api")

API_LIST = [
    "/api/csdn","/api/ithome", "/api/lol","/api/v2ex","/api/weibo",
]

BASE_URL = "http://127.0.0.1:5000"
DB_PATH = "news.db"

def clear_hotnews_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hotnews;")
        conn.commit()
        conn.close()
        print("🗑️ 已清空 hotnews 表")
    except Exception as e:
        print(f"[ERROR] 清空 hotnews 表失败: {e}")

def call_api(endpoint):
    try:
        url = f"{BASE_URL}{endpoint}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return {"endpoint": endpoint, "status": "success"}
    except Exception as e:
        return {"endpoint": endpoint, "status": "fail", "error": str(e)}

# 用于手动刷新接口调用
@refresh_bp.route("/refresh_all", methods=["GET"])
def refresh_all():
    results = refresh_all_direct()
    return jsonify({"results": results})

# ✅ 用于定时任务（不走 HTTP），并清空旧数据
def refresh_all_direct():
    clear_hotnews_table()  # ✅ 每次刷新前先清空

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(call_api, api): api for api in API_LIST}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    print("✅ [定时刷新] 已完成", len(results), "个接口")
    return results

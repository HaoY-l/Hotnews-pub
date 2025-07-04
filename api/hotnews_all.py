# api/hotnews_all.py

from flask import Blueprint, jsonify
import sqlite3

hotnews_all_bp = Blueprint("hotnews_all", __name__, url_prefix="/api")

DB_PATH = "news.db"

@hotnews_all_bp.route("/hotnews", methods=["GET"])
def get_all_hotnews():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 支持字典形式访问字段
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM hotnews ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        data = [dict(row) for row in rows]
        return jsonify({"code": 0, "message": "ok", "data": data})
    except Exception as e:
        return jsonify({"code": 1, "message": f"查询失败: {str(e)}"})

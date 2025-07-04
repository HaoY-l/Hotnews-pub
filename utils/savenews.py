import sqlite3
from typing import List, Dict

DB_PATH = "news.db"

def save_feed_items(data: List[Dict], source: str, category: str):
    if not data:
        print(f"❗️[{source}] 无数据可写入")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in data:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO hotnews (
                    id, title, desc, cover, author, hot, timestamp, url, mobile_url, source, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("id", "未知"),
                item.get("title", "未知"),
                item.get("desc", "未知"),
                item.get("cover", "未知"),
                item.get("author", "未知"),
                item.get("hot", 0),
                item.get("timestamp", 0),
                item.get("url", "未知"),
                item.get("mobileUrl", "未知"),
                source or "未知",
                category or "未知",
            ))
        except Exception as e:
            print(f"⚠️ 插入失败: {item.get('id', '未知')}, 错误: {e}")

    conn.commit()
    conn.close()
    print(f"✅ 已保存 {len(data)} 条数据到 feed_items（来源: {source}, 分类: {category}）")

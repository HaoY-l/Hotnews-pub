import os
import sqlite3
from flask import Flask
from flask_apscheduler import APScheduler

from api import register_blueprints
from api.refresh_all import refresh_all_direct  # 🧠 定时任务直接调用逻辑，不走 HTTP

DB_PATH = "news.db"

# ========== ✅ 初始化 SQLite 数据库 ==========
def init_db():
    if not os.path.exists(DB_PATH):
        print("🔧 数据库文件不存在，正在创建 news.db...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建 hotnews 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hotnews (
            id TEXT PRIMARY KEY,
            source TEXT,
            category TEXT,
            title TEXT,
            desc TEXT,
            cover TEXT,
            author TEXT,
            hot INTEGER,
            timestamp INTEGER,
            url TEXT,
            mobile_url TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")

# ========== ✅ 创建 Flask 应用 ==========
def create_app():
    app = Flask(__name__)

    # 初始化数据库
    init_db()

    # 注册所有蓝图（API 接口）
    register_blueprints(app)

    # 配置定时任务
    class Config:
        SCHEDULER_API_ENABLED = True
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)

    # 注册每小时定时任务（不走 HTTP）
    scheduler.add_job(
        id="refresh_all_news",
        func=refresh_all_direct,  # 🔄 定时调用逻辑函数
        trigger="interval",
        hours=1
    )
    scheduler.start()
    print("⏰ 定时任务已启动，每小时刷新一次数据")

    return app

# ========== ✅ 运行主程序 ==========
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

# 🔥 HotNews API Service

一个基于 Flask 构建的开源新闻聚合接口平台，整合了知乎、微博、B站、少数派、V2EX 等多个网站的热门信息，可自动抓取、存入 SQLite 数据库，支持定时刷新与 Docker 部署。

---

## ✨ 项目特色

* 🌐 多平台热榜聚合（50+ 热门条目来源）
* 🧠 Flask + APScheduler 定时抓取
* 🗓 支持 SQLite 数据持久化（表名：`hotnews`）
* ⚡ 支持并发刷新，提升爬取效率
* 🐳 提供 Docker 打包运行支持

---

## 📁 项目结构

```
Hotnews/
├── api/                    # 所有数据源 API 蓝图
│   ├── smzdm.py
│   ├── weibo.py
│   ├── zhihu.py
│   └── ...
├── savenews.py            # 数据写入 SQLite 的持久化逻辑
├── refresh_all.py         # 并发刷新所有接口的任务逻辑
├── app.py                 # 主应用入口（Flask + APScheduler）
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml     # Docker Compose 管理脚本
├── .env                   # 环境变量配置（如知乎 Cookie）
└── news.db                # SQLite 本地数据库文件
```

---

## 🚀 快速启动

### 方式 1：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量（.env 文件）
ZHIHU_COOKIE=你的cookie

# 启动应用
python app.py
```

刷新消息接口：

```
GET http://127.0.0.1:5000/api/refresh_all
```
获取消息接口：

```
GET http://127.0.0.1:5000/api/hotnews
```
---

### 方式 2：Docker 启动

```bash
# 构建镜像
docker compose build

# 启动服务（端口默认为 8890）
docker compose up -d
```

---


## 🧠 定时任务说明

通过 APScheduler 实现：

* 默认每小时自动执行一次 `/api/refresh_all`

可按需修改 `app.py` 中的定时配置：

```python
scheduler.add_job(id='refresh_all_job', func=refresh_all_direct, trigger='interval', hours=1)
```

---

## 📦 数据库说明

使用 SQLite 数据库：`news.db`

数据表结构：`hotnews`

| 字段名         | 类型      | 说明      |
| ----------- | ------- | ------- |
| id          | TEXT    | 唯一 ID   |
| source      | TEXT    | 来源名称    |
| category    | TEXT    | 分类（可选）  |
| title       | TEXT    | 标题      |
| desc        | TEXT    | 简介/摘要   |
| cover       | TEXT    | 封面图链接   |
| author      | TEXT    | 作者      |
| hot         | INTEGER | 热度值     |
| timestamp   | INTEGER | 发布时间戳   |
| url         | TEXT    | PC 页面链接 |
| mobile\_url | TEXT    | 移动端链接   |

---


## 🧛‍♂️ 作者信息

* 开发者：Haoyu
* 微信：tomorrow_me-

---


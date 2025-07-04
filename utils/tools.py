import requests
from datetime import datetime


def post_json(url, json_body, no_cache=False):
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        response = requests.post(url, json=json_body, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] POST请求失败: {e}")
        return {}


def get_time(timestamp=None):
    if timestamp:
        return int(datetime.now().timestamp() * 1000)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_json(url, headers=None, no_cache=False):
    try:
        # 如果需要无缓存，可加时间戳参数
        if no_cache:
            if '?' in url:
                url += f"&_={int(time.time() * 1000)}"
            else:
                url += f"?_={int(time.time() * 1000)}"
        resp = requests.get(url, headers=headers or {}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] GET请求失败: {e}")
        return None
    
def parse_chinese_number(ch_num: str) -> float:
    """
    解析中文数字热度字符串，如 '1.2万', '3亿' 转为对应数字
    简单支持 万、亿 单位转换
    """
    if not ch_num:
        return 0
    ch_num = ch_num.strip()
    try:
        if ch_num.endswith("万"):
            return float(ch_num[:-1]) * 1e4
        elif ch_num.endswith("亿"):
            return float(ch_num[:-1]) * 1e8
        else:
            return float(ch_num)
    except Exception:
        return 0
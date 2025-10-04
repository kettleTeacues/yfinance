"""
共通ヘルパー関数
insert_yf.stock_info と insert_yf.stock_history で共用
"""
from datetime import datetime
from typing import Dict, Any, Optional


def safe_get(data: Dict[str, Any], key: str) -> Optional[Any]:
    """辞書から安全に値を取得する（KeyErrorを避ける）"""
    return data.get(key) if data else None


def safe_timestamp_to_str(timestamp: Optional[int]) -> Optional[str]:
    """タイムスタンプを安全に文字列に変換する"""
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(timestamp).isoformat()[:24]
    except (ValueError, TypeError):
        return None

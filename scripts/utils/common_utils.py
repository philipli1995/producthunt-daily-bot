import os
import pytz
from datetime import datetime, timezone, timedelta
from typing import Optional

def convert_to_beijing_time(utc_time_str: str, language: str) -> str:
    """
    将UTC时间字符串转换为北京时间字符串
    
    Args:
        utc_time_str: UTC时间字符串，格式为'%Y-%m-%dT%H:%M:%SZ'
        language: 语言: en/zh
    Returns:
        str: 格式化的北京时间字符串
    """
    try:
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
        beijing_tz = pytz.timezone('Asia/Shanghai')
        beijing_time = utc_time.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
        if language == 'zh':
            return beijing_time.strftime('%Y年%m月%d日 %p%I:%M (北京时间)')
        else:
            return beijing_time.strftime('%Y-%m-%d %p%I:%M (UTC+8 Beijing Time)')
    except Exception as e:
        print(f"时间转换失败: {utc_time_str}, 错误: {e}")
        return utc_time_str




def get_yesterday_date() -> str:
    """
    获取昨天的日期字符串
    
    Returns:
        str: 格式为'YYYY-MM-DD'的日期字符串
    """
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def ensure_directory_exists(directory: str) -> None:
    """
    确保指定目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def format_time_duration(seconds: float) -> str:
    """
    格式化时间持续时间
    
    Args:
        seconds: 秒数
    
    Returns:
        str: 格式化的时间字符串，精确到小数点后2位
    """
    return f"{seconds:.2f} 秒"

def get_current_time_str() -> str:
    """
    获取当前时间的格式化字符串
    
    Returns:
        str: 格式为'YYYY-MM-DD HH:MM:SS'的时间字符串
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
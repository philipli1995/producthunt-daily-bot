import requests
from typing import Optional
from bs4 import BeautifulSoup

def fetch_og_image(url: str) -> str:
    """
    获取网页的Open Graph图片URL
    
    Args:
        url: 网页URL
    
    Returns:
        str: Open Graph图片URL，如果未找到则返回空字符串
    """
    try:
        response = safe_request(url)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                return og_image["content"]
    except Exception as e:
        print(f"获取og:image失败: {url}, 错误: {e}")
    return ""

def safe_request(
    url: str, 
    method: str = "GET", 
    headers: Optional[dict] = None, 
    timeout: int = 10, 
    **kwargs
) -> Optional[requests.Response]:
    """
    安全的HTTP请求封装
    
    Args:
        url: 请求URL
        method: 请求方法，默认为"GET"
        headers: 请求头
        timeout: 超时时间（秒）
        **kwargs: 传递给requests的其他参数
    
    Returns:
        Optional[requests.Response]: 响应对象，如果请求失败则返回None
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url}, 错误: {e}")
        return None

def make_request_with_retry(
    url: str,
    method: str = "GET",
    max_retries: int = 3,
    retry_delay: int = 1,
    **kwargs
) -> Optional[requests.Response]:
    """
    带重试机制的HTTP请求
    
    Args:
        url: 请求URL
        method: 请求方法，默认为"GET"
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
        **kwargs: 传递给requests的其他参数
    
    Returns:
        Optional[requests.Response]: 响应对象，如果所有重试都失败则返回None
    """
    from time import sleep
    
    for attempt in range(max_retries):
        response = safe_request(url, method=method, **kwargs)
        if response is not None:
            return response
        
        if attempt < max_retries - 1:  # 如果不是最后一次尝试
            sleep(retry_delay)
            print(f"重试请求 {attempt + 1}/{max_retries}: {url}")
    
    return None

def parse_html(html_content: str, parser: str = 'html.parser') -> BeautifulSoup:
    """
    解析HTML内容
    
    Args:
        html_content: HTML字符串
        parser: BeautifulSoup解析器类型
    
    Returns:
        BeautifulSoup: 解析后的BeautifulSoup对象
    """
    return BeautifulSoup(html_content, parser)
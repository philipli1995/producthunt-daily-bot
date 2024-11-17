from datetime import datetime, timezone
from typing import List
from .common_utils import ensure_directory_exists
from .ph_utils import Product

def generate_markdown_file(products: List[Product], language: str) -> None:
    """
    生成Markdown内容并保存到data目录
    
    Args:
        products: Product对象列表
        date_str: 日期字符串
        language: 语言: en/zh
    """
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 生成markdown内容
    markdown_content = generate_markdown_content(products, date_today, language)

    # 保存文件
    save_markdown_file(markdown_content, date_today, language)

def generate_markdown_content(products: List[Product], date_today: str, language: str) -> str:
    """
    生成Markdown内容
    
    Args:
        products: Product对象列表
        date_today: 今天的日期字符串
    
    Returns:
        str: 生成的Markdown内容
    """
    if language == 'zh':
        markdown_content = f"# Product Hunt 今日热榜 | {date_today}\n\n"
    else:
        markdown_content = f"# Product Hunt Daily Hot | {date_today}\n\n"
    for rank, product in enumerate(products, 1):
        markdown_content += product.to_markdown(rank, language)
    return markdown_content

def save_markdown_file(content: str, date_today: str, language: str) -> None:
    """
    保存Markdown文件到data目录
    
    Args:
        content: Markdown内容
        date_today: 今天的日期字符串
    """
    ensure_directory_exists(f'data/{language}')
    file_name = f"data/{language}/producthunt-daily-{date_today}.md"

    
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"文件 {file_name} 生成成功并已覆盖。")
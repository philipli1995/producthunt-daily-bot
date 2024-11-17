import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from utils.ph_utils import fetch_product_hunt_data
from utils.markdown_utils import generate_markdown_file

# 加载环境变量
load_dotenv()

def main():
    start_time = datetime.now()
    print(f"开始执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    print(f"开始生成 {date_str} 的热榜数据")

    language = os.getenv('LANGUAGE') if os.getenv('LANGUAGE') else 'en'
    print(f"语言: {language}")

    # 获取Product Hunt数据
    fetch_start = datetime.now()
    num = int(os.getenv('NUM')) if os.getenv('NUM') else 10
    ph_api_key = os.getenv('PH_API_KEY')
    ph_api_secret = os.getenv('PH_API_SECRET')
    print(f"PH_API_KEY: {ph_api_key}")
    print(f"PH_API_SECRET: {ph_api_secret}")
    print(f"开始获取 Product Hunt 数据... 获取 {num} 条数据")
    products = fetch_product_hunt_data(
        num,
        language,
        ph_api_key,
        ph_api_secret
    )
    fetch_end = datetime.now()
    print(f"获取数据完成,耗时: {(fetch_end - fetch_start).total_seconds():.2f} 秒")

    # 生成Markdown文件
    md_start = datetime.now() 
    print("开始生成 Markdown 文件...")

    
    generate_markdown_file(products, language)
    md_end = datetime.now()
    print(f"生成 Markdown 完成,耗时: {(md_end - md_start).total_seconds():.2f} 秒")

    end_time = datetime.now()
    print(f"执行结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds():.2f} 秒")

if __name__ == "__main__":
    main()
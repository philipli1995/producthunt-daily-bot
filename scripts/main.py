import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from utils.ph_utils import fetch_product_hunt_data
from utils.markdown_utils import generate_markdown_file

# 加载环境变量
load_dotenv()

def main():

    # 校验环境变量
    ph_api_key = os.getenv('PH_API_KEY')
    ph_api_secret = os.getenv('PH_API_SECRET')
    if not ph_api_key or not ph_api_secret:
        raise ValueError("错误: 未设置 PH_API_KEY 或 PH_API_SECRET 环境变量。请在 GitHub Actions secrets 中设置这些值。")

    num = int(os.getenv('NUM')) if os.getenv('NUM') else 10
    language = os.getenv('LANGUAGE') if os.getenv('LANGUAGE') else 'en'
    print(f"语言: {language}")

    # 记录开始时间
    start_time = datetime.now()
    print(f"开始执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    print(f"开始生成 {date_str} 的热榜数据")

    

    languages = language.split(',')

    for language in languages:
        print(f"开始获取 Product Hunt 数据... 语言：{language} 取 {num} 条数据")
        start = datetime.now()

        # 获取Product Hunt数据
        products = fetch_product_hunt_data(
            num,
            language,
            ph_api_key,
            ph_api_secret
        )

        # 生成Markdown文件
        print(f"获取{language}数据完成, 开始生成 Markdown 文件...")
        generate_markdown_file(products, language)


        end = datetime.now()
        print(f"生成 {language} Markdown 完成,耗时: {(end - start).total_seconds():.2f} 秒")


    end_time = datetime.now()
    print(f"执行结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds():.2f} 秒")

if __name__ == "__main__":
    main()
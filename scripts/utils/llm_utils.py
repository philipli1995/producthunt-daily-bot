import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI客户端初始化
client = OpenAI(
    base_url=os.getenv('OPENAI_BASE_URL'),
    api_key=os.getenv('OPENAI_API_KEY')
)

def generate_ai_keywords(name: str, tagline: str, description: str, language: str) -> str:
    """
    使用AI生成关键词
    
    Args:
        name: 产品名称
        tagline: 产品标语
        description: 产品描述
    
    Returns:
        str: 生成的关键词字符串，用逗号分隔
    """
    prompt = f"根据以下内容生成适合的{language}关键词，用英文逗号分隔开：\n\n产品名称：{name}\n\n标语：{tagline}\n\n描述：{description}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Generate suitable keywords in language {language} based on the product information provided. The keywords should be separated by commas and in the language {language}."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
            temperature=0.7,
        )
        keywords = response.choices[0].message.content.strip()
        if ',' not in keywords:
            keywords = ', '.join(keywords.split())
        return keywords
    except Exception as e:
        print(f"Error occurred during keyword generation: {e}")
        return "无关键词"

def translate_with_ai(text: str, language: str) -> str:
    """
    使用AI翻译文本
    
    Args:
        text: 需要翻译的文本
        language: 语言: en/zh
    Returns:
        str: 翻译后的文本
    """
    try:
        response = client.chat.completions.create(
            extra_headers={
                #  Site url for including your app on openrouter.ai rankings.
                "HTTP-Referer": "https://aibest.tools",
                #  Site name shows in rankings on openrouter.ai.
                "X-Title": "AI Best Tools",
            },
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"你是世界上最专业的翻译工具，擅长多种语言的翻译。你是一位精通{language}语言的专业翻译，尤其擅长将IT公司黑话和专业词汇翻译成简洁易懂的地道表达。你的任务是将以下内容翻译成地道的语言：{language}，风格与科普杂志或日常对话相似。"},
                {"role": "user", "content": text},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error occurred during translation: {e}")
        return text
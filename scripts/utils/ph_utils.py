from datetime import datetime, timezone
from typing import List
from .common_utils import convert_to_beijing_time
from .web_utils import fetch_og_image, safe_request
from .llm_utils import generate_ai_keywords, translate_with_ai
from datetime import timedelta

class Product:
    def __init__(self, id: str, name: str, tagline: str, description: str, 
                 votesCount: int, createdAt: str, featuredAt: str, 
                 website: str, url: str, language: str, **kwargs):
        """
        初始化Product对象
        
        Args:
            id: 产品ID
            name: 产品名称
            tagline: 产品标语
            description: 产品描述
            votesCount: 投票数
            createdAt: 创建时间
            featuredAt: 精选时间
            website: 产品网站
            url: Product Hunt URL
            language: 语言: en/zh
            **kwargs: 其他参数
        """
        self.name = name
        self.tagline = tagline
        self.description = description
        self.votes_count = votesCount
        self.created_at = convert_to_beijing_time(createdAt, language)
        if (language == 'zh'):
            self.featured = "是" if featuredAt else "否"
        else:
            self.featured = "Yes" if featuredAt else "No"
        self.website = website
        self.url = url
        self.language = language
        self.og_image_url = fetch_og_image(self.url)
        self.keyword = generate_ai_keywords(self.name, self.tagline, self.description, self.language)
        self.translated_tagline = translate_with_ai(self.tagline, self.language)
        self.translated_description = translate_with_ai(self.description, self.language)

    def to_markdown(self, rank: int, language: str) -> str:
        """
        生成产品的Markdown格式内容
        
        Args:
            rank: 产品排名
            language: 语言: en/zh
        
        Returns:
            str: Markdown格式的产品信息
        """
        og_image_markdown = f"![{self.name}]({self.og_image_url})"
        if language == 'zh':
            return (
                f"## [{rank}. {self.name}]({self.url})\n"
                f"**标语**：{self.translated_tagline}\n"
                f"**介绍**：{self.translated_description}\n"
                f"**产品网站**: [立即访问]({self.website})\n"
                f"**Product Hunt详情**: [访问Product Hunt详情]({self.url})\n\n"
                f"{og_image_markdown}\n\n"
                f"**关键词**：{self.keyword}\n"
                f"**票数**: 🔺{self.votes_count}\n"
                f"**是否精选**：{self.featured}\n"
                f"**发布时间**：{self.created_at}\n\n"
                f"---\n\n"
            )
        else:
            return (
                f"## [{rank}. {self.name}]({self.url})\n"
                f"**Tagline**：{self.tagline}\n"
                f"**Description**：{self.description}\n"
                f"**Website**：[Visit Website]({self.website})\n"
                f"**Product Hunt**：[View on Product Hunt]({self.url})\n\n"
                f"{og_image_markdown}\n\n"
                f"**Keywords**：{self.keyword}\n"
                f"**Votes**：🔺{self.votes_count}\n"
                f"**Featured**：{self.featured}\n"
                f"**Posted**：{self.created_at}\n\n"
                f"---\n\n"
            )

def get_producthunt_token(api_key: str, api_secret: str) -> str:
    """获取Product Hunt的access_token"""
    url = "https://api.producthunt.com/v2/oauth/token"
    payload = {
        "client_id": api_key,
        "client_secret": api_secret,
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/json"}
    
    response = safe_request(url, method="POST", json=payload, headers=headers)
    if not response:
        raise Exception("Failed to obtain access token")
    
    return response.json().get("access_token")

def fetch_product_hunt_data(num: int, language: str, api_key: str, api_secret: str) -> List[Product]:
    """
    从Product Hunt获取数据并返回Product对象列表
    
    Args:
        num: 获取的产品数量
        language: 语言: en/zh
        api_key: Product Hunt API Key
        api_secret: Product Hunt API Secret
    
    Returns:
        List[Product]: Product对象列表
    """
    token = get_producthunt_token(api_key, api_secret)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    base_query = """
    {
      posts(order: VOTES, postedAfter: "%sT00:00:00Z", postedBefore: "%sT23:59:59Z", after: "%s") {
        nodes {
          id
          name
          tagline
          description
          votesCount
          createdAt
          featuredAt
          website
          url
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """

    all_posts = []
    has_next_page = True
    cursor = ""

    while has_next_page and len(all_posts) < num:
        query = base_query % (date_str, date_str, cursor)
        response = safe_request(url, method="POST", headers=headers, json={"query": query})
        
        if not response:
            raise Exception("Failed to fetch data from Product Hunt")

        data = response.json()['data']['posts']
        posts = data['nodes']
        all_posts.extend(posts)

        has_next_page = data['pageInfo']['hasNextPage']
        cursor = data['pageInfo']['endCursor']

    # 排序并只返回前num个产品
    sorted_posts = sorted(all_posts, key=lambda x: x['votesCount'], reverse=True)[:num]
    return [Product(**post, language=language) for post in sorted_posts]
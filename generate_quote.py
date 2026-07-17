import requests
import random
import os

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_random_quote():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    
    quotes = []
    for result in data.get("results", []):
        properties = result.get("properties", {})
        
        content = ""
        if "Name" in properties and properties["Name"]["title"]:
            content = properties["Name"]["title"][0]["plain_text"]
            
        author = ""
        if "Author" in properties and properties["Author"].get("rich_text"):
            author = properties["Author"]["rich_text"][0]["plain_text"]
            
        if content:
            quotes.append({"content": content, "author": author})
            
    return random.choice(quotes) if quotes else {"content": "目前沒有語錄，請至 Notion 新增！", "author": ""}

def generate_html(quote_data):
    # 高質感極簡風 HTML/CSS 模板
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Quote</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f4f4f5;
                font-family: 'Noto Serif TC', serif;
                color: #27272a;
            }}
            .card {{
                background: white;
                padding: 4rem 5rem;
                border-radius: 16px;
                box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
                max-width: 800px;
                width: 85%;
                text-align: center;
                position: relative;
            }}
            .quote-mark {{
                font-size: 8rem;
                color: #f4f4f5;
                position: absolute;
                top: -10px;
                left: 30px;
                font-family: Arial, sans-serif;
                line-height: 1;
            }}
            .content {{
                font-size: 2.2rem;
                line-height: 1.6;
                margin-bottom: 2rem;
                font-weight: 700;
                position: relative;
                z-index: 1;
            }}
            .author {{
                font-size: 1.3rem;
                color: #71717a;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="quote-mark">“</div>
            <div class="content">{quote_data['content']}</div>
            <div class="author">{f"— {quote_data['author']}" if quote_data['author'] else ""}</div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    quote = get_random_quote()
    generate_html(quote)

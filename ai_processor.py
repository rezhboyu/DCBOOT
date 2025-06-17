import openai
import os
from dotenv import load_dotenv
import json
import datetime

# 載入環境變數
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def processNaturalLanguage(text):
    """
    使用 OpenAI 解析自然語言，提取事件詳情
    返回：包含事件詳情的字典
    """
    now=datetime.datetime.now()
    prompt = f"""
    你是一個事件資訊提取器，只會回傳 JSON 格式
    請不要使用json或'''標籤
    需要可直接使用json.loads處理的格式
    請解析以下自然語言描述，提取事件詳情並以 JSON 格式返回。
    包含以下欄位：
    - summary: 事件標題
    - start_time: 開始時間 (ISO 8601 格式，例: 2025-06-12T10:00:00+08:00)
    - end_time: 結束時間 (ISO 8601 格式，假設事件持續 1 小時如果未指定)
    - location: 地點 (如果未指定則為空字串)
    - description: 描述 (如果未指定則為空字串)
    假如沒有確切日期，使用{now}作為參考
    假如沒有開始與結束時間則設定為全天
    輸入：{text}

    如果無法解析，請返回 null。
    """

    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一個專業的事件解析助手，專注於提取日曆事件詳情。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # 提取 AI 回應
        result = response.choices[0].message.content.strip()
        print("OpenAI 回應：",result)
        event_details = json.loads(result)
        print("event_details:", event_details)

        # 驗證必要欄位
        if not all(key in event_details for key in ["summary", "start_time", "end_time"]):
            return None

        return event_details
    except Exception as e:
        print(f"AI 處理錯誤：{e}")

        return None
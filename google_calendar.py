from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_calendar_event(summary, start_time, end_time, location="", description=""):
    """
    在 Google Calendar 中建立事件
    返回：事件連結
    """
    # 載入或建立憑證
    creds = None
    if os.path.exists("googleToken.json"):
        creds = Credentials.from_authorized_user_file("googleToken.json", SCOPES)
    
    # 如果憑證無效或不存在，進行授權
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # 保存憑證
        with open("googleToken.json", "w") as token:
            token.write(creds.to_json())

    try:
        # 建立 Google Calendar 服務
        service = build("calendar", "v3", credentials=creds)

        # 建立事件
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Taipei",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Taipei",
            },
        }

        # 插入事件
        event = service.events().insert(calendarId="primary", body=event).execute()
        return event.get("htmlLink")
    except Exception as e:
        raise Exception(f"Google Calendar 錯誤：{e}")
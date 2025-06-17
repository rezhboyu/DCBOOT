import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from ai_processor import processNaturalLanguage
from google_calendar import create_calendar_event
import yt_dlp
import asyncio
from YTUi import MusicView,playMusic
#.\venv\Scripts\activate.ps1
# 載入環境變數
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 設定 Discord Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'已登入為 {bot.user}')

# 防止處理機器人自己的訊息
@bot.event
async def on_message(message):
    if message.author == bot.user:  # 忽略自己的訊息
        return
    await bot.process_commands(message)  # 處理指令

@bot.command()
# 當訊息以 !schedule 開頭
async def schedule(ctx, *, user_input):  # 使用 * 捕獲完整輸入
    if not user_input:
        await ctx.send("請提供事件描述，例如：`!schedule 明天上午10點開會`")
        return

    try:
        # 使用 AI 處理自然語言
        event_details = processNaturalLanguage(user_input)
        if not event_details:
            print(f"OpenAI 回應：{user_input}")
            await ctx.send("無法解析事件，請提供更清晰的描述")
            return

        # 建立 Google Calendar 事件
        event_url = create_calendar_event(
            summary=event_details["summary"],
            start_time=event_details["start_time"],
            end_time=event_details["end_time"],
            location=event_details.get("location", ""),
            description=event_details.get("description", "")
        )

        # 回應用戶
        await ctx.send(f"事件已建立！查看：{event_url}")
    except Exception as e:
        await ctx.send(f"發生錯誤：{str(e)}")

#提取UI系統


@bot.command()
async def play(ctx, url):
    title = await playMusic(ctx, url)
    view = MusicView()  # 使用獨立的 UI 類
    await ctx.send(f'正在播放：{title}', view=view)

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("已停止並斷開連線")
    else:
        await ctx.send("我不在語音頻道中！")

@bot.command()
async def download(ctx,url):
    title = await playMusic(ctx, url)
    view = download()  # 使用獨立的 UI 類
    await ctx.send(f'正在播放：{title}', view=view)
# 啟動機器人
bot.run(DISCORD_TOKEN)
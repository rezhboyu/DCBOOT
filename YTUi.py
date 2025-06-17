# ui.py
import discord
import yt_dlp
class MusicView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="播放", style=discord.ButtonStyle.green, emoji="▶️")
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("已恢復播放！", ephemeral=True)
        else:
            await interaction.response.send_message("已播放或無音樂可恢復！", ephemeral=True)

    @discord.ui.button(label="暫停", style=discord.ButtonStyle.blurple, emoji="⏸️")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("已暫停播放！", ephemeral=True)
        else:
            await interaction.response.send_message("目前無播放！", ephemeral=True)

    @discord.ui.button(label="跳過", style=discord.ButtonStyle.red, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("已跳過！", ephemeral=True)
        else:
            await interaction.response.send_message("目前無播放！", ephemeral=True)

    @discord.ui.button(label="循環", style=discord.ButtonStyle.gray, emoji="🔁")
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("循環功能暫未實現！", ephemeral=True)

async def playMusic(ctx, url):
    if not ctx.author.voice:
        await ctx.send("請先加入語音頻道！")
        return
    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        title = info['title']
    audio_source = discord.FFmpegPCMAudio(url2, options='-vn')
    ctx.voice_client.play(audio_source)
    return title
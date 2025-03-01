import os
import discord
from discord.ui import Button, View
from discord.ext import commands, tasks
import random

from myserver import server_on

GUILD_ID = 1320391859322753075
CHANNEL_ID = 1320391859754897484
WEBHOOK_URL = 'https://discord.com/api/webhooks/1324846311526109285/i9iwmQ6SBJxSx7V5ewfVYbXnbGI_i_qAc_bBD6aZFsX8jCE_M0RyLj3JNrYHCibrLQ-f'

# สร้างบอท
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

streaming_status = [
    "Playing a game 🎮",
    "Chatting with users 💬",
    "Helping with support tickets 📝",
    "SHGOP SHOP NO.1 🎥",
    "Playing music 🎶"
]

@tasks.loop(seconds=30)
async def update_stream_status():
    status = random.choice(streaming_status) 
    await bot.change_presence(activity=discord.Game(name=status))

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.open_ticket_button = Button(label="🤍เปิดตั๋วคุยแอดมิน❤", style=discord.ButtonStyle.green)
        self.open_ticket_button.callback = self.open_ticket
        self.add_item(self.open_ticket_button)

    async def open_ticket(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Support")
        
        if not category:
            category = await guild.create_category("Support")

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),  
                interaction.user: discord.PermissionOverwrite(read_messages=True), 
            }
        )

        embed = discord.Embed(
            title=f"❤เปิดตั๋วคุยแอดมิน🤍",
            description=f"สวัสดี {interaction.user.mention} 🧇คุณสามารถคุยกับแอดมินที่นี่ได้เลย👑",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

        close_button = Button(label="🥗ปิดตั๋ว❄", style=discord.ButtonStyle.red)
        async def close_ticket(interaction: discord.Interaction):
            await channel.send("💞ตั๋วนี้จะถูกปิดเนื่องจากคำขอของผู้ใช้ หรือแอดมิน🍜")
            await channel.delete()
        close_button.callback = close_ticket

        await channel.send("💩หากคุณต้องการปิดตั๋วนี้ กรุณากดปุ่มด้านล่าง💩", view=View().add_item(close_button))
        await interaction.response.send_message("❄🧊คุณได้เปิดตั๋วแล้ว! รอแอดมินตอบกลับ🧊", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not update_stream_status.is_running():
        update_stream_status.start()
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🧊 สวัสดี! 🥙",
            description="🍟>ตอนนี้บอทของเราพร้อมให้บริการแล้ว! ⚡\n\n"
                        "🥇หากคุณต้องการเปิดตั๋วเพื่อคุยกับแอดมิน โปรดกดปุ่มด้านล่าง 👇",
            color=discord.Color.blue()
        )
        view = TicketView()
        await channel.send(embed=embed, view=view)

server_on()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("[ERROR] TOKEN not found in environment variables!")
else:
    bot.run(TOKEN)

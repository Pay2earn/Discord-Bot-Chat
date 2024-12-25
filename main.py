import os
import asyncio
import discord
from discord.ext import commands

# โหลด token และข้อความจาก environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
REPLY_MESSAGE = os.getenv('REPLY_MESSAGE', 'Hallo bang')  # ใช้ค่าดีฟอลต์ 'Hallo bang' ถ้าไม่มีใน env
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 111111))  # เปลี่ยนเป็น ID ของช่องที่คุณต้องการ
DELAY = int(os.getenv('DELAY', 15))  # ตั้งเวลาให้ดึงจาก env หรือ 15 ถ้าไม่มี
BLACKLIST_FILE = 'blacklist.txt'

# ดึง MAIN_MESSAGES จาก environment variable และแปลงเป็นรายการข้อความ
MAIN_MESSAGES = os.getenv('MAIN_MESSAGES', '').split(',')  # แยกข้อความด้วยเครื่องหมาย ',' ถ้าไม่พบค่าจะเป็น list ว่าง

# เริ่มต้น Bot
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# โหลด blacklist ลงในหน่วยความจำ
def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE, 'r', encoding='UTF-8') as file:
        return set(line.strip() for line in file)

blacklist = load_blacklist()

@bot.event
async def on_ready():
    print(f'เข้าสู่ระบบสำเร็จ: {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        for msg in MAIN_MESSAGES:
            if msg:  # ตรวจสอบให้แน่ใจว่าไม่เป็นข้อความว่าง
                sent_message = await channel.send(msg)
                print(f'ส่งข้อความ: {msg}')
                await asyncio.sleep(DELAY)
                await sent_message.delete()

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        if str(message.author.id) not in blacklist:
            sent_message = await message.reply(REPLY_MESSAGE)
            print(f'ตอบกลับ {message.author.name}')
            await asyncio.sleep(DELAY)
            await sent_message.delete()
            # เพิ่มผู้ใช้ลงใน blacklist
            blacklist.add(str(message.author.id))
            with open(BLACKLIST_FILE, 'a', encoding='UTF-8') as file:
                file.write(f'{message.author.id}\n')

# รัน Bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("ไม่พบ token ของ bot กรุณาตั้งค่า DISCORD_BOT_TOKEN ใน environment variable.")

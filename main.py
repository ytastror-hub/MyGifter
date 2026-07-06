import os
import discord
from discord.ext import commands

# 1. إعداد المسارات لضمان العثور على الملف في أي بيئة استضافة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "minecraft.txt")

# 2. الإعدادات
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# ضع الـ IDs الخاصة بالأونر والكرييتور هنا
ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] 

def is_admin(ctx):
    return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)

# دالة قراءة الملف
def get_accounts():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# دالة الحذف وتحديث الملف (جوهر النظام)
def update_accounts(accounts):
    with open(FILE_PATH, "w") as f:
        f.write("\n".join(accounts))

@bot.event
async def on_ready():
    # وضع حالة DND
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print(f'✅ {bot.user} يعمل الآن. ملف الحسابات: {FILE_PATH}')

# --- الأوامر ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 قائمة الأوامر", color=0x00FF99)
    embed.add_field(name="🛠️ الإدارة", value="`!send @member [amount]`, `!drop [amount]`", inline=False)
    embed.add_field(name="ℹ️ معلومات", value="`!stock`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def stock(ctx):
    count = len(get_accounts())
    await ctx.send(f"📦 | المتوفر حالياً في المخزون: `{count}` حساب.")

@bot.command()
async def send(ctx, member: discord.Member, amount: int = 1):
    if not is_admin(ctx): return await ctx.send("🚫 | للأونر والكرييتور فقط!")
    
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | الحسابات غير كافية!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) # الحذف الفوري
    
    embed = discord.Embed(title="🔑 حساباتك", description="\n".join([f"||`{i}`||" for i in items]), color=0x00FF99)
    try:
        await member.send(embed=embed)
        await ctx.send(f"✅ | تم إرسال الحساب لـ {member.mention}")
    except: await ctx.send("❌ | تعذر الإرسال (الخاص مغلق).")

@bot.command()
async def drop(ctx, amount: int = 1):
    if not is_admin(ctx): return await ctx.send("🚫 | للأونر والكرييتور فقط!")
    
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | الحسابات غير كافية للـ Drop!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) # الحذف الفوري
    
    embed = discord.Embed(title="🎁 | Drop جديد!", description="\n".join([f"||`{i}`||" for i in items]), color=0xFF5733)
    await ctx.send(embed=embed)

bot.run(os.environ.get('TOKEN'))

import os
import discord
from discord.ext import commands

# 1. إعداد المسارات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "minecraft.txt")

# 2. الإعدادات
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# تعريف البوت بالـ prefix الجديد وتصحيح الخطأ السابق
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# --- إعدادات الرتب (ضع ID رتبتك هنا) ---
ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] 
ROLE_TO_PING = 1523325683286413411  # <--- ضع ID الرتبة للمنشن هنا

def is_admin(ctx):
    return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)

def get_accounts():
    if not os.path.exists(FILE_PATH): return []
    with open(FILE_PATH, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def update_accounts(accounts):
    with open(FILE_PATH, "w") as f: f.write("\n".join(accounts))

@bot.event
async def on_ready():
    # وضع حالة DND
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))
    print(f'✅ البوت يعمل وجاهز بوضعية DND!')

# --- أمر المساعدة ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 قائمة أوامر Blaze Cloud", color=0x00FF99)
    embed.add_field(name="🛠️ الإدارة", value="`$send @member [amount]`, `$drop [amount]`", inline=False)
    embed.add_field(name="ℹ️ معلومات", value="`$stock`", inline=False)
    await ctx.send(embed=embed)

# --- أمر الـ Stock ---
@bot.command()
async def stock(ctx):
    count = len(get_accounts())
    await ctx.send(f"📦 | المتوفر حالياً: `{count}` حساب ماين كرافت ⛏️.")

# --- أمر الـ Send (إبداعي) ---
@bot.command()
async def send(ctx, member: discord.Member, amount: int = 1):
    if not is_admin(ctx): return await ctx.send("🚫 | للأونر فقط!")
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | لا يوجد حسابات كافية!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) 
    
    embed = discord.Embed(title="📨 | طلب استلام حساب ⛏️", color=0x00FF99)
    embed.add_field(name="👤 العضو:", value=f"{member.mention}", inline=True)
    embed.add_field(name="🔢 العدد:", value=f"`{amount}` حساب", inline=True)
    embed.add_field(name="🔑 البيانات:", value="\n".join([f"||`{i}`||" for i in items]), inline=False)
    embed.set_footer(text="Blaze Cloud | ⛏️ تم التسليم بنجاح.")
    
    try:
        await member.send(embed=embed)
        await ctx.send(f"✅ | تم إرسال الحسابات لـ {member.mention} في الخاص.")
    except: await ctx.send("❌ | لم أستطع الإرسال، الخاص مغلق!")

# --- أمر الـ Drop (إبداعي مع منشن) ---
@bot.command()
async def drop(ctx, amount: int = 1):
    if not is_admin(ctx): return await ctx.send("🚫 | للأونر فقط!")
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | لا يوجد حسابات كافية للـ Drop!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) 
    
    embed = discord.Embed(
        title="⛏️ | إفلات حسابات ماين كرافت! | ⛏️",
        description="تم طرح دفعة جديدة، كن الأسرع في الاقتناص! ⚡",
        color=0xFF0055
    )
    embed.add_field(name="🔑 الحسابات المتاحة:", value="\n".join([f"• ||`{i}`||" for i in items]), inline=False)
    embed.set_footer(text="Blaze Cloud | ⛏️ حظاً موفقاً للجميع!")
    
    await ctx.send(f"📢 <@&{ROLE_TO_PING}>", embed=embed)

bot.run(os.environ.get('TOKEN'))

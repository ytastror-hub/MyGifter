import os
import discord
from discord.ext import commands

# --- الإعدادات ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "minecraft.txt")
ROLE_TO_PING = 123456789012345678  # ضع ID الرتبة هنا

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=endents, help_command=None)
ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] 

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
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))
    print(f'✅ البوت يعمل بوضعية DND!')

# --- أمر الـ Drop (شكل إبداعي) ---
@bot.command()
async def drop(ctx, amount: int = 1):
    if not is_admin(ctx): return
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | لا توجد حسابات كافية!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) 
    
    embed = discord.Embed(
        title="🎁 | إفلات حسابات جديدة - Drop!",
        description="تم طرح دفعة جديدة من الحسابات، كن الأسرع في الاقتناص! ⚡",
        color=0xFF0055
    )
    embed.add_field(name="🔑 الحسابات المتاحة:", value="\n".join([f"• ||`{i}`||" for i in items]), inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/8Q5u6S7.png") # يمكنك وضع رابط شعار سيرفرك هنا
    embed.set_footer(text="Blaze Cloud | حظاً موفقاً للجميع!")
    
    await ctx.send(f"📢 <@&{ROLE_TO_PING}>", embed=embed)

# --- أمر الـ Send (شكل إبداعي) ---
@bot.command()
async def send(ctx, member: discord.Member, amount: int = 1):
    if not is_admin(ctx): return
    accounts = get_accounts()
    if len(accounts) < amount: return await ctx.send("❌ | لا توجد حسابات كافية!")

    items = [accounts.pop(0) for _ in range(amount)]
    update_accounts(accounts) 
    
    embed = discord.Embed(title="📨 | طلب استلام حساب", color=0x00FF99)
    embed.add_field(name="👤 العضو:", value=f"{member.mention}", inline=True)
    embed.add_field(name="🔢 العدد:", value=f"`{amount}` حساب", inline=True)
    embed.add_field(name="🔑 الحسابات:", value="\n".join([f"||`{i}`||" for i in items]), inline=False)
    embed.set_footer(text="Blaze Cloud | تم التسليم بنجاح.")
    
    try:
        await member.send(embed=embed)
        await ctx.send(f"✅ | تم إرسال الحسابات لـ {member.mention} في الخاص.")
    except: await ctx.send("❌ | لم أستطع الإرسال، الخاص مغلق!")

bot.run(os.environ.get('TOKEN'))

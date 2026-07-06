import os
import discord
from discord.ext import commands

# --- الإعدادات ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# الرتب المسموح لها (OWNER & CREATOR)
ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] 

def is_admin(ctx):
    return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)

def get_accounts():
    try:
        with open("minecraft.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# --- أمر الإرسال الإداري فقط ---
@bot.command()
async def send(ctx, member: discord.Member):
    # التحقق من الصلاحيات
    if not is_admin(ctx): 
        return await ctx.send("🚫 | هذه الصلاحية فقط للأونر والكرييتور!")
    
    accounts = get_accounts()
    
    if not accounts:
        return await ctx.send("❌ | المخزون فارغ! لا يوجد حسابات في `minecraft.txt`")

    # سحب أول حساب
    item = accounts.pop(0)
    with open("minecraft.txt", "w") as f: f.write("\n".join(accounts))
    
    # رسالة الـ Embed المودرن
    embed = discord.Embed(
        title="⛏️ | Blaze Cloud | مبروك هديتك!",
        description="لقد تم اختيارك لتحصل على حساب ماين كرافت!",
        color=0x00FF99
    )
    embed.add_field(name="🔑 بيانات الحساب:", value=f"||`{item}`||", inline=False)
    embed.set_footer(text="Blaze Cloud | استمتع باللعب!")
    
    try:
        await member.send(embed=embed)
        await ctx.send(f"✅ | تم إرسال الحساب لـ {member.mention} في الخاص.")
    except discord.Forbidden:
        await ctx.send(f"❌ | {member.mention}، يرجى فتح الخاص لاستلام الحساب!")

bot.run(os.environ.get('TOKEN'))

import os
import discord
from discord.ext import commands

# --- الإعدادات ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] 

def is_admin(ctx):
    return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)

def get_accounts():
    try:
        with open("minecraft.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# --- أمر الإرسال المتعدد ---
@bot.command()
async def send(ctx, member: discord.Member, service: str, amount: int = 1):
    if not is_admin(ctx): 
        return await ctx.send("🚫 | فقط للأونر والكرييتور!")
    
    if service.lower() != "minecraft":
        return await ctx.send("❌ | حالياً البوت يدعم `minecraft` فقط.")

    accounts = get_accounts()
    
    if len(accounts) < amount:
        return await ctx.send(f"❌ | لا يوجد ما يكفي من الحسابات! المتوفر حالياً: `{len(accounts)}`")

    # سحب العدد المطلوب
    items = [accounts.pop(0) for _ in range(amount)]
    with open("minecraft.txt", "w") as f: f.write("\n".join(accounts))
    
    # تنسيق الحسابات في نص واحد للـ Embed
    formatted_accounts = "\n".join([f"• ||`{item}`||" for item in items])
    
    embed = discord.Embed(
        title="⛏️ | Blaze Cloud | دفعة حسابات جديدة",
        description=f"لقد حصلت على `{amount}` حساب ماين كرافت!",
        color=0x00FF99
    )
    embed.add_field(name="🔑 البيانات:", value=formatted_accounts, inline=False)
    embed.set_footer(text="Blaze Cloud | استمتع باللعب!")
    
    try:
        await member.send(embed=embed)
        await ctx.send(f"✅ | تم إرسال `{amount}` حساب لـ {member.mention} بنجاح.")
    except discord.Forbidden:
        await ctx.send(f"❌ | {member.mention}، يرجى فتح الخاص لاستلام الحسابات!")

bot.run(os.environ.get('TOKEN'))

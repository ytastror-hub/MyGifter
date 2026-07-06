import os
import discord
from discord.ext import commands

# --- الإعدادات ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)

ADMIN_ROLE_IDS = [1523325683344998515, 1523325683344998516] # OWNER & CREATOR

def is_admin(ctx):
    return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)

def get_accounts():
    try:
        with open("minecraft.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# --- أمر الإرسال المودرن ---
@bot.command()
async def send(ctx, member: discord.Member):
    if not is_admin(ctx): 
        return await ctx.send("🚫 | هذه الصلاحية فقط للأونر والكرييتور!")
    
    accounts = get_accounts()
    
    if not accounts:
        return await ctx.send("❌ | المخزون فارغ! لا يوجد حسابات في `minecraft.txt`")

    # سحب أول حساب من القائمة
    item = accounts.pop(0)
    with open("minecraft.txt", "w") as f: f.write("\n".join(accounts))
    
    # Embed فخم للخاص
    embed = discord.Embed(
        title="🎉 | مبروك! هدية خاصة من Blaze Cloud",
        description="لقد تم اختيارك لتحصل على حساب ماين كرافت مجاني!",
        color=0x00FF99 # لون أخضر فخم
    )
    embed.add_field(name="🔑 بيانات الحساب:", value=f"||`{item}`||", inline=False)
    embed.set_footer(text="Blaze Cloud | استمتع باللعب!")
    embed.set_thumbnail(url="https://i.imgur.com/8Q85N9P.png") # يمكنك تغيير الرابط لصورة أيقونة ماين كرافت
    
    try:
        await member.send(embed=embed)
        
        # رسالة تأكيد في العام
        confirm_embed = discord.Embed(
            title="✅ | تم التسليم",
            description=f"تم إرسال حساب ماين كرافت لـ {member.mention} بنجاح.",
            color=0x2ecc71
        )
        await ctx.send(embed=confirm_embed)
    except discord.Forbidden:
        await ctx.send(f"❌ | {member.mention}، يرجى فتح الخاص لاستلام الحساب!")

bot.run(os.environ.get('TOKEN'))
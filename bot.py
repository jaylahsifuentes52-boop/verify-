import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN MTU0ODc3ODcyMDQzOTk1OTcwMg.GlrK4R.YD4Wd-l2SplcfEQCAwE32u8gQXWIGGSO3OSd7w")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in Render.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="verify", description="Verify using an OTP code")
@app_commands.describe(otp="Enter your OTP code")
async def verify(interaction: discord.Interaction, otp: str):
    if not otp.strip():
        await interaction.response.send_message(
            "❌ Please enter an OTP code.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ OTP received.", ephemeral=True
    )


bot.run(TOKEN)

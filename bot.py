import os
import secrets
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Stores active OTPs in memory
otps = {}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(
    name="generateotp",
    description="Generate a verification OTP"
)
async def generateotp(interaction: discord.Interaction):
    otp = f"{secrets.randbelow(1_000_000):06d}"

    otps[interaction.user.id] = otp

    await interaction.response.send_message(
        f"🔐 Your OTP is: `{otp}`\n"
        "Use `/verify` and enter this code.",
        ephemeral=True
    )


@bot.tree.command(
    name="verify",
    description="Verify using an OTP"
)
@app_commands.describe(otp="Enter your 6-digit OTP")
async def verify(
    interaction: discord.Interaction,
    otp: str
):
    user_id = interaction.user.id

    if user_id not in otps:
        await interaction.response.send_message(
            "❌ You don't have an active OTP.",
            ephemeral=True
        )
        return

    if not secrets.compare_digest(otps[user_id], otp.strip()):
        await interaction.response.send_message(
            "❌ Invalid OTP.",
            ephemeral=True
        )
        return

    # OTP can only be used once
    del otps[user_id]

    await interaction.response.send_message(
        "✅ Verification successful!",
        ephemeral=True
    )


bot.run(TOKEN)
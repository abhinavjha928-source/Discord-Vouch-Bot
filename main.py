import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# 1. Load your secret token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        # 2. Set Intents to ALL so the bot shows as ONLINE and sees members
        intents = discord.Intents.all() 
        
        super().__init__(
            command_prefix="!", 
            intents=intents, 
            help_command=None
        )

    async def setup_hook(self):
        print("--- 🛠️  Starting Setup ---")
        
        # 3. Automatically load all features (cogs) from the cogs folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Loaded Cog: {filename}')
                except Exception as e:
                    print(f'❌ Failed to load {filename}: {e}')
        
        # 4. Sync slash commands so they show up in Discord
        print("--- 🔄 Syncing Commands ---")
        await self.tree.sync()
        print("✅ Commands synced globally!")

    async def on_ready(self):
        print(f'--- 🤖 Bot is Online! ---')
        print(f'Logged in as: {self.user.name} ({self.user.id})')
        print(f'Connected to {len(self.guilds)} servers.')

async def main():
    bot = MyBot()
    async with bot:
        # 5. Start the bot
        await bot.start(TOKEN)

# 6. Protected Shutdown Handling
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Shutdown signal received (Ctrl+C). Closing bot safely...")
    finally:
        print("[!] Bot is now offline. Database and connection are safe.")
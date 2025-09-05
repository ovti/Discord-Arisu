import discord
import requests
import asyncio
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
URL = os.getenv("URL")

YEAR_FILE = "last_year.txt"

# load last year from file if exists
if os.path.exists(YEAR_FILE):
    with open(YEAR_FILE, "r", encoding="utf-8") as f:
        last_year = f.read().strip()
else:
    last_year = None

intents = discord.Intents.default()
intents.message_content = True

class YearWatcherBot(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def setup_hook(self):
        asyncio.create_task(self.check_website())

    async def scrape_year(self):
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(" ", strip=True)

            match = re.search(r"(\d{4}/\d{4})", text)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Error checking site: {e}")
        return None

    async def check_website(self):
        global last_year
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)

        while not self.is_closed():
            current_year = await self.scrape_year()
            if current_year:
                print("Checked website, current_year:", current_year)

                if last_year is None:
                    last_year = current_year
                    print(f"Initial year set to {last_year}")
                    await channel.send(f"Nadal brak nowego planu 😒 Obecny plan: {last_year}.")
                    self.save_year(last_year)

                elif current_year != last_year:
                    await channel.send(
                        f"@everyone Nowy plan **{current_year}** !! 📅\n{URL}"
                    )
                    last_year = current_year
                    self.save_year(last_year)

            await asyncio.sleep(30)  # check every 30s

    def save_year(self, year: str):
        with open(YEAR_FILE, "w", encoding="utf-8") as f:
            f.write(year)

    async def on_message(self, message: discord.Message):
        global last_year

        if message.author == self.user:
            return

        if message.content.lower().startswith("!status"):
            if last_year:
                await message.channel.send(f"📅 Aktualny plan na stronie: **{last_year}**\n{URL}")
            else:
                await message.channel.send("Nie udało się wykryć roku.")

        elif message.content.lower().startswith("!forcecheck"):
            await message.channel.send("🔍 Sprawdzam stronę...")
            current_year = await self.scrape_year()
            if current_year:
                if last_year and current_year != last_year:
                    await message.channel.send(
                        f"@everyone Nowy plan **{current_year}** !! 📅\n{URL}"
                    )
                    last_year = current_year
                    self.save_year(last_year)
                else:
                    await message.channel.send(f"📅 Nadal obowiązuje plan: **{current_year}**\n{URL}")
            else:
                await message.channel.send("⚠️ Błąd podczas sprawdzania strony.")

    async def on_ready(self):
        print(f"Logged in") 

client = YearWatcherBot(intents=intents)
client.run(TOKEN)

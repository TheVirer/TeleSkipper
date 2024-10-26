from telethon   import TelegramClient
import asyncio

trash_sessions = []
valid_clients = []

with open("channels.txt","r",encoding="utf-8") as file:
    channels = file.read().split("\n")

with open("proxies.txt","r",encoding="utf-8") as file:
    proxies = file.read().split("\n")

async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())
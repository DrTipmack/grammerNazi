import discord
import language_tool_python
import asyncio
import re

client = discord.Client()

tool = language_tool_python.LanguageTool("en-UK")
query = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

spamChannels = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    while True:
        await asyncio.sleep(20)
        with open("recents.txt", "r+") as file:
          file.truncate(0)


@client.event
async def on_message(message):
    counter = 0
    out = ""

    matches = re.findall(query, message.content)
    if len(matches) > 0 or len(message.content) > 200 or len(message.content) < 10 or message.author.bot:
        return False
    
    if message.channel.id in spamChannels:
        return False
    
    with open("recents.txt", "r+") as file:
        file.writelines(f"{message.content}\n")
        for lines in file:
            if lines.strip("\n") == message.content:
                counter += 1
            if counter > 5:
                await message.channel.send("Stop spam")
                addToSpam(message.channel.id)
                return False

    # if message.author.id is in recently
    #check = tool.check(message.content)
    # for match in check:
    #     for fix in match.replacements:
    #             out += "*" + fix + " "
    out = "*" + tool.correct(message.content)

    if len(out) > 0:
        await message.reply(out, delete_after=10)

async def addToSpam(channel):
    spamChannels.append(channel) if channel not in spamChannels else None
    asyncio.sleep(10)
    spamChannels.remove(channel) if channel in spamChannels else None

client.run("")

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('message empty')
        return
    if message.author == client.user:
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response = "hello"
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message) -> None:
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


    embed = discord.Embed(
        title="🔔 Add your roles!",
        description="Thank you for joining us! Enjoy your stay.",
        color=discord.Color.blue()  # Choose any color
    )

    embed.add_field(name="Select the roles that you would", value="🟢-Towny\n"
                                                                  "🟢-Survival\n"
                                                                  "🔵-Sneak Peaks\n"
                                                                  "🟣-Server Status\n"
                                                                  "🟡-Events\n"
                                                                  "🔴-Polls\n", inline=False)

    # Send the embed in the current channel
    await message.channel.send(embed=embed)

    embed = discord.Embed(
        title="Custom Banner",
        description="This is a message with a custom banner!",
        color=discord.Color.blue()
    )
    embed.set_image(
        url="https://rukminim2.flixcart.com/image/416/416/kpcy5jk0/poster/h/c/w/large-village-poster-scenery-scenrym-68-original-imag3m8vrkdztzva.jpeg?q=70&crop=false")
    await channel.send(embed=embed)

    embed = discord.Embed(
        title="🔔 Add your roles!",
        description="Thank you for joining us! Enjoy your stay.",
        color=discord.Color.blue()  # Choose any color
    )
    embed.add_field(name="Select the roles that you would", value="🟠-Towny\n"
                                                                  "🟢-Survival\n"
                                                                  "🔵-Sneak Peaks\n"
                                                                  "🟣-Server Status\n"
                                                                  "🟡-Events\n"
                                                                  "🔴-Polls\n", inline=False)
    message = await channel.send(embed=embed)
    await message.add_reaction("🟠")
    await message.add_reaction("🟢")
    await message.add_reaction("🔵")
    await message.add_reaction("🟣")
    await message.add_reaction("🟡")
    await message.add_reaction("🔴")



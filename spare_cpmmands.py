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



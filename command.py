from pyrogram import Client, filters
from pyrogram.types import Message
from chatbot.helpers.helper import process_ai_query

# Replace with your own Telegram chat ID for reports
YOUR_TELEGRAM_CHAT_ID=YOUR_ID_HERE

# Set to store blacklisted user IDs
blacklist = set()

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start_handler(client: Client, message: Message):
        await message.reply_text(
            "Sup /dave to use me."
        )

    # Handle the /dave command
    @app.on_message(filters.command("dave"))
    async def ai_handler(client: Client, message: Message):
        # Check if the user is blacklisted
        if message.from_user.id in blacklist:
            return await message.reply_text("You are blacklisted froom using dave")

        # Extract the query from the message
        query = (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        )

        if not query:
            return await message.reply_text(
                "Are you an idiot Add a question after /dave...."
            )

        # Send an initial message while processing the query
        sent_message = await message.reply_text("wait whilst I check my mainframe...")

        try:
            # Process the AI query
            response_text = await process_ai_query(query, sent_message)

            # Check if response_text is valid before editing the message
            if response_text:
                await sent_message.edit_text(response_text)
            else:
                await sent_message.edit_text("computer says no.")
        except Exception as e:
            # Handle any exceptions that occur during processing
            await sent_message.edit_text("An error occurred and the bug has been logged")
            print(f"Error processing query: {e}")  # Log the error for debugging

    # Handle the /skid command for reporting
    @app.on_message(filters.command("skid"))
    async def report_handler(client: Client, message: Message):
        # Check if the user is blacklisted
        if message.from_user.id in blacklist:
            return await message.reply_text("You are blacklisted from using Dave sorry.")

        # Send the report to your Telegram chat ID
        report_text = f"Report from {message.from_user.id}: {message.text}"
        await client.send_message(YOUR_TELEGRAM_CHAT_ID, report_text)
        await message.reply_text("zlo has received your report.")

    # Command to add a user to the blacklist
    @app.on_message(filters.command("blacklist"))
    async def blacklist_handler(client: Client, message: Message):
        if message.from_user.id == YOUR_TELEGRAM_CHAT_ID:  # Only allow the owner to blacklist
            user_id_to_blacklist = int(message.text.split(maxsplit=1)[1]) if len(message.text.split()) > 1 else None
            if user_id_to_blacklist:
                blacklist.add(user_id_to_blacklist)
                await message.reply_text(f"User {user_id_to_blacklist} has been blacklisted.")
            else:
                await message.reply_text("who we blackljsting g")
        else:
            await message.reply_text("You do not have permission to use this command.")

    # Command to remove a user from the blacklist
    @app.on_message(filters.command("unblacklist"))
    async def unblacklist_handler(client: Client, message: Message):
        if message.from_user.id == YOUR_TELEGRAM_CHAT_ID:  # Only allow the owner to unblacklist
            user_id_to_unblacklist = int(message.text.split(maxsplit=1)[1]) if len(message.text.split()) > 1 else None
            if user_id_to_unblacklist in blacklist:
                blacklist.remove(user_id_to_unblacklist)
                await message.reply_text(f"User {user_id_to_unblacklist} has been unblacklisted.")
            else:
                await message.reply_text("User is not in the blacklist.")
        else:
            await message.reply_text("You do not have permission to use this command.")

    # Handle the /zlo command (disclaimer/tos)
    @app.on_message(filters.command("zlo"))
    async def zlo_handler(client: Client, message: Message):
        zlo_message = (
            "We have our own TOS  keeping in line with telegrams and they are as follows./n/n"

"1. Asking it anything to do with unethical hacking and osint,/n/n"

"2. Asking for any type of type of illegal content and where to find it,/n/n"

"3. Asking it for lorebooks and doxxes,/n/n"

"4. Asking it for unsavoury pictures of others,/n/n"

"Faliure to follow the TOS will result in you being permanently blacklisted from using this bot, Use /skid to send a report  if you see anyone breaking the TOS, FYI these will be reviewed contanstly to abide by Telegram TOS also the bot at the moment is going through constant updates so if it is offline this will be the reason as to why/n/n"

"Thank you and have fun"
            "Your local neighbourhood droid\n\n"
            "-ZłO"
        )
        await message.reply_text(zlo_message)

#codedbyzlocrax(dontbeaskidclaimingitsyours)

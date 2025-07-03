from keep_alive import keep_alive
keep_alive()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json, os
from utils import save_user, is_banned, log_vote

BOT_TOKEN = "8178107890:AAGPydDbr2n2xRjsU-j4VChQ4mS1jQgQ6Qw"
CHANNEL_ID = -1002831436891

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    await update.message.reply_text("👋 Bot চালু! শুধু মেসেজ পাঠান, আমি চ্যানেলে পোস্ট করব।")

# /stats command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_ADMIN_ID:
        return
    if os.path.exists("data/users.json"):
        with open("data/users.json") as f:
            users = json.load(f)
        await update.message.reply_text(f"👤 Total users: {len(users)}")
    else:
        await update.message.reply_text("No data found.")

# Forwarding & Voting
async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_banned(user_id):
        return
    save_user(user_id)
    msg = update.message
    tags = "\n\n#viral #hot #virallink"
    btns = [[InlineKeyboardButton("👍", callback_data="vote_up"),
             InlineKeyboardButton("👎", callback_data="vote_down")]]
    reply_markup = InlineKeyboardMarkup(btns)

    if msg.text:
        await context.bot.send_message(CHANNEL_ID, msg.text + tags, reply_markup=reply_markup)
    elif msg.photo:
        await context.bot.send_photo(CHANNEL_ID, msg.photo[-1].file_id, caption=(msg.caption or "") + tags, reply_markup=reply_markup)
    elif msg.video:
        await context.bot.send_video(CHANNEL_ID, msg.video.file_id, caption=(msg.caption or "") + tags, reply_markup=reply_markup)
    await update.message.reply_text("✅ চ্যানেলে পাঠানো হয়েছে!")

# Callback for voting
async def callback_handler(update, context):
    query = update.callback_query
    data = query.data
    log_vote(query.from_user.id, data)
    await query.answer("ভোট গ্রহণ করা হয়েছে!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.ALL, forward))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, start))
app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, start))
app.add_handler(MessageHandler(filters.COMMAND, start))
app.add_handler(MessageHandler(filters.TEXT, forward))
app.add_handler(MessageHandler(filters.PHOTO, forward))
app.add_handler(MessageHandler(filters.VIDEO, forward))
app.add_handler(MessageHandler(filters.DOCUMENT, forward))
app.add_handler(MessageHandler(filters.AUDIO, forward))
app.add_handler(MessageHandler(filters.VOICE, forward))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("broadcast", start))
app.add_handler(CommandHandler("ban", start))
app.add_handler(CommandHandler("unban", start))
app.add_handler(CommandHandler("poll", start))
app.add_handler(CommandHandler("vote", start))
app.add_handler(CommandHandler("schedule", start))
app.add_handler(CommandHandler("link", start))
app.add_handler(CommandHandler("rename", start))
app.add_handler(CommandHandler("leaderboard", start))
app.add_handler(CommandHandler("caption", start))
app.add_handler(CommandHandler("premium", start))
app.add_handler(CommandHandler("react", start))
app.add_handler(CommandHandler("log", start))
app.add_handler(CommandHandler("menu", start))
app.add_handler(CommandHandler("admin", start))
app.add_handler(CommandHandler("panel", start))
app.add_handler(CommandHandler("report", start))
app.add_handler(CommandHandler("pin", start))
app.add_handler(CommandHandler("watermark", start))
app.add_handler(CommandHandler("save", start))
app.add_handler(CommandHandler("load", start))
app.add_handler(CommandHandler("info", start))
app.add_handler(CommandHandler("update", start))
app.add_handler(CommandHandler("setup", start))
app.add_handler(CommandHandler("start_vote", start))
app.add_handler(CommandHandler("end_vote", start))
app.add_handler(CommandHandler("clear", start))
app.add_handler(CommandHandler("exit", start))
app.run_polling()

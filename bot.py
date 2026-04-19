import os
import logging
from dotenv import load_dotenv
from telegram import Update

load_dotenv()
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Global variables for the simple RL reward system
# In a production app, use a database to persist this per user or globally across restarts.
global_reward_score = 0

# Simple FAQ Dictionary defining the knowledge base
FAQ = {
    "java": "Java is an object-oriented programming language widely used in enterprise software. Key concepts include OOPs, multithreading, and collections.",
    "dbms": "DBMS (Database Management System) manages databases. Important topics encompass SQL, Normalization (1NF, 2NF, 3NF), and ACID properties.",
    "os": "An OS (Operating System) acts as an interface between hardware and software. Focus on: scheduling algorithms, deadlocks, and memory management.",
    "aptitude": "Aptitude tests evaluate logical reasoning and quantitative math. Practice percentages, time & work, and pattern recognition regularly.",
    "python": "Python is a high-level, interpreted language known for its readability. It's great for data science, AI, and web backend development."
}

def get_tone_prefix() -> str:
    """Adapts the bot's tone based on the current reward score."""
    global global_reward_score
    if global_reward_score >= 5:
        return "😎 I'm feeling confident! Here is what you need to know:\n\n"
    elif global_reward_score <= -3:
        return "😥 I'm still learning and trying my best, but maybe this helps:\n\n"
    elif global_reward_score >= 2:
        return "🙂 Here's a helpful summary:\n\n"
    else:
        return "📚 "

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_text = (
        "Hello! I am your AI Study Assistant Bot 🎓.\n"
        "I can help you prepare with quick concepts for Java, DBMS, OS, and Aptitude.\n\n"
        "Just ask me a question or reply with 'good' or 'bad' to rate my answers and help me learn!"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Send me a topic like 'java' or 'os' to get a quick summary.\n"
        "Tell me if my answer was 'good' or 'bad' so I can learn from your feedback!"
    )
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages, applying FAQ lookups and reward logic."""
    global global_reward_score
    text = update.message.text.lower().strip()
    
    # 1. Check for feedback (Reward System)
    if text in ["good", "good bot", "great", "thanks"]:
        global_reward_score += 1
        await update.message.reply_text(f"Thank you! 🌟\nMy confidence (reward score) increased to {global_reward_score}.")
        return
    elif text in ["bad", "bad bot", "wrong", "terrible"]:
        global_reward_score -= 1
        await update.message.reply_text(f"Oh no! 😔\nMy confidence (reward score) decreased to {global_reward_score}. I'll try to do better.")
        return
    
    # 2. Check for FAQ Topics
    found = False
    for topic, explanation in FAQ.items():
        if topic in text:
            tone_prefix = get_tone_prefix()
            await update.message.reply_text(f"{tone_prefix}{explanation}")
            found = True
            break
            
    # 3. Fallback for unknown messages
    if not found:
        await update.message.reply_text(
            "I'm not sure about that topic yet. 🧐\n"
            "Try asking me about Java, DBMS, OS, Python, or Aptitude!"
        )

def main() -> None:
    """Start the bot."""
    # Get the token from environment variables
    # Render or any cloud platform will inject the token here
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables! Please set it before running.")
        return
        
    # Build the application
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register message handler for all non-command text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until user presses Ctrl-C
    # Uses polling which is suitable for background tasks on Render
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

# Telegram Study Assistant Bot

This is a simple AI-powered Telegram bot built with Python, designed to act as a Smart FAQ assistant for college and job preparation. It demonstrates a basic reinforcement learning concept via a global reward score based on user feedback.

## Features
- **FAQ Knowledge Base**: Explains concepts in Java, DBMS, OS, Python, and Aptitude.
- **Reward System**: Learns from user feedback ("good" or "bad") and adapts its tone dynamically based on its confidence (global reward score).
- **Cloud Ready**: Configured for immediate deployment on Render.

---

## 1. Create the Telegram Bot via BotFather
1. Open Telegram and search for `@BotFather`.
2. Start a chat and send the command `/newbot`.
3. Provide a display name for your bot (e.g., *My Study Assistant*).
4. Provide a unique username ending in `bot` (e.g., *smart_study_123_bot*).
5. BotFather will generate an API Token. **Save this token securely**. It looks something like `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`.

---

## 2. Running the Bot Locally
To test the bot on your computer before deploying:

1. **Install Python**: Ensure you have Python 3.8+ installed.
2. **Install Dependencies**: Open a terminal in this directory and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set the Environment Variable**:
   - On Windows (Command Prompt):
     ```cmd
     set TELEGRAM_BOT_TOKEN=your_token_here
     ```
   - On Windows (PowerShell):
     ```powershell
     $env:TELEGRAM_BOT_TOKEN="your_token_here"
     ```
   - On Mac/Linux:
     ```bash
     export TELEGRAM_BOT_TOKEN=your_token_here
     ```
4. **Run the Bot**:
   ```bash
   python bot.py
   ```
5. Open Telegram, find your bot by its username, and send `/start`.

---

## 3. Deploying the Bot on Render
[Render](https://render.com/) is an excellent free cloud platform for running background worker processes like this bot.

1. **Push to GitHub**: Initialize a Git repository in this folder, commit all files (`bot.py`, `requirements.txt`, `Procfile`), and push to a new GitHub repository.
2. **Log into Render**: Create an account on Render and click **New+** -> **Background Worker**.
3. **Connect Repository**: Connect your GitHub account and select your newly created repository.
4. **Configure the Service**:
   - **Name**: Give it a name (e.g., `study-assistant-bot`)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py` (This is also defined in the Procfile, Render might detect it automatically).
5. **Set Environment Variables**:
   - Scroll down to **Environment Variables**, click **Add Environment Variable**.
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your_token_here`
6. **Deploy**: Click **Create Background Worker**. Render will build and start your bot. As long as it is a "Background Worker", it will continuously poll Telegram without sleeping!

---

## 4. Explanation of Reward Logic Implementation
The bot implements a rudimentary Reinforcement Learning construct using a stateless **global reward score**.
- **State**: The current `global_reward_score` (starts at 0).
- **Environment**: User feedback.
- **Reward Signal**: If the user types "good", the bot receives a `+1` reward. If "bad", it gets a `-1` penalty.
- **Action / Policy Adaption**: Depending on the cumulative reward score, the bot selects a different prefix "tone".
  - Score >= 5: Confident tone (😎 I'm feeling confident!)
  - Score >= 2: Helpful tone (🙂 Here's a helpful summary:)
  - Score <= -3: Apologetic/Learning tone (😥 I'm still learning...)

In `bot.py`, this is achieved by checking for keywords in the message text. If feedback is found, we modify `global_reward_score` and return early. The function `get_tone_prefix()` maps the score to the respective string.

---

## 5. Example Interaction
**User**: `/start`
**Bot**: Hello! I am your AI Study Assistant Bot 🎓.
I can help you prepare with quick concepts for Java, DBMS, OS, and Aptitude.
Just ask me a question or reply with 'good' or 'bad' to rate my answers and help me learn!

**User**: `Tell me about java`
**Bot**: 📚 Java is an object-oriented programming language widely used in enterprise software. Key concepts include OOPs, multithreading, and collections.

**User**: `good`
**Bot**: Thank you! 🌟
My confidence (reward score) increased to 1.

*(After multiple "good" messages... score = 5)*

**User**: `What is dbms?`
**Bot**: 😎 I'm feeling confident! Here is what you need to know:
DBMS (Database Management System) manages databases. Important topics encompass SQL, Normalization (1NF, 2NF, 3NF), and ACID properties.
"# Telegram-study-assistant-bot" 

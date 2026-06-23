import config
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from google import genai
from google.genai import types

# Initialize the Gemini client securely using your config file
# It dynamically pulls the key you will set in Railway
GEMINI_API_KEY = getattr(config, "GEMINI_API_KEY", None)
ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def chat_with_gemini(update: Update, context: CallbackContext):
    """
    Catch-all handler that routes normal text chatter to Gemini 
    when no explicit slash command matches.
    """
    # Defensive check: ensure there's a message and it contains actual text
    if not update.message or not update.message.text:
        return

    # Fail gracefully if you haven't added the API key to Railway yet
    if not ai_client:
        print("AI initialization skipped: GEMINI_API_KEY is missing from config.")
        return

    user_text = update.message.text

    try:
        # Let the group/user know the bot is drafting a response
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Call the conversational model
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are Realme Assist, a super-intelligent, witty AI assistant. "
                    "CRITICAL RULE: You are ONLY allowed to answer questions and discuss topics "
                    "related to Information Technology (IT), tech, smartphones, software, programming, "
                    "and Android/Realme UI. "
                    "If a user asks about anything outside of IT (e.g., cooking, sports, celebrity news, "
                    "history, general lifestyle, or creative writing), you must politely decline. "
                    "Tell them that you are an IT-focused assistant and that they should look up that "
                    "information on a search engine instead. Keep your response brief and clear."
                )
            )
        )
        
        # Send the AI response using Markdown formatting
        update.message.reply_text(response.text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        print(f"Error handling Gemini request: {e}")

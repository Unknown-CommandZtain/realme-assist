import os
import re
import requests
from bs4 import BeautifulSoup
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from config import VERIFIED_USERS, CONTROL_GROUP, OFFTOPIC_GROUP, SUPPORT_GROUP, ADMINS

from utils import delay_group, delay_group_preview, delay_html, remove_message, schedule_delete

def search_realme_model(rmx_code):
    """Dynamically searches Yahoo to find the phone name for an RMX code."""
    # We secretly add 'gsmarena' to force a clean, highly structured search result
    url = f"https://search.yahoo.com/search?p=Realme+{rmx_code}+gsmarena"
    
    # We use a modern, complete browser User-Agent so Yahoo doesn't flag us as a script
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Yahoo stores the result title inside an <h3> tag with the class "title"
            first_result = soup.find('h3', class_='title')
            if first_result:
                title = first_result.text.strip()
                
                # 1. Chop off website names (like "- GSMArena")
                clean_title = title.split('|')[0].split('-')[0]
                
                # 2. Remove the RMX code and its parentheses
                clean_title = re.sub(rf'\(?{rmx_code}\)?', '', clean_title, flags=re.IGNORECASE)
                
                # 3. Strip out expanded junk words
                junk_words = [
                    r"specs?", r"review", r"price", r"release date", r"gsmarena", 
                    r"kimovil", r"unboxing", r"technical", r"specifications", r"full", r"phone"
                ]
                for word in junk_words:
                    clean_title = re.sub(rf'(?i)\b{word}\b', '', clean_title)
                
                # 4. Clean up any leftover double spaces and return!
                return re.sub(r'\s+', ' ', clean_title).strip()
                
    except Exception as e:
        print(f"Web search failed for {rmx_code}: {e}")
        
    return "Unknown Realme Device"

def banana(update: Update, context: CallbackContext):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "resources", "where_update.png")
    
    with open(file_path, "rb") as photo_file:
        msg = update.message.reply_photo(photo=photo_file, caption="Where update? 🍌")
        schedule_delete(context, msg.chat_id, msg.message_id)
        schedule_delete(context, update.message.chat_id, update.message.message_id)

def realistic(update: Update, context: CallbackContext):
    delay_html(update, context, "realistic")

def rules(update: Update, context: CallbackContext):
    delay_html(update, context, "onrules")

def about(update: Update, context: CallbackContext):
    delay_html(update, context, "about")

def ban(update: Update, context: CallbackContext):
    update.message.reply_text("Ban hammer goes bonk! 🔨")

def warn(update: Update, context: CallbackContext):
    update.message.reply_text("Warning issued! ⚠️")

def unwarn(update: Update, context: CallbackContext):
    update.message.reply_text("Warning removed! ✅")

def info(update: Update, context: CallbackContext):
    update.message.reply_text("User information retrieved. ℹ️")

def resolve_model(update: Update, context: CallbackContext):
    """Scans the message for RMX codes and searches them online."""
    text = update.effective_message.text.upper()
    
    # Strictly hunts for Realme (RMX) models only
    matches = set(re.findall(r'(?:RMX\d{4})', text))
    
    if matches:
        # Send a typing indicator while the bot browses the web
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        response = "📱 <b>Realme Devices Detected:</b>\n\n"
        for match in matches:
            device_name = search_realme_model(match)
            response += f"• <b>{match}</b> : {device_name}\n"
            
        msg = update.message.reply_text(response, parse_mode=ParseMode.HTML)
        schedule_delete(context, msg.chat_id, msg.message_id)

def cool(update: Update, context: CallbackContext):
    delay_html(update, context, "cool")

def polls(update: Update, context: CallbackContext):
    update.message.reply_text("Current polls: None 📊")

def private_not_available(update: Update, context: CallbackContext):
    update.message.reply_text("This command is not available in private chat.")

def benchmark(update: Update, context: CallbackContext):
    text = open("strings/benchmark.html", encoding="utf-8").read()
    
    norm_text = """Hey {} 🤖\n{}"""
    veri_text = (
        "Hey {} 🤖\n"
        "Pretty cool that you got the latest Update!"
        "\nBefore you update to a newer version, please do "
        "some benchmarks first to be able to compare what "
        "\n{}"
    )
    if update.message.reply_to_message and update.message.from_user.id in VERIFIED_USERS:
        delay_group(update, context, veri_text.format(update.message.reply_to_message.from_user.name, text))
    else:
        delay_group(update, context, norm_text.format(update.message.from_user.name, text))

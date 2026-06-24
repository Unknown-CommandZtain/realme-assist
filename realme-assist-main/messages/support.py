"""These messages are meant to be sent in support group (@realme_support) only."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from config import ADMINS
from utils import (
    delay_group,
    message_button_url,
    delete,
    delay_group_button_url,
    delay_group_preview, delay_html,
)


def ask(update: Update, context: CallbackContext):
    delay_html(update, context, "ask")

def commands(update: Update, context: CallbackContext):
    delay_html(update, context, "commands")

def gcam(update: Update, context: CallbackContext):
    delay_html(update, context, "gcam")

def cleaners(update: Update, context: CallbackContext):
    delay_html(update, context, "cleaners")

def aod(update: Update, context: CallbackContext):
    delay_html(update, context, "aod")

def manual(update: Update, context: CallbackContext):
    delay_html(update, context, "manual")

def apk(update: Update, context: CallbackContext):
    delay_html(update, context, "apk")

def form(update: Update, context: CallbackContext):
    delay_html(update, context, "form")

def bug(update: Update, context: CallbackContext):
    delay_html(update, context, "bug")

def battery(update: Update, context: CallbackContext):
    delay_html(update, context, "battery")

def stable(update: Update, context: CallbackContext):
    delay_html(update, context, "stable")

def push(update: Update, context: CallbackContext):
    delay_html(update, context, "push")

def ram(update: Update, context: CallbackContext):
    delay_html(update, context, "ram")

def rant(update: Update, context: CallbackContext):
    delay_html(update, context, "rant")

def whatsapp(update: Update, context: CallbackContext):
    update.message.delete()
    text = (
        "You can contact the official support directly on WhatsApp:"
        "\n\n+919711012312 🆕"
    )
    button_text = "Message Support 💬"
    button_url = "https://wa.me/+919711012312"

# FIXED: Added explicit UTF-8 decoding to read modern characters perfectly
def android16(update: Update, context: CallbackContext):
    """Handle for /android16."""
    delay_group_preview(update, context, open("strings/android16.html", encoding="utf-8").read())

def debloat(update: Update, context: CallbackContext):
    delay_html(update, context, "debloat")

def fps(update: Update, context: CallbackContext):
    delay_html(update, context, "fps")

def fooview(update: Update, context: CallbackContext):
    delay_html(update, context, "fooview")

def swap(update: Update, context: CallbackContext):
    delay_html(update, context, "swap")

def charge(update: Update, context: CallbackContext):
    delay_html(update, context, "charge")

def miss(update: Update, context: CallbackContext):
    delay_html(update, context, "miss")

def eol(update: Update, context: CallbackContext):
    delay_html(update, context, "eol")

def rumor(update: Update, context: CallbackContext):
    delay_html(update, context, "rumor")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import random
import string
import uuid
import hashlib
import base64
import urllib.parse
from datetime import datetime
import secrets
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found in environment variables!")
    sys.exit(1)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# ============= Utility Functions =============

def generate_password(length=16, use_special=True):
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = []
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    for _ in range(length - len(password)):
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return ''.join(password)

def generate_username(style='standard', length=8):
    """Generate a random username"""
    adjectives = ['cool', 'happy', 'brave', 'mighty', 'swift', 'bright', 'clever', 'wild']
    nouns = ['tiger', 'eagle', 'dragon', 'wolf', 'phoenix', 'storm', 'thunder', 'shadow']
    numbers = ''.join(random.choices(string.digits, k=4))
    
    if style == 'standard':
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        return f"{adj}_{noun}_{numbers}"
    elif style == 'simple':
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    elif style == 'words':
        return f"{random.choice(adjectives)}{random.choice(nouns)}"
    else:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_uuid(version=4):
    """Generate UUID"""
    if version == 4:
        return str(uuid.uuid4())
    elif version == 1:
        return str(uuid.uuid1())
    elif version == 3:
        namespace = uuid.NAMESPACE_DNS
        name = str(time.time())
        return str(uuid.uuid3(namespace, name))
    else:
        return str(uuid.uuid4())

def generate_random_number(min_val=1, max_val=100):
    """Generate random number"""
    return random.randint(min_val, max_val)

def generate_random_string(length=16, include_special=True):
    """Generate random string"""
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_hash(text, algorithm='sha256'):
    """Generate hash of text"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'blake2b': hashlib.blake2b,
        'blake2s': hashlib.blake2s
    }
    
    if algorithm not in algorithms:
        algorithm = 'sha256'
    
    hash_obj = algorithms[algorithm]()
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()

def base64_encode(text):
    """Encode text to base64"""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def base64_decode(text):
    """Decode base64 to text"""
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except:
        return None

def url_encode(text):
    """URL encode text"""
    return urllib.parse.quote(text, safe='')

def url_decode(text):
    """URL decode text"""
    try:
        return urllib.parse.unquote(text)
    except:
        return None

def timestamp_generator(format_type='unix'):
    """Generate timestamp"""
    current_time = time.time()
    
    if format_type == 'unix':
        return str(int(current_time))
    elif format_type == 'unix_ms':
        return str(int(current_time * 1000))
    elif format_type == 'iso':
        return datetime.fromtimestamp(current_time).isoformat()
    elif format_type == 'readable':
        return datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(int(current_time))

def list_hash_algorithms():
    """List available hash algorithms"""
    return ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s']

# ============= Bot Command Handlers =============

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send a message when /start is issued."""
    user_first_name = message.from_user.first_name
    welcome_message = f"""
👋 Hello {user_first_name}!

Welcome to CurePassonMiBot - Your Privacy-Focused Utility Bot!

🔐 I help you generate information securely without collecting any sensitive data.

📋 Available Commands:
/password - Generate secure passwords
/username - Generate random usernames
/uuid - Generate UUIDs
/random - Generate random numbers
/string - Generate random strings
/hash - Generate hashes
/base64 - Encode/Decode Base64
/url - Encode/Decode URLs
/timestamp - Generate timestamps
/help - Show all commands

⚡ All operations are performed locally and securely!

Choose a command to get started, or use /help for more details.
"""
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['help'])
def send_help(message):
    """Send a message when /help is issued."""
    help_text = """
📚 **CurePassonMiBot Help Guide**

🔑 **Password Generator**
/password - Generate default password (16 chars)
/password length - Generate password with specific length
/password length simple - Generate without special chars

👤 **Username Generator**
/username - Generate default username
/username simple - Simple alphanumeric username
/username words - Adjective+Noun combination

🆔 **UUID Generator**
/uuid - Generate UUID v4
/uuid 1 - Generate UUID v1
/uuid 3 - Generate UUID v3

🎲 **Random Number**
/random - Generate number between 1-100
/random min max - Generate number in custom range

📝 **Random String**
/string - Generate default string (16 chars)
/string length - Generate with custom length
/string length nospecial - Without special chars

🔐 **Hash Generator**
/hash text - Generate SHA256 hash
/hash text algorithm - Use specific algorithm (md5, sha1, sha256, etc.)

📦 **Base64 Encode/Decode**
/base64 encode text - Encode text to base64
/base64 decode text - Decode base64 to text

🔗 **URL Encode/Decode**
/url encode text - URL encode text
/url decode text - URL decode text

⏰ **Timestamp Generator**
/timestamp - Generate Unix timestamp
/timestamp unix_ms - Unix timestamp in milliseconds
/timestamp iso - ISO format timestamp
/timestamp readable - Human-readable timestamp
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['password'])
def handle_password(message):
    """Generate password"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    length = 16
    use_special = True
    
    if args:
        try:
            length = int(args[0])
            if length < 6:
                length = 6
            elif length > 64:
                length = 64
        except ValueError:
            pass
        
        if len(args) > 1 and args[1].lower() == 'simple':
            use_special = False
    
    password = generate_password(length, use_special)
    bot.reply_to(
        message,
        f"🔐 **Generated Password:**\n`{password}`\n\nLength: {length}\nSpecial chars: {'Yes' if use_special else 'No'}",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['username'])
def handle_username(message):
    """Generate username"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    style = 'standard'
    if args:
        arg = args[0].lower()
        if arg in ['simple', 'words']:
            style = arg
    
    username = generate_username(style)
    bot.reply_to(
        message,
        f"👤 **Generated Username:**\n`{username}`\n\nStyle: {style}",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['uuid'])
def handle_uuid(message):
    """Generate UUID"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    version = 4
    if args:
        try:
            version = int(args[0])
            if version not in [1, 3, 4]:
                version = 4
        except ValueError:
            version = 4
    
    uid = generate_uuid(version)
    bot.reply_to(
        message,
        f"🆔 **Generated UUID (v{version}):**\n`{uid}`",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['random'])
def handle_random(message):
    """Generate random number"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    min_val = 1
    max_val = 100
    
    if args:
        try:
            if len(args) >= 2:
                min_val = int(args[0])
                max_val = int(args[1])
            else:
                max_val = int(args[0])
                min_val = 1
            
            if min_val > max_val:
                min_val, max_val = max_val, min_val
        except ValueError:
            pass
    
    number = generate_random_number(min_val, max_val)
    bot.reply_to(
        message,
        f"🎲 **Random Number:**\n`{number}`\n\nRange: {min_val} - {max_val}",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['string'])
def handle_string(message):
    """Generate random string"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    length = 16
    include_special = True
    
    if args:
        try:
            length = int(args[0])
            if length < 1:
                length = 1
            elif length > 100:
                length = 100
        except ValueError:
            pass
        
        if len(args) > 1 and args[1].lower() == 'nospecial':
            include_special = False
    
    random_string = generate_random_string(length, include_special)
    bot.reply_to(
        message,
        f"📝 **Generated Random String:**\n`{random_string}`\n\nLength: {length}\nSpecial chars: {'Yes' if include_special else 'No'}",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['hash'])
def handle_hash(message):
    """Generate hash"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    text = " ".join(args) if args else ""
    
    if not text:
        bot.reply_to(message, "❌ Please provide text to hash.\nExample: `/hash Hello World`")
        return
    
    algorithms = list_hash_algorithms()
    parts = text.split()
    algorithm = 'sha256'
    
    if parts and parts[-1].lower() in algorithms:
        algorithm = parts[-1].lower()
        text = " ".join(parts[:-1])
    
    hash_value = generate_hash(text, algorithm)
    bot.reply_to(
        message,
        f"🔐 **Hash Generated:**\nAlgorithm: {algorithm}\nText: `{text}`\nHash: `{hash_value}`",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['base64'])
def handle_base64(message):
    """Base64 encode/decode"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ Please specify operation and text.\nExample: `/base64 encode Hello`\nExample: `/base64 decode SGVsbG8=`"
        )
        return
    
    operation = args[0].lower()
    text = " ".join(args[1:])
    
    if operation == 'encode':
        result = base64_encode(text)
        bot.reply_to(
            message,
            f"📦 **Base64 Encoded:**\nOriginal: `{text}`\nEncoded: `{result}`",
            parse_mode='Markdown'
        )
    elif operation == 'decode':
        result = base64_decode(text)
        if result is None:
            bot.reply_to(message, "❌ Invalid Base64 string provided.")
        else:
            bot.reply_to(
                message,
                f"📦 **Base64 Decoded:**\nEncoded: `{text}`\nDecoded: `{result}`",
                parse_mode='Markdown'
            )
    else:
        bot.reply_to(message, "❌ Invalid operation. Use `encode` or `decode`.")

@bot.message_handler(commands=['url'])
def handle_url(message):
    """URL encode/decode"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ Please specify operation and text.\nExample: `/url encode Hello World`\nExample: `/url decode Hello%20World`"
        )
        return
    
    operation = args[0].lower()
    text = " ".join(args[1:])
    
    if operation == 'encode':
        result = url_encode(text)
        bot.reply_to(
            message,
            f"🔗 **URL Encoded:**\nOriginal: `{text}`\nEncoded: `{result}`",
            parse_mode='Markdown'
        )
    elif operation == 'decode':
        result = url_decode(text)
        if result is None:
            bot.reply_to(message, "❌ Invalid URL encoded string provided.")
        else:
            bot.reply_to(
                message,
                f"🔗 **URL Decoded:**\nEncoded: `{text}`\nDecoded: `{result}`",
                parse_mode='Markdown'
            )
    else:
        bot.reply_to(message, "❌ Invalid operation. Use `encode` or `decode`.")

@bot.message_handler(commands=['timestamp'])
def handle_timestamp(message):
    """Generate timestamp"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    format_type = 'unix'
    if args:
        arg = args[0].lower()
        if arg in ['unix_ms', 'iso', 'readable']:
            format_type = arg
    
    timestamp = timestamp_generator(format_type)
    
    format_names = {
        'unix': 'Unix (seconds)',
        'unix_ms': 'Unix (milliseconds)',
        'iso': 'ISO Format',
        'readable': 'Human Readable'
    }
    
    bot.reply_to(
        message,
        f"⏰ **Timestamp Generated:**\nFormat: {format_names.get(format_type, format_type)}\n`{timestamp}`",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """Handle unknown commands"""
    bot.reply_to(
        message,
        "❌ Unknown command. Please use /help to see available commands."
    )

# ============= Main Function =============

def main():
    """Start the bot."""
    try:
        logger.info("=" * 50)
        logger.info("Starting CurePassonMiBot...")
        logger.info(f"Bot Token: {BOT_TOKEN[:10]}...")
        logger.info("Bot is running and ready to accept commands!")
        logger.info("=" * 50)
        
        # Remove webhook to ensure polling works
        bot.remove_webhook()
        
        # Start polling
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
                
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from utils import UtilityGenerator
import logging

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.utils = UtilityGenerator()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when /start is issued."""
        user = update.effective_user
        welcome_message = f"""
👋 Hello {user.first_name}!

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
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when /help is issued."""
        help_text = """
📚 **CurePassonMiBot Help Guide**

🔑 **Password Generator**
`/password` - Generate default password (16 chars)
`/password length` - Generate password with specific length
`/password length simple` - Generate without special chars

👤 **Username Generator**
`/username` - Generate default username
`/username simple` - Simple alphanumeric username
`/username words` - Adjective+Noun combination

🆔 **UUID Generator**
`/uuid` - Generate UUID v4
`/uuid 1` - Generate UUID v1
`/uuid 3` - Generate UUID v3

🎲 **Random Number**
`/random` - Generate number between 1-100
`/random min max` - Generate number in custom range

📝 **Random String**
`/string` - Generate default string (16 chars)
`/string length` - Generate with custom length
`/string length nospecial` - Without special chars

🔐 **Hash Generator**
`/hash text` - Generate SHA256 hash
`/hash text algorithm` - Use specific algorithm (md5, sha1, sha256, etc.)

📦 **Base64 Encode/Decode**
`/base64 encode text` - Encode text to base64
`/base64 decode text` - Decode base64 to text

🔗 **URL Encode/Decode**
`/url encode text` - URL encode text
`/url decode text` - URL decode text

⏰ **Timestamp Generator**
`/timestamp` - Generate Unix timestamp
`/timestamp unix_ms` - Unix timestamp in milliseconds
`/timestamp iso` - ISO format timestamp
`/timestamp readable` - Human-readable timestamp

🤖 For interactive usage, use the buttons below!
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate password"""
        args = context.args
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
        
        password = self.utils.generate_password(length, use_special)
        await update.message.reply_text(f"🔐 **Generated Password:**\n`{password}`\n\nLength: {length}\nSpecial chars: {'Yes' if use_special else 'No'}", parse_mode='Markdown')

    async def username(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate username"""
        style = 'standard'
        if context.args:
            arg = context.args[0].lower()
            if arg in ['simple', 'words']:
                style = arg
        
        username = self.utils.generate_username(style)
        await update.message.reply_text(f"👤 **Generated Username:**\n`{username}`\n\nStyle: {style}", parse_mode='Markdown')

    async def uuid(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate UUID"""
        version = 4
        if context.args:
            try:
                version = int(context.args[0])
                if version not in [1, 3, 4]:
                    version = 4
            except ValueError:
                version = 4
        
        uid = self.utils.generate_uuid(version)
        await update.message.reply_text(f"🆔 **Generated UUID (v{version}):**\n`{uid}`", parse_mode='Markdown')

    async def random(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate random number"""
        min_val = 1
        max_val = 100
        
        if context.args:
            try:
                if len(context.args) >= 2:
                    min_val = int(context.args[0])
                    max_val = int(context.args[1])
                else:
                    max_val = int(context.args[0])
                    min_val = 1
                
                if min_val > max_val:
                    min_val, max_val = max_val, min_val
            except ValueError:
                pass
        
        number = self.utils.generate_random_number(min_val, max_val)
        await update.message.reply_text(f"🎲 **Random Number:**\n`{number}`\n\nRange: {min_val} - {max_val}", parse_mode='Markdown')

    async def string(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate random string"""
        length = 16
        include_special = True
        
        if context.args:
            try:
                length = int(context.args[0])
                if length < 1:
                    length = 1
                elif length > 100:
                    length = 100
            except ValueError:
                pass
            
            if len(context.args) > 1 and context.args[1].lower() == 'nospecial':
                include_special = False
        
        random_string = self.utils.generate_random_string(length, include_special)
        await update.message.reply_text(f"📝 **Generated Random String:**\n`{random_string}`\n\nLength: {length}\nSpecial chars: {'Yes' if include_special else 'No'}", parse_mode='Markdown')

    async def hash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate hash"""
        text = " ".join(context.args) if context.args else ""
        
        if not text:
            await update.message.reply_text("❌ Please provide text to hash.\nExample: `/hash Hello World`")
            return
        
        # Check if last argument is an algorithm
        algorithms = self.utils.list_hash_algorithms()
        parts = text.split()
        algorithm = 'sha256'
        
        if parts and parts[-1].lower() in algorithms:
            algorithm = parts[-1].lower()
            text = " ".join(parts[:-1])
        
        hash_value = self.utils.generate_hash(text, algorithm)
        await update.message.reply_text(f"🔐 **Hash Generated:**\nAlgorithm: {algorithm}\nText: `{text}`\nHash: `{hash_value}`", parse_mode='Markdown')

    async def base64(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Base64 encode/decode"""
        if not context.args or len(context.args) < 2:
            await update.message.reply_text("❌ Please specify operation and text.\nExample: `/base64 encode Hello`\nExample: `/base64 decode SGVsbG8=`")
            return
        
        operation = context.args[0].lower()
        text = " ".join(context.args[1:])
        
        if operation == 'encode':
            result = self.utils.base64_encode(text)
            await update.message.reply_text(f"📦 **Base64 Encoded:**\nOriginal: `{text}`\nEncoded: `{result}`", parse_mode='Markdown')
        elif operation == 'decode':
            result = self.utils.base64_decode(text)
            if result is None:
                await update.message.reply_text("❌ Invalid Base64 string provided.")
            else:
                await update.message.reply_text(f"📦 **Base64 Decoded:**\nEncoded: `{text}`\nDecoded: `{result}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Invalid operation. Use `encode` or `decode`.")

    async def url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """URL encode/decode"""
        if not context.args or len(context.args) < 2:
            await update.message.reply_text("❌ Please specify operation and text.\nExample: `/url encode Hello World`\nExample: `/url decode Hello%20World`")
            return
        
        operation = context.args[0].lower()
        text = " ".join(context.args[1:])
        
        if operation == 'encode':
            result = self.utils.url_encode(text)
            await update.message.reply_text(f"🔗 **URL Encoded:**\nOriginal: `{text}`\nEncoded: `{result}`", parse_mode='Markdown')
        elif operation == 'decode':
            result = self.utils.url_decode(text)
            if result is None:
                await update.message.reply_text("❌ Invalid URL encoded string provided.")
            else:
                await update.message.reply_text(f"🔗 **URL Decoded:**\nEncoded: `{text}`\nDecoded: `{result}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Invalid operation. Use `encode` or `decode`.")

    async def timestamp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate timestamp"""
        format_type = 'unix'
        if context.args:
            arg = context.args[0].lower()
            if arg in ['unix_ms', 'iso', 'readable']:
                format_type = arg
        
        timestamp = self.utils.timestamp_generator(format_type)
        
        format_names = {
            'unix': 'Unix (seconds)',
            'unix_ms': 'Unix (milliseconds)',
            'iso': 'ISO Format',
            'readable': 'Human Readable'
        }
        
        await update.message.reply_text(f"⏰ **Timestamp Generated:**\nFormat: {format_names.get(format_type, format_type)}\n`{timestamp}`", parse_mode='Markdown')

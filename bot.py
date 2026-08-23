#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
from handlers import BotHandlers

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
    logger.error("Please set BOT_TOKEN in .env file or environment variables")
    sys.exit(1)

def main():
    """Start the bot."""
    try:
        logger.info("Initializing bot application...")
        
        # Create the Application with improved settings
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .build()
        )
        
        # Initialize handlers
        handlers = BotHandlers()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", handlers.start))
        application.add_handler(CommandHandler("help", handlers.help))
        application.add_handler(CommandHandler("password", handlers.password))
        application.add_handler(CommandHandler("username", handlers.username))
        application.add_handler(CommandHandler("uuid", handlers.uuid))
        application.add_handler(CommandHandler("random", handlers.random))
        application.add_handler(CommandHandler("string", handlers.string))
        application.add_handler(CommandHandler("hash", handlers.hash))
        application.add_handler(CommandHandler("base64", handlers.base64))
        application.add_handler(CommandHandler("url", handlers.url))
        application.add_handler(CommandHandler("timestamp", handlers.timestamp))
        
        # Error handler
        async def error_handler(update, context):
            logger.warning(f"Update {update} caused error: {context.error}")
        
        application.add_error_handler(error_handler)
        
        # Start the Bot
        logger.info("Bot is starting and ready to accept commands!")
        logger.info(f"Bot username: @curepassonmibot")
        application.run_polling(allowed_updates=[])
        
    except Exception as e:
        logger.error(f"Fatal error starting bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
